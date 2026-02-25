import importlib
import time

state = "idle"
loaded_state = None

while True:
    try:
        # load and reload only when state changes
        if loaded_state != state:
            module = importlib.import_module(f"states.{state}")
            importlib.reload(module)
            loaded_state = state

        next_state = module.run()

        if next_state:
            print(f"Switching to state: {next_state}")
            state = next_state

    except Exception as e:
        print(f"Error in state {state}: {e}")
        state = "idle"

    time.sleep(0.01)