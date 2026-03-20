import pyttsx3
import time

# --- 1. THE KNOWLEDGE BASE ---
semantic_dictionary = {
    "HELLO": "Hello there! I am using an AI assistant.",
    "YES": "Yes, I agree.",
    "HELP": "Excuse me, I need assistance please.",
    "THANKYOU": "Thank you very much.",
    "POINT": "I would like that item, please.",
    "THUMBSUP": "I am doing good, everything is okay.",
    "BACKGROUND": "" 
}

# --- 2. THE CONTEXT MEMORY ---
# --- 2. EXPANDED CONTEXT MEMORY (Level 3: Sequential Logic) ---
context_dictionary = {
    # 1. The "Point" Interactions (Selecting or indicating something)
    ("POINT", "YES"): "Yes, that is exactly the one I want.",
    ("POINT", "HELP"): "I need some help with this specific item.",
    ("POINT", "THANKYOU"): "Thank you, I will take this one.",
    
    # 2. The "Hello" Interactions (Starting a specific type of conversation)
    ("HELLO", "HELP"): "Hello, this is an emergency! Please help me.",
    ("HELLO", "THUMBSUP"): "Hello there, I am doing very well today.",
    ("HELLO", "POINT"): "Hello, could you show me that item please?",
    
    # 3. The "Help" Interactions (Specifying the type of help)
    ("HELP", "YES"): "Yes, I definitely need some assistance.",
    ("HELP", "POINT"): "Please help me move or reach that.",
    ("HELP", "THANKYOU"): "Thank you for coming to help me.",
    
    # 4. Clarification / Confirmation
    ("THUMBSUP", "YES"): "Yes, everything is absolutely perfect.",
    ("THANKYOU", "THUMBSUP"): "Thank you, I am doing great now."
}

# --- 3. THE NLP STATE MACHINE ---
class NLPEngine:
    def __init__(self):
        self.previous_sign = None
        self.last_spoken_time = 0
        self.cooldown_seconds = 0  # CHANGED TO 0 FOR MANUAL TYPING TEST

    def speak_text(self, text):
        # We re-initialize the engine per-call to prevent the "stuck loop" bug on laptops
        engine = pyttsx3.init()
        engine.setProperty('rate', 150)
        engine.say(text)
        engine.runAndWait()

    def process_and_speak(self, current_sign):
        if current_sign == "BACKGROUND" or current_sign not in semantic_dictionary:
            return

        if time.time() - self.last_spoken_time < self.cooldown_seconds:
            return # Ignored due to cooldown

        sentence_to_speak = ""

        # Check Context Sequence
        if self.previous_sign is not None:
            sequence = (self.previous_sign, current_sign)
            if sequence in context_dictionary:
                sentence_to_speak = context_dictionary[sequence]
                self.previous_sign = None # Reset memory 
        
        # Check Single Sign
        if sentence_to_speak == "":
            sentence_to_speak = semantic_dictionary[current_sign]
            self.previous_sign = current_sign 

        print(f"\n[AI VISION RAW]: {current_sign}")
        print(f"[NLP GENERATED]: {sentence_to_speak}")
        
        # Call our bulletproof speaking function
        self.speak_text(sentence_to_speak)
        
        self.last_spoken_time = time.time()

# --- 4. TEST LOOP ---
if __name__ == "__main__":
    nlp = NLPEngine()
    print("--- NLP ENGINE STARTED ---")
    print("Available: HELLO, YES, HELP, THANKYOU, POINT, THUMBSUP")
    
    while True:
        simulated_ai_output = input("\nSimulate AI Sign > ").upper()
        if simulated_ai_output == 'QUIT':
            break
        nlp.process_and_speak(simulated_ai_output)