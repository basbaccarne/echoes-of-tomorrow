# this code now just plays the recorded file and then goes back to idle, waiting for the next interaction. The processing and upload will be handled separately in the background while we're in the waiting state.
# needs to be replaced with sending
import os
import subprocess
from states.shared import SharedState

def run():
    
    print("\n⏳   Sending the question to the librarian for processing and response generation")
    
    # play prerecorded response
    # hhtp send
    # stop prerecorded response once the response is ready and then play the response
    
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    # use the code below to playback the recording
    # audio_path = os.path.join(base_dir, "audio", f"question_{SharedState.booth_id}.wav")
    audio_path = os.path.join(base_dir, "audio", f"waiting_{SharedState.booth_id}.wav")

    if not os.path.exists(audio_path):
        print("No waiting file found")
        return "idle"

    print(f"\n⏳   Playing the waiting librarian while processing the question")
    # print(f"Playing waiting file: {audio_path}")
    print("ALSA message:")

    try:
        subprocess.run([
            "aplay",
            "-D", "plughw:2,0",
            audio_path
        ], check=True)
    except subprocess.CalledProcessError as e:
        print(f"aplay error: {e}")
        return "idle"

    print("response ready, playing the response and going back to idle")
    
    return "response"