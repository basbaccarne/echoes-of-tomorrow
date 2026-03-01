# Main state machine of the raspi telephone module
# The state machine checks the system global variable state and runs the associated script
# The state scripts can update the state variable to transition to the next state
# General parameters are stored in config.yaml and imported by the state scripts as needed

# to do: add a DIP switch to set the pi in mode 0, 1, 2 or 3 
# and use that to send and receive on a different port of the server and name audio files differently, 
# so we can run 4 parallel state machines on the same server for 4 different pis

# static config is stored in config.yaml
# dynamic config is stored in states/shared.py (SharedState class)

# Libraries
import importlib
import time
import socket
from read_booth_id import read_booth_id
from states.shared import SharedState
from led_controller import LEDController

# detect DIP position and write to shared state (then all states can access it using SharedState.booth_id)
SharedState.booth_id = read_booth_id()

# initiate led animations
led = LEDController()
led.start()
led.set_state("idle")  # set initial animation

# Global "state" variable and loaded state to track which module is currently loaded
state = "idle"
loaded_state = None

# function to get the ip address
def get_ip():
    try:
        # This does not actually connect to the internet,
        # it just determines the active network interface
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "No network connection"
    
# opening statements
print("\n-------------------------------")
print("☎️   Raspberry Pi Telephone Module")
print(f"IP address: {get_ip()}")
print(f'This device is set to booth ID: {SharedState.booth_id}')
print(f"Starting state machine in state: {state}")
print("Waiting for the horn to be picked up, looking forward to this conversation ...\n")

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
                print(f"\nSwitching to state: {next_state}")
                state = next_state
                led.set_state(state)

        except Exception as e:
            print(f"Error in state {state}: {e}")
            state = "idle"

        # Sleep briefly to prevent high CPU usage
        time.sleep(0.01)

# Allow graceful exit on Ctrl+C
except KeyboardInterrupt:
    print("\n🛑   Program stopped by user")

# Clean up GPIO pin usage on exit
finally:
    led.stop()
    print("\n🧹   GPIO cleaned up. All set up for a new run!")
    print("-------------------------------\n")