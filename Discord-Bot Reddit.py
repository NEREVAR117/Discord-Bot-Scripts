import discord
import asyncio
import praw
import random

import logging
logging.basicConfig(level=logging.INFO)


client = discord.Client()




#Prompts the console with start and login confirmation
@client.event
async def on_ready():
    print('Logged in as',client.user.name+'!')
    print('Client ID:',client.user.id)
    print('------')



#Reddit API Log-in
reddit = praw.Reddit(client_id='REMOVED FOR GITHUB',
                    client_secret='REMOVED FOR GITHUB',
                    user_agent='REMOVED FOR GITHUB')




@client.event
async def on_message(message):
#The Subreddit Finder and Poster
    print(message.channel)
    if message.content.startswith('-reddit'):
        subreddit_user = str(message.content.split()[1])

        submission_list = []

        # Gets a list of the top 100 items matching the image-type criteria
        for submission in reddit.subreddit(subreddit_user).hot(limit=100):
            if any(url in submission.url for url in ('gfycat.com', 'imgur.com', 'reddituploads.com', 'redd.it/')):
                submission_list.append(submission.url)

        # Grabs a random image to post
        random_int = random.randint(0, len(submission_list))
        print(submission_list)
        await message.channel.send(submission_list[random_int - 1])









#Turns off SCRIPT
    if (message.content == '-sleep') and (message.author.id == REMOVED FOR GITHUB):
        await client.logout()





client.run(REMOVED FOR GITHUB)



# Written Thursday, August 24th, 2017
# Build v0.1