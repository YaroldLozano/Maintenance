import tkinter as tk
from tkinter import messagebox
import psycopg2
from db import get_db_connection
from TaskManagerGUI import TaskManagerGUI

class LoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Login")

        # Campos de entrada
        tk.Label(root, text="Username").pack()
        self.username_entry = tk.Entry(root)
        self.username_entry.pack()

        tk.Label(root, text="Password").pack()
        self.password_entry = tk.Entry(root, show="*")
        self.password_entry.pack()

        # Botones de Login y Registro
        tk.Button(root, text="Login", command=self.login).pack(pady=5)
        tk.Button(root, text="Register", command=self.register).pack()

    def load_users(self):
        # Conectar a la base de datos y obtener los usuarios
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        conn.close()
        # Devuelve los usuarios como una lista de diccionarios
        return [{"username": user[1], "password": user[2]} for user in users]

    def save_user(self, username, password):
        # Guardar un nuevo usuario en la base de datos
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
        conn.commit()
        conn.close()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Cargar los usuarios desde la base de datos
        users = self.load_users()

        # Verificar las credenciales
        for user in users:
            if user["username"] == username and user["password"] == password:
                messagebox.showinfo("Login successful", f"Welcome, {username}!")
                self.root.destroy()
                self.open_task_manager(username)
                return

        messagebox.showerror("Error", "Invalid username or password")

    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Cargar los usuarios desde la base de datos
        users = self.load_users()

        # Verificar si el usuario ya existe
        if any(user["username"] == username for user in users):
            messagebox.showwarning("Error", "User already exists")
            return

        # Guardar el nuevo usuario en la base de datos
        self.save_user(username, password)
        messagebox.showinfo("Success", "User registered successfully")

    def open_task_manager(self, username):
        root = tk.Tk()
        app = TaskManagerGUI(root, username)
        root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    LoginApp(root)
    root.mainloop()
