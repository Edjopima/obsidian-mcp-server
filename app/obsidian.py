from mcp.server.fastmcp import FastMCP
from typing import TypedDict
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

mcp = FastMCP("obsidian")

class DailyNoteData(TypedDict):
    dayPlanner: list[str]
    tasks: list[str]
    logs: list[str]
# get the daily note path
def get_daily_note_path():
    valut_path = os.getenv("VAULT_PATH")
    daily_notes_path = os.path.join(valut_path, "daily-notes")
    # if path doesn't exist throw an error
    if not os.path.exists(daily_notes_path):
        raise FileNotFoundError(f"Daily notes path {daily_notes_path} does not exist")
    return daily_notes_path

def build_daily_note_content(data: DailyNoteData):
  # get template data
  template_path = os.path.join(os.path.dirname(__file__), "templates", "daily-note.md")
  with open(template_path, "r") as file:
    template = file.read()

  # build the variables for the template
  day_planner = "\n".join(data["dayPlanner"])
  tasks = "\n".join(data["tasks"])
  logs = "\n".join(data["logs"])

  # replace the placeholders with the actual data
  content = template.format(day_planner=day_planner, tasks=tasks, logs=logs)
  return content

def create_daily_note(data: DailyNoteData):
    # create the daily note
    daily_notes_path = get_daily_note_path()
    # get the current date
    current_date = datetime.now()
    # format the date
    date_str = current_date.strftime("%A %d %B %Y")
    # create the daily note
    daily_note_path = os.path.join(daily_notes_path, f"{date_str}.md")
    # return the path to the daily note
    return daily_note_path

@mcp.tool()
def create_daily_note(day_planner: list[str], tasks: list[str], logs: list[str]) -> str:
    """create a daily note

    Args:
        day_planner (list[str]): the day planner
        tasks (list[str]): the tasks
        logs (list[str]): the logs
    """

    data = DailyNoteData(dayPlanner=day_planner, tasks=tasks, logs=logs)
    content = build_daily_note_content(data)
    
    # build a context to pass the llm the markdown template to send it to the user
    context = f""" Tell the user that you can create a daily note for them.
    Here is the markdown template:
    {content}
    """
    return context

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
