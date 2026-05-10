import pygame
import os
import json

MUSIC_STATE_FILE = "music_state.json"

class MusicManager:
    def __init__(self):
        if not pygame.mixer.get_init():
            pygame.mixer.init()

        self.current_track = 0
        self.is_playing = False
        self.paused = False
        self.volume = 0.5

        self.tracks = [
            "whiltswagg_-_Platina_Santa_Klaus_instrumental_(SkySound.cc).mp3",
            "synthwave_goose_-_blade_runner_2049_slowed__reverb_(z3.fm).mp3",
            "Safari_slw_-_Let_Go_slowed_version_(SkySound.cc).mp3",
            "pxlse._hallow_-_numb_(SkySound.cc).mp3"
        ]

        self.available_tracks = []

        for track in self.tracks:
            if os.path.exists(track):
                self.available_tracks.append(track)

        self.load_state()

        if self.available_tracks:
            if self.current_track >= len(self.available_tracks):
                self.current_track = 0

            self.load_track(self.current_track)

            if pygame.mixer.get_init():
                pygame.mixer.music.set_volume(self.volume)

            if self.is_playing:
                pygame.mixer.music.play()

                if self.paused:
                    pygame.mixer.music.pause()

    def load_track(self, index):
        if pygame.mixer.get_init() and self.available_tracks:
            if index < 0:
                index = 0

            if index >= len(self.available_tracks):
                index = 0

            self.current_track = index
            pygame.mixer.music.load(self.available_tracks[self.current_track])

    def play(self):
        if pygame.mixer.get_init() and self.available_tracks:
            if self.paused:
                pygame.mixer.music.unpause()
            else:
                pygame.mixer.music.play()

            pygame.mixer.music.set_volume(self.volume)

        self.is_playing = True
        self.paused = False
        self.save_state()

    def play_music(self):
        self.play()

    def pause(self):
        if pygame.mixer.get_init():
            pygame.mixer.music.pause()

        self.is_playing = False
        self.paused = True
        self.save_state()

    def unpause(self):
        if pygame.mixer.get_init():
            pygame.mixer.music.unpause()

        self.is_playing = True
        self.paused = False
        self.save_state()

    def toggle_play_pause(self):
        if self.is_playing:
            self.pause()
        else:
            if self.paused:
                self.unpause()
            else:
                self.play()

    def next_track(self):
        if pygame.mixer.get_init() and self.available_tracks:
            self.current_track += 1

            if self.current_track >= len(self.available_tracks):
                self.current_track = 0

            self.load_track(self.current_track)

            if self.is_playing:
                pygame.mixer.music.play()

            self.save_state()

    def prev_track(self):
        if pygame.mixer.get_init() and self.available_tracks:
            self.current_track -= 1

            if self.current_track < 0:
                self.current_track = len(self.available_tracks) - 1

            self.load_track(self.current_track)

            if self.is_playing:
                pygame.mixer.music.play()

            self.save_state()

    def set_volume(self, volume):
        self.volume = volume

        if self.volume < 0:
            self.volume = 0

        if self.volume > 1:
            self.volume = 1

        if pygame.mixer.get_init():
            pygame.mixer.music.set_volume(self.volume)

        self.save_state()

    def save_state(self):
        try:
            state = {
                "current_track": self.current_track,
                "is_playing": self.is_playing,
                "paused": self.paused,
                "volume": self.volume
            }

            with open(MUSIC_STATE_FILE, "w") as f:
                json.dump(state, f)

        except:
            pass

    def load_state(self):
        if os.path.exists(MUSIC_STATE_FILE):
            try:
                with open(MUSIC_STATE_FILE, "r") as f:
                    state = json.load(f)

                self.current_track = state.get("current_track", 0)
                self.is_playing = state.get("is_playing", False)
                self.paused = state.get("paused", False)
                self.volume = state.get("volume", 0.5)

            except:
                self.current_track = 0
                self.is_playing = False
                self.paused = False
                self.volume = 0.5

    def cleanup(self):
        self.save_state()
        self.is_playing = False
        self.paused = False


music_manager = MusicManager()