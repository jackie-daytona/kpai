# kpai -- Airline KPI Evaluator

A full-stack AI-powered KPI evaluation tool built with FastAPI, PostgreSQL, and the Anthropic Claude API. Interact via a web dashboard or natural language through Claude Desktop via MCP.

## Stack
- **Backend:** Python, FastAPI
- **Database:** PostgreSQL
- **AI:** Anthropic Claude API
- **Frontend:** HTML, Chart.js
- **MCP Server:** Model Context Protocol integration for Claude Desktop

## Features
- Station-level KPI scorecards with red/yellow/green indicators
- Actual vs target and YoY charts
- AI-generated evaluation reports powered by Claude
- Reports saved and organized by station and date
- Natural language querying via Claude Desktop -- ask Claude to pull and analyze any station's KPIs directly

## Setup

### Web App
1. Clone the repo
2. Create a virtual environment and install dependencies: `pip install -r requirements.txt`
3. Add a `.env` file with your `ANTHROPIC_API_KEY` and `DATABASE_URL`
4. Run the server from the `api/` directory: `uvicorn main:app --reload`
5. Open `index.html` in your browser

### MCP Server (Claude Desktop)
1. Complete steps 1-3 above
2. Add the following to your `claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "kpai": {
      "command": "/path/to/your/python",
      "args": ["/path/to/kpai/mcp_server/server.py"],
      "env": {
        "DATABASE_URL": "postgresql://localhost/kpai"
      }
    }
  }
}
```
3. Restart Claude Desktop and ask it anything about your KPI data
