import tkinter as tk
from tkinter import messagebox
import core.common.constants as constants
# import core.common.resources as cr


def center_window(root, width, height):
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    x_coordinate = int((screen_width / 2) - (width / 2))
    y_coordinate = int((screen_height / 2) - (height / 2))

    root.geometry(f"{width}x{height}+{x_coordinate}+{y_coordinate}")


def delete_file_popup(clipboard):
    # cr.window.opacity = 0.65

    def on_yes():
        popup.destroy()
        clipboard.trigger_operation = True

    def on_no():
        popup.destroy()

    popup = tk.Tk()
    popup.title("Delete File")
    popup.geometry("300x100")
    popup.resizable(width=False, height=False)

    if not constants.IS_LINUX:
        center_window(popup, 300, 100)

    icon_path = "./assets/icon.png"
    popup.iconphoto(True, tk.PhotoImage(file=icon_path))

    label = tk.Label(popup, text="Do you want to delete this file?", padx=20, pady=20)
    label.pack()

    yes_button = tk.Button(popup, text="Yes", command=on_yes)
    yes_button.pack(side=tk.LEFT, padx=25)

    no_button = tk.Button(popup, text="No", command=on_no)
    no_button.pack(side=tk.RIGHT, padx=25)

    popup.mainloop()

    clipboard.has_popup = False
    # cr.window.opacity = 1
