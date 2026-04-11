# 📸 Instagram Followback Checker

A Python script to identify who you follow on Instagram but doesn't follow you back.

[![Python Version](https://img.shields.io/badge/python-3.7+-blue.svg)](https://python.org)
[![Windows](https://img.shields.io/badge/Windows-0078D6?logo=windows&logoColor=white)](https://github.com)
[![Linux](https://img.shields.io/badge/Linux-FCC624?logo=linux&logoColor=black)](https://github.com)
[![macOS](https://img.shields.io/badge/macOS-000000?logo=apple&logoColor=white)](https://github.com)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

## ✨ Features

- ✅ Detects accounts you follow that don't follow you back
- ✅ Two-Factor Authentication (2FA) support
- ✅ Generates HTML report with clickable links
- ✅ Separates verified from non-verified accounts
- ✅ Simple terminal interface
- ✅ No passwords are saved (secure)

## 🚀 How to Use - Choose Your Option

### Option 1: For regular users (NO Python required) 🎯

**Windows only** - Download the ready-to-run executable:

1. Go to the [Releases page](https://github.com/aquinordg/instagram-followback-checker/releases)
2. Download the `instagram_followback.exe` file
3. **Double-click** the downloaded file
4. Follow the instructions in the terminal

> ⚠️ **Note**: Windows may show a security warning. Click "Run anyway" - it's safe!

**Quick download button:**

[![Download Latest Release](https://img.shields.io/badge/⬇️_Download_Latest_Release-2ea44f?style=for-the-badge&logo=github&logoColor=white)](https://github.com/aquinordg/instagram-followback-checker/releases/latest/download/instagram_followback.exe)

### Option 2: For users who prefer the source code 🐍

**Requires Python 3.7+ installed**

#### Quick installation:

```bash
# Clone the repository
git clone https://github.com/aquinordg/instagram-followback-checker.git
cd instagram-followback-checker

# Install the dependency
pip install -r requirements.txt

# Run
python instagram_followback.py
```

### Using automated scripts:

- **Windows**: Double-click `run.bat`
- **Mac/Linux**: Run `./run.sh` (use `chmod +x run.sh` first)

## 📊 How It Works

1. The script asks for your Instagram **username** and **password**
2. If 2FA is enabled, it will ask for the verification code
3. The script analyzes your "following" and "followers" lists
4. Generates an HTML report of who doesn't follow you back
5. The report opens automatically in your browser

## 🔒 Security

- **No credentials are saved** to files
- Passwords are entered via `getpass` (not visible on screen)
- Entire process runs locally on your computer
- **Full 2FA support** - no need to disable it!

## 📸 Sample Generated Report

The HTML report includes:

- Total number of accounts not following back
- Complete list with direct links to profiles
- Separation between regular and verified accounts
- Modern and responsive design
- Clickable links that open in new tabs

## 📦 For Developers: Generating Your Own .EXE

If you want to generate the executable yourself:

```bash
# Install PyInstaller
pip install pyinstaller

# Run the build script
python build_exe.py

# Or use PyInstaller directly
pyinstaller --onefile --console --name "instagram_followback" instagram_followback.py
```
The executable will be generated in the `dist/` folder

## 🖥️ Compatibility

| Operating System | Source Code (.py) | Executable (.exe) |
|-------------------|-------------------|-------------------|
| Windows 10/11     | ✅ Yes            | ✅ Yes (download .exe) |
| macOS             | ✅ Yes            | ❌ No (use source code) |
| Linux             | ✅ Yes            | ❌ No (use source code) |

## ⚠️ Important Warnings

- **Instagram Limits**: Avoid running too frequently
- **Large Accounts**: If you follow many people (+2000), the process may take a few minutes
- **Stable Connection**: Required to collect data

## 🐛 Common Issues and Solutions

### "Windows protected your PC" when running the .exe

1. Click **"More info"**
2. Click **"Run anyway"**
3. This happens because the executable is new, but it's safe

### Login Error

- Check your username/password
- If you have 2FA, wait for the code prompt

### Script is taking too long

- Normal for accounts with many followers (5-10 minutes)
- Instagram limits requests, so there are automatic pauses

## 📄 License

Distributed under the MIT license. See `LICENSE` for more information.

## ⭐ Acknowledgments

- [Instaloader](https://instaloader.github.io/) - Amazing library to interact with Instagram
- [PyInstaller](https://pyinstaller.org/) - To generate the executable
