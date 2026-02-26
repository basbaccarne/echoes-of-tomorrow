import time
import datetime

def run():
    time.sleep(5)  # simulate processing time
    print(f"\n⏱️  [{(datetime.datetime.now().strftime('%H:%M:%S'))}]") 
    print("🎙️  I've transformed the wav to text.")
    print(f"📜  Here's the transcript: {'Hello world, this is a test.'}")
    print("\nSending transcript to n8n for further processing...")

    return "n8n"