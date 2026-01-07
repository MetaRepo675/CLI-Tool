import json
import os
from pathlib import Path
from typing import List, Dict, Any
from .models import Task

class TaskDatabase:
    def __init__(self, db_path: str = "tasks.json"):
        self.db_path = Path(db_path)
        self._ensure_db_exists()
    
    def _ensure_db_exists(self):
        if not self.db_path.exists():
            self.db_path.write_text('{"tasks": [], "next_id": 1}')
    
    def _read_db(self) -> Dict[str, Any]:
        with open(self.db_path, 'r') as f:
            return json.load(f)
    
    def _write_db(self, data: Dict[str, Any]):
        with open(self.db_path, 'w') as f:
            json.dump(data, f, indent=2)
    
    def add_task(self, title: str, description: str = "", due_date: str = None) -> Task:
        data = self._read_db()
        task_id = data["next_id"]
        
        task = Task(
            id=task_id,
            title=title,
            description=description,
            due_date=due_date
        )
        
        data["tasks"].append(task.to_dict())
        data["next_id"] = task_id + 1
        self._write_db(data)
        
        return task
    
    def get_tasks(self, show_completed: bool = False) -> List[Task]:
        data = self._read_db()
        tasks = [Task.from_dict(t) for t in data["tasks"]]
        
        if not show_completed:
            tasks = [t for t in tasks if not t.completed]
        
        return sorted(tasks, key=lambda x: x.id)
    
    def complete_task(self, task_id: int) -> bool:
        data = self._read_db()
        
        for task in data["tasks"]:
            if task["id"] == task_id:
                task["completed"] = True
                self._write_db(data)
                return True
        
        return False
    
    def delete_task(self, task_id: int) -> bool:
        data = self._read_db()
        initial_length = len(data["tasks"])
        
        data["tasks"] = [t for t in data["tasks"] if t["id"] != task_id]
        
        if len(data["tasks"]) < initial_length:
            self._write_db(data)
            return True
        
        return False
    
    def search_tasks(self, keyword: str) -> List[Task]:
        data = self._read_db()
        results = []
        
        for task_data in data["tasks"]:
            task = Task.from_dict(task_data)
            if (keyword.lower() in task.title.lower() or 
                keyword.lower() in task.description.lower()):
                results.append(task)
        
        return results
