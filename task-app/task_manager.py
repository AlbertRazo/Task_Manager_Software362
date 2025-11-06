# CPSC 362 Project: TASKS MANAGER APPLICATION

import customtkinter as ctk
from tkinter import messagebox
import cv2
import os
from datetime import datetime
from plyer import notification
import threading
import time
from PIL import Image


# ----------------------------- Global State -----------------------------
# Store tasks as (task_name, checkbox, task_frame, var, interval_minutes)
tasks = []
points = 0

# Demo credentials
USERNAME = "user"
PASSWORD = "1234"

# ----------------------------- Theme / Root -----------------------------
ctk.set_appearance_mode("black")
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.title("TASKS MANAGER")
root.geometry("520x720")

# Will be assigned inside show_todo_app()
points_label = None
entry = None
task_frame = None
reminder_var = None


# ----------------------------- Helpers -----------------------------
def reminder_loop(task_name, var, interval):
    """Send notifications every X minutes until task is completed."""
    interval = max(1, int(interval))
    while var.get() == 0:  # task not yet completed
        for _ in range(interval * 60):
            if var.get() == 1:
                return
            time.sleep(1)
        if var.get() == 0:
            try:
                notification.notify(
                    title="TASKS MANAGER",
                    message=f"Don’t forget to finish: {task_name}!",
                    timeout=5,
                )
            except Exception:
                pass


def update_points(value):
    """Increment or decrement the points label."""
    global points, points_label
    points += value
    if points_label is not None:
        points_label.configure(text=f"Points: {points}")


def adjust_points(var):
    """Called by each checkbox to award/deduct points."""
    if var.get() == 1:
        update_points(5)
    else:
        update_points(-5)


def take_picture(task_name):
    """Open webcam, allow 's' to save snapshot, 'q' to quit."""
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

        if key == ord("s"):
            folder = "task_photos"
            os.makedirs(folder, exist_ok=True)
            filename = os.path.join(
                folder, f"{task_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            )
            cv2.imwrite(filename, frame)
            messagebox.showinfo("Saved", f"Picture saved for '{task_name}'\nFile: {filename}")

        elif key == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


def remove_task():
    """Remove all tasks that are currently checked."""
    to_remove = [t for t in tasks if t[3].get() == 1]
    if not to_remove:
        messagebox.showinfo("Info", "No tasks checked for removal.")
        return
    for t in to_remove:
        try:
            t[3].set(1)
        except Exception:
            pass
        t[2].destroy()
        tasks.remove(t)


def add_task():
    """Create a new task row with checkbox, camera button, and reminder thread."""
    global entry, task_frame, reminder_var

    task_name = entry.get().strip()
    if task_name == "":
        messagebox.showwarning("Warning", "You must enter a task.")
        return

    task_item = ctk.CTkFrame(task_frame)
    task_item.pack(pady=4, fill="x", anchor="w")

    var = ctk.IntVar(value=0)
    checkbox = ctk.CTkCheckBox(
        task_item,
        text=task_name,
        font=("Open Sans", 14),
        variable=var,
        command=lambda v=var: adjust_points(v),
        checkbox_width=20,
        checkbox_height=20,
    )
    checkbox.pack(side="left", padx=8, pady=8)

    cam_button = ctk.CTkButton(
        task_item,
        text="📸",
        width=40,
        command=lambda t=task_name: take_picture(t),
    )
    cam_button.pack(side="right", padx=6)

    try:
        interval = int(reminder_var.get())
    except Exception:
        interval = 5

    task_tuple = (task_name, checkbox, task_item, var, interval)
    tasks.append(task_tuple)

    threading.Thread(
        target=reminder_loop, args=(task_name, var, interval), daemon=True
    ).start()

    entry.delete(0, "end")


# ----------------------------- UI Screens -----------------------------
def show_login():
    """Simple login gate before main app."""
    login_frame = ctk.CTkFrame(root)
    login_frame.pack(fill="both", expand=True)

    # --- Background image setup ---
    bg_image = ctk.CTkImage(
        light_image=Image.open("classroom_bg.png"),
        size=(520, 720)
    )
    bg_label = ctk.CTkLabel(login_frame, image=bg_image, text="")
    bg_label.place(relx=0.5, rely=0.5, anchor="center")

    # --- Foreground elements (text boxes, buttons) ---
    title = ctk.CTkLabel(
    login_frame,
    text="TASKS MANAGER",
    font=("Times New Roman", 26, "bold"),
    text_color="dodgerblue",
    fg_color="#CBE2FA"
    )
    title.place(relx=0.5, rely=0.15, anchor="center")

    user_entry = ctk.CTkEntry(
    login_frame,
    placeholder_text="Username",
    width=220,
    fg_color="#E6EEF9",              # soft blue-gray box
    text_color="#000000",            # dark text when typing
    placeholder_text_color="#6A747C" # gray placeholder
    )
    user_entry.place(relx=0.5, rely=0.30, anchor="center")
    
    pass_entry = ctk.CTkEntry(
    login_frame,
    placeholder_text="Password",
    show="*",
    width=220,
    fg_color="#E6EEF9",
    text_color="#000000",
    placeholder_text_color="#6C757D"
    )
    pass_entry.place(relx=0.5, rely=0.35, anchor="center")

    def attempt_login():
        if user_entry.get() == USERNAME and pass_entry.get() == PASSWORD:
            login_frame.destroy()
            show_todo_app()
        else:
            messagebox.showerror("Error", "Invalid username or password!")

    login_button = ctk.CTkButton(
    login_frame,
    text="Login",
    command=attempt_login,
    width=120,
    height=35,
    fg_color="#007BFF",      # Blue background
    hover_color="#dodgerblue",   # Darker blue when hovered
    text_color="#FFFFFF"     # Dark text
)

    login_button.place(relx=0.5, rely=0.45, anchor="center")


def logout():
    """Destroy current UI and return to login screen."""
    for widget in root.winfo_children():
        widget.destroy()
    show_login()


def show_todo_app():
    """Build the main Tasks Manager interface."""
    global points_label, entry, task_frame, reminder_var

    top = ctk.CTkFrame(root)
    top.pack(fill="x", padx=12, pady=(12, 0))

    title = ctk.CTkLabel(top, text="Your Tasks", font=("Times New Roman", 22, "bold"))
    title.pack(side="left", padx=6, pady=8)

    logout_btn = ctk.CTkButton(top, text="Logout", width=80, command=logout)
    logout_btn.pack(side="right", padx=6, pady=8)

    points_bar = ctk.CTkFrame(root)
    points_bar.pack(fill="x", padx=12, pady=12)
    points_label = ctk.CTkLabel(points_bar, text=f"Points: {points}", font=("Open Sans", 16, "bold"))
    points_label.pack(side="left", padx=8, pady=8)

    input_row = ctk.CTkFrame(root)
    input_row.pack(fill="x", padx=12)

    entry = ctk.CTkEntry(input_row, placeholder_text="Enter a new task...")
    entry.pack(side="left", fill="x", expand=True, padx=(8, 6), pady=8)

    reminder_var = ctk.StringVar(value="5")
    reminder_menu = ctk.CTkOptionMenu(
        input_row,
        values=["1", "5", "10", "15", "30", "60"],
        variable=reminder_var,
        width=80,
    )
    reminder_menu.pack(side="left", padx=6, pady=8)

    add_btn = ctk.CTkButton(input_row, text="Add", width=80, command=add_task)
    add_btn.pack(side="left", padx=(6, 8), pady=8)

    list_container = ctk.CTkFrame(root)
    list_container.pack(fill="both", expand=True, padx=12, pady=(8, 12))

    task_frame = ctk.CTkScrollableFrame(list_container, label_text="Tasks")
    task_frame.pack(fill="both", expand=True, padx=8, pady=8)

    bottom = ctk.CTkFrame(root)
    bottom.pack(fill="x", padx=12, pady=(0, 12))

    remove_btn = ctk.CTkButton(bottom, text="Remove Checked", command=remove_task)
    remove_btn.pack(side="right", padx=8, pady=8)


# ----------------------------- App Start -----------------------------
if __name__ == "__main__":
    show_login()
    root.mainloop()
#end of part 4
