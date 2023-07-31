import tkinter as tk
from tkinter import simpledialog

def dialog():

    def on_ok():
        input_text = entry.get()
        popup.destroy()
        print(input_text)
        # You can use the 'input_text' variable here, which contains the user's input.

    def on_cancel():
        popup.destroy()

    popup = tk.Tk()
    popup.title("Delete File")
    popup.geometry("300x150")
    popup.resizable(width=False, height=False)

    icon_path = "../assets/icon.png"
    popup.iconphoto(True, tk.PhotoImage(file=icon_path))

    label = tk.Label(popup, text="Enter the text:", padx=20, pady=20)
    label.pack()

    entry = tk.Entry(popup, width=30)
    entry.pack(padx=20)

    ok_button = tk.Button(popup, text="Ok", command=on_ok)
    ok_button.pack(side=tk.LEFT, padx=25)

    cancel_button = tk.Button(popup, text="Cancel", command=on_cancel)
    cancel_button.pack(side=tk.RIGHT, padx=25)

    popup.mainloop()



dialog()