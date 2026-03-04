import subprocess
import os
from hardware import button_stop, button_horn
from states.shared import SharedState
import time

process = None
process_start_time = None
DEBOUNCE = 0.3
MAX_RECORDING_SECONDS = 20  # Auto-stop recording after this duration

def run():
    global process, process_start_time

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
        process_start_time = time.time()

    # horn put back → abort to idle
    if button_horn.is_pressed:
        process.terminate()
        process.wait()
        process = None
        process_start_time = None
        print("📵   Horn replaced during recording — returning to idle.")
        return "idle"

    # stop recording on hashtag button press
    if button_stop.is_pressed:
        process.terminate()
        process.wait()
        process = None
        process_start_time = None
        print("🛑   Hashtag button pressed → Recording stopped.")
        return "waiting"

    # auto-stop after MAX_RECORDING_SECONDS
    if process_start_time and (time.time() - process_start_time) >= MAX_RECORDING_SECONDS:
        process.terminate()
        process.wait()
        process = None
        process_start_time = None
        print(f"⏱️   Max recording time ({MAX_RECORDING_SECONDS}s) reached → Recording stopped.")
        return "waiting"

    return None