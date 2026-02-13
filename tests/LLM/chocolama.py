import requests
import time

def chat(text):
    print(f"\n{'='*50}")
    print(f"User prompt: {text}")
    print(f"{'='*50}")
    
    # Timer: API call
    t1 = time.time()
    print("📤 Sending request to Ollama...")
    
    response = requests.post('http://localhost:11434/api/generate',
        json={
            "model": "llama3.2:3b",
            "prompt": f"Antwoord in het Nederlands: {text}",
            "stream": False
        })
    
    t2 = time.time()
    print(f"⏱️  API response received in {t2-t1:.2f}s")
    
    # Parse response
    t3 = time.time()
    data = response.json()
    answer = data['response']
    t4 = time.time()
    print(f"⏱️  JSON parsing took {t4-t3:.3f}s")
    
    # Total timing
    total_time = t4 - t1
    print(f"\n⏱️  Total time: {total_time:.2f}s")
    print(f"{'='*50}")
    
    return answer

# Test
result = chat("Welke boeken raad je aan over Belgische geschiedenis?")
print(f"\n🤖 Ollama response:\n{result}")
print(f"{'='*50}\n")