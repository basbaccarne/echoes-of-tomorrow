import os
import subprocess
from hardware import button_horn
from states.shared import SharedState

def run():
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    audio_path = os.path.join(base_dir, "audio_files", f"welcome_{SharedState.booth_id}.wav")

    print(f"\n🗣️   Playing the welcome message of the librarian 👴")
    print("ALSA message:")

    try:
        # Start aplay in the background so we can monitor the horn
        process = subprocess.Popen([
            "aplay",
            "-D", "plughw:0,0",
            audio_path
        ])

        # Poll until playback finishes or horn is put back
        while process.poll() is None:
            if not button_horn.is_pressed:
                print("Horn replaced during welcome — returning to idle.")
                process.terminate()
                return "idle"
            time.sleep(0.1)

        # Check if aplay exited with an error
        if process.returncode != 0:
            print(f"aplay exited with code {process.returncode}")
            return "idle"

    except Exception as e:
        print(f"aplay error: {e}")
        return "idle"

    print("Welcome message finished.")
    return "recording"