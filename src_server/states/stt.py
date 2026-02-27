import time
import datetime

def run():
    
    # get the WAV from audio_files/question_0.wav (where 0 is the booth id, to be set in config.yaml)
    # transform to WAV file to text
    # store in audio_files/question_0.txt (where 0 is the booth id, to be set in config.yaml)
    
    time.sleep(5)  # simulate processing time
    response  = "this the the spoken word i tried to get from the audio, but it can be anything, it's just a placeholder for now"
    
    print(f"\n⏱️  [{(datetime.datetime.now().strftime('%H:%M:%S'))}]") 
    print("🎙️  I've transformed the wav to text.")
    print(f"📜  Here's the transcript: {response}")
    print("\nSending transcript to n8n for further processing...")

    return "n8n"