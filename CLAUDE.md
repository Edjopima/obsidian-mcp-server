# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an MCP (Model Context Protocol) server for Obsidian that creates daily notes and inbox notes from user-provided information (typically from images). The server uses FastMCP to expose tools that can be called by LLM clients.

## Architecture

### Core Components

- **[app/server.py](app/server.py)**: Initializes the FastMCP server instance named "obsidian"
- **[app/main.py](app/main.py)**: Entry point that loads environment variables and runs the MCP server with stdio transport
- **[app/tools/](app/tools/)**: MCP tool definitions decorated with `@mcp.tool()`
- **[app/utils/utils.py](app/utils/utils.py)**: Utility functions for building and saving daily notes and inbox notes

### How Tools Work

Tools are defined by decorating functions with `@mcp.tool()` from the `mcp` instance in [server.py](app/server.py). The server imports tool modules in [main.py](app/main.py) to register them. Each tool function:
1. Receives structured parameters from the LLM
2. Performs the requested operation
3. Returns context/results to send back to the LLM

### Note Creation Flow

**Daily Notes** (when image contains "daily note"):
1. User provides information (day planner, tasks, logs) via image containing "daily note"
2. `create_daily_note` tool receives parsed data as lists
3. Creates structured blocks: Day planner, Tasks, Daily Logs, and Youtube Bookmarks
4. Note is saved with date format "Day DD Month YYYY" in the daily notes directory
5. If content is excessive, extract overflow to linked inbox notes

**Inbox Notes** (when image does NOT contain "daily note"):
1. User provides information via image without "daily note" text
2. LLM extracts title from main topic/theme
3. `create_inbox_note` tool receives title, tasks, and logs
4. If multiple distinct topics exist, create separate inbox notes for each
5. Notes are saved with sanitized title as filename and linked using [[wikilinks]]

## Development Commands

```bash
# Run the MCP server
uv run app/main.py

# Install dependencies (uv manages them via pyproject.toml)
uv sync
```

## Environment Setup

Create a `.env` file with:
```
VAULT_PATH=/path/to/your/obsidian/vault
DAILY_NOTES_PATH=daily-notes    # optional, defaults to "daily-notes"
INBOX_NOTES_PATH=inbox           # optional, defaults to "inbox"
```

Required directories:
- `VAULT_PATH/DAILY_NOTES_PATH` - for daily notes
- `VAULT_PATH/INBOX_NOTES_PATH` - for inbox notes

Both paths are relative to `VAULT_PATH`.

## Key Design Patterns

- **Tool registration**: Import tool modules in [main.py](app/main.py) to register them with the server
- **Block-based content generation**: Notes are built with structured markdown blocks (Day planner, Tasks, Daily Logs, etc.)
- **Environment-based paths**: Vault and note locations configured via environment variables with defaults
- **Topic-based note separation**: Multiple topics in one image create separate linked inbox notes
- **Wikilink connections**: Inbox notes use [[wikilinks]] for Obsidian-style linking
