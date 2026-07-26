"""
A real MCP Server exposing simple tools:
- web search :  search the web using DuckDuckGo(free,no API key required)
- calculator : evaluate safe math expressions
- currentime : get current date/time 

This runs as a SEPERATE PROCESS,communicating via stdio . 
"""


from mcp.server.fastmcp import FastMCP
from duckduckgo_search import DDGS
from datetime import datetime

# Create the MCP server instance 
mcp = FastMCP("aegismind-tools")

@mcp.tool()
def web_search(query:str , max_results: int = 3) -> str : 
    """
    Search the web for current information using DuckDuckGo.

    Args:
        query: The search query 
        max_results: Number of results to return (default 3)
    """
    try:
        results = DDGS().text(query,max_results=max_results)
        if not results:
            return "No results found"
        formatted = []
        for r in results:
            formatted.append(f"Title: {r['title']}\nSnippet: {r['body']}\nURL: {r['href']}")
        return "\n\n".join(formatted)
    
    except Exception as e:
        return f"Search error: {e}"
    

@mcp.tool()
def calculator(expression : str) -> str : 
    """
    Evaluate a safe mathematical expression.

    Args:
        expression : Math expression like "2+2 " or "10 * 5"
    """
    allowed_chars =  set("0123456789+-*/.() ")
    if not all(c in allowed_chars for c in expression):
        return "Error: Only basic math operations are allowed. "
    
    try: 
        result = eval(expression,{"__builtins__":{}})
        return f"Result: {result}"
    except Exception as e:
        return f"Calculation error : {e}"
    

@mcp.tool()
def current_time() -> str : 
    """ Get the current date and time."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")




if __name__ == "__main__":
    # Run the server using stdio transport 
    mcp.run(transport ="stdio")
    

