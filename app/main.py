from dotenv import load_dotenv
from server import mcp
from tools.create_daily_note_tool import create_daily_note

load_dotenv()

if __name__ == "__main__":
    import sys # For stderr and exit
    print("Starting MCP server...")
    try:
        # mcp.run typically blocks until stopped or an error occurs
        mcp.run(transport="stdio")
        print("MCP server stopped normally.") # Reached if mcp.run exits cleanly
    except KeyboardInterrupt:
        print("\nMCP server stopped by user.", file=sys.stderr)
        sys.exit(0) # Exit cleanly on Ctrl+C
    except Exception as e:
        # Log any other exceptions that occur during execution
        print(f"MCP server encountered an error: {e}", file=sys.stderr)
        sys.exit(1) # Exit with a non-zero status code to indicate an error
