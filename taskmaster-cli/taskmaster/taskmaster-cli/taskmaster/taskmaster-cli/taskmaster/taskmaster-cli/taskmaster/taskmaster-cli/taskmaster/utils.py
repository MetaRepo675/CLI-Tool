from datetime import datetime

def format_date(date_string: str) -> str:
    try:
        dt = datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S")
        return dt.strftime("%b %d, %Y %I:%M %p")
    except:
        return date_string

def display_task(task, show_details=False):
    status = "✓" if task.completed else "◻"
    output = f"[{status}] #{task.id}: {task.title}"
    
    if show_details:
        if task.description:
            output += f"\n   Description: {task.description}"
        if task.due_date:
            output += f"\n   Due: {task.due_date}"
        output += f"\n   Created: {format_date(task.created_at)}"
    
    return output

def validate_date(date_string: str) -> bool:
    try:
        datetime.strptime(date_string, "%Y-%m-%d")
        return True
    except ValueError:
        return False
