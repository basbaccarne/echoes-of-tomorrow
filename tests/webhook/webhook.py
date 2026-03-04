import requests

def send_to_n8n(text):
    url = "http://localhost:5678/webhook/dae1d29b-5725-47fc-a68b-cba9d669a981/chat"
    
    payload = {"chatInput": text}
    
    response = requests.post(url, json=payload, timeout=60)  # wait up to 60s
    response.raise_for_status()
    
    print(f"Status code: {response.status_code}")
    
    # try JSON first, fall back to plain text
    try:
        data = response.json()
        # the agent reply is usually in one of these fields:
        return data.get("output") or data.get("text") or data.get("message") or str(data)
    except Exception:
        return response.text

result = send_to_n8n("This is a test transcript.")
print(f"Agent response: {result}")