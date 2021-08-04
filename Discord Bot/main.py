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
    global email_channel
    global accessible_channels

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
        if not has_role: 
            print("you do not have the correct roles")
            return
    
    await channel.send('Authentication complete!')
    await channel.send('....')

    # ACCESS CONTROL CONFIGURATION
    select = create_role_select_menu(guild.roles)
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
        roles_select_menu = await components_client.send_component_msg(channel, content = "current roles with access: {0}".format(role_list_to_string_list(roles_with_access)), components = [select])

        response = await bot.wait_for("select_option", check = None)
        response_label = response.component[0].label

        if duplicate_role_response != None:
            await duplicate_role_response.delete()
            duplicate_role_response = None

        if response_label == 'Exit': 
            await  roles_select_menu.delete()
            break

        if response_label in roles_with_access: 
            duplicate_role_response = await channel.send("The role '{0}' already has access".format(response_label))
        else:
            roles_with_access.append(get_role_from_string(response_label, guild.roles))
        
        await  roles_select_menu.delete()
        
        
    await channel.send("final roles with access: {0}".format(role_list_to_string_list(roles_with_access)))
    await channel.send("....")
    
    # CHANNEL CONTROL CONFIGURATION

    await channel.send("choose a channel the bot will mirror emails to.")
    
        
    select = create_channels_select_menu(accessible_channels)
    select.options.append(discord_components.SelectOption(
        label = 'Keep current channel',
        value = 'Keep current channel',
        description = 'Keep {0} as the current email channel'.format(str(email_channel)),
        emoji = None
    ))

    channels_select_menu = await components_client.send_component_msg(
        channel, 
        content = "current chosen channel: {0}  | Viewable channels: {1}".format(str(email_channel), str(channel_list_to_string_list(accessible_channels))), 
        components = [select])

    response = await bot.wait_for("select_option", check = None)
    response_label = response.component[0].label

    if(not response_label == 'Keep current channel'):
        email_channel = get_channel_from_string(response_label, accessible_channels)

    await channels_select_menu.delete()

    await channel.send("final chosen email channel: {0}".format(str(email_channel)))
    

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
    
    
# CREATES A SELECT MENU CONSISTING OF THE GIVEN ROLES
def create_role_select_menu(roles):
    options = create_roles_options(roles)
    select = discord_components.Select(
        placeholder = "choose a role to add.",
        options = options
        )
    return select

# CREATES ALL THE ROLES OPTIONS FOR A SELECT MENU
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

# CREATES A SELECT MENU CONSISTING OF THE GIVEN CHANNELS
def create_channels_select_menu(channels):
    options = create_channels_options(channels)
    select = discord_components.Select(
        placeholder = "choose a channel for Emailia to mirror emails to.",
        options = options
    )
    return select

# CREATES ALL THE CHANNEL OPTIONS FOR A SELECT MENU
def create_channels_options(channels):
    options = []
    for channel in channels:
        option = discord_components.SelectOption(
            label = str(channel),
            value = str(channel),
            description = "select channel: {0}".format(str(channel)),
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

# GETS THE CHANNEL OBJECT FROM THE CHANNEL NAME
def get_channel_from_string(channel_name, channels):
    for channel in channels:
        if channel_name == str(channel):
            return channel
    return None

# GETS THE ROLE OBJECT FROM THE CHANNEL NAME
def get_role_from_string(role_name, roles):
    for role in roles:
        if role_name == str(role):
            return role
    return None

# CONVERT THE CHANNEL LIST TO A LIST OF CHANNEL NAMES
def channel_list_to_string_list(channel_list):
    string_list = []
    for channel in channel_list:
        string_list.append(str(channel))
    return string_list

# CONVER THE ROLE LIST TO A LIST OF ROLE NAMES
def role_list_to_string_list(role_list):
    string_list = []
    for role in role_list:
        string_list.append(str(role))
    return string_list

# GET THE TOTKEN FOR EMAILIA FROM ENVIRONMENT FILE
def get_token():
    token = os.getenv('TOKEN')
    return token

# RUN EMAILIA
bot.run(get_token())

