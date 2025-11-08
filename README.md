# 🧊 Bubbles PyInstaller Forge: Secure Builder

**💬 Join our Discord for support & community:** [https://fnbubbles420.org/discordinvite](https://fnbubbles420.org/discordinvite)

A modern, secure, and user-friendly GUI for building Python executables with PyInstaller. Built with CustomTkinter for a beautiful and accessible experience.

* `If you found this repo useful please star it.`

---

## ✨ Features

* ⚡ Real-time build progress and output
* 🔍 PyPI package search/autocomplete for hidden imports
* 🖥️ Modern, accessible UI with keyboard navigation
* 🗾 Output log saving and 🩹 clear output button
* 🛡️ Security checks (admin/root, world-writable dir, input validation)
* 🚨 Error dialogs and validation for user actions
* 🧊 No drag & drop: File selection is now via a secure button for maximum compatibility

---

## 🄟 What's New

* Drag & drop support removed for improved stability
* Window centering & startup behavior improved for all OS
* Many bug fixes and UI refinements
* Discord support link added to the Help menu

📘 ***[Download-The-Application-Here.md](https://github.com/KernFerm/Bubbles-PyInstaller-Forge/blob/main/WINDOWS-Download-The-Application-Here.md)***

---

## 🧑‍💻 How to Use

### 🪟 **Windows (No Python Needed)**

If you received only the `BubblesPyInstallerForge.exe` file:

**Requirements:**

* Windows 10 or newer (64-bit recommended)
* No Python installation or setup needed

**Steps:**

1. Double-click `BubblesPyInstallerForge.exe`
2. Select your `.py` file and click **Build Executable**
3. The app will handle dependencies automatically
4. If errors occur, view the console or `app_security.log`

---

### 🐧 **Linux (Python Required)**

**Requirements:**

* Python 3.11+ installed
* Pip and venv modules available

**Setup:**

```bash
sudo apt update && sudo apt install python3 python3-pip python3-venv -y
git clone https://github.com/KernFerm/Bubbles-PyInstaller-Forge.git
cd Bubbles-PyInstaller-Forge
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 main.py
```

**Notes:**

* You can build `.bin` or `.AppImage` equivalents using PyInstaller.
* If you get permission errors, avoid running as root.
* Output files will be stored in the `dist/` folder.

---

### 🍎 **macOS (Python Required)**

**Requirements:**

* macOS 12 Monterey or newer
* Python 3.11+ installed via [python.org](https://www.python.org/downloads/macos/) or Homebrew

**Setup:**

```bash
brew install python3 git
git clone https://github.com/KernFerm/Bubbles-PyInstaller-Forge.git
cd Bubbles-PyInstaller-Forge
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 main.py
```

**Notes:**

* Use `pyinstaller --onefile your_script.py` to generate `.app` or `.pkg` bundles.
* macOS may require a notarized or signed build to run executables outside Gatekeeper.

---

## 🛠️ Troubleshooting & Help

* **PyInstaller not found:**
  Install manually with `pip install pyinstaller`
* **Permission issues:**
  Avoid running as root; use a safe directory
* **Blank window or GUI crash:**
  Ensure CustomTkinter and tkinter are installed correctly

**Join our Discord for assistance:** [https://discord.gg/zQbJJgwbUv](https://discord.gg/zQbJJgwbUv)

---

> ⚠️ **Note:**
> This tool builds executables from Python scripts using PyInstaller. It does **not** obfuscate or encrypt code. Use PyArmor or similar tools before building if you need code protection.

---

**🎉 Enjoy secure, modern Python executable building with Bubbles PyInstaller Forge! 🧊**
📦 **[Releases](https://github.com/KernFerm/Bubbles-PyInstaller-Forge/releases/tag/application.zip)**
