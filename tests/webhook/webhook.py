import requests

def send_to_n8n(text):
    url = "http://localhost:5678/webhook/dae1d29b-5725-47fc-a68b-cba9d669a981/chat"
    
    payload = {"chatInput": text}
    
    response = requests.post(url, json=payload)
    
    print(f"Status code: {response.status_code}")
    print(f"Response: {response.text}")
    
    response.raise_for_status()
    return response.text

result = send_to_n8n("This is a test transcript.")
print(f"n8n response: {result}")