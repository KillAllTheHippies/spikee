import tkinter as tk
from tkinter import ttk, messagebox, filedialog, simpledialog
import os
import json
import dotenv
import spikee.list as spikee_list
import spikee.tester as spikee_tester
from .utils import capture_output
from .constants import DEFAULT_INJECTION_DELIMITERS, DEFAULT_SPOTLIGHTING_MARKERS



main_gui_instance = None

def set_main_gui(gui_instance):
    global main_gui_instance
    main_gui_instance = gui_instance


def get_available_modes():
    """
    Returns a dictionary of available modes for the GUI.
    """
    modes = {
        "Generate": GenerateView,
        "Test": TestView,
        "Results": ResultsView,
        "Settings": SettingsView,
    }
    return modes


class GenerateView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        # Create frames for organization
        self.input_frame = ttk.LabelFrame(self, text="Input Configuration")
        self.input_frame.pack(fill=tk.X, padx=5, pady=5)

        # Seed Folder
        self.seed_folder_frame = ttk.Frame(self.input_frame)
        self.seed_folder_frame.pack(fill=tk.X, padx=5, pady=5)
        ttk.Label(self.seed_folder_frame, text="Seed Folder:").pack(side=tk.LEFT)
        self.seed_folder_var = tk.StringVar()
        self.seed_folder_combo = ttk.Combobox(self.seed_folder_frame, textvariable=self.seed_folder_var)
        self.seed_folder_combo.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        # Injection Delimiters
        self.delimiters_frame = ttk.Frame(self.input_frame)
        self.delimiters_frame.pack(fill=tk.X, padx=5, pady=5)
        ttk.Label(self.delimiters_frame, text="Injection Delimiter:").pack(side=tk.LEFT)
        self.delimiter_var = tk.StringVar()
        self.delimiter_combo = ttk.Combobox(self.delimiters_frame, textvariable=self.delimiter_var)
        self.delimiter_combo.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.custom_delimiter_button = ttk.Button(self.delimiters_frame, text="Custom", command=self.add_custom_delimiter)
        self.custom_delimiter_button.pack(side=tk.LEFT, padx=5)

        # Spotlighting Markers
        self.markers_frame = ttk.Frame(self.input_frame)
        self.markers_frame.pack(fill=tk.X, padx=5, pady=5)
        ttk.Label(self.markers_frame, text="Spotlighting Marker:").pack(side=tk.LEFT)
        self.marker_var = tk.StringVar()
        self.marker_combo = ttk.Combobox(self.markers_frame, textvariable=self.marker_var)
        self.marker_combo.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.custom_marker_button = ttk.Button(self.markers_frame, text="Custom", command=self.add_custom_marker)
        self.custom_marker_button.pack(side=tk.LEFT, padx=5)

        # Generate Button
        self.generate_button = ttk.Button(self, text="Generate", command=self.run_generate)
        self.generate_button.pack(pady=10)

    def add_custom_delimiter(self):
        custom = simpledialog.askstring("Custom Delimiter", 
            "Enter custom delimiter (use INJECTION_PAYLOAD as placeholder):")
        if custom:
            current_values = list(self.delimiter_combo['values'])
            if custom not in current_values:
                current_values.append(custom)
                self.delimiter_combo['values'] = current_values
            self.delimiter_var.set(custom)

    def add_custom_marker(self):
        custom = simpledialog.askstring("Custom Marker", 
            "Enter custom marker (use DOCUMENT as placeholder):")
        if custom:
            current_values = list(self.marker_combo['values'])
            if custom not in current_values:
                current_values.append(custom)
                self.marker_combo['values'] = current_values
            self.marker_var.set(custom)

    def activate(self):

        # Populate seed folders
        args = ["--seed-folder", "k:/a/spikee/seeds"]
        seed_folders = capture_output(spikee_list.list_seeds, args)
        self.seed_folder_combo['values'] = seed_folders.splitlines()

        # Set default delimiters and markers
        self.delimiter_combo['values'] = DEFAULT_INJECTION_DELIMITERS
        self.marker_combo['values'] = DEFAULT_SPOTLIGHTING_MARKERS
        
        # Set defaults
        if self.delimiter_combo['values']:
            self.delimiter_combo.set(self.delimiter_combo['values'][0])
        if self.marker_combo['values']:
            self.marker_combo.set(self.marker_combo['values'][0])

    def run_generate(self):
        if not self.seed_folder_var.get():
            messagebox.showerror("Error", "Please select a seed folder")
            return

        # Create args object and run generation
        class DummyArgs:
            pass
        args = DummyArgs()
        args.seed_folder = self.seed_folder_var.get()
        args.injection_delimiters = self.delimiter_var.get()
        args.spotlighting_data_markers = self.marker_var.get()
        args.format = 'full-prompt'  # Default format
        args.positions = ['start', 'middle', 'end']  # Default positions
        args.plugins = []  # No plugins by default
        args.include_suffixes = False
        args.include_system_message = False
        args.match_languages = False
        args.languages = None
        args.instruction_filter = None
        args.jailbreak_filter = None
        args.standalone_attacks = None
        
        try:
            spikee_list.generate_dataset(args)
            messagebox.showinfo("Success", "Dataset generated successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate dataset: {str(e)}")



class TestView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        # Create frames for organization
        self.input_frame = ttk.LabelFrame(self, text="Test Configuration")
        self.input_frame.pack(fill=tk.X, padx=5, pady=5)

        # Dataset Selection
        self.dataset_frame = ttk.Frame(self.input_frame)
        self.dataset_frame.pack(fill=tk.X, padx=5, pady=5)
        ttk.Label(self.dataset_frame, text="Dataset:").pack(side=tk.LEFT)
        self.dataset_var = tk.StringVar()
        self.dataset_entry = ttk.Entry(self.dataset_frame, textvariable=self.dataset_var)
        self.dataset_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.browse_button = ttk.Button(self.dataset_frame, text="Browse", command=self.browse_dataset)
        self.browse_button.pack(side=tk.LEFT)

        # Target Selection
        self.target_frame = ttk.Frame(self.input_frame)
        self.target_frame.pack(fill=tk.X, padx=5, pady=5)
        ttk.Label(self.target_frame, text="Target:").pack(side=tk.LEFT)
        self.target_var = tk.StringVar()
        self.target_combo = ttk.Combobox(self.target_frame, textvariable=self.target_var)
        self.target_combo.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        # Test Button
        self.test_button = ttk.Button(self, text="Run Test", command=self.run_test)
        self.test_button.pack(pady=10)

    def browse_dataset(self):
        filename = filedialog.askopenfilename(
            filetypes=[("JSONL files", "*.jsonl"), ("All files", "*.*")]
        )
        if filename:
            self.dataset_var.set(filename)

    def activate(self):
        # Populate targets
        args = ["--target-folder", "k:/a/spikee/targets"]
        target_list = capture_output(spikee_list.list_targets, args)
        available_targets = []
        for line in target_list.splitlines():
            if line.strip().startswith("-"):
                parts = line.strip().split(" - ")
                if len(parts) > 1:
                    available_targets.append(parts[1])
        self.target_combo['values'] = available_targets

    def run_test(self):
        if not self.dataset_var.get():
            messagebox.showerror("Error", "Please select a dataset file")
            return
        if not self.target_var.get():
            messagebox.showerror("Error", "Please select a target")
            return

        # Create args object and run test
        class DummyArgs:
            pass
        args = DummyArgs()
        args.dataset = self.dataset_var.get()
        args.target = self.target_var.get()
        
        try:
            spikee_tester.test_dataset(args)
            messagebox.showinfo("Success", "Test completed successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to run test: {str(e)}")


### `SettingsView` (New)

class SettingsView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.env_vars = {}  # Dictionary to store references to the Entry widgets

        self.label = tk.Label(self, text="Environment Variables")
        self.label.pack(pady=10)

        self.existing_vars_frame = tk.Frame(self)
        self.existing_vars_frame.pack(fill=tk.X)

        self.add_button = tk.Button(self, text="Add Variable", command=self.add_variable_row)
        self.add_button.pack(pady=5)

        self.load_button = tk.Button(self, text="Load", command=self.load_env_vars)
        self.load_button.pack(side=tk.LEFT, padx=5, pady=10)

        self.save_button = tk.Button(self, text="Save", command=self.save_env_vars)
        self.save_button.pack(side=tk.LEFT, padx=5, pady=10)


    def add_variable_row(self, key="", value="", status=""):
        row_frame = tk.Frame(self.existing_vars_frame)
        row_frame.pack(fill=tk.X)

        key_var = tk.StringVar(value=key)
        key_entry = tk.Entry(row_frame, textvariable=key_var)
        key_entry.pack(side=tk.LEFT, padx=5)

        value_var = tk.StringVar(value=value)
        value_entry = tk.Entry(row_frame, textvariable=value_var)
        value_entry.pack(side=tk.LEFT, padx=5)

        # Status label (for indicating changes)
        status_label = tk.Label(row_frame, text=status)  # Start with empty status
        status_label.pack(side=tk.LEFT, padx=5)

        # Delete button
        delete_button = tk.Button(row_frame, text="Delete", command=lambda: self.delete_variable(row_frame))
        delete_button.pack(side=tk.LEFT, padx=5)

        # Store references to the variables, frame, and status label.
        self.env_vars[row_frame] = (key_var, value_var, status_label)


    def delete_variable(self, row_frame):
        """Deletes a variable row from the UI and the env_vars dictionary."""
        if row_frame in self.env_vars:
            del self.env_vars[row_frame]  # Remove from dictionary
            row_frame.destroy()  # Remove from UI

    def load_env_vars(self):
        # Clear existing rows
        for frame in self.env_vars:
            frame.destroy()
        self.env_vars.clear()

        # Load from .env file
        dotenv.load_dotenv('k:/a/spikee/.env')  # Load from the project root
        loaded_vars = dict(os.environ)

        for key, value in loaded_vars.items():
            self.add_variable_row(key, value)

        self.compare_and_update_ui() # Compare after loading

    def compare_env_vars(self):
        """Compares the current env_vars with the system environment."""
        system_env = dict(os.environ)
        loaded_env = {}
        for frame, (key_var, value_var, _) in self.env_vars.items():
            key = key_var.get().strip()
            value = value_var.get().strip()
            if key:
                loaded_env[key] = value

        diff = {
            'added': {},
            'modified': {},
            'deleted': {},
            'unchanged': {}
        }

        # Find added and modified
        for key, value in loaded_env.items():
            if key not in system_env:
                diff['added'][key] = value
            elif system_env[key] != value:
                diff['modified'][key] = value
            else:
                diff['unchanged'][key] = value

        # Find deleted
        for key, value in system_env.items():
            if key not in loaded_env:
                diff['deleted'][key] = value

        return diff

    def update_ui_status(self, diff):
        """Updates the UI to reflect the differences."""

        # Reset all statuses first
        for frame, (_, _, status_label) in self.env_vars.items():
            status_label.config(text="")
            status_label.config(fg="black") # reset color

        # Iterate through the *displayed* variables, not the diff
        for frame, (key_var, _, status_label) in self.env_vars.items():
            key = key_var.get().strip()
            if key in diff['added']:
                status_label.config(text="Added", fg="green")
            elif key in diff['modified']:
                status_label.config(text="Modified", fg="blue")
            elif key in diff['deleted']:
                status_label.config(text="Deleted", fg="red")  # This should not normally happen after loading
            # No need for an "unchanged" status, leave it blank.

    def compare_and_update_ui(self):
        diff = self.compare_env_vars()
        self.update_ui_status(diff)


    def save_env_vars(self):
        # Gather all key-value pairs
        new_env_vars = {}
        for frame, (key_var, value_var, _) in self.env_vars.items():
            key = key_var.get().strip()
            value = value_var.get().strip()
            if key: # Don't save empty keys
                new_env_vars[key] = value

        # Compare with system environment *before* saving
        diff = self.compare_env_vars()


        # Write to .env file
        with open('k:/a/spikee/.env', 'w') as f:  # Write to the project root
            for key, value in new_env_vars.items():
                f.write(f"{key}={value}\n")

        # Summary message
        added_count = len(diff['added'])
        modified_count = len(diff['modified'])
        deleted_count = len(diff['deleted'])
        message = f"Environment variables saved.\nAdded: {added_count}, Modified: {modified_count}, Deleted: {deleted_count}"
        messagebox.showinfo("Info", message)
        self.compare_and_update_ui() # update UI after saving


    def activate(self):
        self.load_env_vars()



class ResultsView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        
        # Create frames for organization
        self.control_frame = ttk.Frame(self)
        self.control_frame.pack(fill=tk.X, padx=5, pady=5)

        # Add load results button
        self.load_button = ttk.Button(self.control_frame, text="Load Results", command=self.load_results)
        self.load_button.pack(side=tk.LEFT, padx=5)
        
        # Create text widget for displaying results
        self.results_text = tk.Text(self, wrap=tk.WORD)
        self.results_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(self, command=self.results_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.results_text.config(yscrollcommand=scrollbar.set)

    def load_results(self):
        filename = filedialog.askopenfilename(
            filetypes=[("JSONL files", "*.jsonl"), ("All files", "*.*")]
        )
        if not filename:
            return

        try:
            with open(filename, 'r', encoding='utf-8') as f:
                results = [json.loads(line) for line in f]

            self.results_text.config(state=tk.NORMAL)
            self.results_text.delete("1.0", tk.END)

            # Display summary statistics
            total = len(results)
            successful = sum(1 for r in results if r.get('success', False))
            failed = total - successful
            
            summary = f"Results Summary:\n"
            summary += f"Total Tests: {total}\n"
            summary += f"Successful: {successful}\n"
            summary += f"Failed: {failed}\n"
            summary += f"Success Rate: {(successful/total)*100:.2f}%\n\n"
            summary += "=" * 50 + "\n\n"
            
            self.results_text.insert(tk.END, summary)

            # Display individual results
            for result in results:
                # Format each result entry
                entry = f"Test ID: {result.get('id', 'N/A')}\n"
                entry += f"Success: {result.get('success', False)}\n"
                if result.get('error'):
                    entry += f"Error: {result['error']}\n"
                entry += f"Response: {result.get('response', 'N/A')[:200]}...\n"
                entry += "-" * 50 + "\n\n"
                
                self.results_text.insert(tk.END, entry)

            self.results_text.config(state=tk.DISABLED)

        except FileNotFoundError:
            messagebox.showerror("Error", "File not found.")
        except json.JSONDecodeError:
            messagebox.showerror("Error", "Invalid JSONL format.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def activate(self):
        pass