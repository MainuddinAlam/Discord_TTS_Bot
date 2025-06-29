# Import modules for the program
from kokoro import KPipeline
import simpleaudio as sa
import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import numpy as np

# Set up Kokoro
pipeline = KPipeline(lang_code='a')

# Creating a discord bot instance with the specified intents
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)


# Initialize global variables
assigned_voices = {}


# """
# Function to assign voices to users
# """
# def assign_voices_to_users():
  
#     counter = 0
#     # Get the members in the server
#     for guild in bot.guilds:
#         print(f"\n📌 Server name: {guild.name}")
#         for member in guild.members:
#             # Do not assign a voice to the bot
#             if member.display_name == 'Text_To_Speech_Bot':
#                 continue  
#             assigned_voices[member.display_name] = eng_voices[counter].id
#             counter += 1
#             # If there are more members than english voices available, repeat the process
#             if counter == len(assigned_voices) - 1:
#                 counter = 0

"""
Function to convert text to speech

@param text The user text
@param text_user The person giving that particular text
"""
def text_to_speech(text, text_user):
    audio_chunks = pipeline(text, voice='af_heart')

    # Combine all audio chunks
    audio = np.concatenate([chunk for _, _, chunk in audio_chunks])

    # Play the audio
    audio_int16 = (audio * 32767).astype(np.int16)
    sa.play_buffer(audio_int16, 1, 2, 24000).wait_done()
   
     
"""
Function to handle the "on_ready" event which triggers when the bot connects to Discord
"""
@bot.event
async def on_ready():
    # Let the user know that the bot has been connected
    print(f"✅ Bot logged in as {bot.user}")
    


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
