import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
from .modes import get_available_modes, ResultsView
from .utils import capture_output
from .constants import DEFAULT_INJECTION_DELIMITERS, DEFAULT_SPOTLIGHTING_MARKERS


class GUI(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.views = {}
        
        try:
            self.available_modes = get_available_modes()
            if not self.available_modes:
                messagebox.showerror("Error", "No modes available")
                return
        except Exception as e:
            messagebox.showerror("Error", f"Failed to initialize modes: {str(e)}")
            return

        self.create_mode_views()
        
        # Set default mode if available
        if self.available_modes:
            first_mode = list(self.available_modes.keys())[0]
            self.switch_mode(first_mode)

    def create_mode_views(self):
        self.mode_views_frame = tk.Frame(self)
        self.mode_views_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        for mode_name, mode_class in self.available_modes.items():
            view = mode_class(self.mode_views_frame)
            self.views[mode_name] = view
            view.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
            view.pack_forget()  # Hide all views initially

    def switch_mode(self, mode_name):
        for name, view in self.views.items():
            if name == mode_name:
                view.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
                view.activate()  # Call activate when switching to a view
            else:
                view.pack_forget()

    def apply_profile(self, profile_name):
        """Apply the selected profile settings"""
        # TODO: Implement profile application logic
        pass

    def get_default_delimiters(self):
        """Return list of default injection delimiters"""
        return DEFAULT_INJECTION_DELIMITERS

    def get_default_markers(self):
        """Return list of default spotlighting markers"""
        return DEFAULT_SPOTLIGHTING_MARKERS

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Spikee GUI")
    root.geometry("800x600")
    app = GUI(root)
    app.pack(fill=tk.BOTH, expand=True)
    root.mainloop()
