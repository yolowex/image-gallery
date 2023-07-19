import tkinter as tk
from tkinter import messagebox


def delete_file_popup(clipboard):
    def on_yes():
        popup.destroy()
        clipboard.trigger_operation = True

    def on_no():
        popup.destroy()

    popup = tk.Tk()
    popup.title("Delete File")
    popup.geometry("300x100")
    popup.resizable(width=False, height=False)

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
