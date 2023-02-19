# Adapted from the Magic Card bot's code on 6/8/2021 (June 8th)

import discord
import urllib.request
from bs4 import BeautifulSoup
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

#Magic Card Finder V1
@client.event
async def on_message(message):





    if message.content.startswith("-dogecoin"):

        url = 'https://www.coindesk.com/price/dogecoin'

        response = urllib.request.urlopen(url)

        html = response.read()

        #print(html)

        soup = BeautifulSoup(html, "lxml")

        doge_price = soup.findAll("div", class_="price-large")

        doge_price = str(doge_price[0])
        doge_price = doge_price[54:]
        doge_price = doge_price[:4]

        print(doge_price)





        percentage = soup.findAll("span", class_="percent-value-text")

        percentage = str(percentage[0])
        percentage = percentage[33:]
        percentage = percentage[:6]

        print(percentage)





        status = "DC: " + doge_price + "$ (" + percentage + "%)"

        activity = discord.Activity(name=status, type=discord.ActivityType.watching)
        await client.change_presence(activity=activity)














#Turns off SCRIPT
    if (message.content == '-sleep') and (message.author.id == REMOVED FOR GITHUB):
        await client.logout()





client.run(REMOVED FOR GITHUB)