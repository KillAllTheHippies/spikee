import tkinter as tk
from .menu import MenuBar
from .gui import GUI
from . import modes  # Import modes from local package

def main():
    # Initialize the main window
    root = tk.Tk()
    root.title("Spikee GUI")

    # Create and attach the main GUI layout
    main_gui = GUI(root)
    main_gui.pack(fill=tk.BOTH, expand=True)

    # Create and attach the menu bar
    menu_bar = MenuBar(root, main_gui)
    root.config(menu=menu_bar)

    # Pass the main_gui instance to modes.py
    modes.set_main_gui(main_gui)

    # Start the main event loop
    root.mainloop()

if __name__ == "__main__":
    main()
