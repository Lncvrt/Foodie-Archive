import requests
import os
import pygame
import random
import shutil
from sys import exit

from tkinter import messagebox
from tkinter import Tk, filedialog

try:
    try:
        response = requests.get('https://cdn.lncvrt.xyz/foodiedash/version.txt')

        if response.status_code == 200:
            version = response.json().get("version")
        else:
            version = 'n/a'
    except:
        version = 'n/a'

    #client_version is not defined here, it's defined in the compiled version (https://github.com/Lncvrt/Foodie-Archive/blob/client/compiled_client.py)

    if version != 'n/a' and version != client_version:
        messagebox.showwarning("Update required", f"Foodie Dash has a required update\n\nYour version: {client_version}\nLatest version: {version}\n\nPress \"OK\" to update")
        window = Tk()
        window.withdraw()

        default_file_name = "Foodie Dash.exe"
        save_path = filedialog.asksaveasfilename(
            defaultextension=".exe",
            filetypes=[("Executable Files", "*.exe")],
            initialfile=default_file_name
        )

        window.destroy()

        if save_path:
            try:
                print("Downloading update")
                response = requests.get(f"https://github.com/Lncvrt/Foodie-Archive/releases/latest/download/Foodie-Dash.exe")
                os.system("cls")

                if response.status_code == 200:
                    try:
                        with open(save_path, 'wb') as file:
                            file.write(response.content)
                            messagebox.showinfo("Update downloaded successfully", f"Run the file that has been downloaded to your computer at {save_path} to use the update.")
                    except Exception as error:
                        messagebox.showerror("Error while downloading update", f"There was an error while attempting to download the file.\n\nIf you are attempting to save the file to a running program, please try closing the program or temporaily save the file with a different name, or contact us at lncvrtreal@gmail.com for info on how to fix this issue.Error:\n\nError: {error}")
                else:
                    messagebox.showerror("Error while downloading update", f"There was an error while attempting to download the file.\n\nError: {response.text} (code: {response.status_code})\n\nPlease try again or contact us at lncvrtreal@gmail.com for info on how to fix this issue.")
            except:
                messagebox.showerror("Error while downloading update", "There was an error while attempting to download the file.\n\nPlease try again or contact us at lncvrtreal@gmail.com for info on how to fix this issue.")
        else:
            messagebox.showerror("Error while downloading update", "There was an error while attempting to download the file.\n\nPlease try again or contact us at lncvrtreal@gmail.com for info on how to fix this issue.")
    else:
        try:
            response = requests.get("https://raw.githubusercontent.com/Lncvrt/Foodie-Archive/refs/heads/main/foodie-dash.py")
                    
            if response.status_code == 200:
                exec(response.text.strip())
            else:
                messagebox.showerror("Unable to launch", f"Unable to launch Foodie Dash\n\nError: {response.text} (code: {response.status_code})")
        except Exception as error:
            messagebox.showerror("Foodie Dash has Crashed", f"Foodie Dash has crashed, please report this issue to https://github.com/Lncvrt/Foodie-Archive/issues.\n\nError: {error}")
except Exception as error:
    messagebox.showerror("Unable to launch", f"Unable to launch updater\n\nError: {error}")