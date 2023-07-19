import tkinter as tk
from tkinter import messagebox


def delete_file_popup():
    def on_yes():
        # Code to delete the file goes here
        popup.destroy()

    def on_no():
        popup.destroy()

    popup = tk.Tk()
    popup.title("Delete File")
    popup.geometry("300x100")
    popup.resizable(width=False, height=False)  # Make the window not resizable

    # Set the window icon using a .png image (change 'icon.png' to your actual icon file path)
    icon_path = (
        "../assets/icon.png"  # Replace 'icon.png' with the path to your icon file
    )
    popup.iconphoto(True, tk.PhotoImage(file=icon_path))

    label = tk.Label(popup, text="Do you want to delete this file?", padx=20, pady=20)
    label.pack()

    yes_button = tk.Button(popup, text="Yes", command=on_yes)
    yes_button.pack(side=tk.LEFT, padx=25)

    no_button = tk.Button(popup, text="No", command=on_no)
    no_button.pack(side=tk.RIGHT, padx=25)

    popup.mainloop()


# Call the function to display the popup
delete_file_popup()
