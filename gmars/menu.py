from tkinter import *
from PIL import Image, ImageTk
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

def toggle_music_key():
    try:
        music_manager.toggle_play_pause()
    except:
        pass

def volume_up():
    try:
        music_manager.set_volume(min(1.0, music_manager.volume + 0.1))
    except:
        pass

def volume_down():
    try:
        music_manager.set_volume(max(0.0, music_manager.volume - 0.1))
    except:
        pass

def start_game():
    safe_save()
    root.destroy()
    subprocess.Popen([sys.executable, os.path.join(BASE_DIR, "game.py")], cwd=BASE_DIR)

root = Tk()
root.resizable(False, False)
root.protocol("WM_DELETE_WINDOW", root_destroy)
root.geometry("400x400+350+200")
root.title("Menu")

root.bind_all(",", lambda event: prevmusic())
root.bind_all(".", lambda event: nextmusic())
root.bind_all("m", lambda event: toggle_music_key())
root.bind_all("M", lambda event: toggle_music_key())
root.bind_all("=", lambda event: volume_up())
root.bind_all("+", lambda event: volume_up())
root.bind_all("-", lambda event: volume_down())

if not music_manager.is_playing and not music_manager.paused:
    try:
        music_manager.play()
    except:
        pass

try:
    img = Image.open("%3F%3F%3F%3F.webp")
except:
    img = Image.new("RGB", (400, 400), "#0c1d37")

img = img.resize((400, 400))
bg_img = ImageTk.PhotoImage(img)

bg_label = Label(root, image=bg_img)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

def sett():
    root.withdraw()

    root1 = Toplevel(root)
    root1.resizable(False, False)
    root1.geometry("400x400+350+200")
    root1.title("Settings")

    Label(root1, image=bg_img).place(x=0, y=0, relwidth=1, relheight=1)

    def C():
        root1.withdraw()

        root3 = Toplevel(root1)
        root3.resizable(False, False)
        root3.geometry("520x680+330+20")
        root3.title("Control Settings")

        Label(root3, image=bg_img).place(x=0, y=0, relwidth=1, relheight=1)

        def back2():
            root3.destroy()
            root1.deiconify()

        Label(root3, text="Control Settings",
              font="arial 20 bold", fg="white", bg="#0c1d37").pack(pady=10)

        Label(root3, text="← LEFT ARROW: Move Left", font="arial 13 bold",
              fg="white", bg="#832625").pack(pady=4)

        Label(root3, text="→ RIGHT ARROW: Move Right", font="arial 13 bold",
              fg="white", bg="#832625").pack(pady=4)

        Label(root3, text="↑ UP ARROW: Move Up", font="arial 13 bold",
              fg="white", bg="#832625").pack(pady=4)

        Label(root3, text="↓ DOWN ARROW: Move Down", font="arial 13 bold",
              fg="white", bg="#832625").pack(pady=4)

        Label(root3, text="SPACE: Shoot", font="arial 13 bold",
              fg="white", bg="#832625").pack(pady=4)

        Label(root3, text="P: Pause / Settings", font="arial 13 bold",
              fg="white", bg="#832625").pack(pady=4)

        Label(root3, text="ESC: Music Settings", font="arial 13 bold",
              fg="white", bg="#832625").pack(pady=4)

        Label(root3, text="M: Music On / Off", font="arial 13 bold",
              fg="white", bg="#832625").pack(pady=4)

        Label(root3, text="Клавіша , : Previous Track", font="arial 13 bold",
              fg="white", bg="#832625").pack(pady=4)

        Label(root3, text="Клавіша . : Next Track", font="arial 13 bold",
              fg="white", bg="#832625").pack(pady=4)

        Label(root3, text="+ / = : Volume Up", font="arial 13 bold",
              fg="white", bg="#832625").pack(pady=4)

        Label(root3, text="- : Volume Down", font="arial 13 bold",
              fg="white", bg="#832625").pack(pady=4)

        Label(root3, text="DONE →: Move number in game4", font="arial 13 bold",
              fg="white", bg="#832625").pack(pady=4)

        Label(root3, text="DELETE ←: Return number in game4", font="arial 13 bold",
              fg="white", bg="#832625").pack(pady=4)

        Label(root3, text="TRY: Check code in game4", font="arial 13 bold",
              fg="white", bg="#832625").pack(pady=4)

        Button(root3, text="Back", bg="#832625",
               fg="white", font="arial 15 bold", command=back2).pack(pady=10)

    def back1():
        root1.destroy()
        root.deiconify()

    def mus():
        root1.withdraw()

        root2 = Toplevel(root1)
        root2.resizable(False, False)
        root2.geometry("400x400+350+200")
        root2.title("Sound Settings")

        Label(root2, image=bg_img).place(x=0, y=0, relwidth=1, relheight=1)

        def back():
            safe_save()
            root2.destroy()
            root1.deiconify()

        def toggle_music():
            if val.get() == "on":
                try:
                    music_manager.play()
                except:
                    pass
            else:
                try:
                    music_manager.stop()
                except:
                    music_manager.is_playing = False
                    music_manager.paused = False
                    safe_save()

        def set_volume(value):
            try:
                music_manager.set_volume(int(value) / 100)
            except:
                pass

        Label(root2, text="Sound Settings",
              font="arial 20 bold", fg="white", bg="#0c1d37").place(relx=0.5, y=40, anchor="center")

        if music_manager.is_playing:
            val = StringVar(value="on")
        else:
            val = StringVar(value="off")

        Radiobutton(root2, text="On", variable=val, value="on",
                    bg="white", command=toggle_music).place(relx=0.45, rely=0.4, anchor="center")

        Radiobutton(root2, text="Off", variable=val, value="off",
                    bg="white", command=toggle_music).place(relx=0.55, rely=0.4, anchor="center")

        scale = Scale(root2, from_=0, to=100,
                      orient=HORIZONTAL, command=set_volume, bg="#0c1d37", fg="white")
        scale.set(int(music_manager.volume * 100))
        scale.place(relx=0.5, rely=0.3, anchor="center")

        Button(root2, text="Previous", bg="#832625",
               command=prevmusic).place(relx=0.4, rely=0.6, anchor="center")

        Button(root2, text="Next", bg="#832625",
               command=nextmusic).place(relx=0.6, rely=0.6, anchor="center")

        Button(root2, text="Back", bg="#832625",
               command=back).place(relx=0.5, rely=0.75, anchor="center")

        k2 = 0

        def pause():
            nonlocal k2

            if k2 % 2 == 0:
                try:
                    music_manager.pause()
                except:
                    music_manager.is_playing = False
                    music_manager.paused = True
                    safe_save()

                butt["text"] = "▶️"
                val.set("off")
            else:
                try:
                    music_manager.unpause()
                except:
                    music_manager.is_playing = True
                    music_manager.paused = False
                    safe_save()

                butt["text"] = "⏸️"
                val.set("on")

            k2 += 1

        butt = Button(root2, text="⏸️", bg="#832625", command=pause)
        butt.place(relx=0.5, rely=0.5, anchor="center")

    Label(root1, text="Settings",
          font="arial 20 bold", fg="white", bg="#0c1d37").pack(pady=10)

    Button(root1, text="Controls", font="arial 15 bold",
           fg="white", bg="#0c1d37", command=C).pack(pady=10)

    Button(root1, text="Sound", font="arial 15 bold",
           fg="white", bg="#0c1d37", command=mus).pack(pady=10)

    Button(root1, text="Back", bg="#832625",
           font="arial 15 bold", command=back1).pack(pady=20)

Label(root, text="Menu",
      fg="white", bg="#0c1d37",
      font="arial 20 bold").pack(pady=20)

Button(root, text="Start Game",
       font="arial 15", fg="white",
       bg="#0c1d37", command=start_game).pack(pady=10)

def open_music_menu():
    root.withdraw()

    root2 = Toplevel(root)
    root2.resizable(False, False)
    root2.geometry("400x400+350+200")
    root2.title("Sound Settings")

    Label(root2, image=bg_img).place(x=0, y=0, relwidth=1, relheight=1)

    def back():
        safe_save()
        root2.destroy()
        root.deiconify()

    def toggle_music():
        if val.get() == "on":
            try:
                music_manager.play()
            except:
                pass
        else:
            try:
                music_manager.stop()
            except:
                music_manager.is_playing = False
                music_manager.paused = False
                safe_save()

    def set_volume(value):
        try:
            music_manager.set_volume(int(value) / 100)
        except:
            pass

    Label(root2, text="Sound Settings",
          font="arial 20 bold", fg="white", bg="#0c1d37").place(relx=0.5, y=40, anchor="center")

    if music_manager.is_playing:
        val = StringVar(value="on")
    else:
        val = StringVar(value="off")

    Radiobutton(root2, text="On", variable=val, value="on",
                bg="white", command=toggle_music).place(relx=0.45, rely=0.4, anchor="center")

    Radiobutton(root2, text="Off", variable=val, value="off",
                bg="white", command=toggle_music).place(relx=0.55, rely=0.4, anchor="center")

    scale = Scale(root2, from_=0, to=100,
                  orient=HORIZONTAL, command=set_volume, bg="#0c1d37", fg="white")
    scale.set(int(music_manager.volume * 100))
    scale.place(relx=0.5, rely=0.3, anchor="center")

    Button(root2, text="Previous", bg="#832625",
           command=prevmusic).place(relx=0.4, rely=0.6, anchor="center")

    Button(root2, text="Next", bg="#832625",
           command=nextmusic).place(relx=0.6, rely=0.6, anchor="center")

    Button(root2, text="Back", bg="#832625",
           command=back).place(relx=0.5, rely=0.75, anchor="center")

    k2 = 0

    def pause():
        nonlocal k2

        if k2 % 2 == 0:
            try:
                music_manager.pause()
            except:
                music_manager.is_playing = False
                music_manager.paused = True
                safe_save()

            butt["text"] = "▶️"
            val.set("off")
        else:
            try:
                music_manager.unpause()
            except:
                music_manager.is_playing = True
                music_manager.paused = False
                safe_save()

            butt["text"] = "⏸️"
            val.set("on")

        k2 += 1

    butt = Button(root2, text="⏸️", bg="#832625", command=pause)
    butt.place(relx=0.5, rely=0.5, anchor="center")

Button(root, text="Settings",
       font="arial 15", bg="#0c1d37",
       fg="white", command=sett).pack(pady=10)

Button(root, text="Music",
       font="arial 15", bg="#0c1d37",
       fg="white", command=open_music_menu).pack(pady=10)

Button(root, text="Exit",
       font="arial 15 bold", bg="#832625",
       fg="white", command=root_destroy).pack(pady=10)

root.mainloop()