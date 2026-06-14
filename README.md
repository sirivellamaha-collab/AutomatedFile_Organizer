# Automated File Organizer
intern id - 

## Project Details

Project Name : Automated File Organizer
Duration     : 4 Weeks
Language     : Python 3.10.11
intern id    : CITS3409

## Project Scope

The Automated File Organizer is a desktop utility application that scans a user-selected folder and automatically sorts every file into named sub-folders (Images, Documents, Videos, Audio, Archives, Others) based on the file's extension. The application provides a real-time activity log, prevents accidental overwrites by renaming duplicates, and saves a persistent `organization_log.txt` for audit purposes.


## Objective

- Eliminate manual file-sorting effort.
- Provide an intuitive, point-and-click interface accessible to non-technical users.
- Demonstrate practical use of Python's standard library (`pathlib`, `shutil`, `tkinter`, `threading`, `datetime`).

## Technologies Used

• Python 3.10.11 – Core programming language
• Tkinter – Desktop GUI framework
• pathlib – Object-oriented path handling
• shutil – High-level file move operations
• os – Operating system and file system operations
• datetime – Timestamping log entries
• threading – Background processing for a responsive user interface


## Features

- Folder Selection — Browse button opens a native folder picker.
- One-click Organization — Single button to categorize and move all files.
- Automatic Category Folders — Sub-folders are created on demand.
- Duplicate-safe Moves — Conflicting filenames are renamed (file_1.ext, file_2.ext, etc.).
- Real-time Log Display — Every file operation appears instantly in the GUI.
- Stats Bar — Shows Total Scanned, Total Moved, and Error counts.
- Log File — organization_log.txt is written inside the organized folder.
- Error Handling — Graceful messages for missing paths, permission errors, and other exceptions.
- Clear Log — Resets the display without re-running the organizer.
- Dark Themed UI — Professional dark color scheme.

## File Type Categories

• Images: jpg, jpeg, png, gif, bmp, webp

• Documents: pdf, doc, docx, txt, ppt, pptx, xls, xlsx

• Videos: mp4, avi, mkv, mov

• Audio: mp3, wav, aac

• Archives: zip, rar, 7z

• Others: All remaining file extensions

## Installation Steps

No third-party packages are required. All dependencies ship with Python.

```bash
# 1. Verify Python version (3.10.11)
python --version

# 2. Clone or unzip the project
cd Automated_File_Organizer

# 3. (Optional) confirm tkinter is available
python -c "import tkinter; print('tkinter OK')"
```


## Execution Steps

```bash
# Run the application
python main.py
```

1. The GUI window opens.
2. Click Browse and select any folder you want to organize.
3. Click Organize Files.
4. Watch the live log as files are moved.
5. A summary popup appears on completion.
6. Check `organization_log.txt` inside the organized folder for a full record.


## Project Structure

Automated_File_Organizer/
│
├── main.py                  ← Tkinter GUI entry point
├── organizer.py             ← Core organization logic
├── file_utils.py            ← Extension mapping, path helpers, log writer
├── requirements.txt         ← Dependency notes
├── README.md                ← This file
├── organization_log.txt     ← Auto-generated on each run
│
├── screenshots/             ← GUI & output screenshots
└── documentation/
   └── Project_Documentation.md

## Expected Output

After clicking Organize Files on a folder containing mixed files:

MyFolder/
├── Images/
│   ├── photo.jpg
│   └── banner.png
├── Documents/
│   ├── resume.pdf
│   └── notes.txt
├── Videos/
│   └── demo.mp4
├── Audio/
│   └── track.mp3
├── Archives/
│   └── backup.zip
├── Others/
│   └── data.csv
└── organization_log.txt

## Conclusion

The Automated File Organizer demonstrates how a small Python application can solve a real everyday problem. It combines a clean GUI with robust file-system logic and produces an auditable log of every action taken.


## Future Enhancements

- Recursive organization — descend into sub-folders.
- Custom rules — user-defined extension→category mappings via a settings panel.
- Undo — restore files to their original locations from the log.
- Scheduled runs — auto-organize at set intervals using `schedule`.
- System tray — minimize to tray and watch a folder automatically.
- Dark/light theme toggle — user-switchable themes.
