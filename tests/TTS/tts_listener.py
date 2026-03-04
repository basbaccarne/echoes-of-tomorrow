from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
import os
from pathlib import Path
import wave
from piper import PiperVoice, SynthesisConfig

 #assuming we run this from CL when in TTS folder
watch_folder = os.getcwd() + "\\text_in"
write_folder = os.getcwd() + "\\audio_out"
voice = os.getcwd() + "\\voices\\nl_NL-mls_5809-low.onnx"

def wait_until_stable(path, check_interval=0.5, stable_time=1.5, timeout=30):
    """
    Wait until file size stops changing.

    check_interval: how often to check size (seconds)
    stable_time: how long size must remain unchanged
    timeout: max wait time
    """
    start_time = time.time()
    last_size = -1
    stable_since = None

    while True:
        if not os.path.exists(path):
            return False  # file disappeared

        current_size = os.path.getsize(path)

        if current_size == last_size:
            if stable_since is None:
                stable_since = time.time()

            if time.time() - stable_since >= stable_time:
                return True  # file is stable
        else:
            stable_since = None

        last_size = current_size

        if time.time() - start_time > timeout:
            print(f"Timeout waiting for file to stabilize: {path}")
            return False

        time.sleep(check_interval)


class TTSHandler(FileSystemEventHandler):
    def __init__(self, speed, voice, outfolder):
        super().__init__()
        self.speed = speed
        self.voice = voice
        self.outfolder = outfolder
    
    def on_created(self, event):
        if event.is_directory:
            return

        if not event.src_path.lower().endswith(".txt"):
            return

        print(f"New file detected: {event.src_path}")

        if not wait_until_stable(event.src_path):
            print("File not stable. Skipping.")
            return

        print("File is stable. Processing...")

        self.process_text(event.src_path)

    def process_text(self, path_in):
       
        speed_inv = 1/self.speed

        txtinput = ""

        with open(path_in, 'r') as file:
            txtinput = file.read().replace('\n', '')

        print(f"🔊 Speaking (speed {speed_inv}x): {txtinput[:50]}...")
        t1 = time.time()

        syn_config = SynthesisConfig(
            volume=0.5,  # half as loud
            length_scale=speed_inv,  # speed_inv times as slow
            noise_scale=1.0,  # more audio variation
            noise_w_scale=1.0,  # more speaking variation
            normalize_audio=False, # use raw audio from voice
        )

        # Build output file path
        filename = os.path.splitext(os.path.basename(path_in))[0]
        output_path = os.path.join(self.outfolder, f"{filename}.wav")

        with wave.open(output_path, "wb") as wav_file:
            self.voice.synthesize_wav(txtinput, wav_file, syn_config= syn_config)

        t2 = time.time()
        print(f"⏱️  Generated in {t2-t1:.2f}s")

        return t2-t1

def start_tts_listener(speed, voice, folder_in, folder_out):
    v = PiperVoice.load(voice)
    handler = TTSHandler(speed,v,folder_out)

    observer = Observer()
    observer.schedule(handler, folder_in, recursive=False)
    observer.start()

    print("TTS listener running...")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()

if __name__ == "__main__":
    start_tts_listener(1.0, voice, watch_folder, write_folder)