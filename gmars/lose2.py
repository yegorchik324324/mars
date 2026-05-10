from tkinter import *
from PIL import Image, ImageTk
import subprocess
import sys
import os
from music_manager import music_manager

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def safe_save():
    try:
        music_manager.save_state()
    except:
        pass

def try_again():
    safe_save()
    root.destroy()
    subprocess.Popen([sys.executable, os.path.join(BASE_DIR, "game2.py")], cwd=BASE_DIR)

def back_menu():
    safe_save()
    root.destroy()
    subprocess.Popen([sys.executable, os.path.join(BASE_DIR, "menu.py")], cwd=BASE_DIR)

def root_destroy():
    safe_save()
    root.destroy()

root = Tk()
root.resizable(False, False)
root.geometry("400x400+350+200")
root.title("YOU LOST")
root.protocol("WM_DELETE_WINDOW", root_destroy)

try:
    img = Image.open("%3F%3F%3F%3F.webp")
except:
    try:
        img = Image.open("download.jpg")
    except:
        try:
            img = Image.open("images1.jpg")
        except:
            img = Image.new("RGB", (400, 400), "#0c1d37")

img = img.resize((400, 400))
bg_img = ImageTk.PhotoImage(img)

Label(root, image=bg_img).place(x=0, y=0, relwidth=1, relheight=1)

Label(
    root,
    text="YOU LOST",
    font="arial 25 bold",
    fg="white",
    bg="#0c1d37"
).pack(pady=40)

Label(
    root,
    text="Спробуй пройти рівень ще раз",
    font="arial 13 bold",
    fg="yellow",
    bg="#0c1d37"
).pack(pady=10)

Button(
    root,
    text="Try Again",
    font="arial 15 bold",
    fg="white",
    bg="#0c1d37",
    command=try_again
).pack(pady=15)

Button(
    root,
    text="Back",
    font="arial 15 bold",
    fg="white",
    bg="#832625",
    command=back_menu
).pack(pady=15)

root.mainloop()