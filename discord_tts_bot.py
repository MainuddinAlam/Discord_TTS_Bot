import pyttsx3

# Initialize TTS engine
engine = pyttsx3.init()
engine.setProperty('rate', 175)   # Speed of speech
engine.setProperty('volume', 1.0) # Max volume

# Optional: change voice
# voices = engine.getProperty('voices')
# engine.setProperty('voice', voices[1].id)  # Use index 0 or 1 depending on system

print("Type a message and press Enter (type 'exit' to quit):")

while True:
    text = input("> ")
    if text.lower() == "exit":
        break
    engine.say(text)
    engine.runAndWait()
