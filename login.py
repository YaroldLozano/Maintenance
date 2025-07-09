import tkinter as tk
from tkinter import messagebox
import json
import os
from TaskManagerGUI import TaskManagerGUI

USERS_FILE = "users.json"

class LoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Login")

        tk.Label(root, text="Username").pack()
        self.username_entry = tk.Entry(root)
        self.username_entry.pack()

        tk.Label(root, text="Password").pack()
        self.password_entry = tk.Entry(root, show="*")
        self.password_entry.pack()

        tk.Button(root, text="Login", command=self.login).pack(pady=5)
        tk.Button(root, text="Register", command=self.register).pack()

    def load_users(self):
        if not os.path.exists(USERS_FILE):
            return []
        with open(USERS_FILE, "r") as f:
            return json.load(f)

    def save_users(self, users):
        with open(USERS_FILE, "w") as f:
            json.dump(users, f, indent=2)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        users = self.load_users()

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
        users = self.load_users()

        if any(user["username"] == username for user in users):
            messagebox.showwarning("Error", "User already exists")
            return

        users.append({"username": username, "password": password})
        self.save_users(users)
        messagebox.showinfo("Success", "User registered successfully")

    def open_task_manager(self, username):
        root = tk.Tk()
        app = TaskManagerGUI(root, username)
        root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    LoginApp(root)
    root.mainloop()
