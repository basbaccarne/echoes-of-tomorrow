import os
import subprocess
from states.shared import SharedState

def run():
    # build absolute path (project root)
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    audio_path = os.path.join(base_dir, "audio", f"welcome_{SharedState.booth_id}.wav")

    print(f"\n🗣️ Playing the welcome message of the librarian 👴: {audio_path}")
    print("ALSA message:")

    try:
        subprocess.run([
            "aplay",
            "-D", "plughw:2,0",
            audio_path
        ], check=True)
    except subprocess.CalledProcessError as e:
        print(f"aplay error: {e}")
        return "idle"  # fallback

    # aplay holds the script until playback finishes, so we can directly return the next state afterwards
    print("\nWelcome message finished")
    return "recording"