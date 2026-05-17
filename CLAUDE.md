# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Single-file Python CLI tool that uses [Instaloader](https://instaloader.github.io/) to compare a user's following/followers lists on Instagram and generate an HTML report of accounts that don't follow back. Supports 2FA login. No tests, no database — purely interactive and stateless.

## Commands

```bash
# Run the application
python instagram_followback.py

# Install dependencies
pip install -r requirements.txt

# Build Windows .exe (auto-installs PyInstaller if missing)
python build_exe.py

# Build .exe manually via PyInstaller
pyinstaller --onefile --console --name "instagram_followback" instagram_followback.py
```

Platform launchers: `run.bat` (Windows), `run.sh` (Mac/Linux).

## Architecture

The entire application lives in `instagram_followback.py`. There are no modules, packages, or imports from within the repo.

**Flow:**
1. `get_credentials()` — prompts for username/password via `getpass`
2. `instaloader.Instaloader.login()` — authenticates; catches `TwoFactorAuthRequiredException` and calls `two_factor_login()`
3. `profile.get_followees()` / `profile.get_followers()` — iterates all connections (may take minutes; Instaloader sleeps between requests automatically via `sleep=True`)
4. Set subtraction finds non-followers; splits into verified vs. non-verified
5. `save_html_report()` — writes a self-contained HTML file with inline CSS; opens it with `webbrowser.open()`

**Key Instaloader config** (`instagram_followback.py:139-143`):
- `max_connection_attempts=3`, `sleep=True`, `request_timeout=30`
- `sleep=True` is required — removing it will trigger Instagram rate-limiting

## Release Process

Releases are tag-driven. Pushing a `v*` tag triggers `.github/workflows/build.yml`, which builds the `.exe` on `windows-latest` and attaches it to a GitHub Release using `RELEASE_NOTES.md` as the release body. The workflow also produces Linux and macOS binaries as artifacts (not attached to the release).

To cut a release: update `VERSION` in `instagram_followback.py`, update `RELEASE_NOTES.md`, tag and push:
```bash
git tag v1.x.x && git push origin v1.x.x
```
