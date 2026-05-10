from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import random
import subprocess
import sys
import os
import pygame
from music_manager import music_manager

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def safe_save():
    try:
        music_manager.save_state()
    except:
        pass

def root_destroy():
    safe_save()
    root.destroy()

def done():
    af = c.curselection()

    if af:
        number = c.get(af)
        g.insert(END, number)
        c.delete(af)

def delete_number():
    af = g.curselection()

    if af:
        number = g.get(af)
        c.insert(END, number)
        g.delete(af)

def clear_done():
    while g.size() > 0:
        number = g.get(0)
        c.insert(END, number)
        g.delete(0)

def open_win_window():
    root.withdraw()

    win_root = Toplevel(root)
    win_root.title("Victory")
    win_root.geometry("400x300+450+200")
    win_root.resizable(False, False)
    win_root.config(bg="#0c1d37")

    def back():
        safe_save()
        win_root.destroy()
        root.destroy()
        subprocess.Popen([sys.executable, os.path.join(BASE_DIR, "menu.py")], cwd=BASE_DIR)

    Label(
        win_root,
        text="ТИ ПРОЙШОВ ГРУ!",
        font=("Arial", 22, "bold"),
        bg="#0c1d37",
        fg="white"
    ).pack(pady=50)

    Label(
        win_root,
        text="Ти розгадав код бази Марс",
        font=("Arial", 13),
        bg="#0c1d37",
        fg="yellow"
    ).pack(pady=10)

    Button(
        win_root,
        text="Back",
        bg="#832625",
        fg="white",
        font=("Arial", 16, "bold"),
        command=back
    ).pack(pady=35)

def check_win():
    done_numbers = []

    for i in range(g.size()):
        done_numbers.append(g.get(i))

    correct_code = ["17", "1", "21", "22"]

    if done_numbers == correct_code:
        messagebox.showinfo("Перемога!", "Ти зібрав код 17 1 21 22 і пройшов гру!")
        safe_save()
        open_win_window()
    else:
        messagebox.showerror("Неправильно", "Код неправильний. Спробуй ще раз!")
        clear_done()

def nextmusic():
    try:
        music_manager.next_track()
    except:
        pass

def prevmusic():
    try:
        music_manager.prev_track()
    except:
        pass

def play_pause():
    try:
        music_manager.toggle_play_pause()
    except:
        pass

root = Tk()
root.title("Mars Code")
root.geometry("700x450+300+150")
root.resizable(False, False)
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
            img = Image.new("RGB", (700, 450), "#0c1d37")

img = img.resize((700, 450))
bg_img = ImageTk.PhotoImage(img)

bg_label = Label(root, image=bg_img)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

a = [
    "17",
    "1",
    "21",
    "22",
    "3",
    "8",
    "10",
    "14",
    "19",
    "25",
    "30",
    "5",
    "12",
    "7",
    "28",
    "33"
]

random.shuffle(a)

Label(
    root,
    text="Ласкаво просимо до бази \"Марс\"",
    font=("Arial", 18, "bold"),
    bg="#0c1d37",
    fg="white"
).grid(row=0, column=0, columnspan=3, pady=15)

Label(
    root,
    text="Збери код слова МАРС за порядком букв в алфавіті",
    font=("Arial", 12, "italic"),
    bg="#0c1d37",
    fg="white"
).grid(row=1, column=0, columnspan=3, pady=5)

Label(
    root,
    text="Цифри:",
    font=("Arial", 12, "italic"),
    bg="#0c1d37",
    fg="white"
).grid(row=2, column=0)

Label(
    root,
    text="Зібрано ✔:",
    font=("Arial", 12, "italic"),
    bg="#0c1d37",
    fg="white"
).grid(row=2, column=2)

c = Listbox(root, width=30, height=13, font=("Arial", 11))
c.grid(row=3, column=0, rowspan=3, padx=20, pady=10)

for i in a:
    c.insert(END, i)

g = Listbox(root, width=30, height=13, font=("Arial", 11))
g.grid(row=3, column=2, rowspan=3, padx=20, pady=10)

Button(
    root,
    text="DONE →",
    bg="green",
    fg="white",
    font=("Arial", 12, "bold"),
    width=10,
    command=done
).grid(row=3, column=1, padx=10, pady=5)

Button(
    root,
    text="DELETE ←",
    bg="#832625",
    fg="white",
    font=("Arial", 11, "bold"),
    width=10,
    command=delete_number
).grid(row=4, column=1, padx=10, pady=5)

Button(
    root,
    text="TRY",
    bg="#0c1d37",
    fg="white",
    font=("Arial", 13, "bold"),
    width=10,
    command=check_win
).grid(row=5, column=1, padx=10, pady=5)

Button(
    root,
    text="⏮",
    bg="#832625",
    fg="white",
    font=("Arial", 12, "bold"),
    command=prevmusic
).place(x=260, y=405)

Button(
    root,
    text="⏯",
    bg="#832625",
    fg="white",
    font=("Arial", 12, "bold"),
    command=play_pause
).place(x=330, y=405)

Button(
    root,
    text="⏭",
    bg="#832625",
    fg="white",
    font=("Arial", 12, "bold"),
    command=nextmusic
).place(x=400, y=405)

root.mainloop()