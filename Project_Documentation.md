# Project Documentation


## Cover Page

AUTOMATED FILE ORGANIZER

Python Desktop Application

Language  : Python 3.10.11
Framework : Tkinter
Duration  : 4 Weeks

## Abstract

The Automated File Organizer is a Python desktop application that solves the common problem of cluttered, unorganized file systems. Given a folder path, it scans all top-level files, determines each file's category from its extension, creates the appropriate sub-folder if it does not exist, and moves the file into that sub-folder. It handles duplicate filenames gracefully, shows real-time progress in a GUI log panel, and persists an audit trail in `organization_log.txt`. The project uses only Python's standard library, making it dependency-free and easy to deploy.


## 1. Introduction

Modern computer users accumulate hundreds of files in download, desktop, and project folders over time. Manually sorting these files is tedious and error-prone. An automated solution removes that burden, saves time, and keeps the file system maintainable.

This project builds such a solution as a Tkinter desktop application. The user selects a folder through a native file picker, presses a button, and the application handles everything else — categorization, folder creation, file movement, duplicate prevention, and logging.

## 2. Problem Statement

Unorganized file storage leads to:

- Difficulty locating specific files.
- Reduced productivity.
- Duplicate files wasting storage space.
- Risk of accidentally deleting important files when bulk-cleaning.

**Solution:** An automated tool that classifies files by extension and moves them into labelled sub-folders without requiring any manual effort beyond selecting the target folder.


## 3. Objectives

1. Build a cross-platform desktop GUI application using Python and Tkinter.
2. Accurately classify files into Images, Documents, Videos, Audio, Archives, and Others.
3. Create destination folders dynamically without overwriting existing files.
4. Display real-time progress and a summary of results.
5. Generate a persistent log file for audit purposes.
6. Handle all foreseeable errors gracefully.


## 4. System Requirements

• Operating System: Windows 10/11, macOS 12+, Ubuntu 20.04+
• Python Version: 3.10.11 or newer
• Tkinter: Bundled with CPython (no extra installation required)
• RAM: 128 MB minimum
• Disk Space: Approximately 1 MB for application files



## 5. Methodology

Architecture Flow

1. GUI Layer (main.py)
   - User events (button clicks, folder selection)

2. Business Logic Layer (organizer.py)
   - File scanning
   - Category assignment
   - Error handling

3. Utility Layer (file_utils.py)
   - Extension mapping
   - Safe path resolution
   - Log writing

4. File System Layer (os, shutil, pathlib)
   - File and folder operations

Development followed these phases:

1. **Design** — Defined categories, extension lists, and UI wireframe.
2. **Utility layer** — Implemented `CATEGORY_MAP`, `get_category`, `resolve_destination`, and `write_log`.
3. **Business logic** — Implemented `organize_folder` with progress callback support.
4. **GUI** — Built the Tkinter interface with threading to keep the UI responsive.
5. **Testing** — Verified all test cases manually and via automated path checks.

## 6. System Design

### Module Responsibilities
Module Responsibilities

1. main.py
   Responsible for building the graphical user interface, handling user interactions, and managing background threads.

2. organizer.py
   Responsible for scanning folders, organizing files into appropriate categories, and aggregating operation results.

3. file_utils.py
   Responsible for file extension mapping, resolving duplicate file names safely, and performing log file operations.

### Data Flow

1. User selects a target folder.

2. The organize_folder() function is invoked.

3. The selected directory is scanned using Path.iterdir().

4. Each file is processed individually:
   - File category is identified.
   - Destination directory is determined.
   - Destination directory is created if it does not exist.
   - Duplicate-safe destination path is generated.
   - File is moved to the appropriate category folder.
   - Progress information is updated.

5. All operation records are collected.

6. Log information is written to organization_log.txt.

7. The process summary is presented to the user.

## 7. Flowchart

┌─────────────────────────────────┐
│           START                 │
└────────────────┬────────────────┘
                 │
                 ▼
┌─────────────────────────────────┐
│  User opens application         │
│  (main.py → FileOrganizerApp)   │
└────────────────┬────────────────┘
                 │
                 ▼
┌─────────────────────────────────┐
│  User clicks Browse             │
│  → filedialog.askdirectory()    │
│  → folder path stored           │
└────────────────┬────────────────┘
                 │
                 ▼
┌─────────────────────────────────┐
│  User clicks Organize Files     │
└────────────────┬────────────────┘
                 │
                 ▼
┌─────────────────────────────────┐
│  Validate folder path           │
│  Is folder valid?               │
└──────┬──────────────────┬───────┘
       │ NO               │ YES
       ▼                  ▼
┌──────────────┐  ┌────────────────────────┐
│ Show error   │  │ Start background thread │
│ messagebox   │  └───────────┬────────────┘
└──────────────┘              │
                              ▼
              ┌───────────────────────────────┐
              │  Scan folder (iterdir)         │
              │  Collect all files            │
              └──────────────┬────────────────┘
                             │
                             ▼
              ┌───────────────────────────────┐
              │  For each file:               │
              │    get_category(file)         │
              │    Create dest_dir if needed  │
              │    resolve_destination()      │
              │    shutil.move(file, dest)    │
              │    progress_cb(log line)      │
              └──────────────┬────────────────┘
                             │
                             ▼
              ┌───────────────────────────────┐
              │  write_log(log_path, entries) │
              └──────────────┬────────────────┘
                             │
                             ▼
              ┌───────────────────────────────┐
              │  Show summary popup           │
              │  Update stats bar             │
              └──────────────┬────────────────┘
                             │
                             ▼
                        ┌─────────┐
                        │   END   │
                        └─────────┘
## 8. Module Description

### `file_utils.py`
Core Components Description

1. CATEGORY_MAP
   Responsible for storing category-to-extension mappings used during file classification.

2. _EXT_LOOKUP
   A reverse mapping structure that enables fast lookup of categories based on file extensions.

3. get_category(file_path)
   Returns the category name associated with a specified file path.

4. resolve_destination(dest_dir, filename)
   Produces a unique destination path to avoid filename conflicts when moving files.

5. write_log(log_path, entries)
   Records operation details by appending a timestamped session block to the log file.

### `organizer.py`
Core Functions

1. _empty_counts()
   - Creates and returns a dictionary with all category counts initialized to zero.
   - Used for tracking the number of files organized in each category.

2. organize_folder(folder_path, progress_cb)
   - Main processing function of the application.
   - Scans the selected folder.
   - Categorizes files based on their extensions.
   - Moves files to their respective category folders.
   - Updates progress information.
   - Generates log entries and stores operation details.

### `main.py`
Class and Method Descriptions

1. FileOrganizerApp
   - Main application class derived from Tkinter's Tk class.
   - Manages all user interface components and application state.

2. _build_styles()
   - Configures ttk.Style settings.
   - Applies the dark theme to the application.

3. _build_ui()
   - Creates and arranges all user interface widgets.
   - Defines the application layout.

4. _browse()
   - Opens the folder selection dialog.
   - Allows the user to choose a directory for organization.

5. _start_organize()
   - Validates the selected folder path.
   - Disables controls during processing.
   - Starts the organization process in a background thread.

6. _run_organizer()
   - Executes the file organization process in a separate thread.
   - Prevents the user interface from freezing.

7. _post_log_line()
   - Provides a thread-safe mechanism for updating log messages.
   - Passes log entries to the user interface.

8. _append_log()
   - Appends log messages to the log display area.
   - Supports colored log entries for better readability.

9. _on_complete()
   - Executes when the organization process finishes successfully.
   - Updates statistics and user notifications.

10. _on_error()
    - Handles errors that occur during processing.
    - Displays appropriate error messages to the user.

11. _clear_log()
    - Clears all log entries from the display area.
    - Resets statistics and counters.

## 9. Screenshots

 Added screenshots to the `screenshots/` folder and reference them below.

Screenshots and Outputs

1. Main Application Window (screenshots/main_gui.png)
   - Illustrates the user interface when the application starts.

2. Folder Selection Dialog (screenshots/folder_selection.png)
   - Demonstrates the process of selecting a folder for organization.

3. Organization in Progress (screenshots/during_organize.png)
   - Shows live status updates and file movement logs.

4. Success Notification (screenshots/success_popup.png)
   - Displays the completion message after successful execution.

5. Log File Output (screenshots/log_file.png)
   - Presents the contents of the generated organization_log.txt file containing operation details.

## 10. Testing and validation

1. Test Case: Valid Folder with Mixed Files
   - Input: Folder containing jpg, pdf, mp4, mp3, and zip files.
   - Expected Result: Files are moved to their respective category folders.
   - Status: Pass

2. Test Case: Empty Folder
   - Input: Folder containing no files.
   - Expected Result: "Files found: 0" is displayed and no errors occur.
   - Status: Pass

3. Test Case: Duplicate Filename
   - Input: Two files with the name photo.jpg.
   - Expected Result: The second file is renamed to photo_1.jpg.
   - Status: Pass

4. Test Case: Unknown Extension
   - Input: data.csv
   - Expected Result: File is moved to the Others folder.
   - Status: Pass

5. Test Case: No Folder Selected
   - Input: Empty folder path field.
   - Expected Result: Warning message box is displayed.
   - Status: Pass

6. Test Case: Non-Existent Path
   - Input: Invalid folder path entered by the user.
   - Expected Result: Error message box is displayed.
   - Status: Pass

7. Test Case: All Images
   - Input: Folder containing 5 JPG/PNG image files.
   - Expected Result: All files are moved to the Images folder and the count is 5.
   - Status: Pass

8. Test Case: All Documents
   - Input: PDF, DOCX, TXT, XLSX, and PPTX files.
   - Expected Result: All files are moved to the Documents folder and the count is 5.
   - Status: Pass

9. Test Case: Log File Generation
   - Input: Any successful organization process.
   - Expected Result: organization_log.txt is created.
   - Status: Pass

10. Test Case: Multiple Runs
    - Input: Running the organizer twice on the same folder.
    - Expected Result: The second run detects no top-level files because they have already been organized.
    - Status: Pass

11. Test Case: Large Folder
    - Input: Folder containing more than 100 mixed files.
    - Expected Result: All files are organized successfully, progress is displayed, and no crashes occur.
    - Status: Pass

12. Test Case: Read-Only File
    - Input: File without write permission.
    - Expected Result: Error is logged for the affected file while other files continue to be processed.
    - Status: Pass

## 11. Results

All 12 test cases passed. The application correctly:

- Categorizes files across all six categories.
- Creates sub-folders only when needed.
- Prevents overwriting by appending numeric suffixes.
- Streams log output to the GUI in real time via a background thread.
- Writes a complete audit log to disk.
- Displays accurate statistics in the stats bar.


## 12. Conclusion

The Automated File Organizer achieves its objectives: it provides a dependency-free, cross-platform desktop utility that organizes a cluttered folder in seconds. The three-module architecture (GUI / logic / utilities) makes the code easy to read, test, and extend. The project demonstrates practical skills in Python GUI programming, file-system manipulation, thread safety, and error handling.


## 13. Future Scope

1. Recursive Mode
   - Enable the application to scan and organize files within sub-folders recursively.

2. Custom Rules
   - Allow users to define custom extension-to-category mappings based on their requirements.

3. Undo Functionality
   - Provide the ability to restore files to their original locations using information stored in the log file.

4. Scheduled Watch
   - Automatically monitor and organize files in selected folders at regular intervals.

5. Dark/Light Theme Toggle
   - Allow users to switch between dark and light interface themes.

6. Export to CSV
   - Enable exporting organization history, logs, and statistics to a CSV spreadsheet file.

7. System Tray Support
   - Allow the application to run silently in the background and minimize to the system tray.