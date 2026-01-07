from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Optional

@dataclass
class Task:
    id: int
    title: str
    description: str = ""
    completed: bool = False
    created_at: Optional[str] = None
    due_date: Optional[str] = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def to_dict(self):
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data):
        return cls(**data)
