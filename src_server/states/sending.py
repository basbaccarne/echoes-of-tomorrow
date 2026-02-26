import time
import datetime

def run():
    time.sleep(5)  # simulate processing time
    print(f"\n⏱️  [{(datetime.datetime.now().strftime('%H:%M:%S'))}]") 
    print("📤 Audiofile sent back succesfully.")

    return "waiting_for_receive"