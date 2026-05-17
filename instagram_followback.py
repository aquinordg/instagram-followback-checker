#!/usr/bin/env python3
"""
Instagram Followback Checker
Script para verificar quem não segue de volta no Instagram
"""

import instaloader
from datetime import datetime
import webbrowser
import os
import getpass
import html
import pathlib

VERSION = "1.0.0"

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def show_banner():
    clear_screen()
    print("="*60)
    print(f"            INSTAGRAM FOLLOWBACK CHECKER v{VERSION}")
    print("="*60)
    print()

def get_username():
    show_banner()
    print(" PLEASE ENTER YOUR INSTAGRAM USERNAME")
    print("="*50)
    username = input("Enter your username: ").strip().lstrip('@')
    if not username:
        print(" Username cannot be empty. Please try again.")
        return get_username()
    return username

def get_password():
    print("\n Your password will not be saved and is used only for this session.")
    print("   Login is required to access your followers lists.")
    print("="*50)
    return getpass.getpass("Enter your password: ")

def save_html_report(all_users_dict, non_verified_list, verified_list, username):
    """Save the list to an HTML file with clickable links"""
    filename = f'Instagram_Followback_Report_{username}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.html'

    with open(filename, 'w', encoding='utf-8') as f:
        f.write('<!DOCTYPE html>\n<html lang="en">\n<head>\n')
        f.write('<meta charset="UTF-8">\n')
        f.write('<meta name="viewport" content="width=device-width, initial-scale=1.0">\n')
        f.write(f'<title>Instagram Followback Report - @{username}</title>\n')
        f.write("""
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Arial, sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; padding: 40px 20px; }
            .container { max-width: 1000px; margin: 0 auto; background: white; border-radius: 20px; box-shadow: 0 20px 60px rgba(0,0,0,0.3); overflow: hidden; }
            .header { background: linear-gradient(135deg, #f09433 0%, #e6683c 25%, #dc2743 50%, #cc2366 75%, #bc1888 100%); color: white; padding: 40px; text-align: center; }
            .header h1 { font-size: 2.5em; margin-bottom: 10px; }
            .header p { opacity: 0.9; font-size: 1.1em; }
            .content { padding: 40px; }
            .stats { background: #f8f9fa; border-radius: 15px; padding: 25px; margin-bottom: 30px; display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; }
            .stat-card { text-align: center; }
            .stat-number { font-size: 2em; font-weight: bold; color: #e1306c; }
            .stat-label { color: #666; margin-top: 5px; }
            .section { margin-bottom: 40px; }
            .section h2 { color: #262626; border-bottom: 3px solid #e1306c; padding-bottom: 10px; margin-bottom: 20px; display: inline-block; }
            .user-list { display: grid; gap: 10px; }
            .user-item { background: #f8f9fa; padding: 12px 20px; border-radius: 10px; transition: all 0.3s ease; display: flex; align-items: center; }
            .user-item:hover { background: #e9ecef; transform: translateX(5px); }
            .user-number { font-weight: bold; color: #999; margin-right: 15px; min-width: 40px; }
            .username { font-weight: bold; color: #0095f6; text-decoration: none; font-size: 1.1em; }
            .username:hover { text-decoration: underline; }
            .fullname { color: #8e8e8e; margin-left: 10px; }
            .verified-badge { color: #3897f0; margin-left: 8px; font-weight: bold; }
            .footer { background: #f8f9fa; padding: 20px; text-align: center; color: #666; font-size: 0.9em; }
            @media (max-width: 768px) { .content { padding: 20px; } .header h1 { font-size: 1.8em; } }
        </style>
        """)
        f.write('</head>\n<body>\n')

        f.write('<div class="container">\n')
        f.write('<div class="header">\n')
        f.write(f'<h1>📸 Instagram Followback Report</h1>\n')
        f.write(f'<p>Analysis for <strong>@{username}</strong></p>\n')
        f.write(f'<p>📅 {datetime.now().strftime("%d/%m/%Y at %H:%M:%S")}</p>\n')
        f.write('</div>\n')

        f.write('<div class="content">\n')
        f.write('<div class="stats">\n')
        f.write(f'<div class="stat-card"><div class="stat-number">{len(all_users_dict)}</div><div class="stat-label">Don\'t Follow Back</div></div>\n')
        f.write(f'<div class="stat-card"><div class="stat-number">{len(non_verified_list)}</div><div class="stat-label">Regular Accounts</div></div>\n')
        f.write(f'<div class="stat-card"><div class="stat-number">{len(verified_list)}</div><div class="stat-label">Verified Accounts</div></div>\n')
        f.write('</div>\n')

        # Non-verified accounts
        f.write('<div class="section">\n<h2>👥 Regular Accounts</h2>\n<div class="user-list">\n')
        for i, (user, info) in enumerate(non_verified_list, 1):
            f.write(f'<div class="user-item">')
            f.write(f'<span class="user-number">{i:3d}.</span>')
            f.write(f'<a href="https://www.instagram.com/{user}/" target="_blank" class="username">@{user}</a>')
            if info['full_name']:
                f.write(f'<span class="fullname">- {html.escape(info["full_name"])}</span>')
            f.write('</div>\n')
        f.write('</div>\n</div>\n')

        # Verified accounts
        if verified_list:
            f.write('<div class="section">\n<h2>⭐ Verified Accounts</h2>\n<div class="user-list">\n')
            start_num = len(non_verified_list) + 1
            for i, (user, info) in enumerate(verified_list, start_num):
                f.write(f'<div class="user-item">')
                f.write(f'<span class="user-number">{i:3d}.</span>')
                f.write(f'<a href="https://www.instagram.com/{user}/" target="_blank" class="username">@{user}</a>')
                f.write('<span class="verified-badge"> ✓ VERIFIED</span>')
                if info['full_name']:
                    f.write(f'<span class="fullname">- {html.escape(info["full_name"])}</span>')
                f.write('</div>\n')
            f.write('</div>\n</div>\n')

        f.write('</div>\n')
        f.write('<div class="footer">\n')
        f.write('<p>Generated by Instagram Followback Checker | Report opens profiles in new tabs</p>\n')
        f.write('</div>\n')
        f.write('</div>\n')
        f.write('</body>\n</html>')

    return filename


def _do_two_factor_login(L, max_attempts=3):
    """Prompt for a 2FA code and attempt two_factor_login. Returns True on success."""
    for attempt in range(1, max_attempts + 1):
        code = input(f"Enter verification code (attempt {attempt}/{max_attempts}): ").strip()
        try:
            L.two_factor_login(code)
            print(" Verification successful!")
            return True
        except instaloader.exceptions.BadCredentialsException:
            if attempt < max_attempts:
                print(f" Incorrect code. {max_attempts - attempt} attempt(s) left.")
            else:
                print(" Incorrect code. No attempts left.")
        except instaloader.exceptions.InvalidArgumentException:
            print(" Verification session expired. Please restart the script.")
            break
        except Exception as e:
            print(f" Verification error: {e}")
            break
    input("\nPress Enter to exit...")
    return False


def _try_session_login(L, username):
    """Try to load a saved Instaloader session. Returns True if session is valid."""
    try:
        L.load_session_from_file(username)
        logged_in_as = L.test_login()
        if logged_in_as == username:
            print(" Saved session loaded — no password needed.")
            return True
        print(" Saved session is expired, will log in with password.")
        return False
    except FileNotFoundError:
        return False
    except Exception as e:
        print(f" Could not load session: {e}")
        return False


def _print_null_login_help(username):
    print()
    print(" Instagram blocked this login attempt.")
    print(" This usually means your account has a pending verification.")
    print()
    print(" To fix it:")
    print("   1. Open instagram.com in your browser and log in normally.")
    print("   2. Complete any verification Instagram shows")
    print("      (email/phone confirmation, birthday, terms of service, etc.).")
    print("   3. Run this script again.")
    print()
    print(" If the problem persists, try from a different network or wait a few hours.")


def main():
    """Main function"""
    try:
        username = get_username()

        L = instaloader.Instaloader(
            max_connection_attempts=3,
            sleep=True,
            request_timeout=30
        )

        print("\n Logging into Instagram...")

        # Prefer saved session — avoids password prompt and bot-detection errors
        if not _try_session_login(L, username):
            password = get_password()
            try:
                L.login(username, password)
                print("Login successful!")
                try:
                    L.save_session_to_file()
                    print(" Session saved — future logins won't need a password.")
                except Exception:
                    pass
            except instaloader.exceptions.TwoFactorAuthRequiredException:
                print("\n Two-Step Verification Required")
                print("   A code may have been sent to your phone or email,")
                print("   or check your authenticator app.")
                if not _do_two_factor_login(L):
                    return
                try:
                    L.save_session_to_file()
                except Exception:
                    pass
            except instaloader.exceptions.BadCredentialsException:
                print(" Wrong password. Please check your credentials and try again.")
                input("\nPress Enter to exit...")
                return
            except instaloader.exceptions.LoginException as e:
                msg = str(e)
                print(f" Login failed: {msg}")
                if "checkpoint" in msg.lower():
                    print("\n Instagram flagged this login as suspicious.")
                    print("   Open the link above in your browser, complete the")
                    print("   verification, then run the script again.")
                elif "null" in msg.lower() or "unexpected" in msg.lower():
                    _print_null_login_help(username)
                input("\nPress Enter to exit...")
                return
            except instaloader.exceptions.TooManyRequestsException:
                print(" Too many requests. Instagram is rate-limiting this IP.")
                print("   Wait a few minutes and try again.")
                input("\nPress Enter to exit...")
                return
            except Exception as e:
                print(f" Unexpected login error: {e}")
                input("\nPress Enter to exit...")
                return

        try:
            profile = instaloader.Profile.from_username(L.context, username)
            print(" Profile loaded successfully!")
        except Exception as e:
            print(f" Error accessing profile: {e}")
            input("\nPress Enter to exit...")
            return

        # Collect data
        following = {}
        followers = set()

        print("\n Searching for people you follow...")
        print("    This may take a few minutes...")
        try:
            for followee in profile.get_followees():
                following[followee.username] = {
                    'full_name': followee.full_name,
                    'is_verified': followee.is_verified,
                    'userid': followee.userid
                }
                if len(following) % 100 == 0:
                    print(f"    Found {len(following)} profiles so far...")
            print(f" Found {len(following)} profiles you follow")
        except Exception as e:
            print(f" Error fetching following list: {e}")
            input("\nPress Enter to exit...")
            return

        print("\n Searching for your followers...")
        print("    This may take a few minutes...")
        try:
            for follower in profile.get_followers():
                followers.add(follower.username)
                if len(followers) % 100 == 0:
                    print(f"    Found {len(followers)} followers so far...")
            print(f" Found {len(followers)} followers")
        except Exception as e:
            print(f" Error fetching followers list: {e}")
            input("\nPress Enter to exit...")
            return

        # People you follow but who don't follow you back
        non_followers = {user: info for user, info in following.items() if user not in followers}

        # Separate verified and non-verified
        non_verified_users = [(user, info) for user, info in non_followers.items() if not info['is_verified']]
        verified_users = [(user, info) for user, info in non_followers.items() if info['is_verified']]

        # Sort
        non_verified_sorted = sorted(non_verified_users, key=lambda x: x[0].lower())
        verified_sorted = sorted(verified_users, key=lambda x: x[0].lower())

        print(f"\n Analysis completed!")
        print(f"   - Total profiles you follow: {len(following)}")
        print(f"   - Total followers: {len(followers)}")
        print(f"   - Profiles that don't follow you back: {len(non_followers)}")
        print(f"     - Regular accounts: {len(non_verified_sorted)}")
        print(f"     - Verified accounts: {len(verified_sorted)}")

        # Generate report
        html_filename = save_html_report(
            non_followers,
            non_verified_sorted,
            verified_sorted,
            username
        )

        # Open report in browser
        try:
            webbrowser.open(pathlib.Path(os.path.abspath(html_filename)).as_uri())
            print(f"\n Report opened automatically in your browser!")
            print(f" File saved as: {html_filename}")
        except Exception:
            print(f"\n Report saved as: {html_filename}")
            print(" You can open it manually in any web browser")

        print("\n Analysis completed successfully!")
        print(" Tip: In the HTML report, click on any username to open their profile")

        input("\n Press Enter to exit...")

    except KeyboardInterrupt:
        print("\n\n Operation cancelled by user.")
    except Exception as e:
        print(f"\n Unexpected error: {e}")
        input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()
