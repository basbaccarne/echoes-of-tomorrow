import importlib

state = "idle"

while True:
    module = importlib.import_module(f"states.{state}")
    next_state = module.run()

    if next_state:
        state = next_state