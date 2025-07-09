from TaskManager import TaskManager
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import datetime

class TaskManagerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Task Manager GUI")
        self.task_manager = TaskManager()
        
        # Frame principal
        frame = ttk.Frame(root, padding=10)
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Filtro: búsqueda por palabra clave y estado
        filter_frame = ttk.Frame(frame)
        filter_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(filter_frame, text="Buscar:").pack(side=tk.LEFT)
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(filter_frame, textvariable=self.search_var, width=30)
        search_entry.pack(side=tk.LEFT, padx=5)

        ttk.Label(filter_frame, text="Estado:").pack(side=tk.LEFT)
        self.status_var = tk.StringVar()
        status_combo = ttk.Combobox(filter_frame, textvariable=self.status_var, values=["", "Pending", "Completed"], width=15)
        status_combo.pack(side=tk.LEFT, padx=5)
        status_combo.set("")

        ttk.Button(filter_frame, text="Aplicar Filtros", command=self.refresh_tasks).pack(side=tk.LEFT, padx=5)
        ttk.Button(filter_frame, text="Limpiar", command=self.clear_filters).pack(side=tk.LEFT)

        # Treeview para mostrar tareas
        columns = ("ID", "Title", "Status", "Created Date", "Due Date", "Description")
        self.tree = ttk.Treeview(frame, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, minwidth=50, width=100, anchor=tk.W)
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # Botones
        btn_frame = ttk.Frame(root, padding=10)
        btn_frame.pack(fill=tk.X)
        
        ttk.Button(btn_frame, text="Add Task", command=self.add_task).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Edit Task", command=self.edit_task).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Delete Task", command=self.delete_task).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Mark Complete", command=self.mark_complete).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Refresh", command=self.refresh_tasks).pack(side=tk.RIGHT, padx=5)
        
        self.refresh_tasks()

    def refresh_tasks(self):
        # Limpia la tabla
        for row in self.tree.get_children():
            self.tree.delete(row)

        keyword = self.search_var.get().lower()
        status_filter = self.status_var.get()

        for task in self.task_manager.tasks:
            if status_filter and task["status"] != status_filter:
                continue
            if keyword and keyword not in task["title"].lower() and keyword not in task["description"].lower():
                continue

            due = task['due_date'] if task['due_date'] else "No due date"
            self.tree.insert("", tk.END, values=(
                task["id"],
                task["title"],
                task["status"],
                task["created_date"],
                due,
                task["description"][:30] + ("..." if len(task["description"]) > 30 else "")
            ))

    def clear_filters(self):
        self.search_var.set("")
        self.status_var.set("")
        self.refresh_tasks()
    
    def add_task(self):
        dlg = TaskDialog(self.root, "Add Task")
        if dlg.result:
            title, desc, due_date = dlg.result
            if not title.strip():
                messagebox.showerror("Error", "Title cannot be empty!")
                return
            self.task_manager.add_task(title, desc, due_date)
            self.refresh_tasks()
    
    def get_selected_task_id(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "No task selected.")
            return None
        task_id = self.tree.item(selected[0])["values"][0]
        return task_id

    def edit_task(self):
        task_id = self.get_selected_task_id()
        if task_id is None:
            return
        task = next((t for t in self.task_manager.tasks if t["id"] == task_id), None)
        if not task:
            messagebox.showerror("Error", "Selected task not found.")
            return
        
        dlg = TaskDialog(self.root, "Edit Task", task)
        if dlg.result:
            title, desc, due_date = dlg.result
            if not title.strip():
                messagebox.showerror("Error", "Title cannot be empty!")
                return
            task["title"] = title
            task["description"] = desc
            task["due_date"] = due_date if due_date else ""
            self.task_manager.save_tasks()
            self.refresh_tasks()

    def delete_task(self):
        task_id = self.get_selected_task_id()
        if task_id is None:
            return
        answer = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete the selected task?")
        if answer:
            success = self.task_manager.delete_task(task_id)
            if success:
                self.refresh_tasks()
            else:
                messagebox.showerror("Error", "Task not found or could not be deleted.")

    def mark_complete(self):
        task_id = self.get_selected_task_id()
        if task_id is None:
            return
        if self.task_manager.update_status(task_id, "Completed"):
            self.task_manager.save_tasks()  # 👈 Asegura que se guarde el cambio
            self.refresh_tasks()
        else:
            messagebox.showerror("Error", "Could not mark task as complete.")

class TaskDialog(simpledialog.Dialog):
    def __init__(self, parent, title, task=None):
        self.task = task
        super().__init__(parent, title)
    
    def body(self, frame):
        ttk.Label(frame, text="Title:").grid(row=0, column=0, sticky=tk.W)
        self.title_var = tk.StringVar(value=self.task["title"] if self.task else "")
        ttk.Entry(frame, textvariable=self.title_var, width=40).grid(row=0, column=1)

        ttk.Label(frame, text="Description:").grid(row=1, column=0, sticky=tk.W)
        self.desc_var = tk.StringVar(value=self.task["description"] if self.task else "")
        ttk.Entry(frame, textvariable=self.desc_var, width=40).grid(row=1, column=1)

        ttk.Label(frame, text="Due Date (YYYY-MM-DD):").grid(row=2, column=0, sticky=tk.W)
        self.due_var = tk.StringVar(value=self.task["due_date"] if self.task else "")
        ttk.Entry(frame, textvariable=self.due_var, width=40).grid(row=2, column=1)
        return frame

    def validate(self):
        due_date = self.due_var.get().strip()
        if due_date:
            try:
                datetime.strptime(due_date, "%Y-%m-%d")
            except ValueError:
                messagebox.showerror("Invalid date", "Due date must be in YYYY-MM-DD format.")
                return False
        return True
    
    def apply(self):
        self.result = (self.title_var.get().strip(), self.desc_var.get().strip(), self.due_var.get().strip())

if __name__ == "__main__":
    root = tk.Tk()
    app = TaskManagerGUI(root)
    root.mainloop()
