import importlib
import time
from gpiozero import Device

state = "idle"
loaded_state = None

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

            if next_state:
                print(f"Switching to state: {next_state}")
                state = next_state

        except Exception as e:
            print(f"Error in state {state}: {e}")
            state = "idle"

        time.sleep(0.01)

except KeyboardInterrupt:
    print("Program stopped by user")

finally:
    Device.close_all()
    print("GPIO cleaned up")