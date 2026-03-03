from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
import os
from pathlib import Path
import warnings
from faster_whisper import WhisperModel


# Onderdruk alle warnings
warnings.filterwarnings("ignore")
os.environ["OMP_NUM_THREADS"] = "4"

 #assuming we run this from CL when in STT folder
watch_folder = os.getcwd() + "\\audio_in"
write_folder = os.getcwd() + "\\text_out"

""" audios = []

for filename in os.listdir(folder):
    if filename.endswith(".wav"):
        filepath = os.path.join(folder, filename)
        print("Processing:", filepath)
        audios.append(filepath) """


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


class STTHandler(FileSystemEventHandler):
    def __init__(self, model, outfolder):
        super().__init__()
        self.model = model
        self.outfolder = outfolder
    
    def on_created(self, event):
        if event.is_directory:
            return

        if not event.src_path.lower().endswith(".wav"):
            return

        print(f"New file detected: {event.src_path}")

        if not wait_until_stable(event.src_path):
            print("File not stable. Skipping.")
            return

        print("File is stable. Processing...")

        self.process_audio(event.src_path)

    def process_audio(self, path_in):
        # Replace this with your STT logic
        print(f"Transcribing: {path_in}")
    
        transcribe_start = time.time()
        
        segments, info = self.model.transcribe(
            path_in,
            language="nl",
            beam_size=1,
            vad_filter=False,
            without_timestamps=True
        )
        
        print("Processing segments...")
        segments_list = list(segments)
        
        transcribe_time = time.time() - transcribe_start
        
        print(f"Found {len(segments_list)} segments")
        print(f"⏱️  Transcription took {transcribe_time:.2f} seconds")
        
        text = " ".join([segment.text for segment in segments_list])
        
        print("✓ Transcription complete!")

        # Build output file path
        filename = os.path.splitext(os.path.basename(path_in))[0]
        output_path = os.path.join(self.outfolder, f"{filename}.txt")

        with open(output_path, "x", encoding="utf-8") as f:
            f.write(text)

        return text

def start_stt_listener(folder_in, folder_out):
    print("Loading faster-whisper model...")
    load_start = time.time()
    model = WhisperModel(
        "small", 
        device="cpu",
        compute_type="int8"
    )
    load_time = time.time() - load_start
    print(f"✓ Model loaded in {load_time:.2f} seconds!")


    handler = STTHandler(model, folder_out)

    observer = Observer()
    observer.schedule(handler, folder_in, recursive=False)
    observer.start()

    print("STT listener running...")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()

if __name__ == "__main__":
    start_stt_listener(watch_folder, write_folder)