# Written early 2018 (February?) V2
# Updated April 17th to support more cards (double sided, double cards) V2
# Ported to Rewrite on September 6th, 2018. V3
# Updated to V4 (not sure when or to do what)
# Updated to support card prices, April 12th 2019, V5.

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

    message_start = ('-magic ', '-m ', '-c ', '-mtg ')

    message.content = message.content.lower()

    if message.content.startswith(message_start):

        list_message = message.content.split()
        reduced_message = list_message[1:]

        message_length = len(reduced_message)

        new_message = ''

        for x in range(0, message_length):
            new_message = new_message + reduced_message[x]

            new_message = new_message + '%20'

        new_message = new_message[:-3]

        default_url = 'http://gatherer.wizards.com/Pages/Card/Details.aspx?printed=false&name='

        response = urllib.request.urlopen(default_url + new_message)

        html = response.read()

        #This will grab a random card if people call for it
        if (message.content.startswith(message_start) and message.content[-6:] == 'random'):
            random_url = 'http://gatherer.wizards.com/Pages/Card/Details.aspx?action=random'

            response = urllib.request.urlopen(random_url)

            html = response.read()

        #Beautiful Soup grabbing and compiling the images into a list
        soup = BeautifulSoup(html, "lxml")
        images = []
        for img in soup.findAll('img'):
            images.append(img.get('src'))

        #Compiles only the relevant image urls
        new_images = []

        for x in images:
            if x[0:39] == '../../Handlers/Image.ashx?multiverseid=':
                new_images.append(x)

        print()
        print(images)
        print(new_images)

        #Establishes the beginning and end of the final url the bot posts
        first_image_url = 'http://gatherer.wizards.com/Handlers/Image.ashx?multiverseid='
        second_image_url = '&type=card'

        #If no card images are found
        if not new_images:
            await message.channel.send('[No Card Found]')

        #Chosen if a direct page is not found, a card is chooses randomly from the search list
        elif images[1] == '../../Images/ajax_indicator.gif':
            image_url = random.choice(new_images)

            image_url = image_url[39:]
            image_url = image_url[:-10]

            await message.channel.send(first_image_url + image_url + second_image_url)

        #Only -horizontal- dual cards are passed into here. May be buggy!
        elif (new_images[0][0:39] == '../../Handlers/Image.ashx?multiverseid=' and new_images[0][-27:] == '&type=card&options=rotate90'):

            image_url = str(new_images[0])
            image_url = image_url[39:]

            await message.channel.send(first_image_url + image_url)

        #Chosen if a direct page was found, and it prints all the cards on it
        else:
            print("Card found")
            #This removes certain images (ones turned awkwardly)
            for x in new_images:
                if x[-28:] == '&type=card&options=rotate270':
                    new_images.remove(x)

            for x in new_images:
                image_url = x[39:]
                image_url = image_url[:-10]



                #Gets the name of the card from the Wizards website
                wizards_url = 'https://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=' + image_url

                response = urllib.request.urlopen(wizards_url)

                html = response.read()

                html_lines = html.splitlines()

                del html_lines[:310]

                card_title = 'error'

                #Searches the list of HTML lines
                for x in html_lines:
                    if '<span id="ctl00_ctl00_ctl00_MainContent_SubContent_SubContentHeader_subtitleDisplay"' in str(x):

                        #Parses the HTML line using BS4
                        soup = BeautifulSoup(x, 'html.parser')
                        #Finds the span value inside the parsement
                        span = soup.find(id='ctl00_ctl00_ctl00_MainContent_SubContent_SubContentHeader_subtitleDisplay')

                        card_title = span.string

                print(card_title)

                #print(html_lines[314])
                #print(html_lines[315])
                #print(html_lines[316])

                #Takes the now retrieved card name and searches for it on TCG Player
                url_card_title = card_title.replace(' ', '%20')

                tcg_url = 'https://shop.tcgplayer.com/productcatalog/product/show?newSearch=false&ProductType=All&IsProductNameExact=false&ProductName=' + url_card_title

                tcg_response = urllib.request.urlopen(tcg_url)

                tcg_html = tcg_response.read()

                tcg_html_lines = tcg_html.splitlines()

                del html_lines[:1960]

                loop_count = 0

                for x in tcg_html_lines:
                    loop_count = loop_count + 1
                    #print(x)
                    if 'Market Price' in str(x):
                        #loop_count = loop_count + 1
                        break

                #card_price = tcg_html_lines[loop_count]

                #card_price = str(card_price)

                #card_price = card_price[46:]
                #card_price = card_price[:-6]

                #print(card_price)

                await message.channel.send(first_image_url + image_url + second_image_url + '\n' + card_title + " | **Market Price: **")






#Turns off SCRIPT
    if (message.content == '-sleep') and (message.author.id == REMOVED FOR GITHUB):
        await client.logout()





client.run(REMOVED FOR GITHUB)