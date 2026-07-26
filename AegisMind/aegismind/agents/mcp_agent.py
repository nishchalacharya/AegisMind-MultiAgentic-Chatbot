"""
MCP Tool Agent - Acts as an MCP Client 
Connects to our tools_server.py (MCP server) and calls tools based on LLM decisions
"""

import json 
import re 
from pathlib import Path 
from mcp import ClientSession,StdioServerParameters
from mcp.client.stdio import stdio_client 

from orchestration.state import AgentState 
from services.groq_client import GroqClient


class MCPAgent: 
    """
    MCP Client that connects to tools_server.py and execute tools 
    """

    def __init__(self):
        self.llm =  GroqClient()
        # Path to out MCP server script 
        self.server_script =  str (
            Path(__file__).parent.parent/"mcp_servers" / "tools_server.py"
        ) 

    async def execute(self,state: AgentState) -> AgentState:
        """
        Connect to MCP server, discover tools, ask LLM which to use,execute it .
        """
        query = state["user_message"]

        server_params = StdioServerParameters(
            command  = "python",
            args= [self.server_script],

        )

        async with stdio_client(server_params) as (read,write):
            async with ClientSession(read,write) as session:
                await session.initialize()

                # step 1: Discover available tools from the server 
                tools_response = await session.list_tools()
                available_tools = [
                    {"name":t.name , "description":t.description}
                    for t in tools_response.tools
                ] 

                # Step 2 : Ask LLM which tool to call 
                tools_description = "\n".join (
                    [f"-{t['name']}: {t['description']}" for t in available_tools]
                )

                system_prompt = f""" You are a tool calling agent.Based on the user's request , 
                decide which tool to call and with what arguments.

                Available tools:
                {tools_description}

                Respond ONLY with JSON: 
                {{
                "tool":"tool_name" , 
                "arguments" : {{"key":"value"}}
                }}
            """
                
                response= self.llm.generate(
                    messages=[{"role":"user","content":query}],
                    system_prompt=system_prompt,
                    temperature=0.3
                )

                try:
                   json_match = re.search(r'\{.*\}', response, re.DOTALL)
                   tool_call = json.loads(json_match.group())
                
                except Exception : 
                    state["final_response"] = "I couldn't determine which tool to use."
                    return state 
                
                tool_name = tool_call.get("tool")
                arguments = tool_call.get("arguments",{})


                # step 3: Call the tool via MCP protocol 

                result = await session.call_tool(tool_name,arguments=arguments)
                tool_output = result.content[0].text if result.content else "No output "
                print(f"DEBUG - Tool Output:{tool_output}")


                
                # Step 4 : Synthesize final natural language answer 


                final_response = self.llm.generate(
                    messages=[
                        {"role":"user","content":query},
                        {"role":"assistant","content": f"Tool result: {tool_output}"}
                    ],
                    system_prompt=(
                        "Synthesize the tool result into a natural, helpful  response."
                        
                        
                        )
                )

                state["final_response"] = final_response 
                state["tool_calls"].append({
                    "tool":tool_name,
                    "arguments":arguments,
                    "result":tool_output

                })
        return state 
 


            
