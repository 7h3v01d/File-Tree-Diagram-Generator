# File Tree Diagram Generator

⚠️ **LICENSE & USAGE NOTICE — READ FIRST**

This repository is **source-available for private technical evaluation and testing only**.

- ❌ No commercial use  
- ❌ No production use  
- ❌ No academic, institutional, or government use  
- ❌ No research, benchmarking, or publication  
- ❌ No redistribution, sublicensing, or derivative works  
- ❌ No independent development based on this code  

All rights remain exclusively with the author.  
Use of this software constitutes acceptance of the terms defined in **LICENSE.txt**.

---

### Key Features

- Interactive GUI: A simple and intuitive interface built using Python's tkinter library.
- Customizable Root Selection: Easily browse and select any directory on your system as the starting point.
- Granular Selection: A multi-select listbox allows you to choose exactly which top-level files and folders to include in your diagram.
- Recursive Visualization: Automatically traverses subdirectories to build a complete visual representation of your selected path.
- Styled Output: The generated tree is displayed with color-coding—blue for directories, green for files, and red for errors (like permission issues)—making it easy to read at a glance.
- Automatic Formatting: Uses standard tree characters (├──, └──, │) to ensure your diagrams look professional and are ready for copy-pasting.
- Error Handling: Built-in protection against permission errors and invalid paths with real-time status logging.

### Installation
#### Prerequisites

- Python 3.x
- Tkinter: This is typically included with most Python installations. If it is missing, you can install it via:
  - Linux (Ubuntu/Debian): sudo apt-get install python3-tk
  - macOS/Windows: Usually comes pre-installed with Python.

### Setup
1. Download or clone this repository:
```Bash
git clone https://github.com/yourusername/file-tree-generator.git
cd file-tree-generator
```
### Usage
To launch the generator, run the script directly:
```Bash
python file2tree_gui_v1.1.py
```
#### How to Generate a Tree
1. Select Directory: Click the Browse button to choose the root folder you want to visualize.
2. Filter Items: Use the listbox to select or deselect specific items. By default, all immediate children are selected.
3. Generate: Click Generate Tree Diagram to see the result in the output area.
4. Copy: Highlight the text in the "File Tree" section and copy it for use in your own documentation.

### Project Structure

***file2tree_gui_v1.1.py***: The complete standalone application containing both the GUI logic and the recursive tree-building engine.

### Contribution Policy

Feedback, bug reports, and suggestions are welcome.

You may submit:

- Issues
- Design feedback
- Pull requests for review

However:

- Contributions do not grant any license or ownership rights
- The author retains full discretion over acceptance and future use
- Contributors receive no rights to reuse, redistribute, or derive from this code

---

### License
This project is not open-source.

It is licensed under a private evaluation-only license.
See LICENSE.txt for full terms.
