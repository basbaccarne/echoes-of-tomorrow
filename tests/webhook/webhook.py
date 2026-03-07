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
    print(f"I'm using the url:{url})")
    
    payload = {"chatInput": text}
    
    response = requests.post(url, json=payload, timeout=60)
    response.raise_for_status()
    
    print(f"Status code: {response.status_code}")
    
    # try JSON first, fall back to plain text
    try:
        data = response.json()
        return data.get("output") or data.get("text") or str(data)
    except Exception:
        return response.text


def print_menu():
    """Display the phone menu"""
    print("\n" + "="*60)
    print("KIES EEN TELEFOON / CHOOSE A PHONE:")
    print("="*60)
    print("1. Phone 1 - DE DIGITALE JEUGD (Digital Future)")
    print("2. Phone 2 - TERUG NAAR NATUUR (Nature-based)")
    print("3. Phone 3 - COLLECTIEF OPVOEDEN (Collective)")
    print("4. Phone 4 - GENETISCHE OPTIMALISATIE (Genetic)")
    print("5. Test all phones with same question")
    print("0. Exit")
    print("="*60)


def main():
    """Main interactive loop"""
    print("\n🎯 ECHOES OF TOMORROW - Interactive Chatbot")
    print("=" * 60)
    
    while True:
        print_menu()
        choice = input("\nEnter choice (0-5): ").strip()
        
        if choice == "0":
            print("\nGoodbye! 👋")
            break
        
        elif choice in ["1", "2", "3", "4"]:
            # Single phone mode
            phone_map = {"1": "phone_1", "2": "phone_2", "3": "phone_3", "4": "phone_4"}
            phone_id = phone_map[choice]
            future_num = PHONE_CONFIG[phone_id]
            
            question = input("\nEnter your question (Stel je vraag): ").strip()
            
            if not question:
                print("⚠️  Please enter a question!")
                continue
            
            print(f"\n{'='*60}")
            print(f"Phone: {phone_id} (Future {future_num})")
            print(f"Question: {question}")
            print(f"{'='*60}")
            
            result = send_to_n8n(question, phone_id=phone_id)
            print(f"\nAgent response:\n{result}")
        
        elif choice == "5":
            # Test all phones
            question = input("\nEnter your question (Stel je vraag): ").strip()
            
            if not question:
                print("⚠️  Please enter a question!")
                continue
            
            print(f"\nTesting all 4 phones with question: {question}\n")
            
            for phone_id in ["phone_1", "phone_2", "phone_3", "phone_4"]:
                future_num = PHONE_CONFIG[phone_id]
                print(f"\n{'='*60}")
                print(f"Phone: {phone_id} (Future {future_num})")
                print(f"{'='*60}")
                
                result = send_to_n8n(question, phone_id=phone_id)
                print(f"Response: {result}")
        
        else:
            print("❌ Invalid choice! Please enter 0-5.")


if __name__ == "__main__":
    main()
