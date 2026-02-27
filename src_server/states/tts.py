import time
import datetime

def run():
    
    # get the reponse text from audio_files/response_0.txt (where 0 is the booth id, to be set in config.yaml)
    # transform txt to WAV file
    # store in audio_files/response_0.wav (where 0 is the booth id, to be set in config.yaml)
    
    time.sleep(5)  # simulate processing time
        
    print(f"\n⏱️  [{(datetime.datetime.now().strftime('%H:%M:%S'))}]") 
    print("🔊 Audio file ready.")
    print("Sending this back to the pi...")

    return "sending"