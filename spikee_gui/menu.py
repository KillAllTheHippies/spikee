import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
from .modes import get_available_modes
import json
import os

class ProfileDialog(tk.Toplevel):
    def __init__(self, parent, profile_data=None):
        super().__init__(parent)
        self.parent = parent
        self.profile_data = profile_data or {}
        self.title("Profile Editor" if profile_data else "Create Profile")

        # Profile name
        tk.Label(self, text="Profile Name:").grid(row=0, column=0, padx=5, pady=5)
        self.name_entry = tk.Entry(self)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)
        if profile_data:
            self.name_entry.insert(0, profile_data.get('name', ''))

        # Description
        tk.Label(self, text="Description:").grid(row=1, column=0, padx=5, pady=5)
        self.desc_entry = tk.Text(self, height=3, width=30)
        self.desc_entry.grid(row=1, column=1, padx=5, pady=5)
        if profile_data:
            self.desc_entry.insert('1.0', profile_data.get('description', ''))

        # Buttons
        button_frame = tk.Frame(self)
        button_frame.grid(row=2, column=0, columnspan=2, pady=5)
        tk.Button(button_frame, text="Save", command=self.save_profile).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Cancel", command=self.destroy).pack(side=tk.LEFT, padx=5)

    def save_profile(self):
        name = self.name_entry.get().strip()
        if not name:
            messagebox.showerror("Error", "Profile name cannot be empty")
            return

        description = self.desc_entry.get('1.0', tk.END).strip()

        self.profile_data = {
            'name': name,
            'description': description,
            'settings': self.profile_data.get('settings', {})
        }

        self.destroy()

class MenuBar(tk.Menu):
    def __init__(self, parent, main_gui):
        super().__init__(parent)
        self.parent = parent
        self.main_gui = main_gui  # Store reference to MainGUI
        self.profiles_file = os.path.join(os.path.dirname(__file__), 'config', 'profiles.json')
        self.profile_var = tk.StringVar() # Add profile_var
        self.mode_var = tk.StringVar() # Add mode_var

        # File menu
        file_menu = tk.Menu(self, tearoff=False)
        file_menu.add_command(label="Exit", command=parent.quit)
        self.add_cascade(label="File", menu=file_menu)

        # Modes menu
        self.modes_menu = tk.Menu(self, tearoff=False)
        self.add_cascade(label="Modes", menu=self.modes_menu)
        
        # Add mode selection submenu
        self.mode_menu = tk.Menu(self.modes_menu, tearoff=False)
        self.modes_menu.add_cascade(label="Select Mode", menu=self.mode_menu)
        self.populate_mode_menu()

        # Profiles menu
        self.profiles_menu = tk.Menu(self, tearoff=False)
        self.add_cascade(label="Profiles", menu=self.profiles_menu)
        self.create_profiles_menu()  # Use create_profiles_menu
        self.populate_profiles_menu()

        # Help menu
        help_menu = tk.Menu(self, tearoff=False)
        help_menu.add_command(label="About")
        self.add_cascade(label="Help", menu=help_menu)

    def populate_modes_menu(self):
        """Populate the modes menu with additional options"""
        # Add mode selection submenu
        self.mode_menu = tk.Menu(self.modes_menu, tearoff=False)
        self.modes_menu.add_cascade(label="Select Mode", menu=self.mode_menu)
        self.populate_mode_menu()

        # Add separator
        self.modes_menu.add_separator()

        # Add advanced options submenu
        advanced_menu = tk.Menu(self.modes_menu, tearoff=False)
        self.modes_menu.add_cascade(label="Advanced Options", menu=advanced_menu)
        
        # Add options for each mode
        advanced_menu.add_command(label="Generate Options", command=lambda: self.show_advanced_options("Generate"))
        advanced_menu.add_command(label="Test Options", command=lambda: self.show_advanced_options("Test"))
        advanced_menu.add_command(label="Results Options", command=lambda: self.show_advanced_options("Results"))

    def show_advanced_options(self, mode):
        """Show advanced options dialog for the selected mode"""
        dialog = tk.Toplevel(self.parent)
        dialog.title(f"{mode} Advanced Options")
        dialog.transient(self.parent)
        dialog.grab_set()

        # Add mode-specific options
        if mode == "Generate":
            ttk.Label(dialog, text="Default Format:").pack(padx=5, pady=5)
            format_var = tk.StringVar(value="full-prompt")
            ttk.Radiobutton(dialog, text="Full Prompt", variable=format_var, value="full-prompt").pack()
            ttk.Radiobutton(dialog, text="Document", variable=format_var, value="document").pack()
            ttk.Radiobutton(dialog, text="Burp", variable=format_var, value="burp").pack()

            ttk.Label(dialog, text="Positions:").pack(padx=5, pady=5)
            start_var = tk.BooleanVar(value=True)
            middle_var = tk.BooleanVar(value=True)
            end_var = tk.BooleanVar(value=True)
            ttk.Checkbutton(dialog, text="Start", variable=start_var).pack()
            ttk.Checkbutton(dialog, text="Middle", variable=middle_var).pack()
            ttk.Checkbutton(dialog, text="End", variable=end_var).pack()

        elif mode == "Test":
            ttk.Label(dialog, text="Test Settings:").pack(padx=5, pady=5)
            threads_var = tk.IntVar(value=4)
            ttk.Label(dialog, text="Threads:").pack()
            ttk.Entry(dialog, textvariable=threads_var).pack()

            attempts_var = tk.IntVar(value=1)
            ttk.Label(dialog, text="Attempts:").pack()
            ttk.Entry(dialog, textvariable=attempts_var).pack()

        # Add OK button
        ttk.Button(dialog, text="OK", command=dialog.destroy).pack(pady=10)

    def populate_mode_menu(self):
        """Populate the mode selection submenu"""
        for mode in get_available_modes():
            self.mode_menu.add_radiobutton(
                label=mode,
                variable=self.mode_var,
                value=mode,
                command=lambda m=mode: self.handle_mode_select(m)
            )

    def handle_mode_select(self, mode):
        """Handle mode selection from the menu"""
        self.mode_var.set(mode)
        self.main_gui.switch_mode(mode)

    def create_profiles_menu(self):
        """Create the profiles menu with management and selection options"""
        self.profiles_menu.delete(0, tk.END)  # Clear existing entries

        # Management options
        self.profiles_menu.add_command(
            label="Create New Profile",
            command=self.create_profile
        )
        self.profiles_menu.add_command(
            label="Edit Current Profile",
            command=self.edit_profile
        )
        self.profiles_menu.add_command(
            label="Delete Profile",
            command=self.delete_profile
        )
        self.profiles_menu.add_separator()
        self.profiles_menu.add_command(
            label="Refresh Profiles",
            command=self.refresh_profiles
        )
        self.profiles_menu.add_separator()

        # Profile selection
        profiles = self.load_profiles()
        for profile_name in profiles:
            self.profiles_menu.add_command(
                label=profile_name,
                command=lambda name=profile_name: self.apply_profile(name)
            )


    def populate_profiles_menu(self):
        """Populate the profiles menu"""
        self.create_profiles_menu()

    def apply_profile(self, profile_name):
        """Apply the selected profile"""
        self.profile_var.set(profile_name)
        self.main_gui.apply_profile(profile_name)


    def load_profiles(self):
        """Load profiles from the profiles file"""
        try:
            with open(self.profiles_file, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def save_profiles(self, profiles):
        """Save profiles to the profiles file"""
        os.makedirs(os.path.dirname(self.profiles_file), exist_ok=True)
        with open(self.profiles_file, 'w') as f:
            json.dump(profiles, f, indent=2)

    def create_profile(self):
        """Handle creating a new profile"""
        dialog = ProfileDialog(self.parent)
        self.parent.wait_window(dialog)

        if dialog.profile_data:
            profiles = self.load_profiles()
            profile_name = dialog.profile_data['name']

            if profile_name in profiles:
                messagebox.showerror("Error", f"Profile '{profile_name}' already exists")
                return

            profiles[profile_name] = dialog.profile_data
            self.save_profiles(profiles)
            self.refresh_profiles()

    def edit_profile(self):
        """Handle editing the current profile"""
        profiles = self.load_profiles()
        if not profiles:
            messagebox.showinfo("Info", "No profiles available to edit")
            return

        profile_name = simpledialog.askstring("Edit Profile", "Enter profile name to edit:")
        if profile_name and profile_name in profiles:
            dialog = ProfileDialog(self.parent, profiles[profile_name])
            self.parent.wait_window(dialog)

            if dialog.profile_data:
                profiles[profile_name] = dialog.profile_data
                self.save_profiles(profiles)
                self.refresh_profiles()
        elif profile_name:
            messagebox.showerror("Error", f"Profile '{profile_name}' not found")

    def delete_profile(self):
        """Handle deleting a profile"""
        profiles = self.load_profiles()
        if not profiles:
            messagebox.showinfo("Info", "No profiles available to delete")
            return

        profile_name = simpledialog.askstring("Delete Profile", "Enter profile name to delete:")
        if profile_name and profile_name in profiles:
            confirm = messagebox.askyesno("Confirm Delete",
                f"Are you sure you want to delete profile '{profile_name}'?")
            if confirm:
                del profiles[profile_name]
                self.save_profiles(profiles)
                self.refresh_profiles()
        elif profile_name:
            messagebox.showerror("Error", f"Profile '{profile_name}' not found")
    
    def refresh_profiles(self):
        """Refresh the list of profiles and update the GUI"""
        self.create_profiles_menu()  # Rebuild the profiles menu
        # Re-apply the current profile, if any
        if self.profile_var.get():
            self.apply_profile(self.profile_var.get())