import os
import subprocess

from states.shared import SharedState, AUDIO_CARD

# ── Config ────────────────────────────────────────────────────────────────────
audio_dir = "/home/pi/echoes-of-tomorrow/audio_files"


def _play(path: str) -> bool:
    """Play a wav file, return False on error."""
    print(f"\n⏳  Playing {os.path.basename(path)}")
    try:
        subprocess.run(
            ["aplay", "-D", AUDIO_CARD, path],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        return True
    except subprocess.CalledProcessError as e:
        print(f"[response] aplay error: {e}")
        return False


def run():
    booth_id                  = SharedState.booth_id
    fixed_start_path          = os.path.join(audio_dir, f"fixed_response_start_{booth_id}.wav")
    response_path             = os.path.join(audio_dir, f"response_{booth_id}.wav")
    response_0_path           = os.path.join(audio_dir, f"response_0_{booth_id}.wav")

    print(f"\n⏳  Checking for response file at {response_path}")

    if not os.path.exists(response_path):
        print("[response] No response file found — returning to idle.")
        return "idle"

    print(f"\n⏳  Playing response for booth {booth_id}...")

    # 1. Play fixed intro (optional — skip if missing)
    if os.path.exists(fixed_start_path):
        if not _play(fixed_start_path):
            return "idle"
    else:
        print(f"⚠️  No fixed start file at {fixed_start_path} — skipping.")

    # 2. Play main response (required)
    if not _play(response_path):
        return "idle"

    # 3. Play follow-up response (optional — skip if missing)
    if os.path.exists(response_0_path):
        if not _play(response_0_path):
            return "idle"
    else:
        print(f"⚠️  No follow-up file at {response_0_path} — skipping.")

    print("\n--------------------------------")
    print(f"[response] ✅  Done — returning to idle.")
    print(f"[response] Booth ID remains: {booth_id}")
    print("👂  Waiting for horn to be picked up...")

    return "idle"