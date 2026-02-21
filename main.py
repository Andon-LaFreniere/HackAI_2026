import asyncio
import os
from pydantic_ai import Agent, RunContext
from pydantic import BaseModel
from coder import generate_tool_code
from dependency_manager import install_dependencies
from tool_registry import ToolRegistry

# 1. Initialize the persistent registry
registry = ToolRegistry()

class AgentResponse(BaseModel):
    answer: str

# 2. Define the ForgeMCP Agent
agent = Agent(
    "openai:gpt-4o",
    system_prompt=(
        "You are ForgeMCP, an autonomous tool-builder. "
        "1. If you lack a tool, call 'provision_new_capability'. "
        "2. If provision_new_capability fails, analyze the error. If it was a dependency issue, try requesting the tool again with simpler or different libraries. If you have successfully built a tool but it didn't give you enough data (like just HTML when you needed a title), synthesize a SECOND tool to parse that data."
        "3. After the tool is ready, YOU MUST CALL IT to get the data. "
        "4. Provide your final answer as a clear, concise response."
    ),
)

# 3. The Meta-Tool: The 'Forge'
@agent.tool
async def provision_new_capability(ctx: RunContext[None], tool_description: str) -> str:
    """
    Synthesizes and hot-loads a new MCP tool.
    Call this when you lack the functionality to complete a request.
    """
    print(f"\n🧠 BRAIN: I need a new tool for: {tool_description}")

    # Run the generation pipeline
    code = generate_tool_code(tool_description)
    install_dependencies(code)

    # Save to sandbox
    tool_id = len(registry.sessions)
    filename = f"sandbox/autotool_{tool_id}.py"
    os.makedirs("sandbox", exist_ok=True)

    with open(filename, "w", encoding="utf-8") as f:
        f.write(code)

    # Hot-load into registry
    try:
        session, tool_name = await registry.register_and_connect(filename)

        # Dynamically register the new MCP tool into the Agent
        @agent.tool(name=tool_name)
        async def dynamic_tool_wrapper(ctx: RunContext[None], **kwargs) -> str:
            result = await registry.call_tool(tool_name, kwargs)
            return result.content[0].text

        return f"Tool '{tool_name}' is ready. You can now call it with the appropriate arguments."

    except Exception as e:
        return f"Failed to build tool: {str(e)}"

# 4. Execution Loop
async def chat():
    print("--- 🛠️ ForgeMCP: The Self-Synthesizing Architect ---")

    try:
        while True:
            user_msg = input("User > ")

            if user_msg.lower() in ["exit", "quit", "q"]:
                break

            # Run the agent
            result = await agent.run(user_msg)
            
            # Access the output as an attribute, not a method
            output = result.output
            print(f"\nForgeMCP > {output}\n")

    except Exception as e:
        print(f"An error occurred: {e}")
        import traceback
        traceback.print_exc()

    finally:
        await registry.shutdown()

if __name__ == "__main__":
    asyncio.run(chat())