import pygame
import tkinter as tk
from tkinter import messagebox


def delete_file_popup():
    def on_yes():
        # Code to delete the file goes here
        messagebox.showinfo("Deleted", "File has been deleted!")
        popup.destroy()

    def on_no():
        popup.destroy()

    popup = tk.Tk()
    popup.title("Delete File")
    popup.geometry("300x100")
    popup.resizable(width=False, height=False)  # Make the window not resizable

    label = tk.Label(popup, text="Do you want to delete this file?", padx=20, pady=20)
    label.pack()

    yes_button = tk.Button(popup, text="Yes", command=on_yes)
    yes_button.pack(side=tk.LEFT, padx=10)

    no_button = tk.Button(popup, text="No", command=on_no)
    no_button.pack(side=tk.RIGHT, padx=10)

    popup.mainloop()


def main():
    pygame.init()

    # Set up your Pygame window and other elements here
    window = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("My Pygame App")

    # Main loop for Pygame
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                delete_file_popup()
        # Your Pygame game logic and rendering here
        # ...

        # Check if the condition to show the popup is met

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
