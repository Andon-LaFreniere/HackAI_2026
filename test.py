import asyncio
import os
from coder import generate_tool_code
from dependency_manager import install_dependencies
from tool_registry import ToolRegistry

async def run_smoke_test():
    print("🛠️ Starting System Integration Test...")
    registry = ToolRegistry()
    
    requirement = "A tool that uses the 'cowsay' library to return a string of a cow saying the user's input."
    
    # 1. Generate & Save
    code = generate_tool_code(requirement)
    os.makedirs("sandbox", exist_ok=True)
    script_path = "sandbox/test_cowsay.py"
    with open(script_path, "w") as f:
        f.write(code)
    
    # 2. Install
    install_dependencies(code)

    try:
        # 3. Connect
        session, tool_name = await registry.register_and_connect(script_path)
        
        # --- THE FIX FOR THE ARGUMENT ERROR ---
        # Get the tool definition to see what the LLM called the argument
        tools_list = await session.list_tools()
        target_tool = next(t for t in tools_list.tools if t.name == tool_name)
        
        # Usually, it's 'input_text' or 'text'. We'll find the first property name.
        arg_name = list(target_tool.inputSchema.get("properties", {}).keys())[0]
        print(f"Detected argument name: '{arg_name}'")

        print(f"\nStep 4: Calling the NEW tool '{tool_name}'...")
        result = await session.call_tool(tool_name, arguments={arg_name: "ForgeMCP is Alive!"})
        
        print("\n--- TOOL OUTPUT ---")
        print(result.content[0].text)
        print("-------------------")
        print("\n🔥 SYSTEM TEST PASSED!")
    
    except Exception as e:
        print(f"\n❌ SYSTEM TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # Changed from cleanup() to shutdown()
        await registry.shutdown()

if __name__ == "__main__":
    asyncio.run(run_smoke_test())