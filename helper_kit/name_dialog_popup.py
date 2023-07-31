import tkinter as tk
from tkinter import simpledialog


def dialog():
    def on_ok():
        input_text = entry.get()
        if (
            not input_text.strip()
        ):  # Check if the input is empty or contains only whitespaces
            error_label.config(text="Invalid Entry", fg="red")
        else:
            popup.destroy()

    def on_cancel():
        popup.destroy()

    popup = tk.Tk()
    popup.title("New Folder")
    popup.geometry("300x150")
    popup.resizable(width=False, height=False)

    icon_path = "../assets/icon.png"
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


dialog()
