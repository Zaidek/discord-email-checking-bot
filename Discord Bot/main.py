# IMPORT DISCORD LIBRARIES
import discord

# IMPORT STANDARD LIBRARIES
import numpy as np
import os



# INITIALISE CLIENT
client = discord.Client()
  
# INITIALISE VARIABLES
accessable_channels = []
current_guild = None
for guild in client.guilds:
    print(guild.name + "X")


# START UP EVENT
@client.event
async def on_ready():
    print("{0.user} has arrived!".format(client))
    channels = client.get_all_channels()
    update_usable_channels(channels)

# FIND ALL CHANNELS ACCESABLE BY EMAILIA          
def update_usable_channels(channels): 
    for channel in channels:
        if channel.category == None: continue
        if channel.category.name != "Text channels": continue
        if client.user not in channel.members: continue
        accessable_channels.append(channel)

def print_usable_channels():
    for channel in accessable_channels:
        print(channel)

def get_token():
    token = os.getenv('TOKEN')
    return token

client.run(get_token())

