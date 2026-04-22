# waiting.py
# Uploads the recorded question to the server, then opens a listener on the
# booth's unique port and waits for the server to POST the response audio back.
# While waiting, plays a welcome snippet followed by random ambient audio files.
# Interrupts cleanly between snippets when a response arrives or horn is replaced.

import os
import time
import random
import threading
import subprocess
import urllib.request
from http.server import HTTPServer, BaseHTTPRequestHandler

from hardware import button_horn
from states.shared import SharedState, AUDIO_CARD, SERVER_IP, UNIQUE_PORTS

# ── Config ────────────────────────────────────────────────────────────────────
audio_dir = "/home/pi/echoes-of-tomorrow/audio_files"

# ── Module-level state ────────────────────────────────────────────────────────
_response_path  = None
_server         = None
_ready          = False
_audio_process  = None
_played_welcome = False
_random_queue   = []


def run():
    
    print(f"[DEBUG] trigger_time = {SharedState.idle_trigger_time}")
    print(f"[DEBUG] now = {time.time()}")
    print(f"[DEBUG] diff = {time.time() - SharedState.idle_trigger_time if SharedState.idle_trigger_time else None}")
    
    global _response_path, _server, _ready
    global _audio_process, _played_welcome, _random_queue

    booth_id = SharedState.booth_id
    port     = UNIQUE_PORTS.get(booth_id, 8765)

    # ── Step 1: start welcome audio, upload + listen in background ───────────
    if _server is None and _response_path is None and not _ready:
        audio_path    = os.path.join(audio_dir, f"question_{booth_id}.wav")
        welcome_file  = os.path.join(audio_dir, f"waiting_{booth_id}.wav")
        _random_queue = [1, 2, 3, 4, 5, 6, 7]
        _played_welcome = True

        # ── Clear any stale response file from a previous session ────────────
        stale_response = os.path.join(audio_dir, f"response_{booth_id}.wav")
        if os.path.exists(stale_response):
            os.remove(stale_response)
            print("🗑️  Cleared stale response file.")

        if os.path.exists(welcome_file):
            print("🎵  Playing waiting intro...")
            _audio_process = subprocess.Popen(
                ["aplay", "-D", AUDIO_CARD, welcome_file],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
        else:
            print(f"⚠️  Welcome audio not found: {welcome_file}")

        def _upload_and_listen():
            global _server
            print(f"\n📤  Uploading question to {SERVER_IP}:{port}...")
            _upload(audio_path, SERVER_IP, port)
            print(f"👂  Listening for response on port {port}...")
            _server = _start_listener(port, booth_id)

        threading.Thread(target=_upload_and_listen, daemon=True).start()

        time.sleep(0.3)
        _ready = True

    if not _ready:
        return None

    # ── Step 2: abort if horn is replaced ────────────────────────────────────
    if button_horn.is_pressed:
        print("📵  Horn replaced during waiting — returning to idle.")
        _stop_audio()
        _cleanup()
        return "idle"

    # ── Step 3: still playing — wait for snippet to finish ───────────────────
    if _audio_process is not None and _audio_process.poll() is None:
        return None

    # ── Step 4: snippet finished — transition if response arrived ────────────
    if _response_path is not None:
        print(f"✅  Response received: {_response_path}")
        _stop_audio()
        _cleanup()
        return "response"

    # ── Step 5: play next snippet ─────────────────────────────────────────────
    if not _played_welcome:
        next_file = os.path.join(audio_dir, f"waiting_{booth_id}.wav")
        _played_welcome = True
        print("🎵  Playing waiting intro...")
    elif _random_queue:
        idx = _random_queue.pop(0)
        next_file = os.path.join(audio_dir, f"waiting_random_0_{idx}.wav")
        print(f"🎵  Playing ambient snippet {idx}...")
        if not _random_queue:
            _random_queue = [1, 2, 3, 4, 5, 6, 7]
    else:
        return None

    if os.path.exists(next_file):
        _audio_process = subprocess.Popen(
            ["aplay", "-D", AUDIO_CARD, next_file],
        )
    else:
        print(f"⚠️  Audio file not found: {next_file}")

    return None


# ── Helpers ───────────────────────────────────────────────────────────────────

def _stop_audio():
    global _audio_process
    if _audio_process and _audio_process.poll() is None:
        _audio_process.terminate()
        _audio_process.wait()
    _audio_process = None


def _upload(audio_path, server_ip, port):
    """POST the question wav to the server."""
    url = f"http://{server_ip}:{port}"
    try:
        with open(audio_path, "rb") as f:
            data = f.read()
        req = urllib.request.Request(url, data=data, method="POST")
        req.add_header("X-Filename", os.path.basename(audio_path))
        req.add_header("Content-Length", str(len(data)))
        with urllib.request.urlopen(req, timeout=10) as resp:
            print(f"   Server responded: {resp.read().decode()}")
    except Exception as e:
        print(f"   Upload error: {e}")


def _start_listener(port, booth_id):
    """Start HTTP listener in background thread for server to POST response to."""

    class ResponseHandler(BaseHTTPRequestHandler):
        def do_POST(self):
            global _response_path
            length    = int(self.headers["Content-Length"])
            data      = self.rfile.read(length)
            save_path = os.path.join(audio_dir, f"response_{booth_id}.wav")
            with open(save_path, "wb") as f:
                f.write(data)
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"OK")
            _response_path = save_path

        def log_message(self, format, *args):
            pass

    server = HTTPServer(("0.0.0.0", port), ResponseHandler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return server


def _cleanup():
    """Shut down listener and reset all module state."""
    global _response_path, _server, _ready, _played_welcome, _random_queue
    if _server:
        _server.shutdown()
        _server = None
    _response_path  = None
    _ready          = False
    _played_welcome = False
    _random_queue   = []