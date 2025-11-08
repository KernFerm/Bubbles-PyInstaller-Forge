import re
import customtkinter as ctk
import threading
import requests
import tkinter as tk
import os
import sys
import logging
from tkinter import filedialog
import subprocess
import tkinter.messagebox
import queue
import time
from PIL import Image, ImageTk

# Set modern dark theme and accent color
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Set up logging for security
logging.basicConfig(filename="app_security.log", level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s")

# List of common modules for hidden-import selection
HIDDEN_IMPORT_OPTIONS = [
    "customtkinter",
    "requests",
    "PIL",
    "numpy",
    "tkinter",
    "json",
    "threading",
    # Add more as needed
]

# Expanded PyInstaller options, grouped for clarity
PYINSTALLER_OPTION_GROUPS = [
    ("Basic", [
        ("--onefile", "Bundle into one file (recommended for distribution)"),
        ("--onedir", "Create a one-folder bundle containing an executable (default)"),
        ("--name=NAME", "Name to assign to the bundled app and spec file"),
        ("--console", "Enable console window (default, mutually exclusive with --windowed/--noconsole)"),
        ("--windowed", "No console window (Windows/macOS, alias for --noconsole; mutually exclusive with --console)"),
        ("--noconsole", "No console window (Windows/macOS, alias for --windowed; mutually exclusive with --console)"),
        ("--icon=ICON.ico", "File icon for the executable (.ico on Windows)"),
        ("--version-file=FILE", "Add a version resource from FILE to the exe (Windows only)"),
        ("--help", "Show help message and exit"),
        ("--noconfirm", "Replace output directory without asking (default: ask)"),
        ("--clean", "Clean PyInstaller cache and remove temporary files before building"),
        ("--log-level=LEVEL", "Set the logging level (DEBUG, INFO, WARN, ERROR, CRITICAL)"),
        ("--disable-windowed-traceback", "Suppress error popups for GUI apps (Windows/macOS)"),
    ]),
    ("Files & Data", [
        ("--add-data=SRC;DEST", "Additional non-binary files or folders to be added (use ':' on Unix, ';' on Windows)"),
        ("--add-binary=SRC;DEST", "Additional binary files to be added (use ':' on Unix, ';' on Windows)"),
        ("--hidden-import=MOD", "Name an import not automatically detected"),
        ("--collect-data=MOD", "Collect all data from the given module"),
        ("--collect-binaries=MOD", "Collect all binaries from the given module"),
        ("--collect-submodules=MOD", "Collect all submodules from the given module"),
        ("--collect-all=MOD", "Collect all data, binaries, and submodules from the given module"),
        ("--exclude-module=MOD", "Exclude module from analysis"),
        ("--copy-metadata=MOD", "Copy metadata for the given module"),
        ("--recursive-copy-metadata=MOD", "Recursively copy metadata for the given module"),
        ("--runtime-hook=FILE", "Path to a runtime hook file to include in the build"),
    ]),
    ("Paths & Output", [
        ("--distpath=DIR", "Where to put the bundled app (default: ./dist)"),
        ("--workpath=DIR", "Where to put all the temporary work files (default: ./build)"),
        ("--specpath=DIR", "Where to put the generated .spec file (default: current directory)"),
        ("--runtime-tmpdir=PATH", "Where to extract libraries at runtime (advanced)"),
    ]),
    ("Advanced", [
        ("--debug", "Provide debug information in the executable"),
        ("--noupx", "Do not use UPX even if available (disables executable compression)"),
        ("--strip", "Strip the executable and shared libs (remove debug symbols)"),
        ("--ascii", "Do not include unicode encoding support (ASCII only)"),
        ("--no-embed-manifest", "Do not embed manifest in exe (Windows only)"),
        ("--bootloader-ignore-signals", "Ignore signals in bootloader (Linux/Unix)"),
        ("--key=KEY", "The key used to encrypt Python bytecode (obfuscation)"),
        ("--manifest=FILE", "Add manifest FILE to the exe (Windows only)"),
        ("--splash=IMAGE_FILE", "Add splash screen to the application (Windows/macOS)"),
        ("--codesign-identity=IDENTITY", "Code signing identity for macOS"),
        ("--osx-bundle-identifier=ID", "macOS bundle identifier"),
        ("--add-exports=MOD", "Add Java module exports (rare, advanced)"),
    ]),
    ("Windows", [
        ("--uac-admin", "Request admin privileges on Windows"),
        ("--uac-uiaccess", "Allow UIAccess on Windows"),
    ]),
]

# Expanded list of common hidden-import modules
ALL_HIDDEN_IMPORTS = [
    "customtkinter", "requests", "PIL", "numpy", "tkinter", "json", "threading", "pandas", "scipy", "sklearn", "matplotlib", "seaborn", "cv2", "lxml", "bs4", "PyQt5", "PySide2", "PySide6", "PyQt6", "PyQtWebEngine", "PyYAML", "yaml", "dateutil", "jinja2", "sqlalchemy", "sqlite3", "asyncio", "aiohttp", "pyodbc", "pymysql", "psycopg2", "win32com", "win32api", "win32gui", "win32con", "pywintypes", "pyttsx3", "pyperclip", "pystray", "pyautogui", "pygetwindow", "pymsgbox", "pyinputplus", "pyzbar", "pyserial", "serial", "pygments", "pycparser", "cryptography", "bcrypt", "paramiko", "pyOpenSSL", "OpenSSL", "pytz", "tzlocal", "pysocks", "requests_toolbelt", "requests_cache", "requests_oauthlib", "oauthlib", "googleapiclient", "google_auth_oauthlib", "google_auth_httplib2", "googletrans", "speech_recognition", "pyaudio", "sounddevice", "soundfile", "pygame", "pyglet", "pillow", "pytesseract", "pymupdf", "fitz", "reportlab", "tabulate", "xlrd", "xlwt", "openpyxl", "xlsxwriter", "docx", "pythoncom", "comtypes", "pywin32", "notebook", "jupyter", "notebook.services.contents.filemanager", "notebook.services.kernels.kernelmanager", "notebook.services.sessions.sessionmanager", "notebook.services.config.manager", "notebook.services.contents.manager", "notebook.services.contents.checkpoints", "notebook.services.contents.largefilemanager", "notebook.services.contents.filecheckpoints", "notebook.services.contents.fileio", "notebook.services.contents.filemanager", "notebook.services.contents.fileio", "notebook.services.contents.filecheckpoints", "notebook.services.contents.largefilemanager", "notebook.services.contents.manager", "notebook.services.contents.checkpoints", "notebook.services.contents.filemanager", "notebook.services.contents.fileio", "notebook.services.contents.filecheckpoints", "notebook.services.contents.largefilemanager", "notebook.services.contents.manager", "notebook.services.contents.checkpoints"
]

# Simple tooltip class for CustomTkinter widgets
class ToolTip:
    def __init__(self, widget, text, dynamic_fetch=None):
        self.widget = widget
        self.text = text
        self.tipwindow = None
        self.dynamic_fetch = dynamic_fetch
        self.active = False
        self.hide_after_id = None
        widget.bind("<Enter>", self.show_tip)
        widget.bind("<Leave>", self.hide_tip)

    def show_tip(self, event=None):
        self.active = True
        if self.hide_after_id:
            self.widget.after_cancel(self.hide_after_id)
            self.hide_after_id = None
        def _show(text):
            if not self.active or self.tipwindow or not text:
                return
            x, y, cx, cy = self.widget.bbox("insert") if hasattr(self.widget, 'bbox') else (0, 0, 0, 0)
            x = x + self.widget.winfo_rootx() + 40
            y = y + self.widget.winfo_rooty() + 20
            self.tipwindow = tw = ctk.CTkToplevel(self.widget)
            tw.wm_overrideredirect(True)
            tw.wm_geometry(f"+{x}+{y}")
            label = ctk.CTkLabel(tw, text=text, justify='left', font=("Segoe UI", 12), fg_color="#232837", text_color="#00eaff", corner_radius=8, padx=8, pady=4)
            label.pack()
        if self.dynamic_fetch:
            def fetch_and_show():
                try:
                    desc = self.dynamic_fetch()
                except Exception:
                    desc = self.text
                # Only show if still active
                self.widget.after(0, lambda: _show(desc))
            threading.Thread(target=fetch_and_show, daemon=True).start()
        else:
            _show(self.text)

    def hide_tip(self, event=None):
        self.active = False
        if self.hide_after_id:
            self.widget.after_cancel(self.hide_after_id)
        # Destroy tooltip instantly (no delay)
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()

try:
    import platform
    if platform.system() == 'Windows':
        try:
            from tkinterdnd2 import TkinterDnD
            class DnDCTk(ctk.CTk, TkinterDnD.Tk):
                def __init__(self, *args, **kwargs):
                    TkinterDnD.Tk.__init__(self)
                    ctk.CTk.__init__(self, *args, **kwargs)
            MainWindowClass = DnDCTk
        except ImportError:
            MainWindowClass = ctk.CTk
    else:
        MainWindowClass = ctk.CTk
except Exception:
    MainWindowClass = ctk.CTk

class SanitizeApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        # Remove centering logic, just set window size and show
        self.title("🧊 Bubbles PyInstaller Forge: Secure Builder")
        self.geometry("1000x900")
        self.resizable(False, False)
        self.minsize(1000, 900)
        self.configure(bg="#181c24")

        # Add menubar (using Tkinter)
        self.tk_menu = tk.Menu(self)
        self.config(menu=self.tk_menu)
        file_menu = tk.Menu(self.tk_menu, tearoff=0)
        file_menu.add_command(label="Exit", command=self.safe_exit)
        self.tk_menu.add_cascade(label="File", menu=file_menu)
        help_menu = tk.Menu(self.tk_menu, tearoff=0)
        help_menu.add_command(label="About", command=self.show_about)
        help_menu.add_command(label="Discord", command=lambda: self.open_discord())
        self.tk_menu.add_cascade(label="Help", menu=help_menu)

        # Security checks
        self.security_checks()

        # Main frame (reduced padding)
        self.main_frame = ctk.CTkFrame(self, corner_radius=20, fg_color="#232837")
        self.main_frame.pack(padx=8, pady=8, fill="both", expand=True)

        # Title
        self.title_label = ctk.CTkLabel(self.main_frame, text="Sanitize & Build Helper", font=("Segoe UI Semibold", 24), text_color="#00eaff")
        self.title_label.pack(pady=(8, 2))

        # Build output box (top, under title, slightly reduced height)
        self.build_output_frame = ctk.CTkFrame(self.main_frame, fg_color="#232837")
        self.build_output_frame.pack(padx=8, pady=(2, 4), fill="x")
        self.build_output = ctk.CTkTextbox(self.build_output_frame, height=110, font=("Consolas", 11), fg_color="#181c24", text_color="#e0e0e0")
        self.build_output.pack(fill="both", expand=True)
        self.build_output.configure(state="disabled")
        # Clear Output button
        self.clear_output_btn = ctk.CTkButton(self.build_output_frame, text="Clear Output", command=self.clear_output, fg_color="#232837", hover_color="#00eaff", font=("Segoe UI", 11), corner_radius=8, width=110)
        self.clear_output_btn.pack(side="left", padx=4, pady=2)
        # Save Log button
        self.save_log_btn = ctk.CTkButton(self.build_output_frame, text="Save Log", command=self.save_log, fg_color="#232837", hover_color="#00eaff", font=("Segoe UI", 11), corner_radius=8, width=110)
        self.save_log_btn.pack(side="left", padx=4, pady=2)

        # Progress indicator (spinner)
        self.spinner = ctk.CTkProgressBar(self.main_frame, width=180, height=16, corner_radius=8, mode="indeterminate")
        self.spinner.pack(pady=(0, 4))
        self.spinner.stop()
        self.spinner.pack_forget()

        # File selection row (move to just above build button)
        self.file_select_frame = ctk.CTkFrame(self.main_frame, fg_color="#232837")
        self.file_select_frame.pack(fill="x", padx=8, pady=(0, 4))
        self.file_select_btn = ctk.CTkButton(self.file_select_frame, text="Select file to build", command=self.select_file, fg_color="#00eaff", hover_color="#007c91", font=("Segoe UI", 12), corner_radius=8, width=180)
        self.file_select_btn.pack(side="left", padx=(0, 8))
        self.file_select_label = ctk.CTkLabel(self.file_select_frame, text="app.py", font=("Consolas", 11), text_color="#e0e0e0")
        self.file_select_label.pack(side="left")
        self.file_select_progress = ctk.CTkProgressBar(self.file_select_frame, width=100, height=14, corner_radius=8)
        self.file_select_progress.pack(side="left", padx=(12, 0))
        self.file_select_progress.set(0)
        self.file_select_progress.stop()
        self.file_select_status = ctk.CTkLabel(self.file_select_frame, text="", font=("Segoe UI", 10), text_color="#00eaff")
        self.file_select_status.pack(side="left", padx=(8, 0))

        # Top row: options and hidden-imports side by side
        self.top_row = ctk.CTkFrame(self.main_frame, fg_color="#232837")
        self.top_row.pack(fill="both", expand=True, padx=0, pady=0)

        # PyInstaller options (left)
        self.options_col = ctk.CTkFrame(self.top_row, fg_color="#232837")
        self.options_col.pack(side="left", fill="both", expand=True, padx=(0,6), pady=0)
        self.build_label = ctk.CTkLabel(self.options_col, text="PyInstaller Build Options:", font=("Segoe UI Semibold", 14), text_color="#00eaff")
        self.build_label.pack(anchor="w", padx=8, pady=(6, 0))
        self.options_scroll = ctk.CTkScrollableFrame(self.options_col, fg_color="#232837", corner_radius=10, width=340, height=220)
        self.options_scroll.pack(padx=8, pady=(0, 4), fill="both", expand=True)
        self.option_vars = {}
        for group_idx, (group_name, options) in enumerate(PYINSTALLER_OPTION_GROUPS):
            group_label = ctk.CTkLabel(self.options_scroll, text=group_name, font=("Segoe UI Semibold", 13), text_color="#00eaff")
            group_label.grid(row=group_idx*20, column=0, sticky="w", pady=(10, 2), padx=4, columnspan=2)
            for idx, (opt, desc) in enumerate(options):
                var = ctk.BooleanVar(value=False)  # All options unchecked by default
                cb = ctk.CTkCheckBox(self.options_scroll, text=f"{opt}", variable=var, command=self.update_command, font=("Segoe UI", 12), corner_radius=6)
                cb.grid(row=group_idx*20+idx+1, column=0, sticky="w", padx=8, pady=2)
                ToolTip(cb, desc)
                self.option_vars[opt] = var

        # Hidden-imports (right)
        self.hidden_col = ctk.CTkFrame(self.top_row, fg_color="#232837")
        self.hidden_col.pack(side="left", fill="both", expand=True, padx=(6,0), pady=0)
        self.hidden_label = ctk.CTkLabel(self.hidden_col, text="Select hidden-import modules:", font=("Segoe UI", 12), text_color="#00eaff")
        self.hidden_label.pack(anchor="w", padx=8, pady=(6,0))
        self.pypi_search_var = ctk.StringVar()
        self.pypi_search_entry = ctk.CTkEntry(self.hidden_col, textvariable=self.pypi_search_var, placeholder_text="Search PyPI package...", height=26, font=("Segoe UI", 11), corner_radius=6)
        self.pypi_search_entry.pack(padx=8, pady=(0, 2), fill="x")
        self.pypi_search_entry.bind("<KeyRelease>", self.on_pypi_search)
        self.pypi_search_entry.bind("<Return>", self.add_pypi_package)
        self.pypi_suggestions_box = None
        self.pypi_search_results = []

        self.hidden_scroll = ctk.CTkScrollableFrame(self.hidden_col, fg_color="#232837", corner_radius=10, width=340, height=220)
        self.hidden_scroll.pack(padx=8, pady=(0, 4), fill="both", expand=True)
        self.hidden_vars = {}
        for idx, mod in enumerate(ALL_HIDDEN_IMPORTS):
            var = ctk.BooleanVar(value=False)
            cb = ctk.CTkCheckBox(self.hidden_scroll, text=mod, variable=var, command=self.update_command, font=("Consolas", 11), corner_radius=6)
            cb.grid(row=idx, column=0, sticky="w", padx=8, pady=2)
            ToolTip(cb, mod, dynamic_fetch=lambda m=mod: self.get_package_info(m))
            self.hidden_vars[mod] = var

        # Text to sanitize
        self.input_entry = ctk.CTkEntry(self.main_frame, placeholder_text="Enter text to sanitize...", height=28, font=("Segoe UI", 13), corner_radius=8)
        self.input_entry.pack(pady=(4, 4), padx=12, fill="x")
        self.sanitize_btn = ctk.CTkButton(self.main_frame, text="Sanitize", command=self.sanitize_text, fg_color="#00eaff", hover_color="#007c91", font=("Segoe UI", 13), corner_radius=8, width=120)
        self.sanitize_btn.pack(pady=4)
        self.output_label = ctk.CTkLabel(self.main_frame, text="", wraplength=700, justify="left", font=("Segoe UI", 11), text_color="#e0e0e0")
        self.output_label.pack(pady=(0, 6), padx=12)
        self.separator = ctk.CTkFrame(self.main_frame, height=2, fg_color="#00eaff")
        self.separator.pack(fill="x", padx=12, pady=4)

        # Custom options entry
        self.custom_label = ctk.CTkLabel(self.main_frame, text="Custom PyInstaller options:", font=("Segoe UI", 12), text_color="#00eaff")
        self.custom_label.pack(anchor="w", padx=12, pady=(4,0))
        self.custom_entry = ctk.CTkEntry(self.main_frame, placeholder_text="e.g. --icon=myicon.ico --add-data=src;dest", height=24, font=("Segoe UI", 11), corner_radius=6)
        self.custom_entry.pack(padx=12, fill="x")
        self.custom_entry.bind("<KeyRelease>", lambda e: self.update_command())

        # Command display
        self.cmd_label = ctk.CTkLabel(self.main_frame, text="Build command:", font=("Segoe UI", 12), text_color="#00eaff")
        self.cmd_label.pack(anchor="w", padx=12, pady=(4,0))
        self.command_display = ctk.CTkEntry(self.main_frame, state="readonly", font=("Consolas", 11), height=24, corner_radius=6)
        self.command_display.pack(padx=12, fill="x")

        # Build Executable button and output
        self.build_btn = ctk.CTkButton(self.main_frame, text="Build Executable (Alt+B)", command=self.build_executable, fg_color="#00eaff", hover_color="#007c91", font=("Segoe UI", 13), corner_radius=8, width=180)
        self.build_btn.pack(pady=(4, 0))
        self.build_status = ctk.CTkLabel(self.main_frame, text="", font=("Segoe UI", 11), text_color="#00eaff")
        self.build_status.pack(pady=(2, 0))
        # Set a minimum window size
        self.minsize(1000, 900)

        # Accessibility: keyboard shortcuts
        self.bind_all('<Alt-b>', lambda e: self.build_executable())
        self.build_btn.configure(text="Build Executable (Alt+B)")
        # Focus ring: increase thickness and color
        style = """
        *:focus {
            outline: 3px solid #00eaff !important;
            outline-offset: 2px !important;
        }
        """
        try:
            self.tk.call('tk', 'scaling', 1.2)
        except Exception:
            pass

        # Initial command update
        self.selected_file = None
        self.update_command()

        # Package info cache
        self.package_info_cache = {}

        # Output queue for build process
        self.output_queue = queue.Queue()
        self.after(100, self.poll_output_queue)

        # Build button state
        self.build_btn_enabled = True

        # Clean up old temp build folders on startup
        self.cleanup_temp_build_dirs()
        # Check PyInstaller version
        self.pyinstaller_version = self.get_pyinstaller_version()

        # PyInstaller version display
        pyver = self.pyinstaller_version or "Not found"
        self.pyver_label = ctk.CTkLabel(self.main_frame, text=f"PyInstaller version: {pyver}", font=("Segoe UI", 11), text_color="#ffb300")
        self.pyver_label.pack(anchor="ne", padx=8, pady=(0,2))
        if not self.pyinstaller_version:
            tk.messagebox.showwarning("PyInstaller Missing", "PyInstaller is not installed or not found in PATH. Please install it before building.")

    def poll_output_queue(self):
        if getattr(self, '_closing', False):
            return
        try:
            while True:
                text = self.output_queue.get_nowait()
                self.append_build_output(text)
        except Exception:
            # Silently ignore all errors (including queue.Empty)
            pass
        if not getattr(self, '_closing', False):
            self.after(100, self.poll_output_queue)

    def cleanup_temp_build_dirs(self):
        try:
            import shutil, glob, os, time
            base = os.path.abspath(os.getcwd())
            now = time.time()
            for d in glob.glob(os.path.join(base, "build_output_temp*")):
                try:
                    # Remove if older than 1 hour or empty
                    if os.path.isdir(d):
                        if not os.listdir(d) or now - os.path.getmtime(d) > 3600:
                            shutil.rmtree(d)
                except Exception:
                    pass
        except Exception:
            pass

    def get_pyinstaller_version(self):
        import subprocess
        try:
            out = subprocess.check_output(["pyinstaller", "--version"], universal_newlines=True, stderr=subprocess.STDOUT, timeout=5)
            return out.strip()
        except Exception:
            return None

    def security_checks(self):
        # Warn if running as admin/root
        try:
            if os.name == "nt":
                import ctypes
                if ctypes.windll.shell32.IsUserAnAdmin():
                    logging.warning("App running as administrator.")
            else:
                if os.geteuid() == 0:
                    logging.warning("App running as root.")
        except Exception as e:
            logging.error(f"Security check failed: {e}")
        # Warn if running from world-writable directory
        try:
            if os.access(os.getcwd(), os.W_OK):
                logging.info("App running from writable directory: %s", os.getcwd())
        except Exception as e:
            logging.error(f"Directory check failed: {e}")

    def safe_exit(self):
        self._closing = True
        try:
            if hasattr(self, 'build_thread') and self.build_thread.is_alive():
                # Optionally, join the thread with timeout
                self.build_thread.join(timeout=1)
        except Exception:
            pass
        self.destroy()
        sys.exit(0)

    def show_about(self):
        tk.messagebox.showinfo("About", "Sanitize & Build Helper\nVersion 1.0\nSecure CustomTkinter GUI")

    def sanitize_text(self):
        raw = self.input_entry.get()
        cleaned = re.sub(r'[^A-Za-z0-9 ]+', '', raw)
        self.output_label.configure(text=f"Sanitized:\n{cleaned}")

    def select_file(self):
        self.file_select_status.configure(text="Waiting for file selection...")
        self.file_select_progress.set(0.1)
        self.file_select_progress.start()
        self.update_idletasks()
        self.after(100, self._select_file_dialog)

    def _select_file_dialog(self):
        file_path = filedialog.askopenfilename(filetypes=[("Python files", "*.py"), ("All files", "*")])
        self.file_select_progress.stop()
        self.file_select_progress.set(0)
        if file_path:
            self.selected_file = file_path
            self.file_select_label.configure(text=file_path)
            self.file_select_status.configure(text="File selected.")
            self.update_command()
        else:
            self.file_select_status.configure(text="No file selected.")

    def update_command(self):
        parts = ["pyinstaller"]
        for opt, var in self.option_vars.items():
            if var.get():
                if "=" in opt and not opt.endswith("="):
                    parts.append(opt)
                elif opt.endswith("="):
                    parts.append(f"{opt}<value>")
                else:
                    parts.append(opt)
        # Only add selected hidden-imports
        selected_hidden = [mod for mod, var in self.hidden_vars.items() if var.get()]
        hidden_opts = [f"--hidden-import={mod}" for mod in selected_hidden]
        parts.extend(hidden_opts)
        custom = self.custom_entry.get().strip()
        # Security: block dangerous characters in custom options
        if any(x in custom for x in [';', '|', '`', '$', '&&', '||', '>', '<']):
            logging.warning(f"Blocked dangerous custom option: {custom}")
            custom = ""  # Remove dangerous input
        if custom:
            parts.append(custom)
        # Use selected file or default to app.py
        main_file = self.selected_file if self.selected_file else "app.py"
        parts.append(f'"{main_file}"' if ' ' in main_file else main_file)
        cmd = " ".join(parts)
        self.command_display.configure(state="normal")
        self.command_display.delete(0, "end")
        self.command_display.insert(0, cmd)
        self.command_display.configure(state="readonly")

    def on_pypi_search(self, event=None):
        query = self.pypi_search_var.get().strip()
        if not query:
            self.hide_pypi_suggestions()
            return
        def fetch():
            try:
                # Fuzzy search: get top 5 matches from PyPI's search API
                resp = requests.get(f"https://pypi.org/search/?q={query}", timeout=3)
                names = re.findall(r'<a class="package-snippet" href="/project/([^"]+)/', resp.text)
                suggestions = list(dict.fromkeys(names))[:5] if names else [query]
            except Exception:
                suggestions = [query]
            self.after(0, lambda: self.show_pypi_suggestions(suggestions))
        self.pypi_search_entry.configure(placeholder_text="Searching...")
        threading.Thread(target=fetch, daemon=True).start()

    def show_pypi_suggestions(self, suggestions):
        self.pypi_search_entry.configure(placeholder_text="Search PyPI package...")
        self.pypi_search_results = suggestions
        if self.pypi_suggestions_box:
            self.pypi_suggestions_box.destroy()
        if not suggestions:
            return
        width = self.pypi_search_entry.winfo_width()
        self.pypi_suggestions_box = ctk.CTkFrame(self.hidden_col, fg_color="#232837", corner_radius=6, width=width)
        self.pypi_suggestions_box.place(x=self.pypi_search_entry.winfo_x(), y=self.pypi_search_entry.winfo_y()+32)
        for idx, pkg in enumerate(suggestions):
            btn = ctk.CTkButton(self.pypi_suggestions_box, text=pkg, fg_color="#232837", hover_color="#00eaff", font=("Consolas", 11), corner_radius=6, command=lambda p=pkg: self.add_pypi_package_name(p))
            btn.pack(fill="x")

    def hide_pypi_suggestions(self):
        if self.pypi_suggestions_box:
            self.pypi_suggestions_box.destroy()
            self.pypi_suggestions_box = None

    def add_pypi_package(self, event=None):
        pkg = self.pypi_search_var.get().strip()
        if pkg and pkg not in self.hidden_vars:
            var = ctk.BooleanVar(value=True)
            idx = len(self.hidden_vars)
            cb = ctk.CTkCheckBox(self.hidden_scroll, text=pkg, variable=var, command=self.update_command, font=("Consolas", 11), corner_radius=6)
            cb.grid(row=idx, column=0, sticky="w", padx=8, pady=2)
            self.hidden_vars[pkg] = var
            self.update_command()
        self.pypi_search_var.set("")
        self.hide_pypi_suggestions()

    def add_pypi_package_name(self, pkg):
        self.pypi_search_var.set(pkg)
        self.add_pypi_package()

    def get_package_info(self, pkg):
        if pkg in self.package_info_cache:
            return self.package_info_cache[pkg]
        try:
            resp = requests.get(f"https://pypi.org/pypi/{pkg}/json", timeout=3)
            if resp.status_code == 200:
                data = resp.json()
                summary = data.get("info", {}).get("summary", "")
                if summary:
                    self.package_info_cache[pkg] = summary
                    return summary
        except Exception:
            pass
        self.package_info_cache[pkg] = pkg
        return pkg

    def clear_output(self):
        self.build_output.configure(state="normal")
        self.build_output.delete("1.0", "end")
        self.build_output.configure(state="disabled")

    def show_error(self, title, message):
        logging.error(f"{title}: {message}")
        # Only show error if window is not closing/destroyed
        if not getattr(self, '_closing', False) and self.winfo_exists():
            try:
                tkinter.messagebox.showerror(title, message)
            except Exception:
                pass

    def report_callback_exception(self, exc, val, tb):
        import traceback
        msg = ''.join(traceback.format_exception(exc, val, tb))
        self.show_error("Unhandled Exception", msg)
        # Optionally, log all running threads
        import threading
        logging.error(f"Active threads: {[th.name for th in threading.enumerate()]}")

    def build_executable(self):
        import subprocess
        import tempfile
        import shutil
        import os
        # Validation: must select a file
        main_file = self.selected_file if self.selected_file else None
        if not main_file or not os.path.isfile(main_file):
            tkinter.messagebox.showerror("Error", "Please select a valid Python file to build.")
            return
        # Validation: check for dangerous custom options
        custom = self.custom_entry.get().strip()
        # Only allow safe options (letters, numbers, dashes, underscores, dots, slashes, equals, spaces)
        if not re.fullmatch(r'[\w\-\./= ]*', custom):
            tkinter.messagebox.showerror("Error", "Custom options contain dangerous or invalid characters.")
            return
        # Block if running as admin/root or from world-writable dir
        if self.is_admin_or_root() or self.is_world_writable():
            tkinter.messagebox.showerror("Security Error", "Running as admin/root or from a world-writable directory is not allowed.")
            return
        self.build_btn_enabled = False
        self.build_btn.configure(state="disabled")
        self.build_status.configure(text="Building...")
        self.build_output.configure(state="normal")
        self.build_output.delete("1.0", "end")
        # Show spinner
        self.spinner.pack(pady=(0, 4))
        self.spinner.start()
        self.update_idletasks()
        # Create a temp output folder for this build
        temp_dir = os.path.abspath(os.path.join(os.getcwd(), f"build_output_temp_{os.getpid()}"))
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
        os.makedirs(temp_dir, exist_ok=True)
        # Patch the command to use --distpath and --workpath
        cmd = self.command_display.get()
        cmd = re.sub(r"--distpath=\\S+", "", cmd)
        cmd = re.sub(r"--workpath=\\S+", "", cmd)
        cmd = f"{cmd} --distpath=\"{temp_dir}\" --workpath=\"{temp_dir}\\work\""
        def run_build():
            try:
                process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True, bufsize=1)
                for line in iter(process.stdout.readline, ''):
                    if not line:
                        break
                    self.output_queue.put(line)
                process.stdout.close()
                process.wait()
                if process.returncode == 0:
                    exe_path = self.find_exe_path(temp_dir)
                    self.after(0, self.build_status.configure, {"text": f"Build succeeded! {exe_path}"})
                else:
                    self.after(0, self.build_status.configure, {"text": "Build failed."})
                    self.after(0, lambda: tkinter.messagebox.showerror("Build Failed", "PyInstaller build failed. Check output for details."))
            except Exception as e:
                self.after(0, self.build_status.configure, {"text": f"Error: {e}"})
                self.after(0, lambda: tkinter.messagebox.showerror("Build Error", str(e)))
            finally:
                self.after(0, self.build_output.configure, {"state": "disabled"})
                self.after(0, self.spinner.stop)
                self.after(0, self.spinner.pack_forget)
                self.after(0, self.enable_build_btn)
        t = threading.Thread(target=run_build, daemon=True)
        t.start()
        # Track build thread for future exception handling
        self.build_thread = t

    def enable_build_btn(self):
        self.build_btn_enabled = True
        self.build_btn.configure(state="normal")

    def is_admin_or_root(self):
        try:
            if os.name == "nt":
                import ctypes
                return ctypes.windll.shell32.IsUserAnAdmin()
            else:
                return os.geteuid() == 0
        except Exception:
            return False

    def is_world_writable(self):
        try:
            if os.name == "nt":
                # On Windows, ignore directory writability (normal for user folders)
                return False
            else:
                # On Unix, check if directory is world-writable
                import stat
                mode = os.stat(os.getcwd()).st_mode
                return bool(mode & stat.S_IWOTH)
        except Exception:
            return False

    def append_build_output(self, text):
        self.build_output.configure(state="normal")
        # Limit output to last 3000 lines
        lines = self.build_output.get("1.0", "end").splitlines()
        if len(lines) > 3000:
            self.build_output.delete("1.0", f"{len(lines)-2999}.0")
        self.build_output.insert("end", text)
        self.build_output.see("end")
        self.build_output.configure(state="disabled")

    def save_log(self):
        from tkinter import filedialog
        log = self.build_output.get("1.0", "end")
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(log)

    def find_exe_path(self, dist_dir=None):
        import glob
        import os
        main_file = self.selected_file if self.selected_file else "app.py"
        base = os.path.splitext(os.path.basename(main_file))[0]
        if dist_dir is None:
            dist_dir = os.path.join(os.getcwd(), "dist")
        pattern = os.path.join(dist_dir, base, f"{base}.exe")
        matches = glob.glob(pattern)
        if matches:
            return matches[0]
        pattern2 = os.path.join(dist_dir, f"{base}.exe")
        matches2 = glob.glob(pattern2)
        if matches2:
            return matches2[0]
        # Also check for any .exe in dist_dir
        pattern3 = os.path.join(dist_dir, "*.exe")
        matches3 = glob.glob(pattern3)
        if matches3:
            return matches3[0]
        return f"(exe not found in {dist_dir})"

    def open_discord(self):
        import webbrowser
        webbrowser.open_new("https://discord.gg/zQbJJgwbUv")

if __name__ == "__main__":
    app = SanitizeApp()
    app.report_callback_exception = app.report_callback_exception
    app.mainloop()
