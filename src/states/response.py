import os
import subprocess
from states.shared import SharedState

def run():
        
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    audio_path = os.path.join(base_dir, "audio", f"response_{SharedState.booth_id}.wav")
    print(f"\n⏳   Checking for the response file at {audio_path}")

    if not os.path.exists(audio_path):
        print("No response file found")
        return "idle"

    print(f"\n⏳   Playing the response for booth ID {SharedState.booth_id}")
    print("ALSA message:")

    try:
        subprocess.run([
            "aplay",
            "-D", "plughw:1,0",
            audio_path
        ], check=True)
    except subprocess.CalledProcessError as e:
        print(f"aplay error: {e}")
        return "idle"

    print("\n--------------------------------\n")
    print(f"Going back to the idle state.")
    print(f'This device is still set to booth ID: {SharedState.booth_id}')
    print("👂   Waiting for the horn to be picked up, looking forward to the next conversation ...")
    
    return "idle"