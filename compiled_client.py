import requests
import os
import pygame
import random
import shutil
from sys import exit

from tkinter import messagebox
from tkinter import Tk, filedialog

client_version = '1.0.0'

try:
    response = requests.get("https://raw.githubusercontent.com/Lncvrt/Foodie-Archive/refs/heads/client/client.py")
        
    if response.status_code == 200:
        exec(response.text.strip())
    else:
        messagebox.showerror("Unable to launch", f"Unable to launch updater\n\nError: {response.text} (code: {response.status_code})")
except Exception as error:
    messagebox.showerror("Unable to launch", f"Unable to launch updater\n\nError: {error}")