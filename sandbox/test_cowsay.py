# depends: cowsay
from fastmcp import FastMCP
import cowsay

mcp = FastMCP("GeneratedTool")

@mcp.tool()
def cow_say(message: str) -> str:
    try:
        return cowsay.get_output_string('cow', message)
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    mcp.run()