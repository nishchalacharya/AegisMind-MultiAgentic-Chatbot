"""
Global state schema for LangGraph agent orchestration
"""

from typing import TypeDict,List,Dict,Any,Optional
from enum import Enum 

class AgentType(str,Enum):
    """Availabe Agent types"""
    PLANNER="planner"
    DOC_QA="doc_qa"
    MEMORY="memory"
    VOICE="voice"
    MCP_TOOL="mcp_tool"
    GENERAL="general"
    
    
class AgentState(TypeDict):
    """
    Shared state passed between all agents in the graph
    """   
    # User input
    user_message:str 
    user_id:str 
    
    #Conversational context 
    messages: List[Dict[str,str]]  #chat history 
    short_term_memory:List[str]    #Recent context
    
    # Planning and Routing
    intent:Optional[str]                 # Detected intent 
    next_agent:Optional[AgentType]       # Which agent to call next
    
    # Agent Outputs:
    current_response:str
    final_response:str
    
    # RAG context:
    retrieved_documents:List[Dict[str,Any]]
    
    # Memory Operations:
    memory_updates: List[Dict[str,Any]]
    
    # Tool usage:
    tool_calls:List[Dict[str,Any]]
    tool_results:List[Any]
    
    # Meta data
    iteration_count:int 
    error:Optional[str]
    
    
    
    
    
    
      
    
    
    
     
    
