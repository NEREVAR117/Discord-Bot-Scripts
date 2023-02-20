# Written Monday, April 15th, 2019 for casual D&D with friendos (REMOVED FOR GITHUB, etc)
# July 12, 2020 -- Updating the bot to support better dice roll mechanics for the REMOVED FOR GITHUB D&D campaign
# Original version was the basic -r mechanics (like flipping a coin) from the General Commands script, so it wasn't worth holding onto really
# August 8, 2020 -- Shuffled code around to a more organized state, added basic features like -map and -characters
# March 16, 2021 -- Added stat tracking dice rolls (between 1 and 20) for each person
# August 26, 2021 -- Structured code better, add support for multiple dice dolls (like 1d20+5, 1d8+4 outputting together)
# February 22, 2022 -- Optimized code some, added catches for maximum dice rolls to prevent people breaking the bot, catch for responses over discord's max message length

import discord
import asyncio
import random
import sqlite3

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure

import logging
logging.basicConfig(level=logging.INFO)

client = discord.Client()

#Prompts the console with start and login confirmation
@client.event
async def on_ready():
    print('Logged in as',client.user.name+'!')
    print('Client ID:',client.user.id)
    print('------')

    await client.change_presence(activity=discord.Game(name='with some dice'))

# The dice rolling logic built into a function
async def roll_logic(message):

    # Format:
    # -r AdX+C
    # -r 3d6 + 4 outputs 3 dice rolls, and provides the sum plus four

    # Establishes variables in format above in case none are mentioned
    A = 1
    C = 0

    # Removes spaces from the post
    modified_message = message.content.replace(" ", "")

    # Checks if there's a + number at the end
    modified_message = modified_message.split('+')

    # If there is a + number in the post, it assigns it to the appropriate variable
    if len(modified_message) > 1:
        C = int(modified_message[1])

    # Places the rest of the message back into string form
    modified_message = modified_message[0]

    # Splits the before and after d character
    modified_message = modified_message.split('d')

    # If there is number before the d character it assigns it here
    if modified_message[0] != '':
        A = int(modified_message[0])

    X = int(modified_message[1])

    # Prints coded form for testing
    print(str(A) + "d" + str(X) + "+" + str(C))

    # Prepares needed variables with a base value
    roll_results = ''
    roll_total = 0

    # Rolls dice (with value of X) A number of times, adds together, and creates initial message response
    for roll_count in range(A):
        roll_value = random.randint(1, X)

        roll_total = roll_total + roll_value
        roll_results = roll_results + str(roll_value) + ", "

    roll_results = roll_results[:-2]

    # Keeps the initial roll result for use later
    roll_results_keep = roll_results

    # Adds the + number part to the message and roll total (if there is one)
    if C != 0:
        roll_total = roll_total + C
        roll_results = roll_results + ' + ' + str(C)

    final_message = roll_results + " = " + str(roll_total)

    #print("Roll Results: " + final_message)

    #await message.channel.send("Roll Results: " + final_message)

    # Checks if this is done in the REMOVED FOR GITHUB discord. If it is, it updates to the player database their dice rolls
    if message.guild == REMOVED FOR GITHUB:

        # Only triggers if the dice being rolled is a 20-sided dice
        if X == 20:

            # We make a list for cases where there's multiple d20 dice being rolled
            roll_results_keep = roll_results_keep.replace(" ", "")
            multi_rolls = roll_results_keep.split(",")

            # Establishes the connection to the database and sets the cursor
            db_conn = sqlite3.connect('D&D_stats.db')
            theCursor = db_conn.cursor()

            # Cycle through the d20 results and input them into the database one at a time
            for dice_roll in multi_rolls:

                player_data = db_conn.execute("SELECT * FROM Members WHERE User_ID = " + str(message.author.id))
                player_data = player_data.fetchone()

                # Iterates into the player data's list to the proper location
                number_counter = player_data[int(dice_roll) + 2]

                number_counter += 1

                # Necessary for SQLite3 to trace to a numeric-only column name
                column_name = "'"
                column_name += dice_roll
                column_name += "'"

                db_conn.execute(f"UPDATE Members SET {column_name} = {number_counter} WHERE User_ID = {message.author.id}")
                db_conn.commit()


    return final_message





# Discord event trigger (aka if something happens and is updated to the client)
@client.event
async def on_message(message):

    # Establishes the connection to the database and sets the cursor
    db_conn = sqlite3.connect('D&D_stats.db')
    theCursor = db_conn.cursor()


    # We preserve the message in a list, exactly-how-it-is, so when people update their URLs it preserve capital letters
    uppercase_message_split = message.content.split()

    # Lowers the post to lowercase so caps don't keep people from doing commands
    message.content = message.content.lower()






    # IDs of the desired channel(s) you want the bot to only operate in (don't name it channel.id)
    channel_id = [REMOVED FOR GITHUB, REMOVED FOR GITHUB, REMOVED FOR GITHUB, REMOVED FOR GITHUB]

    # First checks if the message is even in the registered channel. This is done so not every message in the REMOVED FOR GITHUB server is passed through all the below checks.
    if message.channel.id in channel_id and message.author.id != REMOVED FOR GITHUB:























        # Adds user to the D&D database (CURRENTLY BROOOOOOOOOOKEN)
        if message.content.startswith('D&D join'):

            # Attempts to fetch the joining member's ID from the database (if it's there)
            check_if_present = db_conn.execute("SELECT User_ID FROM Members WHERE User_ID = " + str(message.author.id))
            check_if_present = check_if_present.fetchone()

            # Conditional statement if the member is in the database or not already
            if check_if_present != None:

                await message.channel.send('You\'re already in the D&D database.')

            elif check_if_present == None:
                db_conn.execute(
                    "INSERT INTO Members (User_ID, Username, Nickname, '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20') VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (message.author.id, message.author.display_name, "[Placeholder]", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0))
                db_conn.commit()

                await message.channel.send('Welcome to the D&D group! :)')



















        # Prints the current useable commands
        if message.content == 'help' and message.channel.id in channel_id:
            # avatar = message.author.avatar_url_as(static_format="png")
            embed = discord.Embed(color=0xff0000)
            # embed.set_thumbnail(url=avatar)
            embed.add_field(name="[Casual D&D Commands]", value="""
**coin** and **flip** return a heads or tails result
**roll** and **r** return a standard D20 result
**map** returns a link to the world map
**character(s)** and **char** return a list of character stat sheets
**update (link)** will update your character sheet's link
**rolls (irl name)** will show your rolled D20 statistics

For more advanced rolling please use the format **AdX+C**.
A being the number of dice, X being the maximum number on the dice itself,
and C being the modifier to the final results.
All variants (such as d4, or 4d6, d6+2, or 4d6+2 all work). Use ! or . at the
beginning or end to roll for advantage or disadvantage.
                    """, inline=False)
            await message.channel.send(embed=embed)
















        # Flips a coin for heads or tails
        if (message.content == 'coin' or message.content == 'flip') and message.channel.id in channel_id:
            coin_side = ['The coin landed on **heads**', 'The coin landed on **tails**']
            coin_random = random.randint(0, 1)
            await message.channel.send(coin_side[coin_random])
















        # Calls a server or specific member piechart related to various monetary values
        if message.content.startswith('rolls'):

            split_message = message.content.split()

            # If server is specified
            if split_message[1] == 'serverrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr':

                # Gets all current member data
                server_money = db_conn.execute("SELECT * FROM Members")
                server_money = server_money.fetchall()

                # Gets the total net worth of the server right now
                total_net_worth = 0
                for net_worth in server_money:
                    total_net_worth += net_worth[3]

                print("Total net worth is", total_net_worth)

                # Gets the percentages for each user
                net_worth_percentage = []
                for net_worth in server_money:
                    net_worth_percentage.append(round(net_worth[3] / total_net_worth * 100, 2))

                print("Sum of percentages should be 100, it is currently:", sum(net_worth_percentage))

                # Combines the user name with their money value
                name_and_net_worth = []
                for user in server_money:
                    name_and_value = str(user[2]) + " - "
                    name_and_value += str(user[3]) + "$"

                    name_and_net_worth.append(name_and_value)

                # labels = 'Frogs', 'Hogs', 'Dogs', 'Logs'
                # sizes = [15, 30, 45, 10]
                # explode = (0, 0.2, 0, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')

                # Makes the graph bigger (default is 3, 4)
                plt.figure(figsize=(10, 10))

                fig1, ax1 = plt.subplots()
                ax1.pie(net_worth_percentage, labels=name_and_net_worth, autopct='%1.1f%%', shadow=True, startangle=90)
                ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

                ax1.set_title("Server Total Users", fontsize=20)

                plt.savefig('pie.png')
                # plt.show()

                plt.clf()

                # channel = client.get_channel(REMOVED FOR GITHUB)
                await message.channel.send(file=discord.File('pie.png'))






            # If the server isn't specified (instead checking a user)
            else:

                irl_name = split_message[1]
                irl_name = irl_name.capitalize()

                # Gets all current member data from chosen irl name
                user_profile = db_conn.execute("SELECT * FROM Members WHERE Nickname = ?", (irl_name,))
                user_profile = user_profile.fetchone()

                # We assign the chosen dice rolled data to a list
                member_data = []

                member_data.append(user_profile[3])
                member_data.append(user_profile[4])
                member_data.append(user_profile[5])
                member_data.append(user_profile[6])
                member_data.append(user_profile[7])

                member_data.append(user_profile[8])
                member_data.append(user_profile[9])
                member_data.append(user_profile[10])
                member_data.append(user_profile[11])
                member_data.append(user_profile[12])

                member_data.append(user_profile[13])
                member_data.append(user_profile[14])
                member_data.append(user_profile[15])
                member_data.append(user_profile[16])
                member_data.append(user_profile[17])

                member_data.append(user_profile[18])
                member_data.append(user_profile[19])
                member_data.append(user_profile[20])
                member_data.append(user_profile[21])
                member_data.append(user_profile[22])

                # We get the total dice rolls
                total_rolls = sum(member_data)


                # We compile a list of the relevant data into a list with readable labels to be used in the final image
                member_data_labels = []

                member_data_labels.append("Ones: " + str(user_profile[3]))
                member_data_labels.append("Twos: " + str(user_profile[4]))
                member_data_labels.append("Threes: " + str(user_profile[5]))
                member_data_labels.append("Fours: " + str(user_profile[6]))
                member_data_labels.append("Fives: " + str(user_profile[7]))

                member_data_labels.append("Sixes: " + str(user_profile[8]))
                member_data_labels.append("Sevens: " + str(user_profile[9]))
                member_data_labels.append("Eights: " + str(user_profile[10]))
                member_data_labels.append("Nines: " + str(user_profile[11]))
                member_data_labels.append("Tens: " + str(user_profile[12]))

                member_data_labels.append("Elevens: " + str(user_profile[13]))
                member_data_labels.append("Twelves: " + str(user_profile[14]))
                member_data_labels.append("Thirteens: " + str(user_profile[15]))
                member_data_labels.append("Fourteens: " + str(user_profile[16]))
                member_data_labels.append("Fifteens: " + str(user_profile[17]))

                member_data_labels.append("Sixteens: " + str(user_profile[18]))
                member_data_labels.append("Seventeens: " + str(user_profile[19]))
                member_data_labels.append("Eighteens: " + str(user_profile[20]))
                member_data_labels.append("Nineteens: - " + str(user_profile[21]))
                member_data_labels.append("Twenties: - " + str(user_profile[22]))


                # Sets the image size
                plt.figure(figsize=(10, 10))

                # Plot library functions / logic
                fig1, ax1 = plt.subplots()
                ax1.pie(member_data, labels=member_data_labels, autopct='%1.1f%%', shadow=True, startangle=90)
                ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

                # Title of the pie chart
                ax1.set_title(irl_name + "'s total rolls: " + str(total_rolls), fontsize=20)

                plt.savefig('pie.png')
                # plt.show()

                plt.clf()

                await message.channel.send(file=discord.File('pie.png'))


















        # Links players to the map for quick access
        if message.content == 'map' and message.channel.id in channel_id:

            # Gets data from the character sheets column for the map
            character_sheets = db_conn.execute("SELECT Sheet_URL FROM Character_sheets")
            character_sheets = character_sheets.fetchall()

            # Sends the stored map's URL in a message
            await message.channel.send(character_sheets[4][0])




















        # Links to the players' character sheets
        if (message.content == 'character' or message.content == 'characters' or message.content == 'char') and message.channel.id in channel_id:

            # Gets data from the character sheets column
            character_sheets = db_conn.execute("SELECT Sheet_URL FROM Character_sheets")
            character_sheets = character_sheets.fetchall()

            # Builds the output message
            output_message = 'Aedalan: '
            output_message += str(character_sheets[3][0])
            output_message += '\nAtlas: '
            output_message += str(character_sheets[2][0])
            output_message += '\nArdwyn: '
            output_message += str(character_sheets[0][0])
            output_message += '\nReja: '
            output_message += str(character_sheets[5][0])
            output_message += '\nWorlin: '
            output_message += str(character_sheets[1][0])

            # Sends the message
            await message.channel.send(output_message)

























        # Lets users update their character sheets (or map if it's REMOVED FOR GITHUB)
        if message.content.startswith('update'):

            # Checks if REMOVED FOR GITHUB (our DM) is updating the map or not. If it's the map being updated we do want it to be embedded when posted, so no < > brackets will be added
            if message.author.id == REMOVED FOR GITHUB:
                character_url = uppercase_message_split[1]

            else:
                character_url = "<" + uppercase_message_split[1] + ">"

            db_conn.execute("UPDATE Character_Sheets SET Sheet_URL = ? WHERE User_ID = ?", (character_url, message.author.id))
            db_conn.commit()

            await message.channel.send('Updated! :)')



















        # Rolls a standard d20 die and adds the output to the database
        if (message.content == 'roll' or message.content == 'r') and message.channel.id in channel_id:

            roll_result = random.randint(1, 20)

            player_data = db_conn.execute("SELECT * FROM Members WHERE User_ID = " + str(message.author.id))
            player_data = player_data.fetchone()

            # Iterates into the player data's list to the proper location
            number_counter = player_data[int(roll_result) + 2]

            number_counter += 1

            # Necessary for SQLite3 to trace to a numeric-only column name
            column_name = "'"
            column_name += str(roll_result)
            column_name += "'"

            db_conn.execute(f"UPDATE Members SET {column_name} = {number_counter} WHERE User_ID = {message.author.id}")
            db_conn.commit()

            await message.channel.send('You rolled a ' + str(roll_result) + ' out of 20.')



























        # Dice-rolling checks and function, message string is modified here

        # We first establish the base output message
        output_message = ''

        # Gets the total score and adds to it as we go through the dice rolls
        total_score = 0

        # Cycles through the various called dice rolls (if there are any)
        multiple_dice_rolls = message.content.split(",")

        for dice_roll in multiple_dice_rolls:

            # By re-assigning back to message.content I avoided having to change a lot of internal logic in the roll function. May backfire later on though
            message.content = dice_roll

            # Triggers if someone rolled with advantage
            if message.content[0] == '!' or message.content[-1] == '!':
                # Removes the ! from the message
                message.content = message.content.replace("!", "")

                # Rolls and displays roll results twice
                roll_1 = await roll_logic(message)
                roll_2 = await roll_logic(message)

                # Gets the roll results assigned to its own variable
                result_1 = roll_1.split("=")
                result_1 = int(result_1[1])

                result_2 = roll_2.split("=")
                result_2 = int(result_2[1])

                # Gets and assigns the higher score
                if result_1 >= result_2:
                    winning_result = result_1

                else:
                    winning_result = result_2

                # Compiles this part of the message to be displayed
                output_message = output_message + "\n\nAdvantage Roll: " + str(winning_result) + "\n"
                output_message = output_message + roll_1 + ",     " + roll_2

                # Adds to the total score
                total_score += int(winning_result)



            # Triggers if someone rolled with disadvantage
            elif message.content[0] == '.' or message.content[-1] == '.':

                # Removes the . from the message
                message.content = message.content.replace(".", "")

                # Rolls and displays roll results twice
                roll_1 = await roll_logic(message)
                roll_2 = await roll_logic(message)

                # Gets the roll results assigned to its own variable
                result_1 = roll_1.split("=")
                result_1 = int(result_1[1])

                result_2 = roll_2.split("=")
                result_2 = int(result_2[1])

                # Gets and assigns the higher score
                if result_1 <= result_2:
                    losing_result = result_1

                else:
                    losing_result = result_2

                # Compiles this part of the message to be displayed
                output_message = output_message + "\n\nDisadvantage Roll: " + str(losing_result) + "\n"
                output_message = output_message + roll_1 + ",     " + roll_2

                # Adds to the total score
                total_score += int(losing_result)



            # Triggers for a normal roll
            else:
                roll_result = await roll_logic(message)

                result = roll_result.split("=")
                result = result[1]

                # Changes output depending on if 1 dice was rolled, or more
                output_message = output_message + "\n\nNormal Roll:" + result + "\n" + roll_result

                total_score += int(result)



        # Compiles the final message to send to the channel, then sends it

        temp_message = "Total Roll Score: **" + str(total_score) + "**```"

        # Combines the final message response together before posting
        output_message = temp_message + output_message + "```"

        await message.channel.send(output_message)






















    #Turns off SCRIPT
    if (message.content == '-sleep') and (message.author.id == REMOVED FOR GITHUB):
        await client.logout()




client.run(REMOVED FOR GITHUB)



# Written Monday, April 15th, 2019
# Build v0.1

# Updated on July 12, 2020 to Build v0.2