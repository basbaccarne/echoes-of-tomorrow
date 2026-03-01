import subprocess
import os
from hardware import button_stop, button_horn
from states.shared import SharedState

process = None
DEBOUNCE = 0.3

def run():
    global process

    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    audio_path = os.path.join(base_dir, "audio_files", f"question_{SharedState.booth_id}.wav")

    # start recording if not already
    if process is None:
        time.sleep(DEBOUNCE)
        print(f"\n🎤   Recording the question in file {audio_path}")
        print("Press the #️⃣   button to stop the recording.")
        print("ALSA message:")
        process = subprocess.Popen([
            "arecord",
            "-D", "plughw:0,0",
            "-f", "cd",
            "-t", "wav",
            audio_path
        ])

    # horn put back → abort to idle
    if button_horn.is_pressed:
        process.terminate()
        process.wait()
        process = None
        print("📵   Horn replaced during recording — returning to idle.")
        return "idle"
    
    # stop recording on hashtag button press
    if button_stop.is_pressed:
        process.terminate()
        process.wait()
        process = None
        # go to the next state once the recording is stored
        print("🛑   Hashtag button pressed → Recording stopped.")
        return "waiting"

    return None