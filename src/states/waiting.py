# waiting.py
# Uploads the recorded question to the server, then opens a listener on the
# booth's unique port and waits for the server to POST the response audio back.
# Falls back to idle if the horn is replaced at any point.

import os
import time
import threading
import urllib.request
from http.server import HTTPServer, BaseHTTPRequestHandler
import yaml
from hardware import button_horn
from states.shared import SharedState

# ── Load config ──────────────────────────────────────────────────────────────
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

with open(os.path.join(base_dir, "/echoes-of-tomorrow/src/config.yaml"), "r") as f:
    config = yaml.safe_load(f)

SERVER_IP    = config["serverip"]
UNIQUE_PORTS = config["unique_port"]

# ── Module-level state ───────────────────────────────────────────────────────
_response_path = None   # set by the HTTP handler when response arrives
_server        = None   # HTTPServer instance, kept so we can shut it down
_ready         = False  # horn debounce flag


def run():
    global _response_path, _server, _ready

    booth_id   = SharedState.booth_id
    port       = UNIQUE_PORTS.get(booth_id, 8765)
    audio_path = os.path.join(base_dir, "audio_files", f"question_{booth_id}.wav")

    # ── Step 1: upload question and start listener (runs once) ───────────────
    if _server is None and _response_path is None:
        print(f"\n📤   Uploading question to {SERVER_IP}:{port} ...")
        _upload(audio_path, SERVER_IP, port)

        print(f"👂   Listening for response on port {port} ...")
        _server = _start_listener(port)
        time.sleep(0.3)   # horn debounce
        _ready = True

    if not _ready:
        return None

    # ── Step 2: abort if horn is replaced ────────────────────────────────────
    if button_horn.is_pressed:
        print("📵   Horn replaced during waiting — returning to idle.")
        _cleanup()
        return "idle"

    # ── Step 3: response received → move to response state ───────────────────
    if _response_path is not None:
        print(f"✅   Response received: {_response_path}")
        SharedState.response_path = _response_path
        _cleanup()
        return "response"

    return None


# ── Helpers ──────────────────────────────────────────────────────────────────

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


def _start_listener(port):
    """Start a one-shot HTTP server in a background thread."""

    class ResponseHandler(BaseHTTPRequestHandler):
        def do_POST(self):
            global _response_path
            filename = self.headers.get("X-Filename", "response.wav")
            length   = int(self.headers["Content-Length"])
            data     = self.rfile.read(length)

            save_path = os.path.join(base_dir, "audio_files", filename)
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
    """Shut down the listener and reset module state."""
    global _response_path, _server, _ready
    if _server:
        _server.shutdown()
        _server = None
    _response_path = None
    _ready = False