import requests

def send_to_n8n(text):
    #Tims hook
    #url = "http://localhost:5678/webhook/dae1d29b-5725-47fc-a68b-cba9d669a981/chat"
    
    #local test
    # url = "http://localhost:5678/webhook/4a373672-3af4-4cae-a776-67fe0c43a3e6/chat"
    
    #SSH test
    url = "http://localhost:5678/webhook/70f7a510-eec9-410d-b623-de8bc323273a/chat"
    
    payload = {"chatInput": text}
    
    response = requests.post(url, json=payload, timeout=60)  # wait up to 60s
    response.raise_for_status()
    
    print(f"Status code: {response.status_code}")
    
    # try JSON first, fall back to plain text
    try:
        data = response.json()
        return data.get("output") or data.get("text") or (data.get("message") or {}).get("content") or str(data)
    except Exception:
        return response.text

question = "What does parenting look like in the year 2080? Answer in three sentences."
print(f"Sending question to n8n: {question}")
result = send_to_n8n(question)
print(f"Agent response: {result}")