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

# Example credentials
USERNAME = "user"
PASSWORD = "1234"

def show_login():
    login_frame = ctk.CTkFrame(root)
    login_frame.pack(fill="both", expand=True)

    # App name on top of the page
    title = ctk.CTkLabel(login_frame, text="TASKS MANAGER", font=("Times New Roman", 24, "bold"))
    title.pack(pady=20)
    # boxes for username and password
    user_entry = ctk.CTkEntry(login_frame, placeholder_text="Username", width=200)
    user_entry.place(relx=0.5, rely=0.45, anchor="center")
    # Cover password while being typed out
    pass_entry = ctk.CTkEntry(login_frame, placeholder_text="Password", show="*", width=200)
    pass_entry.place(relx=0.5, rely=0.55, anchor="center")


    # try loging in, if username and password is incorrect then it will display error
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

# END OF PART 1

# Using a point updating system to add points when tasks are marked as complete
def update_points(value):
    global points
    points += value
    points_label.configure(text = f"Points: {points}")

# Adding a task by having the user type in the field then click "Add task"
def add_task():
    task_name = entry.get()
    if task_name != "":
        # This makes sure the tasks get added on the application
        task_item = ctk.CTkFrame(task_frame)
        task_item.pack(pady = 2, fill = "x", anchor = "w")

        # Create a checkbox to let users know what they have done
        # Can also add points to keep track
        var = ctk.IntVar()
        checkbox = ctk.CTkCheckBox(
            task_item, text = task_name, font = ("Open Sans", 14),
            variable = var, command = lambda v = var: adjust_points(v),
            checkbox_width = 20,
            checkbox_height = 20,
        )
        checkbox.pack(side = "left", padx = 5, pady = 5)

        # Camera Feature to ensure certain tasks are done (correctly)
        cam_button = ctk.CTkButton(
            task_item, text = "📸", width = 40,
            command = lambda t = task_name: take_picture(t)
        )
        cam_button.pack(side = "right", padx = 5)

        tasks.append((task_name, checkbox, task_item, var))

        # Save interval chosen in dropdown
        interval = int(reminder_var.get())

        tasks.append((task_name, checkbox, task_item, var, interval))

        # Start reminder thread
        threading.Thread(target=reminder_loop, args=(task_name, var, interval), daemon=True).start()
        entry.delete(0, "end")
    else:
        messagebox.showwarning("Warning", "You must enter a task.")

# END OF PART 2

def adjust_points(var):
    if var.get() == 1:  # checked
        # Add 5 points if checkbox is checked off
        update_points(5)
    else:  # unchecked
        # Minus 5 points if check mark is taken off
        update_points(-5)

def remove_task():
    to_remove = [t for t in tasks if t[3].get() == 1]
    if not to_remove:
        messagebox.showinfo("Info", "No tasks checked for removal.")
        return
    for t in to_remove:
        t[2].destroy()
        tasks.remove(t)

def take_picture(task_name):
    # Asking for permission to use Camera Feature on the device
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        messagebox.showerror("Error", "Camera not found.")
        return

    messagebox.showinfo("Camera", f"Taking picture for: {task_name}\nPress 's' to save, 'q' to quit.")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        cv2.imshow(f"Camera - Task: {task_name}", frame)

        key = cv2.waitKey(1)
        if key == ord("s"):  # Save snapshot
            folder = "task_photos"
            os.makedirs(folder, exist_ok = True)
            filename = os.path.join(
                folder, f"{task_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            )
            cv2.imwrite(filename, frame)
            messagebox.showinfo("Saved", f"Picture saved for '{task_name}'\nFile: {filename}")
        elif key == ord("q"):  # Quit camera
            break

    cap.release()
    cv2.destroyAllWindows()
    #end of part 3
