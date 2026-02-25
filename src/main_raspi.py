from enum import Enum
from gpiozero import Button
import time

# GPIO pin 4 is verbonden met de telefoonknop
button_horn = Button(4)
button_hashtag = Button(3)
debounce = 0.3


class State(Enum):
    IDLE = "idle"
    PRELISTENING = "pre-listening"
    LISTENING = "listening"
    PROCESSING = "processing"
    SPEAKING = "speaking"

class PhoneStateMachine:
    def __init__(self):
        self.state = State.IDLE
        self.transcript = ""
        self.response = ""
    
    def transition(self, new_state):
        """Verander state"""
        print(f"🔄 State: {self.state.value} → {new_state.value}")
        self.state = new_state
    
    def run(self):
        """Main loop"""
        print("Phone system started!")
        
        while True:
            if self.state == State.IDLE:
                self.handle_idle()
                
            elif self.state == State.PRELISTENING:
                self.handle_prelistening()
            
            elif self.state == State.LISTENING:
                self.handle_listening()
            
            elif self.state == State.PROCESSING:
                self.handle_processing()
            
            elif self.state == State.SPEAKING:
                self.handle_speaking()
            
            time.sleep(0.1)
    
    def handle_idle(self):
        """Wacht op telefoon opname"""
        print("💤 Waiting for phone pickup...")
        time.sleep(2)
        
        # Simuleer: telefoon opgenomen
        if self.detect_phone_pickup():
            self.transition(State.LISTENING)
    
    def handle_prelistening(self):
        """Wacht op stilte"""
        print("👂 Pre-listening: waiting for silence...")
        time.sleep(2)
        
        # Simuleer: stilte gedetecteerd
        self.transition(State.LISTENING)
    
    def handle_listening(self):
        """Neem audio op"""
        print("🎤 Recording audio...")
        
        # Simuleer opname
        time.sleep(3)
        self.transcript = "Wat zijn de toekomstbeelden?"
        
        self.transition(State.PROCESSING)
        
        
    def handle_processing(self):
        print(f"🧠 Processing: '{self.transcript}'")
        # Simuleer processing
        time.sleep(2)
        self.response = "De toekomstbeelden gaan over groene mobiliteit en circulaire economie."
        
        self.transition(State.SPEAKING)
    
    def handle_processing(self):
        """STT → RAG → LLM"""
        print(f"🧠 Processing: '{self.transcript}'")
        
        # Simuleer processing
        time.sleep(2)
        self.response = "De toekomstbeelden gaan over groene mobiliteit en circulaire economie."
        
        self.transition(State.SPEAKING)
    
    def handle_speaking(self):
        """TTS + afspelen"""
        print(f"🔊 Speaking: '{self.response}'")
        
        # Simuleer TTS + playback
        time.sleep(2)
        
        # Klaar - terug naar idle
        self.transition(State.IDLE)
    
    def detect_phone_pickup(self):
        """Detecteer of telefoon is opgenomen"""
        # Was button net ingedrukt?
        if button_horn.is_pressed:
            # Wacht op release
            while button_horn.is_pressed:
                time.sleep(0.01)
            print("Button released - phone picked up")
            time.sleep(debounce)
            return True

# Run
if __name__ == "__main__":
    machine = PhoneStateMachine()
    
    try:
        machine.run()
    except KeyboardInterrupt:
        print("\n👋 Shutdown")