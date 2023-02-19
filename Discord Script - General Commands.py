# Written Thursday, August 24th, 2017. Starting making random stuff for friends.
# April 11th, 2022 - Cleaned up code slightly and added a new image reaction for certain speech

import discord
import asyncio
import random
import datetime

import logging
logging.basicConfig(level=logging.INFO)

client = discord.Client()

global current_time
global time_channel_changed

#Prompts the console with start and login confirmation
@client.event
async def on_ready():
    print('Logged in as',client.user.name+'!')
    print('Client ID:',client.user.id)
    print('------')

    #await client.change_presence(game=discord.Game(name='Under Development'))

#Dictionary - POINTS SYSTEM
@client.event
async def on_message(message):


    # Lowercases the user message
    message.content = message.content.lower()





    unwanted_words = ['', 'is', 'taking', 'oh', 'the', 'be', 'to', 'of', 'and', 'a', 'in', 'that', 'have', 'i', 'it', 'for', 'not', 'on', 'with', 'he', 'as', 'you', 'do', 'at', 'this', 'but', 'his', 'by', 'from', 'they', 'we', 'say', 'her', 'she', 'or', 'an', 'will', 'my', 'one', 'all', 'would', 'there', 'their', 'what', 'so', 'up', 'out', 'if', 'about', 'who', 'get', 'which', 'go', 'me', 'when', 'make', 'can', 'like', 'time', 'no', 'just', 'him', 'know', 'take', 'people', 'into', 'year', 'your', 'good', 'some', 'could', 'them', 'see', 'other', 'than', 'then', 'now', 'look', 'only', 'come', 'its', 'over', 'think', 'also', 'back', 'after', 'use', 'two', 'how', 'our', 'first', 'well', 'way', 'even', 'new', 'want', 'because', 'any', 'these', 'give', 'most', 'us', 'near', 'while']

    # Changes channel name (1 in 10 chance of triggering per post)
    if message.content != "" and message.channel.id == REMOVED FOR GITHUB:
        chance = random.randint(1, 10)  # 1 in 10 chance
        if chance == 1:

            # Split the message into a list of words
            words = message.content.split()

            # Remove all non-alphabetic characters from the word
            position = 0
            for word in words:
                words[position] = ''.join(character for character in word if character.isalpha())
                position += 1



            # Removes all unwanted words from the list
            new_list = []
            for word in words:
                if word not in unwanted_words:
                    new_list.append(word)

            words = new_list



            # Choose a random word from the list
            chosen_word = random.choice(words)
            chosen_word += "-channel"

            # Open the file in read mode
            with open('channel_name_change_timestamp.txt', 'r') as file:
                # Read the contents of the file
                time_channel_changed = int(file.read())

            # Gets the current time
            dt = datetime.datetime.now()
            # Converts the current time to unix time (in seconds) as an integer
            current_time = int(dt.timestamp())

            # Checks if more than 28,800 seconds (8 hours) has passed since the last channel name change
            if current_time - time_channel_changed > 28800:
                await message.channel.edit(name=chosen_word)

                # Sets the time the channel's name was changed to now
                time_channel_changed = current_time

            # Open the file in write mode
            with open('channel_name_change_timestamp.txt', 'w') as file:
                # Write the contents to the file (overwriting what was in it)
                file.write(str(time_channel_changed))









    # Summons doge
    if message.content == "-doge":
        await message.channel.send("https://images.techhive.com/images/article/2013/12/memesof2013_hero-100221127-large.jpg")




    # Pikachu oh reaction
    if message.content in ('oh', "Oh", "OH", "oH"):
        random_num = random.randint(1, 6) # 1 in 6 chance
        if random_num == 1:
            print("Random number was 1")
            await message.channel.send("https://i.kym-cdn.com/entries/icons/original/000/027/475/Screen_Shot_2018-10-25_at_11.02.15_AM.png")





    # "Excuse me" reaction gif
    if message.content in ("excuse me", "excuse me.", "excuse me?"):
        random_num = random.randint(1, 6) # 1 in 6 chance
        if random_num == 1:
            print("Random number was 1")
            await message.channel.send("https://tenor.com/view/umm-confused-blinking-okay-white-guy-blinking-gif-7513882")








    # Posts the most amazing gif when good ol' JC is called upon us
    if (message.content.lower() == 'jesus') or (message.content.lower() == 'jesus christ'):
        await message.channel.send("https://cdn.discordapp.com/attachments/436723866279215104/583478461444915200/EssentialDetailedFerret.webm")





    #THE GREAT AND HOLY CONCH SHELL
    conch_list = ['Maybe someday.', 'I don\'t think so.', 'No.', 'No.', 'No.', 'Yes.', 'Yes.', 'Yes.', 'Try asking again.', 'Follow the seahorse.']
    if message.content.startswith('-conch'):
        random_conch = random.randint(0, 7)
        await message.channel.send(conch_list[random_conch])

        print(random_conch)
        print(conch_list[random_conch])





    #Makes the bot leave the server it's in
    if message.content == '-abandon' and message.author.id == REMOVED FOR GITHUB:
        to_leave = client.get_guild(REMOVED FOR GITHUB)
        await to_leave.leave()





    #Flips a coin for heads or tails
    if message.content == '-coin' or message.content == '-flip':
        coin_side = ['The coin landed on **heads**', 'The coin landed on **tails**']
        coin_random = random.randint(0,1)
        await message.channel.send(coin_side[coin_random])



    #Rolls a dice of a chosen value
    if message.content == '-roll' or message.content == '-r':
        await message.channel.send('You rolled a ' + str(random.randint(1, 20)) + ' out of 20.')
    elif ((message.content.startswith('-roll')) or (message.content.startswith('-r'))) and (((message.content.split()[0]) == '-roll') or ((message.content.split()[0]) == '-r')):
        dice_number = int(message.content.split()[1])
        if dice_number <= 1:
            await message.channel.send("You must roll a number higher than 1!")
        elif dice_number > 1:
            await message.channel.send('You rolled a ' + str(random.randint(1, dice_number)))
        else:
            await message.channel.send("You must use a number.")








    #Turns off SCRIPT
    if (message.content == '-sleep') and (message.author.id == REMOVED FOR GITHUB):
        await client.logout()





client.run(REMOVED FOR GITHUB)