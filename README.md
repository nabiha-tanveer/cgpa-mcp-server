# CGPA Guider: MCP + Memory + Streaming

PUCIT BS Computer Science CGPA assistant. The agent's tools live on a separate MCP server hosted on the internet, and the agent has persistent memory and streaming output.

## MCP Server
- Hosted on: FastMCP Horizon
- Server URL: https://cgpa-guider.fastmcp.app/mcp
- Authentication: required (Bearer API key)
- API key: <YAHAN APNI HORIZON KEY PASTE KARO>
- Server code (GitHub): https://github.com/nabiha-tanveer/cgpa-mcp-server

## Project structure
- `server/`: FastMCP server exposing 7 tools: `marks_to_grade_points`, `calculate_semester_gpa`, `calculate_new_cgpa`, `required_gpa_for_target`, `get_semester_courses`, `get_remaining_credit_hours`, `save_report`
- `agent/`: async LangChain agent (`create_agent`) that loads its tools from the MCP server

## How to run the agent
1. `cd agent`
2. Install dependencies:
   ```
   pip install -U "langchain[mcp]" langgraph langchain-groq langgraph-checkpoint-sqlite aiosqlite python-dotenv
   ```
3. Create a `.env` file in `agent/`:
   ```
   GROQ_API_KEY=<your Groq key>
   MCP_URL=https://cgpa-guider.fastmcp.app/mcp
   FASTMCP_KEY=<Horizon API key from above>
   ```
4. Run `python agent.py`

Commands inside the chat: `/switch`, `/history`, `/forget`, `exit`.

## Features
- **MCP (Task 1, 2, 5):** tools moved from `tools.py` to a FastMCP server and deployed on Horizon. The agent only needs `MCP_URL` and the key in `.env`.
- **Memory (Task 3):** `AsyncSqliteSaver` (`memory.db`), `thread_id` is the person's name, so chats survive restarts.
- **Streaming (Task 4):** `astream` with `stream_mode=["updates", "messages"]`. Tokens print live and tool calls are shown as `[tool: name]`.
- **Server down (Task 6):** a failed tool call is turned into an error `ToolMessage`, so the model tells the user the service is down. `repair_history` adds an error `ToolMessage` for any old tool call left without an answer, so the chat is never stuck.
