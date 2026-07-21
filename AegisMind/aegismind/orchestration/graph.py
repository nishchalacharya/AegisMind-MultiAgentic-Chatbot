# aegismind/orchestration/graph.py
"""
LangGraph orchestrator - defines the agent execution flow
"""

from langgraph.graph import StateGraph,END
from orchestration.state import AgentState,AgentType
from agents.planner import PlannerAgent
from typing import Literal
from services.groq_client import GroqClient
from agents.memory import MemoryAgent 

import asyncio 
from agents.mcp_agent import MCPAgent



class AgentOrchestrator:
    """
    Orchestrates the flow between planning and execution agents
    """
    
    def __init__(self):
        self.planner = PlannerAgent()
        self.graph   =   self._build_graph()
        
    def _build_graph(self) -> StateGraph:
        """
        Build the LangGraph  workflow 
        Flow:
        1. Start -> Planner (analyze intent)
        2. Planner -> Route to appropriate agent
        3. Agent executes -> End
        
        """     
        # Create Graph 
        workflow = StateGraph(AgentState)
        
        # Add nodes
        workflow.add_node("planner",self._planner_node)
        workflow.add_node("doc_qa",self._doc_qa_node)
        workflow.add_node("memory",self._memory_node)
        workflow.add_node("general",self._general_node)
        workflow.add_node("mcp_tool",self._mcp_tool_node)
        
        # set entry point 
        workflow.set_entry_point("planner")
        
        # Add conditional routing from planner 
        workflow.add_conditional_edges(
            "planner",
            self._route_after_planning,
        {
            
            AgentType.DOC_QA:"doc_qa",
            AgentType.MEMORY:"memory",
            AgentType.GENERAL:"general",
            AgentType.MCP_TOOL:"mcp_tool",
        }  
        ) 
        # All execution agents end the flow 
        workflow.add_edge("doc_qa",END)
        workflow.add_edge("memory",END)
        workflow.add_edge("general",END)
        workflow.add_edge("mcp_tool",END)
        
        return workflow.compile()
    
    def _planner_node(self,state:AgentState)-> AgentState:
        """planning node execution """
        print("\n" + "="*50)
        print("🧠 PLANNER AGENT")
        print("="*50)
        return self.planner.plan(state)
    
    
    def _route_after_planning(self,state:AgentState)-> Literal[
        AgentType.DOC_QA,
        AgentType.MEMORY,
        AgentType.GENERAL,
        AgentType.MCP_TOOL
    ]:
        """  
        Conditional edge: decide which agent to call after planning
        """
        return state["next_agent"]
    
    # Execution agent nodes (placeholder implementations)
    
    def _doc_qa_node(self,state:AgentState) -> AgentState:
        """Document Q&A Agent - will implement with RAG"""
        print("\n" + "="*50)
        print("📄 DOCUMENT Q&A AGENT")
        print("="*50)
    
        # TODO: Implement RAG retrieval and generation 
        state["final_response"]= "Document Q&A agent not yet implemented. This will use RAG ."
        return state 
    
    def _memory_node(self,state:AgentState)->AgentState:
        """Memory agent - store/retrieve user information"""
        print("\n" + "="*50)
        print("🧠 MEMORY AGENT")
        print("="*50)
        
        agent=  MemoryAgent()
        return agent.execute(state)
    
     
    def _general_node(self,state:AgentState)->AgentState:
        """General conversation agent"""
        print("\n" + "="*50)
        print("💬 GENERAL AGENT")
        print("="*50) 
        
        llm=GroqClient()
        
        #Build context from chat history 
        messages=state.get("messages",[])[-5:] #last 5 messages
        messages.append({
            "role": "user",
            "content": state["user_message"]
        })
        response = llm.generate(
            messages=messages,
            system_prompt="You are a helpful AI assistant.Respond naturally and conversationally."
            )
        state['final_response']=response 
        return state 
    
    def _mcp_tool_node(self,state:AgentState)-> AgentState:
        """MCP tool agent - external tool calls"""
        print("\n" + "="*50)
        print("🔧 MCP TOOL AGENT")
        print("="*50)
        

        agent = MCPAgent()
        # Bridge sync orchestrator with sync MCP agent 
        result = asyncio.run(agent.execute(state=state))
        return result 
   
    
    
    def run(self, user_message: str, user_id: str = "default") -> str:
       
        """
        Execute the agent workflow
        
        Args:
            user_message: User's input
            user_id: User identifier for memory
        
        Returns:
            Final response from the system
        """
        # Initialize state
        initial_state: AgentState = {
            "user_message": user_message,
            "user_id": user_id,
            "messages": [],
            "short_term_memory": [],
            "intent": None,
            "next_agent": None,
            "current_response": "",
            "final_response": "",
            "retrieved_documents": [],
            "memory_updates": [],
            "tool_calls": [],
            "tool_results": [],
            "iteration_count": 0,
            "error": None
        }
        
        # Run the graph
        final_state = self.graph.invoke(initial_state)
        
        return final_state["final_response"]
        
    
    
        
                                                               
                                                               
                                                               
    
        
