import argparse
import sys
from .database import TaskDatabase
from .utils import display_task, validate_date

def main():
    parser = argparse.ArgumentParser(
        description="TaskMaster - A simple CLI task manager",
        prog="taskmaster"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Add command
    add_parser = subparsers.add_parser("add", help="Add a new task")
    add_parser.add_argument("title", help="Title of the task")
    add_parser.add_argument("-d", "--description", help="Task description", default="")
    add_parser.add_argument("--due", help="Due date (YYYY-MM-DD)")
    
    # List command
    list_parser = subparsers.add_parser("list", help="List all tasks")
    list_parser.add_argument("-a", "--all", action="store_true", 
                           help="Show all tasks including completed")
    list_parser.add_argument("-v", "--verbose", action="store_true",
                           help="Show detailed task information")
    
    # Complete command
    complete_parser = subparsers.add_parser("complete", help="Mark a task as complete")
    complete_parser.add_argument("task_id", type=int, help="ID of the task to complete")
    
    # Delete command
    delete_parser = subparsers.add_parser("delete", help="Delete a task")
    delete_parser.add_argument("task_id", type=int, help="ID of the task to delete")
    
    # Search command
    search_parser = subparsers.add_parser("search", help="Search tasks")
    search_parser.add_argument("keyword", help="Keyword to search for")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    db = TaskDatabase()
    
    if args.command == "add":
        due_date = args.due
        if due_date and not validate_date(due_date):
            print("Error: Invalid date format. Use YYYY-MM-DD")
            sys.exit(1)
        
        task = db.add_task(args.title, args.description, due_date)
        print(f"Task added successfully (ID: {task.id})")
    
    elif args.command == "list":
        tasks = db.get_tasks(show_completed=args.all)
        
        if not tasks:
            print("No tasks found.")
            return
        
        for task in tasks:
            print(display_task(task, args.verbose))
            if not args.verbose and task != tasks[-1]:
                print()
    
    elif args.command == "complete":
        if db.complete_task(args.task_id):
            print(f"Task #{args.task_id} marked as complete")
        else:
            print(f"Task #{args.task_id} not found")
            sys.exit(1)
    
    elif args.command == "delete":
        if db.delete_task(args.task_id):
            print(f"Task #{args.task_id} deleted")
        else:
            print(f"Task #{args.task_id} not found")
            sys.exit(1)
    
    elif args.command == "search":
        tasks = db.search_tasks(args.keyword)
        
        if not tasks:
            print(f"No tasks found matching '{args.keyword}'")
        else:
            print(f"Found {len(tasks)} task(s):")
            print("-" * 40)
            for task in tasks:
                print(display_task(task, True))
                if task != tasks[-1]:
                    print()

if __name__ == "__main__":
    main()
