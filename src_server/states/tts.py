import time
import datetime

def run():
    time.sleep(5)  # simulate processing time
    print(f"\n⏱️  [{(datetime.datetime.now().strftime('%H:%M:%S'))}]") 
    print("🔊 Audio file ready.")
    print("Sending this back to the pi...")

    return "sending"