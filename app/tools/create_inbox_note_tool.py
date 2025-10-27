from utils.utils import InboxNoteData, build_inbox_note_content, save_inbox_note
from server import mcp

@mcp.tool()
def create_inbox_note(title: str, tasks: list[str], logs: list[str]) -> str:
    """create an inbox note

    Main goal:
        - create an inbox note for the user based on information sent by the user

    Args:
        title (str): the title of the inbox note (extract from the main topic/theme of the content)
        tasks (list[str]): the tasks related to this topic
        logs (list[str]): the notes/thoughts/information related to this topic

    Rules:
      - Only return information that the user gives to you, don't generate any information
      - Execute this tool when the user sends you a picture that DOES NOT contain the words "daily note"
      - If the content has multiple distinct topics/themes, you should create separate inbox notes for each topic
      - Extract a clear, descriptive title from the main theme of the content
      - If there's too much content for a daily note, extract the excess to inbox notes and link them
      - all the tasks related to this topic place them in the tasks list
      - all other information place it in the logs list
    """

    data = InboxNoteData(tasks=tasks, logs=logs)
    content = build_inbox_note_content(title, data)

    # create the inbox note
    note_path, safe_title = save_inbox_note(title, content)

    # build a context to pass to the llm
    context = f"""Tell the user you created the inbox note and here is the markdown template:
    {content}

    The note was saved as: [[{safe_title}]]
    """
    return context
