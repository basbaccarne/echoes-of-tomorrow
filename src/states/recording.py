import subprocess
import os
from hardware import button_stop

process = None

def run():
    global process

    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    audio_path = os.path.join(base_dir, "audio", f"recorded_{SharedState.booth_id}.wav")

    # start recording if not already
    if process is None:
        print(f"\n🎤 Recording the question in file {audio_path}")
        print("Press the #️⃣ button to stop the recording.")
        print("ALSA message:")
        process = subprocess.Popen([
            "arecord",
            "-D", "plughw:2,0",
            "-f", "cd",
            "-t", "wav",
            audio_path
        ])
        # print("Recording started")

    # stop on button press
    if button_stop.is_pressed:
        process.terminate()
        process.wait()
        process = None
        # go to the next state once the recording is stored
        print("Hashtag button pressed → Recording stopped → waiting for processing")
        return "waiting"

    return None