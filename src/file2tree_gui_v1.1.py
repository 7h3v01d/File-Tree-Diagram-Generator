import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import os

class FileTreeGeneratorGUI:
    def __init__(self, master):
        self.master = master
        master.title("File Tree Diagram Generator")
        master.geometry("800x700") # Increased initial window size to accommodate new listbox
        master.resizable(True, True)

        # Configure grid weights for responsive layout
        master.grid_rowconfigure(0, weight=0) # Input Frame (Directory selection)
        master.grid_rowconfigure(1, weight=0) # Label for Listbox
        master.grid_rowconfigure(2, weight=1) # Listbox (expands vertically)
        master.grid_rowconfigure(3, weight=0) # Generate Button
        master.grid_rowconfigure(4, weight=0) # Output Label
        master.grid_rowconfigure(5, weight=1) # Output Text Area (expands vertically)
        
        master.grid_columnconfigure(0, weight=1) # Main column (expands horizontally)
        master.grid_columnconfigure(1, weight=0) # Column for Listbox scrollbar and Browse button

        # --- Input Frame (Directory Selection) ---
        self.input_frame = tk.LabelFrame(master, text="Select Root Directory", padx=10, pady=10)
        self.input_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew", columnspan=2) # Span 2 columns
        
        self.input_frame.grid_columnconfigure(0, weight=1) # Entry field column expands
        self.input_frame.grid_columnconfigure(1, weight=0) # Browse button column fixed

        self.directory_label = tk.Label(self.input_frame, text="Selected Directory:")
        self.directory_label.grid(row=0, column=0, sticky="w", pady=5)

        self.directory_entry = tk.Entry(self.input_frame, width=70)
        self.directory_entry.grid(row=1, column=0, sticky="ew", padx=5, pady=5)
        self.directory_entry.insert(0, os.path.expanduser("~") if os.name == 'posix' else os.getcwd())

        self.browse_button = tk.Button(self.input_frame, text="Browse", command=self._browse_directory)
        self.browse_button.grid(row=1, column=1, sticky="e", padx=5, pady=5)

        # --- Items to Include Listbox ---
        self.include_label = tk.Label(master, text="Items to Include (Select multiple with Ctrl/Shift):")
        self.include_label.grid(row=1, column=0, sticky="nw", padx=10, pady=(0, 5))

        self.file_listbox = tk.Listbox(master, selectmode=tk.MULTIPLE, height=10) # Set initial height
        self.file_listbox.grid(row=2, column=0, sticky="nsew", padx=10, pady=(0, 10))

        self.listbox_scrollbar = tk.Scrollbar(master, command=self.file_listbox.yview)
        self.listbox_scrollbar.grid(row=2, column=1, sticky="ns", pady=(0, 10))
        self.file_listbox['yscrollcommand'] = self.listbox_scrollbar.set

        # --- Action Button ---
        self.generate_button = tk.Button(master, text="Generate Tree Diagram", command=self._generate_tree)
        self.generate_button.grid(row=3, column=0, columnspan=2, pady=10) # Span both columns

        # --- Output Area ---
        self.output_label = tk.Label(master, text="File Tree:")
        self.output_label.grid(row=4, column=0, sticky="nw", padx=10, pady=(10, 0))

        self.output_text = scrolledtext.ScrolledText(master, wrap=tk.WORD, height=15, width=100)
        self.output_text.grid(row=5, column=0, sticky="nsew", padx=10, pady=(20, 10), columnspan=2) # Span 2 columns

        self.output_scrollbar = tk.Scrollbar(master, command=self.output_text.yview)
        self.output_scrollbar.grid(row=5, column=2, sticky="ns", pady=(20, 10)) # Place scrollbar in its own column
        self.output_text['yscrollcommand'] = self.output_scrollbar.set

        # Configure tags for output styling
        self.output_text.tag_config("dir", foreground="blue", font=("TkDefaultFont", 9, "bold"))
        self.output_text.tag_config("file", foreground="green")
        self.output_text.tag_config("error", foreground="red", font=("TkDefaultFont", 9, "bold"))
        self.output_text.tag_config("info", foreground="gray")

        self._log_message("Please select a directory to load its contents for selection.\n", "info")

    def _log_message(self, message, tag="normal"):
        """Helper to insert messages into the ScrolledText widget."""
        self.output_text.insert(tk.END, message, tag)
        self.output_text.see(tk.END) # Auto-scroll to the end

    def _browse_directory(self):
        """
        Opens a dialog to select a directory, updates the entry field,
        and populates the listbox with its immediate contents.
        """
        initial_dir = self.directory_entry.get() if os.path.isdir(self.directory_entry.get()) else os.getcwd()
        selected_directory = filedialog.askdirectory(parent=self.master,
                                                     initialdir=initial_dir, # Corrected from initial_dir
                                                     title="Select Directory for Tree Diagram")
        if selected_directory:
            self.directory_entry.delete(0, tk.END)
            self.directory_entry.insert(0, selected_directory)
            self._log_message(f"Selected root: {selected_directory}\n", "info")
            self._populate_listbox(selected_directory)
        else:
            self._log_message("Directory selection cancelled.\n", "info")

    def _populate_listbox(self, directory_path):
        """Populates the listbox with immediate children of the given directory."""
        self.file_listbox.delete(0, tk.END) # Clear existing items
        
        try:
            items = sorted(os.listdir(directory_path))
            for item in items:
                full_path = os.path.join(directory_path, item)
                if os.path.isdir(full_path):
                    self.file_listbox.insert(tk.END, f"{item}/") # Add '/' for directories
                else:
                    self.file_listbox.insert(tk.END, item)
            
            # Select all items by default for convenience, user can deselect
            for i in range(self.file_listbox.size()):
                self.file_listbox.selection_set(i)

            self._log_message(f"Loaded {len(items)} items from '{os.path.basename(directory_path)}'. Select items to include.\n", "info")

        except PermissionError:
            self._log_message(f"ERROR: Permission denied to access '{directory_path}'.\n", "error")
            messagebox.showerror("Permission Error", f"Permission denied to access '{directory_path}'.")
        except Exception as e:
            self._log_message(f"ERROR: Failed to load directory contents: {e}\n", "error")
            messagebox.showerror("Error", f"Failed to load directory contents: {e}")

    def _generate_tree(self):
        """Generates and displays the file tree diagram based on selected items."""
        self.output_text.delete(1.0, tk.END) # Clear previous output
        directory_path = self.directory_entry.get().strip()

        if not directory_path:
            messagebox.showerror("Error", "Please select a root directory first.")
            self._log_message("ERROR: No root directory selected.\n", "error")
            return

        if not os.path.isdir(directory_path):
            messagebox.showerror("Error", "Invalid root directory path. Please select a valid directory.")
            self._log_message(f"ERROR: Invalid root directory: {directory_path}\n", "error")
            return
        
        selected_indices = self.file_listbox.curselection()
        if not selected_indices:
            messagebox.showwarning("Warning", "No items selected. The tree will be empty except for the root.")
            self._log_message("WARNING: No items selected for tree generation.\n", "info")
            selected_items = [] # No items selected, so an empty list
        else:
            # Get the actual item names (remove trailing '/' for directories)
            selected_items = [self.file_listbox.get(i).strip('/') for i in selected_indices]

        self._log_message(f"Generating tree for selected items in: {directory_path}\n", "info")
        self._log_message("-" * 40 + "\n", "info")

        tree_string = self._build_filtered_tree_string(directory_path, selected_items)
        self.output_text.insert(tk.END, tree_string)
        self.output_text.see(tk.END) # Ensure full tree is visible

        self._log_message("\n" + "-" * 40 + "\n", "info")
        self._log_message("Tree generation complete.\n", "info")

    def _build_filtered_tree_string(self, root_dir, selected_top_level_items):
        """
        Builds the tree string, starting from the root_dir and only including
        the specified selected_top_level_items at the first level.
        """
        tree_lines = []
        tree_lines.append(f"{os.path.basename(root_dir)}/")

        # Sort selected items to ensure consistent tree output
        # Directories first, then files, both alphabetically
        sorted_selected_items = sorted(selected_top_level_items, 
                                       key=lambda x: (not os.path.isdir(os.path.join(root_dir, x)), x.lower()))

        for i, item_name in enumerate(sorted_selected_items):
            full_item_path = os.path.join(root_dir, item_name)
            is_last_item = (i == len(sorted_selected_items) - 1)
            
            # Start recursion for each selected top-level item
            self._recursive_add_to_tree(tree_lines, full_item_path, 0, [], is_last_item)
        
        return "\n".join(tree_lines)

    def _recursive_add_to_tree(self, tree_lines, current_path, level, parent_vertical_lines, is_last_sibling):
        """
        Helper function to recursively add lines to the tree_lines list.
        parent_vertical_lines: list of booleans, True if parent needs a '│', False if ' '
        """
        # Determine the indentation and prefix for the current item
        indent_parts = []
        for is_parent_last in parent_vertical_lines:
            indent_parts.append("    " if is_parent_last else "│   ")
        
        current_prefix = '└── ' if is_last_sibling else '├── '
        indent_str = "".join(indent_parts) + current_prefix
        
        item_name = os.path.basename(current_path)
        
        if os.path.isdir(current_path):
            tree_lines.append(f"{indent_str}{item_name}/")
            
            # Prepare for children: add current item's vertical line status to parent_vertical_lines
            new_parent_vertical_lines = list(parent_vertical_lines)
            new_parent_vertical_lines.append(is_last_sibling)

            try:
                children = sorted(os.listdir(current_path))
                # Separate directories and files to ensure correct 'last' prefix logic
                child_dirs = sorted([d for d in children if os.path.isdir(os.path.join(current_path, d))])
                child_files = sorted([f for f in children if os.path.isfile(os.path.join(current_path, f))])

                all_children_sorted = child_dirs + child_files

                for i, child_name in enumerate(all_children_sorted):
                    child_path = os.path.join(current_path, child_name)
                    is_last_child_sibling = (i == len(all_children_sorted) - 1)
                    self._recursive_add_to_tree(tree_lines, child_path, level + 1, new_parent_vertical_lines, is_last_child_sibling)
            except PermissionError:
                tree_lines.append(f"{indent_str}    <Permission Denied>\n")
            except Exception as e:
                tree_lines.append(f"{indent_str}    <Error: {e}>\n")
        else: # It's a file
            tree_lines.append(f"{indent_str}{item_name}")

# --- Main execution block ---
if __name__ == "__main__":
    root = tk.Tk()
    app = FileTreeGeneratorGUI(root)
    root.mainloop()
