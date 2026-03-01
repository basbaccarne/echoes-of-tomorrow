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
send_wav("/home/pi/echoes-of-tomorrow/tests/http_send_receive/sample_question.wav", server_ip="10.63.235.157")