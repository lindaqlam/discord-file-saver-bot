import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import requests

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
CHANNEL_NAME = 'designs'
LOCAL_PATH = os.getenv('LOCAL_PATH')
client = discord.Client()

@client.event
async def on_ready():
    print("The FileSaverBot is waking up")

# #Bot initializer 
client = commands.Bot(command_prefix='')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if (message.channel.name == CHANNEL_NAME):
        if (message.attachments):
            attachment = message.attachments[0]
            url = attachment.url
            file_name = attachment.filename
            file_type = os.path.splitext(file_name)[1]
            await download_file(message, url, file_name, file_type)
    
async def download_file(message, url, file_name, file_type):
    valid_types = ('.jpeg', '.jpg', '.png')
    if file_type not in valid_types:
        return
    
    if not os.path.exists(LOCAL_PATH + '/' + file_name): 
        response = requests.get(url)
        file = open(LOCAL_PATH + '/' + file_name, 'wb')
        file.write(response.content)
        file.close()
        print("Downloading image")
    else:
        print("File already exists")

client.run(TOKEN)