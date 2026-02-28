# main state machine of the server
# quickest hack is to run this script for each pi on a different port
# to each pi sends to another port, so we can run 4 paralllel state machines on the same server

# run using "python main.py --booth-id=0" (or 1, 2, 3)

# static config is stored in config.yaml
# dynamic config is stored in states/shared.py (SharedState class)

import importlib
import time
import argparse
from states.shared import SharedState

# parse arguments
parser = argparse.ArgumentParser()
parser.add_argument("--booth-id", type=int, required=True)
args = parser.parse_args()

# set shared state
SharedState.booth_id = args.booth_id
print("Server started")
print(f"🆔 Booth ID for this instance is set to: {SharedState.booth_id}")

state = "stt"
# for testing: uncomment the line below and change with the state you want to start from
# state = "tts"

loaded_state = None
last_sender_ip = None

try:
    while True:
        try:
            # load module only when state changes
            if loaded_state != state:
                module = importlib.import_module(f"states.{state}")
                importlib.reload(module)
                loaded_state = state

            # run state (module always exists after load)
            next_state = module.run()

            if next_state and next_state != state:
                print(f"\n➡️  Switching to state: {next_state}")
                state = next_state

        except Exception as e:
            print(f"Error in state {state}: {e}")
            state = "waiting_for_receive"

        time.sleep(0.01)

except KeyboardInterrupt:
    print("Program stopped by user")