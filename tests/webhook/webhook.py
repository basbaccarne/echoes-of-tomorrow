import requests

# Configuration: Map phone identifiers to future scenarios
PHONE_CONFIG = {
    "phone_1": 1,  # Phone 1 talks about "DE DIGITALE JEUGD"
    "phone_2": 2,  # Phone 2 talks about "TERUG NAAR NATUUR"
    "phone_3": 3,  # Phone 3 talks about "COLLECTIEF OPVOEDEN"
    "phone_4": 4,  # Phone 4 talks about "GENETISCHE OPTIMALISATIE"
}

# Base webhook URL (the same for all phones)
BASE_WEBHOOK_URL = "http://localhost:5678/webhook/ab3e469b-5e4c-4605-b34a-6bde15477a11"

def send_to_n8n(text, phone_id="phone_1"):
    """
    Send text to n8n chatbot with dynamic future scenario based on phone.
    
    Args:
        text (str): The user's question
        phone_id (str): Which phone is making the request (phone_1, phone_2, etc.)
    
    Returns:
        str: The chatbot's response
    """
    
    # Get the future number for this phone
    future = PHONE_CONFIG.get(phone_id, 1)  # Default to future 1 if phone not found
    
    # Build the URL with the future parameter
    url = f"{BASE_WEBHOOK_URL}?future={future}"
    
    payload = {"chatInput": text}
    
    response = requests.post(url, json=payload, timeout=60)
    response.raise_for_status()
    
    print(f"Status code: {response.status_code}")
    print(f"Phone: {phone_id}, Future: {future}")
    
    # try JSON first, fall back to plain text
    try:
        data = response.json()
        return data.get("output") or data.get("text") or str(data)
    except Exception:
        return response.text

# Test with different phones
if __name__ == "__main__":
    question = "Hoe ziet een internaat er uit in 2030?"
    
    # Test all 4 phones
    for phone_id in ["phone_1", "phone_2", "phone_3", "phone_4"]:
        print(f"\n{'='*60}")
        print(f"Sending question from {phone_id}: {question}")
        print(f"{'='*60}")
        result = send_to_n8n(question, phone_id=phone_id)
        print(f"Agent response: {result}")
