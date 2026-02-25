import pygame
import time

played = False

def run():
    global played

    if not played:
        pygame.mixer.init()
        pygame.mixer.music.load("audio.wav")
        pygame.mixer.music.play()
        played = True
        print("Audio playing...")

    # wait until finished
    if not pygame.mixer.music.get_busy():
        print("Audio finished → switching to listening")
        return "listening"

    return None