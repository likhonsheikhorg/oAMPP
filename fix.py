/**
 * Likhon Sheikh 
 *
 * @author Likhon Sheikh <https://likhonsheikh.com>
 * @copyright 2023-2024 Likhon Sheikh
 * @telegram Likhon Sheikh  <https://t.me/likhondotxyz>
 */

import os
import time
import ctypes
import subprocess
import sys
import requests
import winreg as reg
import webbrowser

# Function to check if the script is run as an administrator
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

# Function to display animated text
def show_animated_text(text, delay_ms=30, color="cyan"):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay_ms / 1000)
    print()

# Function to create a progress bar
def show_progress(percentage):
    progress_bar = "[" + ("=" * (percentage // 2)) + (" " * ((100 - percentage) // 2)) + "]"
    sys.stdout.write(f"\r{progress_bar} {percentage}%")
    sys.stdout.flush()

# Function to modify registry
def modify_registry():
    registry_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System"
    name = "EnableLUA"
    
    try:
        reg_key = reg.OpenKey(reg.HKEY_LOCAL_MACHINE, registry_path, 0, reg.KEY_ALL_ACCESS)
        current_value, reg_type = reg.QueryValueEx(reg_key, name)
        
        show_animated_text("Checking current EnableLUA value...", color="cyan")
        for i in range(0, 101, 10):
            show_progress(i)
            time.sleep(0.1)
        print()
        
        if current_value == 1:
            show_animated_text("EnableLUA is currently set to 1. Changing to 0...", color="yellow")
            reg.SetValueEx(reg_key, name, 0, reg.REG_DWORD, 0)
            show_animated_text("EnableLUA has been set to 0. Please restart your computer for changes to take effect.", color="green")
        else:
            show_animated_text("EnableLUA is already set to 0. No changes needed.", color="green")
        
        reg.CloseKey(reg_key)
    except Exception as e:
        show_animated_text(f"Failed to modify registry: {str(e)}", color="red")

# Function to create a registry file
def create_registry_file():
    reg_content = """Windows Registry Editor Version 5.00

[HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System]
"EnableLUA"=dword:00000000
"""
    with open("oAMPP_UAC_Fix.reg", "w") as reg_file:
        reg_file.write(reg_content)
    show_animated_text("Created oAMPP_UAC_Fix.reg file for manual fixing.", color="cyan")

# Function to create a batch file for easy execution
def create_batch_file():
    batch_content = """@echo off
powershell -ExecutionPolicy Bypass -File "%~dp0oAMPP_UAC_Fix.ps1"
pause
"""
    with open("Run_oAMPP_UAC_Fix.bat", "w") as batch_file:
        batch_file.write(batch_content)
    show_animated_text("Created Run_oAMPP_UAC_Fix.bat for easy execution.", color="cyan")

# Function to download XAMPP installer
def download_xampp_installer():
    url = "https://www.apachefriends.org/xampp-files/8.2.4/xampp-windows-x64-8.2.4-0-VS16-installer.exe"
    output = "xampp-installer.exe"
    
    show_animated_text("Downloading latest XAMPP installer...", color="yellow")
    
    try:
        response = requests.get(url, stream=True)
        total_length = response.headers.get('content-length')
        
        if total_length is None:  # no content length header
            with open(output, "wb") as file:
                file.write(response.content)
        else:
            total_length = int(total_length)
            with open(output, "wb") as file:
                for data in response.iter_content(chunk_size=4096):
                    file.write(data)
                    done = int(50 * file.tell() / total_length)
                    sys.stdout.write("\r[{}{}]".format('=' * done, ' ' * (50 - done)))
                    sys.stdout.flush()
        show_animated_text("Download complete!", color="green")
    except Exception as e:
        show_animated_text(f"Failed to download XAMPP installer: {str(e)}", color="red")

# Function to open a web page
def open_web_page(url):
    webbrowser.open(url)
    show_animated_text("Opening Telegram channel...", color="magenta")

# Main script execution
def main():
    if not is_admin():
        show_animated_text("Please run this script as an Administrator!", color="red")
        sys.exit(1)

    os.system('cls' if os.name == 'nt' else 'clear')
    show_animated_text("Welcome to oAMPP - The Ultimate XAMPP UAC Warn Solution!", color="magenta")
    show_animated_text("Developed by Apache Friends, enhanced by VorTexCyberBD", color="green")
    
    modify_registry()
    create_registry_file()
    create_batch_file()
    download_xampp_installer()
    open_web_page("https://t.me/VorTexCyberBD")
    
    input("Press Enter to exit")

if __name__ == "__main__":
    main()
