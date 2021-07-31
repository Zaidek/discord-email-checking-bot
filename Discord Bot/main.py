# IMPORT DISCORD LIBRARIES
import discord

# IMPORT STANDARD LIBRARIES
import numpy as np
import os


# INITIALISE CLIENT
client = discord.Client()
    
# START UP EVENT
@client.event
async def on_ready():
    print("{0.user} has arrived!".format(client))


client.run(os.getenv('TOKEN'))

