import requests

def send_to_n8n(text):
    url = "http://localhost:5678/webhook/dae1d29b-5725-47fc-a68b-cba9d669a981/chat"
    
    response = requests.post(url, data=text, headers={"Content-Type": "text/plain"})
    response.raise_for_status()
    
    print(f"✓ Sent to n8n (status {response.status_code})")
    return response.text  # also .text instead of .json() since response may be plain text too

result = send_to_n8n(transcript)
print(f"n8n response: {result}")