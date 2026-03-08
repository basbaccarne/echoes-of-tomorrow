import time 

class SharedState:
    booth_id = 0
    sender_ip = None
    whisper_model = None
    piper_voice = None
    session_start = time.time()