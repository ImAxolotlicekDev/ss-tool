import os
import re
import socket
import requests
import psutil
import platform
import random
from subprocess import check_output
import tkinter as tk
from tkinter import messagebox

def get_public_ip():
    try:
        response = requests.get('https://api.ipify.org?format=json')
        return response.json().get('ip')
    except requests.RequestException:
        return None

def get_os_version():
    return platform.platform()

def get_strange_named_apps(directory='C:\\'):
    strange_apps = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if re.match(r'^[A-Za-z]{8}\.exe$', file):
                strange_apps.append(os.path.join(root, file))
    return strange_apps

def get_recent_apps():
    try:
        recent_apps = check_output('powershell "Get-StartApps | Sort-Object LastAccessTime -Descending | Select-Object -First 10"', shell=True)
        return recent_apps.decode()
    except Exception as e:
        return str(e)

def get_sgrm_data():
    sgrm_data = {
        "example_key_1": "example_value_1",
        "example_key_2": "example_value_2",
    }
    return sgrm_data

def copy_to_clipboard(text):
    r = tk.Tk()
    r.withdraw()
    r.clipboard_clear()
    r.clipboard_append(text)
    r.update() 
    r.destroy()
    messagebox.showinfo("Copied", "PIN copied to clipboard!")

def collect_and_send_data():
    data = {
        'public_ip': get_public_ip(),
        'os_version': get_os_version(),
        'strange_named_apps': get_strange_named_apps(),
        'recent_apps': get_recent_apps(),
        'sgrm_data': get_sgrm_data()
    }

    pin = ''.join([random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789') for _ in range(16)])

    url = f"http://yourserver.net/scan/{pin}"
    response = requests.post(url, json=data)
    
    if response.status_code == 200:
        show_pin_window(pin)
    else:
        messagebox.showerror("Error", f"Failed to send data. Status code: {response.status_code}")

def show_pin_window(pin):
    root = tk.Tk()
    root.title("PIN Information")
    
    label = tk.Label(root, text=f"Your PIN is: {pin}", font=("Helvetica", 16))
    label.pack(pady=20)
    
    copy_button = tk.Button(root, text="Copy to Clipboard", command=lambda: copy_to_clipboard(pin))
    copy_button.pack(pady=10)
    
    root.mainloop()

if __name__ == "__main__":
    collect_and_send_data()
