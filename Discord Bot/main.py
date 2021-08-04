# IMPORT DISCORD LIBRARIES
import discord
from discord.ext import commands
import discord_components

# IMPORT STANDARD LIBRARIES
import numpy as np
import os

#INITALISE BOT COMMANDS
bot = commands.Bot(command_prefix="EM")

# CREATE COMPONENTS CLIENT 
components_client = discord_components.DiscordComponents(bot)
  
# INITIALISE VARIABLES
accessible_channels = []
email_channel = None
roles_with_access = []


# COMMANDS
@bot.command()
async def configure(context):

    global roles_with_access

     # GET MESSAGE CONTEXT
    author = context.author
    channel = context.channel
    guild = channel.guild

    # AUTHENTICATE MESSAGE
    if roles_with_access == []:
        if not author.permissions_in(channel).administrator: return
    else: 
        # AUTHENTICATION FLAG
        has_role = False

        # LOOP THROUGH EACH OF THE USERS ROLES
        for role in author.roles:
            if role in roles_with_access: 
                has_role = True
                break

        # IF USER HAS INCORRECT ROLES, EXIT FUNCTION
        if not has_role: return
    
    await channel.send('Authentication complete!')
    await channel.send('....')

    # ACCESS CONTROL CONFIGURATION
    select = create_role_select_menu(channel, guild.roles)
    select.options.append(discord_components.SelectOption(
        label = 'Exit',
        value = 'exit',
        description = 'exit roles interaction',
        emoji = None
    ))

    await channel.send('What roles should be able to access Emailia?')
    roles_with_access = []
    duplicate_role_response = None
    while True:
        select_menu = await components_client.send_component_msg(channel, content = "current roles with access: " + str(roles_with_access), components = [select])

        response = await bot.wait_for("select_option", check = None)
        response_label = response.component[0].label

        if duplicate_role_response != None:
            await duplicate_role_response.delete()
            duplicate_role_response = None

        if response_label == 'Exit': 
            await select_menu.delete()
            break

        if response_label in roles_with_access: 
            duplicate_role_response = await channel.send("The role '{0}' already has access".format(response_label))
        else:
            roles_with_access.append(response_label)
        
        await select_menu.delete()
        
        
    await channel.send("final roles with access: " + str(roles_with_access))
    await channel.send("...")
        

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
    
    
def create_role_select_menu(channel, roles):
    options = create_roles_options(roles)
    select = discord_components.Select(
        placeholder = "choose a role to add.",
        options = options
        )
    return select

def create_roles_options(roles):
    options = []
    for role in roles:
        option = discord_components.SelectOption(
            label = str(role),
            value = str(role),
            description = "add role: {0}".format(str(role)),
            emoji = None
        )
        options.append(option)
    return options

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

