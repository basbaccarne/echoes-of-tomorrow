from http.server import HTTPServer, BaseHTTPRequestHandler
import os
import yaml
from pathlib import Path
import socket

BASE_DIR = Path(__file__).resolve().parent.parent
CONFIG_PATH = BASE_DIR / "config.yaml"

with open(CONFIG_PATH, "r") as f:
    config = yaml.safe_load(f)

SAVE_DIR = config["audio_path"]
os.makedirs(SAVE_DIR, exist_ok=True)

file_received = False  # ← state flag


class UploadHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        global file_received

        filename = self.headers.get("X-Filename", "recording.wav")
        length = int(self.headers["Content-Length"])
        data = self.rfile.read(length)

        filepath = os.path.join(SAVE_DIR, filename)
        with open(filepath, "wb") as f:
            f.write(data)

        print(f"\nReceived: {filepath}")
        # self.send_response(200)
        # self.end_headers()
        # self.wfile.write(b"OK")

        # print("Audio file received → processing (speech to text)")
        file_received = True  # ← set flag


def run():
    global file_received

    PORT = 8765
    server = HTTPServer(("0.0.0.0", PORT), UploadHandler)
    server.timeout = 0.1  # ← IMPORTANT
    print("--------------------------------------------")
    print(f"Server IP: {socket.gethostbyname(socket.gethostname())}")
    print(f"Is there anybody out there? I'm listening on port {PORT}...")

    while not file_received:
        server.handle_request()  # ← non-blocking

    file_received = False  # reset for next time
    server.server_close()
    return "stt"