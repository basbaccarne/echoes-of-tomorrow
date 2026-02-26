# Main state machine of the raspi telephone module
# The state machine checks the system global variable state and runs the associated script
# The state scripts can update the state variable to transition to the next state
# General parameters are stored in config.yaml and imported by the state scripts as needed

# Libraries
import importlib
import time
from gpiozero import Device

# Global "state" variable and loaded state to track which module is currently loaded
state = "idle"
loaded_state = None

# Main loop to continuously check the state and run the corresponding module
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

        # Sleep briefly to prevent high CPU usage
        time.sleep(0.01)

# Allow graceful exit on Ctrl+C
except KeyboardInterrupt:
    print("Program stopped by user")

# Clean up GPIO pin usage on exit
finally:
    Device.close_all()
    print("GPIO cleaned up")