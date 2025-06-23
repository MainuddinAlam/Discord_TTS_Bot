# Import modules for the program
import pyttsx3
import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

# Creating a discord bot instance with the specified intents
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Initialize TTS engine and adjust the rate and volume of speech
engine = pyttsx3.init()
engine.setProperty('rate', 175)   
engine.setProperty('volum e', 1.0) 

# Initialize global variables
assigned_voices = {}

"""
Function to only get the english voices

@returns english_only_voices The voices in english
"""
def get_english_voices():
    # Get the information of all the voices
    voices = engine.getProperty('voices')
    # Loop through the all the voices and get only the english ones
    english_only_voices = []
    for voice in voices:
        if ('en' in voice.id.lower()) or ('english' in voice.name.lower()):
            english_only_voices.append(voice)

    # for v in english_only_voices:
    #     print(f"- {v.name} ({v.id})")
    return english_only_voices

"""
Function to assign voices to users
"""
def assign_voices_to_users():
    # Get the english voices
    eng_voices = get_english_voices()
    counter = 0
    # Get the members in the server
    for guild in bot.guilds:
        print(f"\n📌 Server name: {guild.name}")
        for member in guild.members:
            # Do not assign a voice to the bot
            if member.display_name == 'Text_To_Speech_Bot':
                continue  
            assigned_voices[member.display_name] = eng_voices[counter].id
            counter += 1
            # If there are more members than english voices available, repeat the process
            if counter == len(assigned_voices) - 1:
                counter = 0

"""
Function to convert text to speech

@param text The user text
@param text_user The person giving that particular text
"""
def text_to_speech(text, text_user):
    # Retrieve the correct voice
    voice_id = assigned_voices.get(text_user)  
    engine.setProperty('voice', voice_id)
    engine.say(text)
    engine.runAndWait()
    
"""
Function to handle the "on_ready" event which triggers when the bot connects to Discord
"""
@bot.event
async def on_ready():
    # Let the user know that the bot has been connected
    print(f"✅ Bot logged in as {bot.user}")
    
    # Assign english voices to users
    assign_voices_to_users()


"""
Function to handle the "on_message" event which triggers when any message is sent
"""
@bot.event
async def on_message(message):
    # Skip the bot’s own messages
    if message.author == bot.user:
        return  
    # Call the function to generate text to speech
    text_to_speech(message.content, message.author.display_name)

# Run the bot using the Bot token from Discord
load_dotenv()
bot.run(os.getenv("DISCORD_BOT_TOKEN"))
