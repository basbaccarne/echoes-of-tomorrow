# script that waits for the audio file to be sent from the client, then saves it and moves to the next state (STT)

# Libraries
from http.server import HTTPServer, BaseHTTPRequestHandler
import os
import yaml
from pathlib import Path
import socket
import datetime
from states.shared import SharedState

# Directories
BASE_DIR = Path(__file__).resolve().parent.parent
CONFIG_PATH = BASE_DIR / "config.yaml"

# Settings
with open(CONFIG_PATH, "r") as f:
    config = yaml.safe_load(f)
SAVE_DIR = config["audio_path"]
os.makedirs(SAVE_DIR, exist_ok=True)

# State variable
file_received = False

class UploadHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        global file_received
        filename = self.headers.get("X-Filename", f"recording_{SharedState.booth_id}.wav")
        length = int(self.headers["Content-Length"])
        data = self.rfile.read(length)

        filepath = os.path.join(SAVE_DIR, filename)
        with open(filepath, "wb") as f:
            f.write(data)

        print(f"\n⏱️  [{(datetime.datetime.now().strftime('%H:%M:%S'))}]")    
        print(f"📩 Whoop, I received: {filepath}")        
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")

        file_received = True

def run():
    global file_received

    # Start server
    PORT = config["port"]
    server = HTTPServer(("0.0.0.0", PORT), UploadHandler)
    server.timeout = 0.1 
    print("--------------------------------------------")
    print(f"📍 Server IP: {socket.gethostbyname(socket.gethostname())}")
    print(f"🎯 I'm the python handler for booth {SharedState.booth_id}, so I'm listening on port {PORT} ...")
    print(f"👂 Is there anybody out there?")

    # Hold the line until the file is received
    while not file_received:
        server.handle_request()

    # Clean up and move to next state
    file_received = False 
    server.server_close()
    return "stt"