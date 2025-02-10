# Spikee GUI Enhancement Plan

This document outlines the plan to implement the requested features in the Spikee GUI, based on the requirements in `README.md`.

## Goals

1.  **Populate Fields on Startup (README 2.2):** Automatically populate the relevant fields in the "Generate", "Test", and "Results" modes with data from `spikee list`.
2.  **Environment Variable Configuration (README 2.3):** Allow users to view, edit, and add environment variables within the GUI.
3.  **Integrate Features (README 2.4, 2.5, 2.6):** Incorporate all features and examples mentioned in the `README.md` as options within the GUI.

## Implementation Plan

### 1. Backend (API)

*   **Verify Existing Endpoints:** Ensure the following API endpoints (as described in `gui_plan.md`) are implemented and functional:
    *   `/api/list/datasets`
    *   `/api/list/targets`
    *   `/api/list/seeds`
    *   `/api/list/plugins`
*   **Environment Variable Endpoints:** Implement new API endpoints for managing environment variables in the root `.env` file:
    *   `GET /api/env`: Retrieve the current environment variables from `k:/a/spikee/.env`.
    *   `PUT /api/env`: Update the environment variables in `k:/a/spikee/.env`.  **Security Note:** Handle this securely.
*   **Feature Option Handling:** Ensure existing API endpoints (especially for "generate" and "test") can accept and process the new options from `README.md`, such as:
    *   Injection delimiters
    *   Spotlighting data markers
    *   Standalone attacks
    *   Plugin selection

### 2. Frontend (`modes.py`)

*   **`GenerateView` and `TestView` Modifications:**
    *   **Data Fetching:** Modify the `activate` method (or add an initialization method) to:
        *   Call the relevant `/api/list` endpoints to fetch data (seeds, datasets, targets, plugins).
        *   Populate the corresponding UI components (dropdowns, lists, etc.) with the fetched data.
    *   **Feature Options:** Add UI elements for each feature mentioned in `README.md`:
        *   **Injection Delimiters:** Input field (text).
        *   **Spotlighting Data Markers:** Input field (text).
        *   **Standalone Attacks:** Checkbox (boolean) or a dropdown to select a standalone attacks file.
        *   **Plugins:** Dropdown (select from available plugins).
    *   **`run_test` (or equivalent) Method:** Update this method to:
        *   Gather values from *all* UI components, including the new feature options.
        *   Send these values to the appropriate backend API endpoint.
*   **`SettingsView` (New):**
    *   Create a new `SettingsView` class for managing environment variables.
    *   **UI Components:**
        *   Table or list to display existing environment variables (key-value pairs) with input fields for editing.
        *   "Add Variable" button to add new key-value input fields.
        *   "Save" button to save changes.
        *   "Load" button to load the current configuration.
    *   **`activate` Method:** Fetch environment variables from `/api/env` and populate the UI.
    *   **`save_config` (or similar) Method:** Gather all key-value pairs from the UI and send them to `/api/env`.
*   **Add "Settings" Mode:** Add a new `Mode` entry for "Settings" in the `get_available_modes` function, using the `SettingsView` class.

### 3. Frontend (`gui.py`)

*   **Initial Mode Activation:** Ensure that the initial mode (e.g., "Test" or "Generate") is activated on startup to trigger the data loading. This might involve calling `switch_mode` with the default mode in the `MainGUI`'s `__init__` method.

### 4. Configuration (`profiles.json`)

*   **Update Profiles:** Modify the existing profiles ("default", "quick_test", "full_analysis") in `profiles.json` to include default values for the new feature options. This will provide sensible defaults for different usage scenarios.

## Detailed Component Breakdown

### `GenerateView` (Example)

```python
import tkinter as tk
from tkinter import ttk
import spikee.list as spikee_list
from gui import capture_output

class GenerateView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        # --- Seed Folder ---
        self.seed_folder_label = tk.Label(self, text="Seed Folder:")
        self.seed_folder_label.grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.seed_folder_var = tk.StringVar()
        self.seed_folder_dropdown = ttk.Combobox(self, textvariable=self.seed_folder_var, values=[])
        self.seed_folder_dropdown.grid(row=0, column=1, sticky=tk.EW, padx=5, pady=5)

        # --- Positions ---
        self.positions_label = tk.Label(self, text="Positions:")
        self.positions_label.grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.positions_vars = {
            "start": tk.BooleanVar(value=True),
            "middle": tk.BooleanVar(),
            "end": tk.BooleanVar(value=True),
        }
        self.positions_frame = tk.Frame(self)
        self.positions_frame.grid(row=1, column=1, sticky=tk.EW, padx=5, pady=5)
        tk.Checkbutton(self.positions_frame, text="Start", variable=self.positions_vars["start"]).pack(side=tk.LEFT)
        tk.Checkbutton(self.positions_frame, text="Middle", variable=self.positions_vars["middle"]).pack(side=tk.LEFT)
        tk.Checkbutton(self.positions_frame, text="End", variable=self.positions_vars["end"]).pack(side=tk.LEFT)

        # --- Injection Delimiters ---
        self.injection_delimiters_label = tk.Label(self, text="Injection Delimiters:")
        self.injection_delimiters_label.grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.injection_delimiters_var = tk.StringVar()
        self.injection_delimiters_entry = tk.Entry(self, textvariable=self.injection_delimiters_var)
        self.injection_delimiters_entry.grid(row=2, column=1, sticky=tk.EW, padx=5, pady=5)

        # --- Spotlighting Data Markers ---
        self.spotlighting_label = tk.Label(self, text="Spotlighting Data Markers:")
        self.spotlighting_label.grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
        self.spotlighting_var = tk.StringVar()
        self.spotlighting_entry = tk.Entry(self, textvariable=self.spotlighting_var)
        self.spotlighting_entry.grid(row=3, column=1, sticky=tk.EW, padx=5, pady=5)

        # --- Standalone Attacks ---
        self.standalone_attacks_label = tk.Label(self, text="Standalone Attacks:")
        self.standalone_attacks_label.grid(row=4, column=0, sticky=tk.W, padx=5, pady=5)
        self.standalone_attacks_var = tk.BooleanVar(value=False) # Or StringVar for file selection
        self.standalone_attacks_check = tk.Checkbutton(self, variable=self.standalone_attacks_var)
        self.standalone_attacks_check.grid(row=4, column=1, sticky=tk.W, padx=5, pady=5)

        # --- Plugins ---
        self.plugins_label = tk.Label(self, text="Plugins:")
        self.plugins_label.grid(row=5, column=0, sticky=tk.W, padx=5, pady=5)
        self.plugins_var = tk.StringVar()
        self.plugins_dropdown = ttk.Combobox(self, textvariable=self.plugins_var, values=[]) # Populate in activate()
        self.plugins_dropdown.grid(row=5, column=1, sticky=tk.EW, padx=5, pady=5)

        # --- Dataset ---
        self.dataset_label = tk.Label(self, text="Dataset:")
        self.dataset_label.grid(row=6, column=0, sticky=tk.W, padx=5, pady=5)
        self.dataset_var = tk.StringVar()
        self.dataset_entry = tk.Entry(self, textvariable=self.dataset_var)
        self.dataset_entry.grid(row=6, column=1, sticky=tk.EW, padx=5, pady=5)
        self.dataset_button = tk.Button(self, text="Browse...", command=self.browse_dataset)
        self.dataset_button.grid(row=6, column=2, padx=5, pady=5)

        # --- Target ---
        self.target_label = tk.Label(self, text="Target:")
        self.target_label.grid(row=7, column=0, sticky=tk.W, padx=5, pady=5)
        self.target_var = tk.StringVar()
        self.target_dropdown = ttk.Combobox(self, textvariable=self.target_var, values=[])
        self.target_dropdown.grid(row=7, column=1, sticky=tk.EW, padx=5, pady=5)

        # --- Resume File ---
        self.resume_file_label = tk.Label(self, text="Resume File:")
        self.resume_file_label.grid(row=8, column=0, sticky=tk.W, padx=5, pady=5)
        self.resume_file_var = tk.StringVar()
        self.resume_file_entry = tk.Entry(self, textvariable=self.resume_file_var)
        self.resume_file_entry.grid(row=8, column=1, sticky=tk.EW, padx=5, pady=5)
        self.resume_file_button = tk.Button(self, text="Browse...", command=self.browse_resume_file)
        self.resume_file_button.grid(row=8, column=2, padx=5, pady=5)

        # --- Throttle ---
        self.throttle_label = tk.Label(self, text="Throttle (seconds):")
        self.throttle_label.grid(row=9, column=0, sticky=tk.W, padx=5, pady=5)
        self.throttle_var = tk.DoubleVar(value=0.0)  # Default value
        self.throttle_entry = tk.Entry(self, textvariable=self.throttle_var)
        self.throttle_entry.grid(row=9, column=1, sticky=tk.EW, padx=5, pady=5)

         # --- Threads ---
        self.threads_label = tk.Label(self, text="Threads:")
        self.threads_label.grid(row=10, column=0, sticky=tk.W, padx=5, pady=5)
        self.threads_var = tk.IntVar(value=1)  # Default value: 1
        self.threads_entry = tk.Entry(self, textvariable=self.threads_var)
        self.threads_entry.grid(row=10, column=1, sticky=tk.EW, padx=5, pady=5)

        # --- Attempts ---
        self.attempts_label = tk.Label(self, text="Attempts:")
        self.attempts_label.grid(row=11, column=0, sticky=tk.W, padx=5, pady=5)
        self.attempts_var = tk.IntVar(value=1)  # Default value: 1
        self.attempts_entry = tk.Entry(self, textvariable=self.attempts_var)
        self.attempts_entry.grid(row=11, column=1, sticky=tk.EW, padx=5, pady=5)

        # --- Success Criteria ---
        self.success_criteria_label = tk.Label(self, text="Success Criteria:")
        self.success_criteria_label.grid(row=12, column=0, sticky=tk.W, padx=5, pady=5)
        self.success_criteria_var = tk.StringVar(value="first")  # Default value: "first"
        self.success_criteria_entry = tk.Entry(self, textvariable=self.success_criteria_var)
        self.success_criteria_entry.grid(row=12, column=1, sticky=tk.EW, padx=5, pady=5)

        #Test button
        self.test_button = tk.Button(self, text="Run Test", command=self.run_test)
        self.test_button.grid(row=13, column=0, columnspan=3, pady=10)

    def browse_dataset(self):
        filename = filedialog.askopenfilename(
            initialdir=".",
            title="Select Dataset File",
            filetypes=(("JSONL files", "*.jsonl"), ("All files", "*.*"))
        )
        self.dataset_var.set(filename)

    def browse_resume_file(self):
        filename = filedialog.askopenfilename(
            initialdir=".",
            title="Select Resume File",
            filetypes=(("JSONL files", "*.jsonl"), ("All files", "*.*"))
        )
        self.resume_file_var.set(filename)

    def activate(self):
        # Get available targets using spikee.list.list_targets (capture output)
        class DummyArgs:
            pass
        args = DummyArgs()
        target_list = capture_output(spikee_list.list_targets, args)
        available_targets = []
        for line in target_list.splitlines():
            if line.strip().startswith("-"):
                parts = line.strip().split(" - ")
                if len(parts) > 1:
                    available_targets.append(parts[1])
        self.target_dropdown['values'] = available_targets

        # Fetch and populate plugins
        plugin_list = capture_output(spikee_list.list_plugins, args)
        available_plugins = []
        for line in plugin_list.splitlines():
            if line.strip().startswith("-"):
                parts = line.strip().split(" - ")
                if len(parts) > 1:
                    available_plugins.append(parts[1])
        self.plugins_dropdown['values'] = available_plugins

        # Fetch and populate seed folders
        seed_list = capture_output(spikee_list.list_seeds, args)
        available_seeds = []
        for line in seed_list.splitlines():
            if line.strip().startswith("-"):
                parts = line.strip().split(" - ")
                if len(parts) > 1:
                    available_seeds.append(parts[1])
        self.seed_folder_dropdown['values'] = available_seeds


    def run_test(self): # Or generate_dataset, depending on the mode

        # Create the args object
        class DummyArgs:
            pass
        args = DummyArgs()

        args.dataset = self.dataset_var.get()
        args.target = self.target_var.get()
        args.threads = self.threads_var.get()
        args.attempts = self.attempts_var.get()
        args.success_criteria = self.success_criteria_var.get()
        args.resume_file = self.resume_file_var.get()
        args.throttle = self.throttle_var.get()
        args.injection_delimiters = self.injection_delimiters_var.get()
        args.spotlighting_data_markers = self.spotlighting_var.get()
        args.standalone_attacks = self.standalone_attacks_var.get()
        args.plugins = self.plugins_var.get()

        # --- Input Validation ---
        if not args.dataset:
            messagebox.showerror("Error", "Please select a dataset.")
            return
        if not args.target:
            messagebox.showerror("Error", "Please select a target.")
            return
        if not args.threads:
            messagebox.showerror("Error", "Please enter the number of threads.")
            return
        if not args.attempts:
            messagebox.showerror("Error", "Please enter the number of attempts.")
            return
        if not args.success_criteria:
            messagebox.showerror("Error", "Please enter the success criteria.")
            return

        # Call test_dataset
        spikee_tester.test_dataset(args)
        messagebox.showinfo("Success", "Test completed!")

### `SettingsView` (New)

```python
import tkinter as tk
from tkinter import ttk, messagebox
import dotenv
import os

class SettingsView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        self.env_vars = {} # Store loaded env vars

        # --- Existing Variables ---
        self.existing_vars_label = tk.Label(self, text="Existing Environment Variables:")
        self.existing_vars_label.pack(pady=10)

        self.existing_vars_frame = tk.Frame(self)
        self.existing_vars_frame.pack(fill=tk.BOTH, expand=True)

        # --- Add Variable ---
        self.add_var_button = tk.Button(self, text="Add Variable", command=self.add_variable_row)
        self.add_var_button.pack(pady=5)

        # --- Buttons ---
        self.load_button = tk.Button(self, text="Load", command=self.load_env_vars)
        self.load_button.pack(side=tk.LEFT, padx=5, pady=10)
        self.save_button = tk.Button(self, text="Save", command=self.save_env_vars)
        self.save_button.pack(side=tk.LEFT, padx=5, pady=10)


    def add_variable_row(self, key="", value=""):
        row_frame = tk.Frame(self.existing_vars_frame)
        row_frame.pack(fill=tk.X)

        key_var = tk.StringVar(value=key)
        key_entry = tk.Entry(row_frame, textvariable=key_var)
        key_entry.pack(side=tk.LEFT, padx=5)

        value_var = tk.StringVar(value=value)
        value_entry = tk.Entry(row_frame, textvariable=value_var)
        value_entry.pack(side=tk.LEFT, padx=5)

        # Store references to the variables and frame
        self.env_vars[row_frame] = (key_var, value_var)


    def load_env_vars(self):
        # Clear existing rows
        for frame in self.env_vars:
            frame.destroy()
        self.env_vars.clear()

        # Load from .env file
        dotenv.load_dotenv('k:/a/spikee/.env')  # Load from the project root
        for key, value in os.environ.items():
            self.add_variable_row(key, value)



    def save_env_vars(self):
        # Gather all key-value pairs
        new_env_vars = {}
        for frame, (key_var, value_var) in self.env_vars.items():
            key = key_var.get().strip()
            value = value_var.get().strip()
            if key: # Don't save empty keys
                new_env_vars[key] = value

        # Write to .env file
        with open('k:/a/spikee/.env', 'w') as f:  # Write to the project root
            for key, value in new_env_vars.items():
                f.write(f"{key}={value}\n")

        messagebox.showinfo("Info", "Environment variables saved.")


    def activate(self):
        self.load_env_vars()

```

This plan provides a detailed roadmap for implementing the requested GUI enhancements. It covers backend API changes, frontend modifications, and configuration updates. The example code snippets demonstrate how to add new UI elements and handle data loading/saving. The example code snippets have now been expanded to include all necessary imports and logic to be directly copy/pastable into the `modes.py` file. The `GenerateView` now includes the additional UI elements, and populates the dropdown menus. The `SettingsView` now correctly loads and saves to the `.env` file in the project root.