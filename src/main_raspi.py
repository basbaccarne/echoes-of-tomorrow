import importlib
import time

state = "idle"

while True:
    # dynamically load the current state module
    module = importlib.import_module(f"states.{state}")

    # run the state
    next_state = module.run()

    # if state returns a new name → switch
    if next_state:
        print(f"Switching to state: {next_state}")
        state = next_state

    time.sleep(0.01)