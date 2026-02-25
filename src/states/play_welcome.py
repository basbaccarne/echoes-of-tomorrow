import os
import subprocess

played = False

def run():
    global played

    if not played:
        # build absolute path to audio file
        base_dir = os.path.dirname(os.path.dirname(__file__))
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
            return "idle"  # fallback

        played = True

    # since aplay is blocking, we are already finished
    print("Welcome finished → recording")
    return "recording"