# CPSC 362 Project: TASKS MANAGER APPLICATION

# importing Custom Tkinter features, OpenCV, Plyer for the app, camera, notification
import customtkinter as ctk
from tkinter import messagebox
import cv2
import os
from datetime import datetime
from plyer import notification
import threading
import time

# Store tasks as (task_name, checkbox, task_frame, interval)
tasks = []
# Keeping points
points = 0



# Hardcoded credentials (for demo)
USERNAME = "user"
PASSWORD = "1234"

def show_login():
    login_frame = ctk.CTkFrame(root)
    login_frame.pack(fill="both", expand=True)

    title = ctk.CTkLabel(login_frame, text="TASKS MANAGER", font=("Times New Roman", 24, "bold"))
    title.pack(pady=20)

    user_entry = ctk.CTkEntry(login_frame, placeholder_text="Username", width=200)
    user_entry.place(relx=0.5, rely=0.45, anchor="center")
    # Cover password while being typed out
    pass_entry = ctk.CTkEntry(login_frame, placeholder_text="Password", show="*", width=200)
    pass_entry.place(relx=0.5, rely=0.55, anchor="center")


def attempt_login():
    if user_entry.get() == USERNAME and pass_entry.get() == PASSWORD:
        login_frame.destroy()   # remove login page
        show_todo_app()        # load main app
    else:
        messagebox.showerror("Error", "Invalid username or password!")

    login_button = ctk.CTkButton(login_frame, text="Login", command=attempt_login, width=100)
    login_button.place(relx=0.5, rely=0.65, anchor="center")

# Log out function
def logout():
    for widget in root.winfo_children():
        widget.destroy()   # erase to do list and content
    show_login()           # go back to log in screen

# Initialize the main application window
root = ctk.CTk()
root.title("Tasks Manager Application")
root.geometry("800x600")

# Show the login screen
show_login()

# Start the Tkinter event loop
root.mainloop()

#End of stage 1 code