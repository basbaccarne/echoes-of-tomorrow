# send file from pi

import requests
import os

def send_wav(filepath, server_ip, port=8765):
    filename = os.path.basename(filepath)
    with open(filepath, "rb") as f:
        response = requests.post(
            f"http://{server_ip}:{port}/upload",
            data=f,
            headers={
                "Content-Type": "audio/wav",
                "X-Filename": filename
            }
        )
    if response.ok:
        print("File sent successfully")
    else:
        print(f"Upload failed: {response.status_code}")

# Call after recording finishes
send_wav("/home/pi/recordings/output.wav", server_ip="192.168.1.xxx")