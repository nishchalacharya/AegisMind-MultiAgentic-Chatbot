import asyncio 
from agents.mcp_agent import MCPAgent

async def main():
    agent =  MCPAgent()

    
    state = {
        "user_message": "What is 25 times 4?",
        "user_id": "test",
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

    result = await agent.execute(state)
    print("\n" + "="*50)
    print("ANSWER:", result["final_response"])
    print("TOOL CALLS:", result["tool_calls"])



if __name__ == "__main__":
    asyncio.run(main())






    