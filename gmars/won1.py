from tkinter import *
from PIL import Image, ImageTk 
import subprocess
import pygame
from music_manager import music_manager

def resume_game():
    with open("resume.txt", "w") as f:
        f.write("1")
    subprocess.Popen(["python", "game1.py"])
    root.destroy()

def root_destroy():
    subprocess.Popen(["python", "menu.py"])
    root.destroy()

def nextmusic():
    music_manager.next_track()

def prevmusic():
    music_manager.prev_track()

root = Tk()
root.resizable(False, False)
root.geometry("400x400+350+200")
root.title("YOU WON!!!!")

# Музика вже запущена з music_manager

img = Image.open("%3F%3F%3F%3F.webp")
img = img.resize((400, 400))
bg_img = ImageTk.PhotoImage(img)

Label(root, image=bg_img).place(x=0, y=0, relwidth=1, relheight=1)

Label(root, text="YOU WON!!!!", font="arial 20 bold", fg="white", bg="#0c1d37").pack(pady=20)

Button(root, text="Next Level", bg="#0c1d37",
       font="arial 15 bold", fg="white",
       command=resume_game).pack(pady=20)

Button(root, text="Exit", bg="#832625",
       font="arial 15 bold", fg="white",
       command=root_destroy).pack(pady=20)

root.mainloop()