import asyncio
import sys
import os
from contextlib import AsyncExitStack
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

class ToolRegistry:
    def __init__(self):
        # Maps tool_name -> ClientSession
        self.sessions = {}
        # This stack manages the lifecycle of all active tool connections
        self.exit_stack = AsyncExitStack()
        # Track spawned filenames for logging/cleanup
        self.active_scripts = []

    async def register_and_connect(self, script_path: str):
        """
        Spawns the MCP server, establishes a persistent connection,
        and adds it to the active registry.
        """
        # Ensure the script exists before trying to run it
        if not os.path.exists(script_path):
            raise FileNotFoundError(f"Could not find MCP script at {script_path}")

        # Define parameters to run the Python script as a subprocess
        server_params = StdioServerParameters(
            command=sys.executable,
            args=[script_path],
            env=os.environ.copy() # Pass current env vars (like API keys)
        )

        print(f"🔗 Establishing link to: {os.path.basename(script_path)}...")

        try:
            # 1. Start the subprocess and get the communication streams
            # We push the context manager onto the stack to keep the pipe open
            read_stream, write_stream = await self.exit_stack.enter_async_context(
                stdio_client(server_params)
            )

            # 2. Start the MCP Client Session over those streams
            session = await self.exit_stack.enter_async_context(
                ClientSession(read_stream, write_stream)
            )

            # 3. Initialize the protocol handshake
            await session.initialize()

            # 4. Discover the tool(s) inside the newly spawned server
            tools_response = await session.list_tools()
            
            if not tools_response.tools:
                print(f"⚠️ Warning: No tools found in {script_path}")
                return None, None

            # Register each tool found in this server
            # Note: For simplicity, we assume one primary tool per file for now
            main_tool = tools_response.tools[0]
            self.sessions[main_tool.name] = session
            self.active_scripts.append(script_path)

            print(f"✅ Registered capability: '{main_tool.name}'")
            return session, main_tool.name

        except Exception as e:
            print(f"❌ Failed to connect to MCP server {script_path}: {e}")
            raise

    async def call_tool(self, tool_name: str, arguments: dict):
        """
        Helper to call a registered tool by name.
        """
        if tool_name not in self.sessions:
            raise ValueError(f"Tool '{tool_name}' is not registered.")
        
        session = self.sessions[tool_name]
        return await session.call_tool(tool_name, arguments)

    async def shutdown(self):
        """Cleanly closes all active subprocesses and streams."""
        print("\n🛑 Shutting down all MCP bridges...")
        try:
            await self.exit_stack.aclose()
            # A tiny sleep gives the event loop time to clean up threads
            await asyncio.sleep(0.5) 
        except Exception:
            # In a hackathon, we can safely ignore teardown artifacts
            # as long as the processes are killed.
            pass
        print("Done.")
