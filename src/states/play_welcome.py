import os
import subprocess

def run():
    # build absolute path (project root)
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
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

    # audio finished → next state
    print("Welcome finished → recording")
    return "recording"