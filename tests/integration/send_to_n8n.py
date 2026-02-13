import requests
import json
import time

# Lokale n8n webhook URL
N8N_WEBHOOK_URL = "http://localhost:5678/webhook-test/033ff2a7-95e6-44e3-bdaf-e62d1f6687c2"

def send_test_to_n8n():
    """Stuur test data naar n8n"""
    print("📤 Sending test data to n8n...")
    
    payload = {
        "text": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
        "language": "nl",
        "transcription_time": 1.23,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
    }
    
    print(f"\nPayload:")
    print(json.dumps(payload, indent=2))
    print(f"\nSending to: {N8N_WEBHOOK_URL}")
    
    try:
        response = requests.post(
            N8N_WEBHOOK_URL,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=5
        )
        
        print(f"\n✓ Status code: {response.status_code}")
        
        if response.status_code == 200:
            print("✓ Successfully sent to n8n!")
            print(f"\nn8n response:")
            print(json.dumps(response.json(), indent=2))
        else:
            print(f"❌ n8n returned error")
            print(f"Response: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print(f"\n❌ Could not connect to n8n at {N8N_WEBHOOK_URL}")
        print(f"   Is n8n running?")
        print(f"   Try: curl {N8N_WEBHOOK_URL}")
    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    print("="*50)
    print("n8n Webhook Test")
    print("="*50)
    send_test_to_n8n()
    print("="*50)