import pygame
from tkinter import *
from PIL import Image, ImageTk
from music_manager import music_manager


def open_music_settings():
    root = Tk()
    root.resizable(False, False)
    root.geometry("400x400+350+200")
    root.title("Pause Menu")

    bg_img = None
    try:
        img = Image.open("%3F%3F%3F%3F.webp")
        img = img.resize((400, 400))
        bg_img = ImageTk.PhotoImage(img)
        Label(root, image=bg_img).place(x=0, y=0, relwidth=1, relheight=1)
    except Exception:
        root.configure(bg="#0c1d37")

    def close_root():
        root.destroy()

    def open_controls():
        root.withdraw()
        ctrl = Toplevel(root)
        ctrl.resizable(False, False)
        ctrl.geometry("400x400+350+200")
        ctrl.title("Control Settings")

        try:
            Label(ctrl, image=bg_img).place(x=0, y=0, relwidth=1, relheight=1)
        except Exception:
            ctrl.configure(bg="#0c1d37")

        Label(ctrl, text="Control Settings", font="arial 20 bold", fg="white", bg="#0c1d37").pack(pady=20)
        Label(ctrl, text="W: Move Forward", font="arial 15", fg="white", bg="#832625").pack(pady=10)
        Label(ctrl, text="S: Move Backward", font="arial 15", fg="white", bg="#832625").pack(pady=10)
        Label(ctrl, text="A: Move Left", font="arial 15", fg="white", bg="#832625").pack(pady=10)
        Label(ctrl, text="D: Move Right", font="arial 15", fg="white", bg="#832625").pack(pady=10)

        def back():
            ctrl.destroy()
            root.deiconify()

        Button(ctrl, text="Back", bg="#832625", font="arial 15", command=back).pack(pady=20)
        ctrl.protocol("WM_DELETE_WINDOW", back)

    def open_sound():
        root.withdraw()
        snd = Toplevel(root)
        snd.resizable(False, False)
        snd.geometry("400x400+350+200")
        snd.title("Sound Settings")

        try:
            Label(snd, image=bg_img).place(x=0, y=0, relwidth=1, relheight=1)
        except Exception:
            snd.configure(bg="#0c1d37")

        def back():
            snd.destroy()
            root.deiconify()

        def toggle_music():
            if music_manager.is_playing:
                music_manager.pause()
                pause_button.config(text="▶️")
            else:
                if pygame.mixer.music.get_busy():
                    music_manager.unpause()
                else:
                    music_manager.play()
                pause_button.config(text="⏸️")
            update_status()

        def set_volume(value):
            music_manager.set_volume(int(value) / 100)
            update_status()

        def prev_track():
            music_manager.prev_track()
            update_status()

        def next_track():
            music_manager.next_track()
            update_status()

        def update_status():
            track_label.config(text=f"Track: {music_manager.current_track + 1}/{len(music_manager.available_tracks)}")
            status_label.config(text=f"Status: {'Playing' if music_manager.is_playing else 'Paused'}")

        Label(snd, text="Sound Settings", font="arial 20 bold", fg="white", bg="#0c1d37").place(relx=0.5, y=40, anchor="center")

        radio_var = StringVar(value="on" if music_manager.is_playing else "off")
        Radiobutton(snd, text="On", variable=radio_var, value="on", bg="white", command=lambda: [music_manager.play(), pause_button.config(text="⏸️"), update_status()]).place(relx=0.45, rely=0.3, anchor="center")
        Radiobutton(snd, text="Off", variable=radio_var, value="off", bg="white", command=lambda: [music_manager.stop(), pause_button.config(text="▶️"), update_status()]).place(relx=0.55, rely=0.3, anchor="center")

        scale = Scale(snd, from_=0, to=100, orient=HORIZONTAL, command=set_volume, bg="#0c1d37", fg="white")
        scale.set(int(music_manager.volume * 100))
        scale.place(relx=0.5, rely=0.45, anchor="center")

        track_label = Label(snd, text=f"Track: {music_manager.current_track + 1}/{len(music_manager.available_tracks)}", font="arial 12", fg="white", bg="#0c1d37")
        track_label.place(relx=0.5, rely=0.58, anchor="center")

        status_label = Label(snd, text=f"Status: {'Playing' if music_manager.is_playing else 'Paused'}", font="arial 12", fg="white", bg="#0c1d37")
        status_label.place(relx=0.5, rely=0.65, anchor="center")

        Button(snd, text="Previous", bg="#832625", command=prev_track).place(relx=0.4, rely=0.75, anchor="center")
        Button(snd, text="Next", bg="#832625", command=next_track).place(relx=0.6, rely=0.75, anchor="center")

        pause_button = Button(snd, text="⏸️" if music_manager.is_playing else "▶️", bg="#832625", command=toggle_music)
        pause_button.place(relx=0.5, rely=0.85, anchor="center")

        Button(snd, text="Back", bg="#832625", command=back).place(relx=0.5, rely=0.92, anchor="center")
        snd.protocol("WM_DELETE_WINDOW", back)

    Label(root, text="Pause Menu", font="arial 20 bold", fg="white", bg="#0c1d37").pack(pady=20)

    Button(root, text="Resume", font="arial 15 bold", fg="white", bg="#0c1d37", command=close_root).pack(pady=10)
    Button(root, text="Sound", font="arial 15 bold", fg="white", bg="#0c1d37", command=open_sound).pack(pady=10)
    Button(root, text="Controls", font="arial 15 bold", fg="white", bg="#0c1d37", command=open_controls).pack(pady=10)

    root.protocol("WM_DELETE_WINDOW", close_root)
    root.mainloop()