from app.utils.utils import DailyNoteData, build_daily_note_content
from server import mcp

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
