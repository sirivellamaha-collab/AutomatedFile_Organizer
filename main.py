"""
Tkinter GUI for the Automated File Organizer.

Layout

1. Title Bar

2. Folder Path Entry Field

3. Browse Button

4. Organize Files Button

5. Clear Log Button

6. Progress Bar

7. Log / Status Text Area

8. Statistics Bar
   - Total Files Scanned
   - Files Moved
   - Errors Encountered

"""

import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from organizer import organize_folder

# Colour palette
BG         = "#1e1e2e"      # window background
SURFACE    = "#2a2a3e"      # card / panel background
ACCENT     = "#7c6af7"      # purple accent
ACCENT2    = "#5a4ed1"      # darker accent (hover)
SUCCESS    = "#50fa7b"      # green for success
ERROR_COL  = "#ff5555"      # red for errors
TEXT       = "#cdd6f4"      # primary text
TEXT_DIM   = "#6c7086"      # secondary text
ENTRY_BG   = "#313244"      # entry / text-area background
BORDER     = "#45475a"      # border / separator


class FileOrganizerApp(tk.Tk):
    """Main application window."""

    #  Construction 
    def __init__(self):
        super().__init__()

        self.title("Automated File Organizer")
        self.resizable(True, True)
        self.minsize(680, 520)
        self.configure(bg=BG)

        # Centre window on screen
        self.update_idletasks()
        w, h = 780, 620
        x = (self.winfo_screenwidth()  - w) // 2
        y = (self.winfo_screenheight() - h) // 2
        self.geometry(f"{w}x{h}+{x}+{y}")

        self._build_styles()
        self._build_ui()

    #  ttk style definitions 
    def _build_styles(self):
        style = ttk.Style(self)
        style.theme_use("clam")

        style.configure("TFrame",       background=BG)
        style.configure("Card.TFrame",  background=SURFACE)

        style.configure(
            "TLabel",
            background=BG,
            foreground=TEXT,
            font=("Segoe UI", 10),
        )
        style.configure(
            "Title.TLabel",
            background=BG,
            foreground=TEXT,
            font=("Segoe UI", 16, "bold"),
        )
        style.configure(
            "Sub.TLabel",
            background=BG,
            foreground=TEXT_DIM,
            font=("Segoe UI", 9),
        )
        style.configure(
            "Stat.TLabel",
            background=SURFACE,
            foreground=TEXT,
            font=("Segoe UI", 10, "bold"),
        )

        # Primary action button
        style.configure(
            "Accent.TButton",
            background=ACCENT,
            foreground="#ffffff",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            borderwidth=0,
            padding=(16, 8),
        )
        style.map(
            "Accent.TButton",
            background=[("active", ACCENT2), ("disabled", BORDER)],
            foreground=[("disabled", TEXT_DIM)],
        )

        # Secondary / ghost button
        style.configure(
            "Ghost.TButton",
            background=SURFACE,
            foreground=TEXT,
            font=("Segoe UI", 10),
            relief="flat",
            borderwidth=1,
            padding=(12, 7),
        )
        style.map("Ghost.TButton", background=[("active", ENTRY_BG)])

        # Progress bar
        style.configure(
            "Accent.Horizontal.TProgressbar",
            troughcolor=ENTRY_BG,
            background=ACCENT,
            thickness=6,
            borderwidth=0,
        )

    #  UI layout 
    def _build_ui(self):
        outer = ttk.Frame(self, padding=20)
        outer.pack(fill="both", expand=True)

        #  Title 
        ttk.Label(outer, text="📁  Automated File Organizer", style="Title.TLabel").pack(
            anchor="w"
        )
        ttk.Label(
            outer,
            text="Select a folder and click Organize Files to sort by category.",
            style="Sub.TLabel",
        ).pack(anchor="w", pady=(2, 16))

        #  Folder selection row 
        folder_frame = ttk.Frame(outer, style="Card.TFrame")
        folder_frame.pack(fill="x", pady=(0, 12))
        folder_frame.configure(padding=12)

        ttk.Label(folder_frame, text="Folder:", background=SURFACE, foreground=TEXT).pack(
            side="left", padx=(0, 8)
        )

        self.folder_var = tk.StringVar()
        entry = tk.Entry(
            folder_frame,
            textvariable=self.folder_var,
            bg=ENTRY_BG,
            fg=TEXT,
            insertbackground=TEXT,
            relief="flat",
            font=("Segoe UI", 10),
        )
        entry.pack(side="left", fill="x", expand=True, padx=(0, 8), ipady=5)

        ttk.Button(
            folder_frame,
            text="Browse",
            command=self._browse,
            style="Ghost.TButton",
        ).pack(side="right")

        #─ Action buttons 
        btn_frame = ttk.Frame(outer)
        btn_frame.pack(fill="x", pady=(0, 10))

        self.organize_btn = ttk.Button(
            btn_frame,
            text="⚡  Organize Files",
            command=self._start_organize,
            style="Accent.TButton",
        )
        self.organize_btn.pack(side="left", padx=(0, 8))

        ttk.Button(
            btn_frame,
            text="Clear Log",
            command=self._clear_log,
            style="Ghost.TButton",
        ).pack(side="left")

        #  Progress bar 
        self.progress = ttk.Progressbar(
            outer,
            mode="indeterminate",
            style="Accent.Horizontal.TProgressbar",
        )
        self.progress.pack(fill="x", pady=(0, 10))

        #  Log text area 
        log_frame = tk.Frame(outer, bg=BORDER, padx=1, pady=1)
        log_frame.pack(fill="both", expand=True, pady=(0, 12))

        self.log_text = tk.Text(
            log_frame,
            bg=ENTRY_BG,
            fg=TEXT,
            insertbackground=TEXT,
            relief="flat",
            font=("Consolas", 9),
            state="disabled",
            wrap="word",
        )
        self.log_text.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(log_frame, command=self.log_text.yview)
        scrollbar.pack(side="right", fill="y")
        self.log_text.configure(yscrollcommand=scrollbar.set)

        # Colour tags for log lines
        self.log_text.tag_configure("moved",   foreground=SUCCESS)
        self.log_text.tag_configure("error",   foreground=ERROR_COL)
        self.log_text.tag_configure("info",    foreground=TEXT)
        self.log_text.tag_configure("heading", foreground=ACCENT, font=("Consolas", 9, "bold"))

        # ── Stats bar 
        stats_frame = tk.Frame(outer, bg=SURFACE, padx=10, pady=8)
        stats_frame.pack(fill="x")

        self.stat_scanned = self._stat_cell(stats_frame, "Scanned", "0")
        ttk.Separator(stats_frame, orient="vertical").pack(side="left", fill="y", padx=10)
        self.stat_moved   = self._stat_cell(stats_frame, "Moved",   "0")
        ttk.Separator(stats_frame, orient="vertical").pack(side="left", fill="y", padx=10)
        self.stat_errors  = self._stat_cell(stats_frame, "Errors",  "0")

    def _stat_cell(self, parent, label: str, initial: str) -> tk.StringVar:
        """Create a labelled stat cell and return its StringVar."""
        cell = tk.Frame(parent, bg=SURFACE)
        cell.pack(side="left")
        var = tk.StringVar(value=initial)
        tk.Label(cell, text=label, bg=SURFACE, fg=TEXT_DIM, font=("Segoe UI", 8)).pack()
        tk.Label(cell, textvariable=var, bg=SURFACE, fg=TEXT, font=("Segoe UI", 13, "bold")).pack()
        return var

    # ── Browse 
    def _browse(self):
        """Open a directory picker and populate the folder entry."""
        path = filedialog.askdirectory(title="Select Folder to Organize")
        if path:
            self.folder_var.set(path)

    # ── Organize 
    def _start_organize(self):
        """Validate input and kick off the organizer in a background thread."""
        folder = self.folder_var.get().strip()
        if not folder:
            messagebox.showwarning("No Folder", "Please select a folder first.")
            return

        # Disable button while running
        self.organize_btn.configure(state="disabled")
        self._clear_log()
        self.progress.start(12)

        # Run organizer in a daemon thread to keep GUI responsive
        thread = threading.Thread(
            target=self._run_organizer,
            args=(folder,),
            daemon=True,
        )
        thread.start()

    def _run_organizer(self, folder: str):
        """Background worker — calls organize_folder and posts results to GUI."""
        try:
            result = organize_folder(folder, progress_cb=self._post_log_line)
            # Schedule GUI update on main thread
            self.after(0, self._on_complete, result)
        except (FileNotFoundError, NotADirectoryError, PermissionError) as exc:
            self.after(0, self._on_error, str(exc))
        except Exception as exc:  # noqa: BLE001
            self.after(0, self._on_error, f"Unexpected error: {exc}")

    def _post_log_line(self, line: str):
        """Thread-safe: append a log line to the text widget."""
        self.after(0, self._append_log, line)

    def _append_log(self, line: str):
        """Append *line* to the log widget with appropriate colour tagging."""
        self.log_text.configure(state="normal")
        tag = "info"
        if "[MOVED]"  in line: tag = "moved"
        elif "[ERROR]" in line: tag = "error"
        elif line.startswith("=") or line.startswith("-"): tag = "heading"
        self.log_text.insert("end", line + "\n", tag)
        self.log_text.see("end")
        self.log_text.configure(state="disabled")

    def _on_complete(self, result: dict):
        """Called on the main thread when organizing finishes successfully."""
        self.progress.stop()
        self.organize_btn.configure(state="normal")

        # Update stats
        self.stat_scanned.set(str(result["total_scanned"]))
        self.stat_moved.set(str(result["total_moved"]))
        self.stat_errors.set(str(result["errors"]))

        # Summary popup
        cats = "\n".join(
            f"  {cat}: {count}"
            for cat, count in result["category_counts"].items()
            if count
        )
        log_path = result["log_path"]
        messagebox.showinfo(
            "Organization Complete ✅",
            f"Files scanned : {result['total_scanned']}\n"
            f"Files moved   : {result['total_moved']}\n"
            f"Errors        : {result['errors']}\n\n"
            f"Category breakdown:\n{cats or '  (none)'}\n\n"
            f"Log saved → {log_path}",
        )

    def _on_error(self, message: str):
        """Called on the main thread when a fatal error occurs."""
        self.progress.stop()
        self.organize_btn.configure(state="normal")
        self._append_log(f"[ERROR] {message}")
        messagebox.showerror("Error", message)

    #  Helpers 
    def _clear_log(self):
        """Clear the log text area and reset stat counters."""
        self.log_text.configure(state="normal")
        self.log_text.delete("1.0", "end")
        self.log_text.configure(state="disabled")
        self.stat_scanned.set("0")
        self.stat_moved.set("0")
        self.stat_errors.set("0")


# Entry point

if __name__ == "__main__":
    app = FileOrganizerApp()
    app.mainloop()
