from typing import TypedDict
from datetime import datetime
import os

class DailyNoteData(TypedDict):
    dayPlanner: list[str]
    tasks: list[str]
    logs: list[str]

class InboxNoteData(TypedDict):
    tasks: list[str]
    logs: list[str]
# get the daily note path
def get_daily_note_path():
    vault_path = os.getenv("VAULT_PATH")
    daily_notes_relative_path = os.getenv("DAILY_NOTES_PATH", "daily-notes")
    if not vault_path:
        raise ValueError("VAULT_PATH environment variable is not set")
    daily_notes_path = os.path.join(vault_path, daily_notes_relative_path)
    # if path doesn't exist throw an error
    if not os.path.exists(daily_notes_path):
        raise FileNotFoundError(f"Daily notes path {daily_notes_path} does not exist")
    return daily_notes_path

# get the inbox note path
def get_inbox_note_path():
    vault_path = os.getenv("VAULT_PATH")
    inbox_notes_relative_path = os.getenv("INBOX_NOTES_PATH", "inbox")
    if not vault_path:
        raise ValueError("VAULT_PATH environment variable is not set")
    inbox_notes_path = os.path.join(vault_path, inbox_notes_relative_path)
    # if path doesn't exist throw an error
    if not os.path.exists(inbox_notes_path):
        raise FileNotFoundError(f"Inbox notes path {inbox_notes_path} does not exist")
    return inbox_notes_path

def build_daily_note_content(data: DailyNoteData):
  # get template data
  template_path = os.path.join(os.path.dirname(__file__), "templates", "daily-note.md")
  with open(template_path, "r") as file:
    template = file.read()

  # Build sections with proper block formatting
  sections = []

  # Day planner section
  sections.append("## Day planner\n")
  if data["dayPlanner"]:
    sections.append("\n".join(["- " + line for line in data["dayPlanner"]]))
  sections.append("\n")

  # Tasks section
  sections.append("\n## Tasks\n")
  if data["tasks"]:
    sections.append("\n".join(["- [ ] " + line for line in data["tasks"]]))
  sections.append("\n")

  # Daily Logs section
  sections.append("\n## Daily Logs\n")
  if data["logs"]:
    sections.append("\n".join(["- " + line for line in data["logs"]]))
  sections.append("\n")

  # Youtube Bookmarks section (static)
  sections.append("\n## Youtube Bookmarks\n\n```dataview\nlist from \"Youtube Bookmarks\" where contains(file.outlinks, this.file.link)\n```\n")

  content = "".join(sections)
  return content

def save_daily_note(content: str):
    # create the daily note
    daily_notes_path = get_daily_note_path()
    # get the current date
    current_date = datetime.now()
    # format the date
    date_str = current_date.strftime("%A %d %B %Y")
    # create the daily note
    daily_note_path = os.path.join(daily_notes_path, f"{date_str}.md")
    # return the path to the daily note
    with open(daily_note_path, 'w') as f:
        f.write(content)
    return daily_note_path

def build_inbox_note_content(title: str, data: InboxNoteData):
    # Build sections with proper block formatting
    sections = []

    # Title
    sections.append(f"# {title}\n")

    # Tasks section
    if data["tasks"]:
        sections.append("\n## Tasks\n\n")
        sections.append("\n".join(["- [ ] " + line for line in data["tasks"]]))
        sections.append("\n")

    # Logs section
    if data["logs"]:
        sections.append("\n## Logs\n\n")
        sections.append("\n".join(["- " + line for line in data["logs"]]))
        sections.append("\n")

    content = "".join(sections)
    return content

def save_inbox_note(title: str, content: str):
    # create the inbox note
    inbox_notes_path = get_inbox_note_path()
    # sanitize title for filename (remove special characters)
    safe_title = "".join(c if c.isalnum() or c in (' ', '-', '_') else '' for c in title)
    safe_title = safe_title.replace(' ', '-')
    # create the inbox note with title as filename
    inbox_note_path = os.path.join(inbox_notes_path, f"{safe_title}.md")
    # write the content
    with open(inbox_note_path, 'w') as f:
        f.write(content)
    return inbox_note_path, safe_title