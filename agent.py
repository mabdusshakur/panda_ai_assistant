from google.adk.agents.llm_agent import Agent
import uuid
reminders = {}
todo_list = {}

# Tool: Set a reminder
def set_reminder(task: str, time_str: str) -> dict:
    reminder_id = str(uuid.uuid4())
    reminders[reminder_id] = {"task" : task, "time": time_str}
    return {"status": "success", "message": f"Reminder set for '{task}' at {time_str}."}

# Tool: Get reminders
def list_reminders() -> dict:
    if not reminders:
        return {"status": "success", "message": "You have no reminders set.", "items": []}
    items = [{"id": k, "task": v["task"], "time": v["time"]} for k, v in reminders.items()]
    return {"status": "success", "message": f"You have {len(items)} reminder(s) set.", "items": items}

# Tool: Get current time
def get_current_time() -> dict:
    from datetime import datetime
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return {"status": "success", "message": f"Current time is {current_time}."}

# Tool: Add to-do item
def add_todo(todo: str) -> dict:
    todo_id = str(uuid.uuid4())
    todo_list[todo_id] = todo
    return {"status": "success", "message": f"To-do item '{todo}' added."}

# Tool: List to-do items
def list_todos() -> dict:
    if not todo_list:
        return {"status": "success", "message": "You have no to-do items.", "items": []}
    items = [{"id": k, "task": v} for k, v in todo_list.items()]
    return {"status": "success", "message": f"You have {len(items)} to-do item(s) set.", "items": items}

# Tool: Delete to-do item
def delete_todo(todo_id: str) -> dict:
    if todo_id in todo_list:
        todo = todo_list.pop(todo_id)
        return {"status": "success", "message": f"To-do item '{todo}' deleted."}
    else:
        return {"status": "error", "message": f"No to-do item found with ID {todo_id}."}
    
root_agent = Agent(
    model='gemini-2.5-flash',
    name='root_agent',
    description='A helpful assistant for user questions.',
    instruction='You are a helpful assistant. Call the relevant tool for reminders, to-dos, times',
    tools=[set_reminder, list_reminders, get_current_time, add_todo, list_todos, delete_todo],
)