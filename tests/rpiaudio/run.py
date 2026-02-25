import os
from pathlib import Path
import toml

def run_audio():
    # load configuration
    toml_config = toml.load("../config.toml")["rpiaudio"]["run"]
    #print("toml_config", toml_config)
    RECEIVER = toml_config["receiver"]  # Replace with receiver's IP
    LISTEN_DIR = Path(toml_config["listen_dir"])  # Directory to watch for new wav files
    PROCESSED_DIR = Path(toml_config["processed_dir"])  # Directory to move processed files
    WAIT_TIME = toml_config.get("wait_time", 5)  # Time to wait between checks (in seconds)
    PLAY_DIR = Path(toml_config["play_dir"])
    # repeatedly check
    while True:
        # for new recordings
        to_be_processed = os.listdir(LISTEN_DIR)
        # if we have some
        if len(to_be_processed) > 0:
            print(f"Found {len(to_be_processed)} files to process.")
            process_file = LISTEN_DIR / to_be_processed[0]  # Process the first file in the list
            print(f"Processing files: {process_file}")
            # process new recording
            if os.system(f"scp {process_file} pi@{RECEIVER}:~/receive") == 0:  # copy wav file
                os.system(f"mv {process_file} {PROCESSED_DIR}")  # move processed file
                print(f"Successfully sent {str(process_file)} to {RECEIVER} and moved to processed directory.")
            else:
                print(f"Failed to send {str(process_file)} to {RECEIVER}")
            ## nevermind: we don't wait!
            #os.wait(WAIT_TIME)  # Wait for 5 seconds before sending the file again
        to_be_played = os.listdir(PLAY_DIR)
        if len(to_be_played) > 0:
            print(f"Found {len(to_be_played)} files to play.")
            play_file = PLAY_DIR / to_be_played[0]  # Play the first file in the list
            print(f"Playing file: {play_file}")
            if os.system(f"aplay {play_file}"):  # Play the audio file
                os.system(f"mv {play_file} {PROCESSED_DIR}")  # Move played file to processed directory
            else:
                print(f"Failed to play {str(play_file)}")

if __name__ == "__main__":
    run_audio()
            