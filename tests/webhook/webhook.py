import requests

def send_to_n8n(text, booth_id):
    url = "http://localhost:5678/webhook/dae1d29b-5725-47fc-a68b-cba9d669a981/chat"
    
    payload = {
        "message": text,
        "booth_id": booth_id
    }
    
    response = requests.post(url, json=payload)
    response.raise_for_status()
    
    print(f"✓ Sent to n8n (status {response.status_code})")
    return response.json()

send_to_n8n("dit is een vraag", 0):