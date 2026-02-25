from http.server import HTTPServer, BaseHTTPRequestHandler
import os

SAVE_DIR = r"C:\audio_files"
os.makedirs(SAVE_DIR, exist_ok=True)

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
    
def run():
    server = HTTPServer(("0.0.0.0", 8765), UploadHandler)
    print("Listening on port 8765...")
    server.serve_forever()
    
    # after release 
    if false:
        # go to the next state
        print("Audio file received → processing")
        return "waiting_for_receive"

    return None