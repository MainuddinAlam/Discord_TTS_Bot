# Import modules for the program
import pyttsx3
import discord

# Creating a discord bot instance with the specified intents
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# Initialize TTS engine and adjust the rate and volume of speech
engine = pyttsx3.init()
engine.setProperty('rate', 175)   
engine.setProperty('volume', 1.0) 

# Assign voices
voices = engine.getProperty('voices')
text_users_voices = {
    "PersonA": voices[18].id,
    "PersonB": voices[29].id
}

"""
Function to handle the "on_ready" event which triggers when the bot connects to Discord
"""
@client.event
async def on_ready():
    print(f"✅ Bot logged in as {client.user}")

# Step 4: Define the "on_message" event – runs when any message is sent
@client.event
async def on_message(message):
    if message.author == client.user:
        return  # Skip the bot’s own messages
    print(f"{message.author.display_name}: {message.content}")


"""
Function to convert text to speech
"""
def text_to_speech(text, text_user):
    # Retrieve the correct voice
    voice_id = text_users_voices.get(text_user, voices[0].id)  # Default to voice 0 if user unknown
    engine.setProperty('voice', voice_id)
    engine.say(text)
    engine.runAndWait()

# Example usage:
text_to_speech("Hello, this is Person A speaking.", "PersonA")
text_to_speech("Hi there, Person B here!", "PersonB")

# for i, voice in enumerate(voices):
#     print(f"{i}: {voice.name} ({voice.id})")