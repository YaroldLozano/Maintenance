import json
import os
from datetime import datetime

class TaskManager:
    def __init__(self, username):
        self.username = username
        self.file_path = f"tasks_{username}.json"
        self.tasks = self.load_tasks()

    def load_tasks(self):
        if not os.path.exists(self.file_path):
            return []
        with open(self.file_path, "r") as f:
            return json.load(f)

    def save_tasks(self):
        with open(self.file_path, "w") as f:
            json.dump(self.tasks, f, indent=2)

    def add_task(self, title, description, due_date):
        new_task = {
            "id": self.generate_id(),
            "title": title,
            "description": description,
            "status": "Pending",
            "created_date": datetime.now().strftime("%Y-%m-%d"),
            "due_date": due_date or ""
        }
        self.tasks.append(new_task)
        self.save_tasks()

    def generate_id(self):
        return max((task["id"] for task in self.tasks), default=0) + 1

    def delete_task(self, task_id):
        initial_len = len(self.tasks)
        self.tasks = [t for t in self.tasks if t["id"] != task_id]
        self.save_tasks()
        return len(self.tasks) < initial_len

    def update_status(self, task_id, new_status):
        for task in self.tasks:
            if task["id"] == task_id:
                task["status"] = new_status
                return True
        return False
