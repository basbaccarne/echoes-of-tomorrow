import time
import subprocess
import os

from hardware import button_stop, button_horn
from states.shared import SharedState, AUDIO_CARD

# ── Config ────────────────────────────────────────────────────────────────────
audio_dir = "/home/pi/echoes-of-tomorrow/audio_files"
DEBOUNCE = 0.3
MAX_RECORDING_SECONDS = 20

_process = None


def _stop_recording():
    """Terminate the recording process and reset module state."""
    global _process
    if _process is not None:
        _process.terminate()
        _process.wait()
        _process = None


def run():
    global _process

    audio_path = os.path.join(audio_dir, f"question_{SharedState.booth_id}.wav")

    # ── Start recording if not already running ────────────────────────────────
    if _process is None:
        time.sleep(DEBOUNCE)
        print(f"\n🎤  Recording to {audio_path}")
        print("Press the #️⃣  button to stop.")
        _process = subprocess.Popen(
            ["arecord", "-D", AUDIO_CARD, "-f", "cd", "-t", "wav", audio_path],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        SharedState.recording_start_time = time.time()

    # ── Horn replaced → abort to idle ────────────────────────────────────────
    if button_horn.is_pressed:
        _stop_recording()
        print("📵  Horn replaced during recording — returning to idle.")
        return "idle"

    # ── Stop button → proceed to waiting ─────────────────────────────────────
    if button_stop.is_pressed:
        _stop_recording()
        print("🛑  Stop button pressed — recording stopped.")
        return "waiting"

    # ── Auto-stop after MAX_RECORDING_SECONDS ─────────────────────────────────
    if (time.time() - SharedState.recording_start_time) >= MAX_RECORDING_SECONDS:
        _stop_recording()
        print(f"⏱️  Max recording time ({MAX_RECORDING_SECONDS}s) reached — recording stopped.")
        return "waiting"

    return None