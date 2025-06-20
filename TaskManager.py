import os
import json
from datetime import datetime

class TaskManager:
    def __init__(self):
        self.tasks = []
        self.file_name = "tasks.json"
        self.load_tasks()
    
    def load_tasks(self):
        if os.path.exists(self.file_name):
            try:
                with open(self.file_name, "r") as file:
                    self.tasks = json.load(file)
            except:
                print("Error loading task data. Starting with empty task list.")
                self.tasks = []
    
    def save_tasks(self):
        with open(self.file_name, "w") as file:
            json.dump(self.tasks, file)
    
    def add_task(self, title, description, due_date=None):
        """
        due_date debe ser string en formato 'YYYY-MM-DD' o None
        """
        task = {
            "id": len(self.tasks) + 1,
            "title": title,
            "description": description,
            "status": "Pending",  # Nuevo estado por defecto "Pending"
            "created_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "due_date": due_date if due_date else ""
        }
        self.tasks.append(task)
        self.save_tasks()
        print(f"Task '{title}' added successfully!")
    
    def list_tasks(self, filter_status=None, search_title=None):
        # Filtrar tareas según criterios
        filtered_tasks = self.tasks

        if filter_status:
            filtered_tasks = [task for task in filtered_tasks if task["status"].lower() == filter_status.lower()]

        if search_title:
            filtered_tasks = [task for task in filtered_tasks if search_title.lower() in task["title"].lower()]

        if not filtered_tasks:
            print("No tasks found with the given criteria.")
            return

        # Función auxiliar para ordenar por due_date
        def due_date_key(task):
            if task['due_date']:
                return datetime.strptime(task['due_date'], "%Y-%m-%d")
            else:
                return datetime.max

        sorted_tasks = sorted(filtered_tasks, key=due_date_key)

        print("\n" + "=" * 100)
        print(f"{'ID':<5} {'TITLE':<20} {'STATUS':<15} {'CREATED DATE':<20} {'DUE DATE':<12} {'DESCRIPTION':<30}")
        print("-" * 100)

        for task in sorted_tasks:
            due = task['due_date'] if task['due_date'] else "No due date"
            print(f"{task['id']:<5} {task['title'][:18]:<20} {task['status']:<15} {task['created_date']:<20} {due:<12} {task['description'][:28]:<30}")

        print("=" * 100 + "\n")
    
    def update_status(self, task_id, new_status):
        for task in self.tasks:
            if task["id"] == task_id:
                if new_status not in ["Pending", "In Progress", "Completed"]:
                    print("Invalid status. Please choose 'Pending', 'In Progress' or 'Completed'.")
                    return False
                task["status"] = new_status
                self.save_tasks()
                print(f"Task '{task['title']}' status updated to '{new_status}'!")
                return True
        return False
    
    def mark_complete(self, task_id):
        # Ahora usamos update_status para marcar como Completed
        if not self.update_status(task_id, "Completed"):
            # Mensaje mejorado cuando no encuentra la tarea
            input(f"Task with ID {task_id} not found. Press Enter to return to the menu.")
    
    def delete_task(self, task_id):
        for i, task in enumerate(self.tasks):
            if task["id"] == task_id:
                removed = self.tasks.pop(i)
                # Reasignar IDs para que no haya huecos
                for index, task in enumerate(self.tasks, start=1):
                    task["id"] = index
                self.save_tasks()
                print(f"Task '{removed['title']}' deleted successfully!")
                return True
        print(f"Task with ID {task_id} not found.")
        return False

    def edit_task(self, task_id):
        for task in self.tasks:
            if task["id"] == task_id:
                print(f"Current title: {task['title']}")
                new_title = input("Enter new title (leave blank to keep current): ").strip()
                if new_title:
                    task["title"] = new_title
                print(f"Current description: {task['description']}")
                new_description = input("Enter new description (leave blank to keep current): ").strip()
                if new_description:
                    task["description"] = new_description
                self.save_tasks()
                print(f"Task ID {task_id} updated successfully!")
                return True
        print(f"Task with ID {task_id} not found.")
        return False

def main():
    task_manager = TaskManager()
    
    while True:
        print("\nTASK MANAGER")
        print("1. Add Task")
        print("2. List Tasks")
        print("3. Mark Task as Complete")
        print("4. Update Task Status")
        print("5. Delete Task")
        print("6. Search and Filter Tasks")
        print("7. Edit Task")
        print("8. Exit")
        
        choice = input("Enter your choice (1-7): ")
        
        if choice == "1":
            title = input("Enter task title: ")
            if not title.strip():
                print("Error: Task title cannot be empty.")
                continue  # vuelve al menú principal sin agregar la tarea
            description = input("Enter task description: ")
            due_date_input = input("Enter due date (YYYY-MM-DD) or leave blank: ").strip()
            
            # Validar formato de fecha
            if due_date_input:
                try:
                    datetime.strptime(due_date_input, "%Y-%m-%d")
                except ValueError:
                    print("Invalid date format! Task will be added without due date.")
                    due_date_input = None
            else:
                due_date_input = None
            
            task_manager.add_task(title, description, due_date_input)
        
        elif choice == "2":
            # Listar todas sin filtro
            task_manager.list_tasks()
        
        elif choice == "3":
            while True:
                task_id_input = input("Enter task ID to mark as complete: ")
                if task_id_input.isdigit():
                    task_id = int(task_id_input)
                    task_manager.mark_complete(task_id)
                break
            else:
                print("Invalid input. Please enter a numeric task ID.")

        elif choice == "4":
            while True:
                task_id_input = input("Enter task ID to update status: ")
                if task_id_input.isdigit():
                    task_id = int(task_id_input)
                    print("Choose new status: Pending, In Progress, Completed")
                    new_status = input("Enter new status: ").strip()
                    if not task_manager.update_status(task_id, new_status):
                        input(f"Task with ID {task_id} not found or invalid status. Press Enter to return to menu.")
                    break  # Sale del while si todo va bien
                else:
                    print("Invalid input. Please enter a numeric task ID.")

        elif choice == "5":
            try:
                task_id = int(input("Enter task ID to delete: "))
                task_manager.delete_task(task_id)
            except ValueError:
                print("Invalid input. Please enter a valid integer ID.")

        elif choice == "6":
            search_title = input("Enter title keyword to search (leave blank to skip): ").strip()
            filter_status = input("Filter by status (Pending, In Progress, Completed) or leave blank: ").strip()
            # Validamos que el status sea válido o vacío
            if filter_status and filter_status not in ["Pending", "In Progress", "Completed"]:
                print("Invalid status filter. Showing all tasks.")
                filter_status = None
            if search_title == "":
                search_title = None
            
            task_manager.list_tasks(filter_status=filter_status, search_title=search_title)

        elif choice == "7":
            task_id_input = input("Enter task ID to edit: ")
            if task_id_input.isdigit():
                task_id = int(task_id_input)
                task_manager.edit_task(task_id)
            else:
                print("Invalid input. Please enter a numeric task ID.")

        elif choice == "8":
            print("Exiting Task Manager. Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
