# IMPORT DISCORD LIBRARIES
import discord
from discord.ext import commands

# IMPORT STANDARD LIBRARIES
import numpy as np
import os

#INITALISE BOT COMMANDS
bot = commands.Bot(command_prefix="EM")
  
# INITIALISE VARIABLES
accessible_channels = []
email_channel = None
roles_with_access = []


# COMMANDS
@bot.command()
async def configure(context):

     # GET MESSAGE CONTEXT
    author = context.author
    channel = context.channel
    guildID = channel.guild.id 

    # AUTHENTICATE MESSAGE
    if roles_with_access == []:
        if not author.permissions_in(channel).administrator: return
    else: 
        has_role = False
        for role in author.roles:
            if role in roles_with_access: 
                has_role = True
                break
        if not has_role: return
    
    await channel.send('Authentication complete!')
    await channel.send('....')

    # ACCESS CONTROL CONFIGURATION
    await channel.send('What roles should be able to access Emailia?')


    # EMAIL CONTROL CONFIGURATION

# START UP EVENT
@bot.event
async def on_ready():
    print("{0.user} has arrived!".format(bot))
    channels = bot.get_all_channels()
    update_usable_channels(channels)

# ON MESSAGE EVENT
@bot.event
async def on_message(message):

    # GO TO COMMANDS IF POSSIBLE
    await bot.process_commands(message)
    
    

# FIND ALL CHANNELS ACCESABLE BY EMAILIA          
def update_usable_channels(channels): 
    for channel in channels:
        if channel.category == None: continue
        if channel.category.name != "Text channels": continue
        if bot.user not in channel.members: continue
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
bot.run(get_token())

