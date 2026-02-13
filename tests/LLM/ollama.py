import requests

print("Testing Ollama LLM...")

def chat_ollama(text):
    response = requests.post('http://localhost:11434/api/generate',
        json={
            "model": "llama3.2:3b", # or gemma2:2b (smaller)
            "prompt": f"Gebruiker zegt: {text}\n\nAntwoord in het Nederlands:",
            "stream": False
        })
    return response.json()['response']

# Test
print("Sending message to Ollama...")
answer = chat_ollama("Hoe zullen we kinderen opoveden in de toekomst?")
print("Received answer from Ollama:")
print(answer)   