import tkinter as tk
from tkinter import simpledialog

from core.common import constants


def center_window(root, width, height):
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    x_coordinate = int((screen_width / 2) - (width / 2))
    y_coordinate = int((screen_height / 2) - (height / 2))

    root.geometry(f"{width}x{height}+{x_coordinate}+{y_coordinate}")


def name_dialog(clipboard):
    clipboard.has_popup = True

    def on_ok():
        input_text = entry.get()
        if (
            not input_text.strip()
        ):  # Check if the input is empty or contains only whitespaces
            error_label.config(text="Invalid Entry", fg="red")
        else:
            clipboard.new_folder_name = input_text.replace(" ", "_")
            clipboard.trigger_operation = True
            popup.destroy()

    def on_cancel():
        popup.destroy()

    popup = tk.Tk()
    popup.title("Create New Folder")
    popup.geometry("300x150")
    popup.resizable(width=False, height=False)

    if not constants.IS_LINUX:
        center_window(popup, 300, 100)

    icon_path = "./assets/icon.png"
    popup.iconphoto(True, tk.PhotoImage(file=icon_path))

    label = tk.Label(popup, text="Folder name:", padx=20, pady=20)
    label.pack()

    entry = tk.Entry(popup, width=30, justify="center")
    entry.insert(0, "New Folder")
    entry.pack(padx=20)

    ok_button = tk.Button(popup, text="Ok", command=on_ok)
    ok_button.pack(side=tk.LEFT, padx=25)

    cancel_button = tk.Button(popup, text="Cancel", command=on_cancel)
    cancel_button.pack(side=tk.RIGHT, padx=25)

    # Label to display error message
    error_label = tk.Label(popup, text="", fg="red")
    error_label.pack()

    popup.mainloop()
    clipboard.has_popup = False
