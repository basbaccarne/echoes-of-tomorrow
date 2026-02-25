import pygame

played = False

def run():
    global played

    if not played:
        pygame.mixer.init()
        pygame.mixer.music.load("welcome.wav")
        pygame.mixer.music.play()
        played = True
        print("Playing welcome audio")

    if not pygame.mixer.music.get_busy():
        print("Welcome finished → recording")
        return "recording"

    return None