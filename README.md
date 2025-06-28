```python
COMING SOON
```


# 🧊 Bubbles PyInstaller Forge: Secure Builder

A modern, secure, and user-friendly GUI for building Python executables with PyInstaller. Built with CustomTkinter for a beautiful and accessible experience.

## ✨ Features
- ⚡ Real-time build progress and output
- 🔒 Secure file selection and drag & drop support (Windows with tkinterdnd2)
- 🔍 PyPI package search/autocomplete for hidden imports
- 🖥️ Modern, accessible UI with keyboard navigation
- 💾 Output log saving and 🧹 clear output button
- 🛡️ Security checks (admin/root, world-writable dir, input validation)
- 🚨 Error dialogs and validation for user actions

## 🧑‍💻 How to Use BubblesPyInstallerForge.exe (No Python Needed)

If you received only the `BubblesPyInstallerForge.exe` file (no Python script required):

**Requirements:**
- Windows 10 or newer (64-bit recommended)
- No Python installation or extra dependencies needed

1. **Just double-click the .exe**
   - No installation or setup is needed. You do not need Python installed.
2. **The app will open**
   - Use the graphical interface to select and build your own Python scripts into executables.
3. **No dependencies required**
   - All necessary libraries are bundled inside the .exe.
4. **Troubleshooting**
   - If you see errors about missing DLLs, try running on a different Windows machine or contact the provider for help.

---

## 🛠️ Troubleshooting & Help

- ❓ **App won't start or GUI is blank:**
  - If you are using the .exe, you do NOT need Python installed. If you are running the .py version, make sure you are using Python 3.8 or newer (Python 3.11+ recommended).
  - If you see errors about `tkinterdnd2`, drag & drop will be unavailable unless you install it on Windows.

- ❓ **Build fails or no .exe is produced:**
  - Check the build output for error messages.
  - Make sure your script runs without errors before building.
  - Some packages may require extra hidden imports—add them using the search or checkboxes.
  - If antivirus blocks the build, temporarily disable it or whitelist the output folder.

- ❓ **PyInstaller not found:**
  - Only relevant if running the .py version. Install it with `pip install pyinstaller` and ensure it's in your PATH.

- ❓ **Permission or security errors:**
  - Do not run the app as administrator/root unless necessary.
  - Avoid running from world-writable or system directories.

- ❓ **Drag & drop doesn't work:**
  - Only available on Windows with `tkinterdnd2` installed.
  - Otherwise, use the file selection button.

- ❓ **Other issues:**
  - Check the `app_security.log` file for details (if present).
  - Try running the app from a terminal/command prompt to see error messages.
  - If you need more help, open an issue or ask in the relevant Python/CustomTkinter community.

---

**🎉 Enjoy secure, modern Python executable building with Bubbles PyInstaller Forge! 🧊**
