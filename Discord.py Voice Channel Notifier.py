# Ported code from the 'Voice Channel Members Bot (Rewrite)' code on November 15th, 2021
# Heavily modified, checks for voice channel events, notifies me if people join a voice channel in REMOVED FOR GITHUB's server
# Added support for the new REMOVED FOR GITHUB server made by REMOVED FOR GITHUB (August 29, 2022)



import discord
import asyncio

import logging
logging.basicConfig(level=logging.INFO)

# Allows the bot to get member server member lists and certain data
intents = discord.Intents.default()
intents.members = True

# Must be set like this to get member name via their IDs
client = discord.Client(intents=intents)
#client = discord.Client()





# Prompts the console with start and login confirmation
@client.event
async def on_ready():
    print('Logged in as',client.user.name+'!')
    print('Client ID:',client.user.id)
    print('------')




# The logic for voice channel events
@client.event
async def on_voice_state_update(member, before, after):

    # First establishes the presence as being False
    user_presence = False

    # The voice channels
    voice_channels = [REMOVED FOR GITHUB, REMOVED FOR GITHUB, REMOVED FOR GITHUB, REMOVED FOR GITHUB, REMOVED FOR GITHUB]



    # We get a list of the members in the first voice channel
    for channel in voice_channels:
        voice_channel = client.get_channel(channel)
        members = voice_channel.members

        #print(members)

        # We check the first channel for my (the user's) presence
        for member in members:
            # If I'm in the voice channel we assign the presence variable to True
            if member.id == REMOVED FOR GITHUB:
                user_presence = True




    # First checks if there is even a channel ID (to avoid unnecessary warning messages in the console) AND if it's me joining the channel or not AND if I'm in the voice channel when someone else joins
    if after.channel != None and member.id != REMOVED FOR GITHUB and user_presence == False:

        # Only shows activity in specific channels if a person JOINS a channel (without being in one previously)
        if after.channel.id in voice_channels:
            #print(member)
            #print(member.id)
            #print(member.display_name)
            #print(before)
            #print(before.channel)
            #print(after)
            #print(after.channel)
            #print(after.channel.id)

            if before.channel == None:
                user = client.get_user(REMOVED FOR GITHUB)
                await user.send(member.display_name + " joined a voice channel.")




# The logic for message events
@client.event
async def on_message(message):





    # This is purely for debugging and deleting bot messages where needed
    if message.content == "-delete":
        #channel = client.get_channel(REMOVED FOR GITHUB)

        test = await message.channel.fetch_message(REMOVED FOR GITHUB) #Put message ID here
        await test.delete()






    # Creates a list of the message content split up to we can use its parts
    split_message = message.content.split()

    # Catches the bot's own messages about people joining the server, then deletes after some time
    if message.author.id == REMOVED FOR GITHUB: # Two-step check keeps unnecessary error messages
        if split_message[-2] == "voice" and split_message[-1] == "channel." and message.guild == None:

            # Waits 60 minutes before deleting the alert it just sent
            await asyncio.sleep(3600)

            bot_alert = await message.channel.fetch_message(message.id)

            await bot_alert.delete()




client.run(REMOVED FOR GITHUB)