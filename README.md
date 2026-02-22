# ForgeMCP

## HackAI 2026
Team Name: ForgeMCP
Team Members: Andon Lafreniere

ForgeMCP is an autonomous agent framework that solves the problem of static toolsets in modern ai agents such as OpenClaw. Instead of relying on pre-configured tools, ForgeMCP identifies capability gaps in real-time and bridges them by autonomously writing, installing, and hot-loading its own Model Context Protocol servers.

Inspired by the vision of **OpenClaw**, ForgeMCP transforms the AI from a tool-user into a tool-maker.

## Recursive Synthesis Loop

1. The Agent identifies a task it cannot complete with current tools.
2. A coding Agent generates a Python FastMCP server.
3. The Dependency Manager auto-installs required libraries.
4. The Tool Registry hot-loads the new server via `stdio` transport.
5. The Agent immediately uses the new capability to fulfill the request.

## Architecture

- **Orchestrator (`main.py`)**: A PydanticAI-powered reasoning engine.
- **The Forge (`coder.py`)**: High-fidelity FastMCP code generation.
- **Process Manager (`tool_registry.py`)**: Managing the lifecycle of dynamic subprocesses.
- **Sandbox (`/sandbox`)**: Isolated storage for the agent's growing library of capabilities.

## Setup

```bash
# Clone and enter venv
python -m venv venv
source venv/bin/activate # or venv\Scripts\activate

# Install core dependencies
pip install pydantic-ai mcp fastmcp logfire requests psutil

# Run the architect
python main.py
```
