import os
import subprocess

def run():
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    audio_path = os.path.join(base_dir, "audio", "recorded.wav")

    if not os.path.exists(audio_path):
        print("No recording found")
        return "idle"

    print(f"Playing recorded file: {audio_path}")

    try:
        subprocess.run([
            "aplay",
            "-D", "plughw:2,0",
            audio_path
        ], check=True)
    except subprocess.CalledProcessError as e:
        print(f"aplay error: {e}")
        return "idle"

    print("Playback finished → idle")
    return "idle"