from utils.utils import DailyNoteData, build_daily_note_content, save_daily_note
from server import mcp

@mcp.tool()
def create_daily_note(day_planner: list[str], tasks: list[str], logs: list[str]) -> str:
    """create a daily note

    Main goal:
        - create a daily note for the user based on a picture sent by the user

    Args:
        day_planner (list[str]): the day planner
        tasks (list[str]): the tasks
        logs (list[str]): the logs

    Rules:
      - Only return information that the user gives to you, don't generate any information
      - the information will be given to you by the user in a picture
      - Execute this tool when the user sends you a picture that include information about the day, tasks or the user's thoughts
      - all the meeting information place it in the day_planner list
      - all the tasks place it in the tasks list
      - other information place it in the logs list
    """

    data = DailyNoteData(dayPlanner=day_planner, tasks=tasks, logs=logs)
    content = build_daily_note_content(data)

    # create the daily note in the main folder of this project
    save_daily_note(content)

    # build a context to pass the llm the markdown template to send it to the user
    context = f""" Tell the user you created the daily note and here is the markdown template:
    {content}
    """
    return context
