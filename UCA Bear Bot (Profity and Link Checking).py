# Ported code from the 'Bois Voice Channel Notifier (Rewrite)' code on August 29th, 2022




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

    #await client.change_presence(activity=discord.Game(name='with some dice'))


# The logic for when someone joins the server
@client.event
async def on_member_join(member):



    role = discord.Object(id=REMOVED FOR GITHUB)
    await member.add_roles(role)




# The logic for voice channel events
@client.event
async def on_voice_state_update():


    pass



# The logic for message events
@client.event
async def on_message(message):



    # Profanity filter
    banned_words = [""]
    for word in banned_words:
        if word in message.content.lower() and message.author.id != REMOVED FOR GITHUB and message.author.id != REMOVED FOR GITHUB:

            # Sends to ME their message for review
            user = client.get_user(REMOVED FOR GITHUB)
            await user.send("User " + message.author.name + "#" + message.author.discriminator + " tried posting the following message:\n```" + message.content + "```")

            # Posts in the server they can't do that
            await message.delete()
            await message.channel.send("Certain words are not allowed. Please refrain from using them.")




    # Detects discord links
    allowed_links = [REMOVED FOR GITHUB]
    if REMOVED FOR GITHUB in message.content.lower() and message.author.id != REMOVED FOR GITHUB and message.author.id != REMOVED FOR GITHUB:
        for link in allowed_links:
            if link not in message.content:

                # Sends to ME their message for review
                user = client.get_user(REMOVED FOR GITHUB)
                await user.send("User **" + message.author.name + "#" + message.author.discriminator + "** tried posting the following message:\n```" + message.content + "```")

                # Posts in the server they can't do that
                await message.delete()
                await message.channel.send("Only approved server invites are allowed. Contact <@REMOVED FOR GITHUB> to request approval. Thank you. :)")




    # This is purely for debugging and deleting bot messages where needed
    if message.content == "-delete":
        #channel = client.get_channel(REMOVED FOR GITHUB)

        test = await message.channel.fetch_message(REMOVED FOR GITHUB) # Put message ID here
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