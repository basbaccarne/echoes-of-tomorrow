import os
import pygame

def run():
    global played

    if not played:
        pygame.mixer.init()

        # build absolute path relative to this file (src/main.py)
        base_dir = os.path.dirname(os.path.dirname(__file__))  # src -> project root
        audio_path = os.path.join(base_dir, "audio", "welcome.wav")

        pygame.mixer.music.load(audio_path)
        pygame.mixer.music.play()
        played = True

        print(f"Playing: {audio_path}")

    if not pygame.mixer.music.get_busy():
        return "recording"

    return None