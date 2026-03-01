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
import yaml
from hardware import button_horn
from states.shared import SharedState

# ── Config ───────────────────────────────────────────────────────────────────
base_dir  = "/home/pi/echoes-of-tomorrow/src"
audio_dir = "/home/pi/echoes-of-tomorrow/audio_files"

with open(os.path.join(base_dir, "config.yaml"), "r") as f:
    config = yaml.safe_load(f)

SERVER_IP    = config["serverip"]
UNIQUE_PORTS = config["unique_port"]

# ── Module-level state ───────────────────────────────────────────────────────
_response_path  = None   # set by the HTTP handler when response arrives
_server         = None   # HTTPServer instance
_ready          = False  # horn debounce flag
_audio_process  = None   # current aplay subprocess
_played_welcome = False  # ensure welcome snippet plays first
_random_queue   = []     # shuffled queue of random snippets


def run():
    global _response_path, _server, _ready
    global _audio_process, _played_welcome, _random_queue

    booth_id = SharedState.booth_id
    port     = UNIQUE_PORTS.get(booth_id, 8765)

    # ── Step 1: upload and start listener (runs once) ────────────────────────
    if _server is None and _response_path is None:
        audio_path = os.path.join(audio_dir, f"question_{booth_id}.wav")
        print(f"\n📤   Uploading question to {SERVER_IP}:{port} ...")
        _upload(audio_path, SERVER_IP, port)

        print(f"👂   Listening for response on port {port} ...")
        _server = _start_listener(port, booth_id)

        # Build shuffled queue of random snippets
        _random_queue = random.sample(range(1, 11), 10)
        _played_welcome = False
        _audio_process  = None

        time.sleep(0.3)  # horn debounce
        _ready = True

    if not _ready:
        return None

    # ── Step 2: abort if horn is replaced ────────────────────────────────────
    if button_horn.is_pressed:
        print("📵   Horn replaced during waiting — returning to idle.")
        _stop_audio()
        _cleanup()
        return "idle"

    # ── Step 3: check if current snippet finished ────────────────────────────
    if _audio_process is not None and _audio_process.poll() is None:
        # Still playing — check for response but don't interrupt
        if _response_path is not None:
            # Wait for current snippet to finish before transitioning
            # (feels more natural than cutting off mid-sentence)
            pass
        return None

    # ── Step 4: snippet finished (or none started yet) ───────────────────────

    # If response arrived, transition now (between snippets = clean cutoff)
    if _response_path is not None:
        print(f"✅   Response received: {_response_path}")
        _stop_audio()
        _cleanup()
        return "response"

    # ── Step 5: play next snippet ─────────────────────────────────────────────
    if not _played_welcome:
        next_file = os.path.join(audio_dir, f"waiting_{booth_id}.wav")
        _played_welcome = True
        print(f"🎵   Playing waiting intro ...")
    elif _random_queue:
        idx = _random_queue.pop(0)
        next_file = os.path.join(audio_dir, f"waiting_random_{booth_id}_{idx}.wav")
        print(f"🎵   Playing ambient snippet {idx} ...")
        # Reshuffle when queue is exhausted
        if not _random_queue:
            _random_queue = random.sample(range(1, 11), 10)
    else:
        return None  # shouldn't happen but guard anyway

    if os.path.exists(next_file):
        _audio_process = subprocess.Popen([
            "aplay", "-D", "plughw:0,0", next_file
        ])
    else:
        print(f"   ⚠️  Audio file not found: {next_file}")

    return None


# ── Helpers ──────────────────────────────────────────────────────────────────

def _stop_audio():
    global _audio_process
    if _audio_process and _audio_process.poll() is None:
        _audio_process.terminate()
        _audio_process.wait()
    _audio_process = None


def _upload(audio_path, server_ip, port):
    """POST the question wav to the server."""
    url      = f"http://{server_ip}:{port}"
    filename = os.path.basename(audio_path)
    try:
        with open(audio_path, "rb") as f:
            data = f.read()
        req = urllib.request.Request(url, data=data, method="POST")
        req.add_header("X-Filename", filename)
        req.add_header("Content-Length", str(len(data)))
        with urllib.request.urlopen(req, timeout=10) as resp:
            print(f"   Server responded: {resp.read().decode()}")
    except Exception as e:
        print(f"   Upload error: {e}")


def _start_listener(port, booth_id):
    """Start HTTP listener in a background thread for the server to POST response to."""

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

            _response_path = save_path  # signal the main loop

        def log_message(self, format, *args):
            pass  # suppress default HTTP log noise

    server = HTTPServer(("0.0.0.0", port), ResponseHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server


def _cleanup():
    """Shut down the listener and reset all module state."""
    global _response_path, _server, _ready, _played_welcome, _random_queue
    if _server:
        _server.shutdown()
        _server = None
    _response_path  = None
    _ready          = False
    _played_welcome = False
    _random_queue   = []