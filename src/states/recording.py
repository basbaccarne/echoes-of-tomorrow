import subprocess
import os
from hardware import button_stop, button_horn
from states.shared import SharedState
import time
import yaml



# ── Config ───────────────────────────────────────────────────────────────────
base_dir  = "/home/pi/echoes-of-tomorrow/src"
audio_dir = "/home/pi/echoes-of-tomorrow/audio_files"

with open(os.path.join(base_dir, "config.yaml"), "r") as f:
    config = yaml.safe_load(f)

AUDIO_CARD = config.get("audio_card", "plughw:0,0")
DEBOUNCE = 0.3  # seconds — adjust if needed
MAX_RECORDING_SECONDS = 20

process = None
playback_process = None  # ← new: tracks the static sound playback

STATIC_SOUND_PATH = os.path.join(audio_dir, "static.wav")  # ← point to your static file


def _stop_all():
    """Terminate both recording and playback processes."""
    global process, playback_process
    for p in (process, playback_process):
        if p is not None:
            p.terminate()
            p.wait()
    process = None
    playback_process = None


def run():
    global process, playback_process

    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    audio_path = os.path.join(base_dir, "audio_files", f"question_{SharedState.booth_id}.wav")

    # start recording + static playback if not already running
    if process is None:
        time.sleep(DEBOUNCE)
        print(f"\n🎤   Recording the question in file {audio_path}")
        print("Press the #️⃣   button to stop the recording.")
        print("ALSA message:")
        process = subprocess.Popen([
            "arecord",
            "-D", AUDIO_CARD,
            "-f", "cd",
            "-t", "wav",
            audio_path
        ])

        # ── Play static sound on loop alongside recording ──────────────────
        if os.path.exists(STATIC_SOUND_PATH):
            playback_process = subprocess.Popen([
                "aplay",
                "-D", AUDIO_CARD,
                "--buffer-time=50000",  # low latency
                STATIC_SOUND_PATH
                # Note: aplay doesn't loop natively; see tip below for looping
            ])

        SharedState.recording_start_time = time.time()

    # horn put back → abort to idle
    if button_horn.is_pressed:
        _stop_all()
        print("📵   Horn replaced during recording — returning to idle.")
        return "idle"

    # stop recording on hashtag button press
    if button_stop.is_pressed:
        _stop_all()
        print("🛑   Hashtag button pressed → Recording stopped.")
        return "waiting"

    # auto-stop after MAX_RECORDING_SECONDS
    if (time.time() - SharedState.recording_start_time) >= MAX_RECORDING_SECONDS:
        _stop_all()
        print(f"⏱️   Max recording time ({MAX_RECORDING_SECONDS}s) reached → Recording stopped.")
        return "waiting"

    return None