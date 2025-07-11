import psycopg2
from db import get_db_connection
from datetime import datetime

class TaskManager:
    def __init__(self, username):
        self.username = username
        # Establecer conexión a la base de datos
        self.connection = get_db_connection()
        self.cursor = self.connection.cursor()  # Aquí inicializamos el cursor

    def load_tasks(self):
        # Ejecutamos la consulta SQL para cargar las tareas desde la base de datos
        self.cursor.execute("SELECT * FROM tasks WHERE username = %s", (self.username,))
        tasks = self.cursor.fetchall()
        return [{"id": task[0], "title": task[1], "description": task[2], 
                 "status": task[3], "created_date": task[4], "due_date": task[5]} for task in tasks]

    def save_tasks(self):
        # Guardar los cambios en la base de datos
        self.connection.commit()

    def add_task(self, title, description, due_date):
        # Agregar una tarea a la base de datos
        self.cursor.execute("""
            INSERT INTO tasks (title, description, status, created_date, due_date, username) 
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (title, description, "Pending", datetime.now().strftime("%Y-%m-%d"), due_date, self.username))
        self.save_tasks()

    def delete_task(self, task_id):
        # Eliminar una tarea de la base de datos
        self.cursor.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
        self.save_tasks()

    def update_status(self, task_id, new_status):
        # Actualizar el estado de una tarea en la base de datos
        self.cursor.execute("UPDATE tasks SET status = %s WHERE id = %s", (new_status, task_id))
        self.save_tasks()
