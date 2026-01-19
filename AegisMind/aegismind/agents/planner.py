# aegismind/agents/planner.py
"""
Planner Agent - Intent detection and routing
This is the "brain" that decides which specialized agent should handle the request
"""

from aegismind.services.groq_client import GroqClient
from aegismind.orchestration.state import AgentState, AgentType
import json
import re

class PlannerAgent:
    """
    Analyzes user intent and routes to appropriate agent
    """
    
    def __init__(self):
        self.llm = GroqClient()
        self.system_prompt = self._build_system_prompt()
    
    def _build_system_prompt(self) -> str:
        """Build the planning system prompt"""
        return """You are a planning agent that analyzes user requests and routes them to the correct specialized agent.

Available agents:
- DOC_QA: Answer questions about uploaded documents (PDFs, text files)
- MEMORY: Store or retrieve personal information, preferences, facts about the user
- GENERAL: General conversation, questions not requiring documents or memory
- MCP_TOOL: Use external tools (web search, calculations, etc.)
- VOICE: Process voice input/output

Analyze the user's message and respond ONLY with a JSON object:
{
    "intent": "brief description of what user wants",
    "next_agent": "DOC_QA|MEMORY|GENERAL|MCP_TOOL|VOICE",
    "reasoning": "why you chose this agent",
    "needs_memory_context": true/false
}

Examples:
User: "What does the contract say about payment terms?"
Response: {"intent": "document question", "next_agent": "DOC_QA", "reasoning": "asking about document content", "needs_memory_context": false}

User: "Remember that I'm allergic to peanuts"
Response: {"intent": "store fact", "next_agent": "MEMORY", "reasoning": "user wants to store personal info", "needs_memory_context": false}

User: "What's the weather like?"
Response: {"intent": "general query", "next_agent": "GENERAL", "reasoning": "general question not requiring documents", "needs_memory_context": false}

Respond ONLY with valid JSON, no other text."""
    
    def plan(self, state: AgentState) -> AgentState:
        """
        Analyze user message and determine routing
        
        Args:
            state: Current agent state
        
        Returns:
            Updated state with intent and next_agent set
        """
        # Prepare context
        messages = [
            {
                "role": "user",
                "content": f"User message: {state['user_message']}\n\nRecent context: {state.get('short_term_memory', [])}"
            }
        ]
        
        # Get planning decision
        try:
            response = self.llm.generate_structured(
                messages=messages,
                system_prompt=self.system_prompt
            )
            
            # Parse JSON response
            plan = self._parse_plan(response)
            
            # Update state
            state["intent"] = plan.get("intent", "unknown")
            state["next_agent"] = AgentType(plan.get("next_agent", "GENERAL"))
            
            # Add planning info to metadata
            if "planning_info" not in state:
                state["planning_info"] = {}
            
            state["planning_info"]["reasoning"] = plan.get("reasoning", "")
            state["planning_info"]["needs_memory"] = plan.get("needs_memory_context", False)
            
            print(f" Planner: Intent='{state['intent']}', Route={state['next_agent']}")
            
        except Exception as e:
            # Fallback to general agent on error
            print(f" Planning error: {e}, defaulting to GENERAL agent")
            state["intent"] = "fallback"
            state["next_agent"] = AgentType.GENERAL
            state["error"] = str(e)
        
        return state
    
    def _parse_plan(self, response: str) -> dict:
        """
        Parse JSON from LLM response
        Handles cases where LLM adds extra text
        """
        # Try to extract JSON from response
        json_match = re.search(r'\{.*\}', response, re.DOTALL)
        if json_match:
            json_str = json_match.group()
            return json.loads(json_str)
        
        # Fallback
        raise ValueError(f"Could not parse JSON from response: {response}")