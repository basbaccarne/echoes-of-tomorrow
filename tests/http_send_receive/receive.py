# receiver.py
# receiver.py
from http.server import HTTPServer, BaseHTTPRequestHandler
import os
import socket

SAVE_DIR = r"C:\audio_files"
os.makedirs(SAVE_DIR, exist_ok=True)


def get_local_ip():
    """Get the local IP address of this machine."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Doesn't need to be reachable, just used to get correct interface
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip


class UploadHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        filename = self.headers.get("X-Filename", "recording.wav")
        length = int(self.headers["Content-Length"])
        data = self.rfile.read(length)

        filepath = os.path.join(SAVE_DIR, filename)
        with open(filepath, "wb") as f:
            f.write(data)

        print(f"Received: {filepath}")
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")

        # Trigger your processing here
        process_audio(filepath)


def process_audio(filepath):
    print(f"Processing {filepath}...")
    # your processing logic here


if __name__ == "__main__":
    PORT = 8765
    local_ip = get_local_ip()

    server = HTTPServer(("0.0.0.0", PORT), UploadHandler)
    print(f"Listening on:")
    print(f"  → http://127.0.0.1:{PORT}")
    print(f"  → http://{local_ip}:{PORT}")
    server.serve_forever()