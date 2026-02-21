# depends: psutil
from fastmcp import FastMCP
import psutil
from collections import defaultdict

mcp = FastMCP("GeneratedTool")

@mcp.tool()
def get_processes_by_user() -> str:
    try:
        user_processes = defaultdict(int)
        for proc in psutil.process_iter(['username']):
            try:
                user = proc.info['username']
                if user:
                    user_processes[user] += 1
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue
        return str(dict(user_processes))
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    mcp.run()