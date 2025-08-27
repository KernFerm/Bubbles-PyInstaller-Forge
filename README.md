# 🧊 Bubbles PyInstaller Forge: Secure Builder

**💬 Join our Discord for support & community:** [https://discord.gg/zQbJJgwbUv](https://discord.gg/zQbJJgwbUv)

A modern, secure, and user-friendly GUI for building Python executables with PyInstaller. Built with CustomTkinter for a beautiful and accessible experience.

- If you found this useful please star it. 

## ✨ Features
- ⚡ Real-time build progress and output
- 🔍 PyPI package search/autocomplete for hidden imports
- 🖥️ Modern, accessible UI with keyboard navigation
- 💾 Output log saving and 🧹 clear output button
- 🛡️ Security checks (admin/root, world-writable dir, input validation)
- 🚨 Error dialogs and validation for user actions
- 🧊 No drag & drop: File selection is now via a secure button for maximum compatibility

---

## 🆕 What's New
- Drag & drop support has been removed for improved stability and compatibility
- Window centering and startup behavior fixed for better OS compatibility
- Many bug fixes and UI improvements for a smoother experience
- Discord support link added to the Help menu

### ***[Download-The-Application-Here.md](https://github.com/KernFerm/Bubbles-PyInstaller-Forge/blob/main/Download-The-Application-Here.md)***
---

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

- ❓ **Other issues:**
  - Check the `app_security.log` file for details (if present).
  - Try running the app from a terminal/command prompt to see error messages.
  - If you need more help, open an issue or ask in the relevant Python/CustomTkinter community.
  - **Join our Discord for help:** [https://discord.gg/zQbJJgwbUv](https://discord.gg/zQbJJgwbUv)

---

> **Note:**
> This tool is only for making Windows `.exe` applications from Python scripts using PyInstaller. It does **not** apply PyArmor or any code obfuscation to your scripts. If you want to protect or obfuscate your code, you must use PyArmor (or similar tools) on your scripts **yourself before building** with Bubbles PyInstaller Forge.

---

**🎉 Enjoy secure, modern Python executable building with Bubbles PyInstaller Forge! 🧊**


- **[Releases](https://github.com/KernFerm/Bubbles-PyInstaller-Forge/releases/tag/application.zip)**


