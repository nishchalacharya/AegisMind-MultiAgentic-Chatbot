
"""
Memory Agent - Stores and retrieves facts about the user
Uses LongTermMemory (SQLite) for persistence
"""

import json 
import re 
from orchestration.state import AgentState 
from services.groq_client import GroqClient 
from memory.long_term import LongTermMemory


class MemoryAgent:
    """
    Handles storing and retrieving persistent facts about the user . 
    """

    def __init__(self):
        self.llm = GroqClient()
        self.long_term = LongTermMemory()

    
    def execute(self,state:AgentState) -> AgentState:
        """
        Decide whether  this is a STORE or RETRIEVE request then act 
        """
        user_id =  state.get("user_id","default")
        query = state.get("user_message","")

        #step 1 : Ask LLM to classify + extract  
        system_prompt = """ You analyze messages about personal facts and respond ONLY with JSON.
        
       Determine if the user wants to STORE or RETRIEVE a fact.

        IMPORTANT: Always use one of these EXACT keys (never invent new ones):
            - "name"
            - "city"
            - "occupation"
            - "age"
            - "email"
            - "favorite_color"

        If the user's fact doesn't clearly match one of these, use "general_note" as the key.

        When RETRIEVING, map the user's phrasing to the closest matching key above 
        (e.g., "where do I live" → key "city", NOT "address" or "location").

        Respond ONLY with JSON:
        {
            "action": "STORE" or "RETRIEVE",
            "key": "one_of_the_keys_above",
            "value": "the fact value (only for STORE, else null)"
        }
    """
        
        response = self.llm.generate_structured(
            messages = [{"role":"user","content":query}],
            system_prompt = system_prompt
        )

        try:
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            parsed = json.loads(json_match.group())
        except Exception as e:
            state["final_response"]="I couldn't understand that memory request."
            return state 
        
        action = parsed.get("action")
        key = parsed.get("key")
        value = parsed.get("value")


        #Step 2: Act based on Classification 
        if action == "STORE":
            self.long_term.store_fact(user_id,key,value)
            state["final_response"]= f"Got it! I'll remember that your {key.replace('_',' ')} is {value}."
        elif action == "RETRIEVE":
            value = self.long_term.get_fact(user_id,key)
            if value is not None:
                state["final_response"]= f"Your {key.replace('_',' ')} is {value}."
            else:
                state["final_response"]= f" I don't have that information yet.You haven't told me your {key.replace('_',' ')}." 
        else: 
            state["final_response"]= "I'm not sure if you want me to remember or recall something."
        
        return state 
    



# Test the agent 

if __name__ == "__main__":
    agent= MemoryAgent()

    
    def make_state(message):
        return {
            "user_message": message,
            "user_id": "test_user",
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
    
    # Test storing
    state1 = agent.execute(make_state("Remember that my favorite color is blue"))
    print("Response 1:", state1["final_response"])
    
    # Test retrieving
    state2 = agent.execute(make_state("What's my favorite color?"))
    print("Response 2:", state2["final_response"])
    