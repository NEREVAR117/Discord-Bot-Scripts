#Written Novemebr 18th, Sunday, 2018 for Leia (requested from Reddit). Ported code from Voice Channel DOTA 2 code
#

import discord
import asyncio
import random
import sqlite3
import sys

import logging
logging.basicConfig(level=logging.INFO)

client = discord.Client()

#Prompts the console with start and login confirmation
@client.event
async def on_ready():
    print('Logged in as',client.user.name+'!')
    print('Client ID:',client.user.id)
    print('------')

    #await client.change_presence(game=discord.Game(name='Under Development'))

    activity = discord.Activity(name="In Development", type=discord.ActivityType.playing)
    await client.change_presence(activity=activity)

    #await client.change_presence(activity=discord.Activity(name="Test"))


#All the actual logic (duh)
@client.event
async def on_message(message):
    #Establishes the connection to the database and sets the cursor
    db_conn = sqlite3.connect('leia_team_xp.db')
    theCursor = db_conn.cursor()


    #Creating the database and table
    if message.content.startswith('-leia database create'):
        def printDB():

            try:
                table = theCursor.execute("SELECT User_ID, Username, Team, Total_Points, Team_Red, Team_Blue FROM Members")

                for row in table:
                    print('User ID :', row[0])
                    print('Username :', row[1])
                    print('Current Team :', row[2])
                    print('Total Points :', row[3])
                    print('Team 1 Points:', row[4])
                    print('Team 2 Points::', row[5])
                    print('Team 3 Points:', row[6])
                    print('Team 4 Points::', row[7])

            except sqlite3.OperationalError:
                print("The Table Doesn't Exist")

            except:
                print("Couldn't Retrieve Data From Database")

        db_conn = sqlite3.connect('leia_team_xp.db')
        print("Database Created")

        theCursor = db_conn.cursor()

        try:
            db_conn.execute("CREATE TABLE Members(User_ID INTEGER NOT NULL, Username TEXT NOT NULL, Team TEXT NOT NULL, Total_Points INTEGER NOT NULL, Team_1 INTEGER NOT NULL, Team_2 INTEGER NOT NULL, Team_3 INTEGER NOT NULL, Team_4 INTEGER NOT NULL);")

            db_conn.commit()

            print("Table Created")

        except sqlite3.OperationalError:
            print("Table Couldn't Be Created")

        #db_conn.execute("INSERT INTO Members (User_ID, Username, Points, Last_Post) VALUES ('50', 'Mia', 500, date('now'))")

        db_conn.commit()

        printDB()

        db_conn.close()
        print("Database Closed")






    #Displays a helpful message of commands for admin
    if message.content == '-help' and message.author.id in (REMOVED FOR GITHUB, REMOVED FOR GITHUB) and message.guild.id == REMOVED FOR GITHUB:
        await message.channel.send('''```   You may use:
        -join     (-join Team_#)
        -leave    (leaves your team)
        -points   (checks your points)
        -teams    (displays the teams```''')

    #Displays a helpful message of commands for normal users
    if message.content == '-help' and message.author.id not in (REMOVED FOR GITHUB, REMOVED FOR GITHUB) and message.guild.id == REMOVED FOR GITHUB:
        await message.channel.send('''```   You may use:
        -join     (-join Team_#)
        -leave    (leaves your team)
        -points   (checks your points)
        -teams    (displays the teams```''')







    #This increments databased members by one point
    team = db_conn.execute("SELECT Team FROM Members WHERE User_ID = " + str(message.author.id))
    team = team.fetchone()

    #Only activates if the user is in the database
    if team != None:

        #Checks if the user has a chosen team
        if team[0] in ('Team_1', 'Team_2', 'Team_3', 'Team_4'):

            db_conn.execute("UPDATE Members SET %s = %s + 1 WHERE User_ID = %s" % (team[0], team[0], message.author.id))

            db_conn.execute("UPDATE Members SET Total_Points = Total_Points + 1 WHERE User_ID = " + str(message.author.id))
            db_conn.commit()








    #Adds user with chosen team to database
    if message.content.startswith('-join'):
        split_message = message.content.split()

        team = split_message[1]

        #Checks if the -join command is only 2 words
        if len(split_message) != 2:
            await message.channel.send(':no_entry_sign: That command needs to be in this format: `-join (team name)`')

        else:
            #Initial grabbing of potential team (if the user is in the database)
            check_if_present = db_conn.execute("SELECT Team FROM Members WHERE User_ID = " + str(message.author.id))
            check_if_present = check_if_present.fetchone()

            #Conditional statement if the member is in the database or not already
            if check_if_present != None:
                db_conn.execute("UPDATE Members SET Team = ? WHERE User_ID = ?", (team, message.author.id))
                db_conn.commit()

                await message.channel.send('User\'s chosen team was already in the database, and has been updated. :white_check_mark:')

            elif check_if_present == None:
                db_conn.execute("INSERT INTO Members (User_ID, Username, Team, Total_Points, Team_1, Team_2, Team_3, Team_4) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (message.author.id, message.author.display_name, team, 0, 0, 0, 0, 0))
                db_conn.commit()

                await message.channel.send('User\'s chosen team has been added to the database. :white_check_mark:')






    #User removes themself from their team
    if message.content == '-leave':

        check_if_present = db_conn.execute("SELECT Team FROM Members WHERE User_ID = " + str(message.author.id))
        check_if_present = check_if_present.fetchone()

        #Checks first if the user is in the database
        if check_if_present == None or check_if_present[0] == 'No Team':

            await message.channel.send('You already don\'t have a chosen team. :no_entry_sign:')

        else:
            team = 'No Team'

            db_conn.execute("UPDATE Members SET Team = ? WHERE User_ID = ?", (team, message.author.id))
            db_conn.commit()

            await message.channel.send('You have abandoned your team. :white_check_mark:')







    #Displays the teams and information
    if message.content == '-teams':
        await message.channel.send('Team 1\nTeam 2\nTeam 3\nTeam 4')





    #Gets the user's points
    if message.content == '-points':

        total_points = db_conn.execute("SELECT Total_Points FROM Members WHERE User_ID = " + str(message.author.id))
        total_points = total_points.fetchone()

        team_1_points = db_conn.execute("SELECT Team_1 FROM Members WHERE User_ID = " + str(message.author.id))
        team_1_points = team_1_points.fetchone()

        team_2_points = db_conn.execute("SELECT Team_2 FROM Members WHERE User_ID = " + str(message.author.id))
        team_2_points = team_2_points.fetchone()

        team_3_points = db_conn.execute("SELECT Team_3 FROM Members WHERE User_ID = " + str(message.author.id))
        team_3_points = team_3_points.fetchone()

        team_4_points = db_conn.execute("SELECT Team_4 FROM Members WHERE User_ID = " + str(message.author.id))
        team_4_points = team_4_points.fetchone()

        await message.channel.send('Total points: %s\n\nTeam 1 Points: %s\nTeam 2 Points: %s\nTeam 3 Points: %s\nTeam 4 Points: %s' % (total_points[0], team_1_points[0], team_2_points[0], team_3_points[0], team_4_points[0]))













#Turns off SCRIPT
    if message.content == '-sleep' and message.author.id == REMOVED FOR GITHUB:
        await client.logout()




client.run(REMOVED FOR GITHUB)