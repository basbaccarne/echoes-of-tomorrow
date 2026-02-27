import time
import datetime

def run():
    
    # get the question text from audio_files/question_0.txt (where 0 is the booth id, to be set in config.yaml)
    # send a webhook to n8n
    # wait for the reponse (while loop)
    # store in audio_files/response_0.txt (where 0 is the booth id, to be set in config.yaml)

    
    time.sleep(5)  # simulate processing time
    response  = "this the reponse from n8n, but it can be anything, it's just a placeholder for now"

    print(f"\n⏱️  [{(datetime.datetime.now().strftime('%H:%M:%S'))}]") 
    print("🤖 Agent response ready.")
    print(f"💬 Here's the reply: {response}")
    print("\nSending this text to the text to speech module...")
    return "tts"