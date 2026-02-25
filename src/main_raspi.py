import importlib
import time

state = "idle"

while True:
    try:
        module = importlib.import_module(f"states.{state}")
        importlib.reload(module)

        next_state = module.run()

        if next_state:
            print(f"Switching to state: {next_state}")
            state = next_state

    except Exception as e:
        print(f"Error in state {state}: {e}")
        state = "idle"

    time.sleep(0.01)