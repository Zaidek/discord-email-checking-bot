# IMPORT DISCORD LIBRARIES
import discord

# IMPORT STANDARD LIBRARIES
import numpy as np
import os



# INITIALISE CLIENT
client = discord.Client()
  
# INITIALISE VARIABLES
accessible_channels = []

# START UP EVENT
@client.event
async def on_ready():
    print("{0.user} has arrived!".format(client))
    channels = client.get_all_channels()
    update_usable_channels(channels)

@client.event
async def on_message(message):
    author = message.author
    channel = message.channel
    guildID = channel.guild.id 


    if not message.content.startswith('!EMConfigure'): return
    if not author.permissions_in(channel).administrator: return
    print("hi")
    


# FIND ALL CHANNELS ACCESABLE BY EMAILIA          
def update_usable_channels(channels): 
    for channel in channels:
        if channel.category == None: continue
        if channel.category.name != "Text channels": continue
        if client.user not in channel.members: continue
        accessible_channels.append(channel)

# PRINT OUT ALL CHANNELS ACCESSIBLE BY EMAILIA
def print_usable_channels():
    for channel in accessible_channels:
        print(channel)

# GET THE TOTKEN FOR EMAILIA FROM ENVIRONMENT FILE
def get_token():
    token = os.getenv('TOKEN')
    return token

# RUN EMAILIA
client.run(get_token())

