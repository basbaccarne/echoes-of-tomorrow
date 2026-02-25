import os
import subprocess

played = False

def run():
    global played

    if not played:
        # go up from:
        # src/states/play_welcome.py
        # -> src/states
        # -> src
        # -> project root
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

        # audio at: /home/pi/echoes-of-tomorrow/audio/welcome.wav
        audio_path = os.path.join(base_dir, "audio", "welcome.wav")

        print(f"Playing via aplay: {audio_path}")

        try:
            subprocess.run([
                "aplay",
                "-D", "plughw:2,0",
                audio_path
            ], check=True)
        except subprocess.CalledProcessError as e:
            print(f"aplay error: {e}")
            return "idle"  # fallback to safe state

        played = True

    print("Welcome finished → recording")
    return "recording"