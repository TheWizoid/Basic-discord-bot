#It works!
import asyncio
import discord
import json
import oauth2
import os
import pafy
import pickle
import simplejson
import sys
import time
from datetime import datetime
from random import randint
import urllib
import urllib.request
import urllib.response
import urllib.error
import youtube_dl

import points_stuff
import messages
import general_commands
import mod_commands
import chat_logging
import music

client = discord.Client()

modlist = open("modlist.txt","r")
mod = modlist.read()#List of mods on 1 line, edit at your pleasure
mod = mod.split(";")
modlist.close()

#Main Body
@client.async_event
def on_message(message):
    split_message = message.content.split()
    server = str(message.server)
    message.author.name = message.author.name.lower()
    message_author = message.author.name

    chat_logging.logging_consent(message)
    if "!chatlog" in message.content.lower():
        logging_chat = chat_logging.logging_config(message)
        if logging_chat != None:
            yield from client.send_message(message.author, logging_chat)

    adding_points = points_stuff.add_points(message)
    if adding_points != True:
        print("An error has occurred.")

    #General Commands
    result = general_commands.command_check(message)
    if result != None:
        yield from client.send_message(message.channel, result)

    #Adding commands
    if message.content.startswith("!addcom".casefold()):
        if message_author in mod:
            added_command = mod_commands.add_command(message)
            yield from client.send_message(message.channel, added_command)
        else:
            yield from client.send_message(message.author, "You do not have permission to perform that command.")

    #Replacing commands
    if message.content.startswith("!repcom".casefold()) or message.content.startswith("!editcom".casefold()):
        if message_author in mod:
            edited_command = mod_commands.edit_command(message)
            yield from client.send_message(message.channel, edited_command)
        else:
            yield from client.send_message(message.author, "You do not have permission to perform that command.")

    #Deleting commands
    if message.content.startswith("!delcom".casefold()):
        if message_author in mod:
            if len(split_message) < 2:
                yield from client.send_message(message.author, "Invalid amount of parameters")
            else:
                mod_commands.delete_command(message,split_message[1])
                yield from client.send_message(message.channel, "Successfully deleted.")
        else:
            yield from client.send_message(message.author, "You do not have permission to perform that command.")

    #Banning
    if message.content.startswith("!ban".casefold()):
        if message_author in mod:
            if len(split_message) < 2:
                yield from client.send_message(message.author, "Invalid user")
            else:
                try:
                    for member in message.server.members:
                        split_message[1] = split_message[1].replace("<", "")
                        split_message[1] = split_message[1].replace(">", "")
                        split_message[1] = split_message[1].replace("@", "")#strips the string down to the id of the member
                        if split_message[1] in member.id:#is this the member that you want to ban?
                            yield from client.ban(member)
                            yield from client.send_message(message.channel, "{} Has been banned from the server".format(split_message[1]))
                            break
                except:
                    yield from client.send_message(message.author, "That user does not exist")


    #Command info
    if message.content.startswith("!commandinfo".casefold()):
        command_info = general_commands.command_info(message)
        yield from client.send_message(message.channel, command_info)


    #!commands
    if message.content.startswith("!commands".casefold()):
        list_of_commands = general_commands.list_commands(message)
        yield from client.send_message(message.channel, list_of_commands)

    #is it?
    if message.content.startswith("!itis".casefold()):
        number = randint(1,10)
        if number % 4 == 0:
            yield from client.send_message(message.channel, "Is it?")
        else:
            yield from client.send_message(message.channel, "It isn't")

    #Checking if a stream is live using urllib and json
    if message.content.startswith("!live".casefold()):
        try:
            bot_message = general_commands.stream_live_check(message.content.split()[1])
        except IndexError:
            bot_message = general_commands.stream_live_check("r00kieoftheyear")
        yield from client.send_message(message.channel, bot_message)

    if message.content.startswith("!info".casefold()):
        roles = ""
        for i in range(len(message.author.roles)):
            message.author.roles[i] = str(message.author.roles[i]).replace("@", "")
            roles += message.author.roles[i] + " "

        bot_message = "```"
        bot_message += "ID: {}\n".format(message.author.id)
        bot_message += "Username: {0} and {1}\n".format(message.author, message.author.name)
        bot_message += "Account created: {}\n".format(message.author.created_at)
        bot_message += "Date joined: {}\n".format(message.author.joined_at)
        bot_message += "Roles: {}\n".format(roles)
        bot_message += "Your avatar is {}\n```".format(message.author.avatar_url)
        yield from client.send_message(message.channel, bot_message)

    if message.content.startswith("!serverinfo".casefold()):
        bot_message = "Name: {}\n".format(message.server.name)
        bot_message += "Server Owner: {}\n".format(message.server.owner.name)
        bot_message += "ID: {}\n".format(message.server.id)
        bot_message += "Region: {}\n".format(message.server.region)
        bot_message += "Server Picture: {}\n".format(message.server.icon_url)
        temp = ""
        for i in message.server.roles:
            temp += i.name.replace("@", "") + ", "
        bot_message += "Available Roles: {}\n".format(temp)

        bot_message += "AFK Timeout: {}\n".format(message.server.afk_timeout)

        temp = ""
        for i in message.server.channels:
            temp += i.name + ", "
        bot_message += "Channels: {}\n".format(temp)
        temp = ""
        for i in message.server.members:
            temp += i.name+ "\n"
        bot_message += "Members: {}\n".format(temp)

        yield from client.send_message(message.author, bot_message)

    if message.content.startswith("!selfdestruct".casefold()):
        for i in range(10,-1,-1):
            if i == 0:
                yield from client.send_message(message.channel, ":boom:")
                break
            yield from asyncio.sleep(1)
            yield from client.send_message(message.channel, "{}".format(i))

    #kill (only available to mods)
    if message.content.startswith("!kill".casefold()):
        if message_author in mod:
            yield from client.send_message(message.channel, "Barry Bot going down")
            os._exit(5)
        else:
            yield from client.send_message(message.author, "You do not have permission to perform that command.")

    #Rock, paper, scissors
    if message.content.startswith("!rps".casefold()) or message.content.startswith("!rockpaperscissors".casefold()):
        result = general_commands.rock_paper_scissors(message, message.author.name)
        yield from client.send_message(message.channel, result)

    #!userpointsc
    if message.content.startswith("!userpoints".casefold()):
        if len(split_message) < 2:
            client.send_message(message.author, "This command requires a user.")
        else:
            for i in range(2,len(split_message)):
                split_message[1] += " " + split_message[i]
            amount = points_stuff.user_points(message, split_message[1])
            yield from client.send_message(message.channel, amount)

    #!points
    if message.content.startswith("!points".casefold()):
        amount = points_stuff.see_points(message)
        yield from client.send_message(message.channel, amount)

    #!roulette
    if message.content.startswith("!roulette".casefold()):
        message.content = message.content.lower()
        roulette_result = points_stuff.bet_points(message)
        yield from client.send_message(message.channel, roulette_result)

    #Lets perople give each other their points
    if message.content.startswith("!givepoints".casefold()):
        if len(split_message) >= 3:
            amount_given = points_stuff.give_points(message)
            yield from client.send_message(message.channel, amount_given)
        else:
            yield from client.send_message(message.author, "Invalid parameters")

    #Allows mods abuse
    if message.content.startswith("!setpoints".casefold()):
        if message_author in mod:
            points_set_to = points_stuff.set_points(message)
            yield from client.send_message(message.channel, points_set_to)
        else:
            yield from client.send_message(message.author, "You must be a mod to use this command")

    #Let's a user see the amount of messages they've sent since this has been added (26/5/2016)
    if message.content.startswith("!messages".casefold()):
        amount = messages.message_amount(message)
        yield from client.send_message(message.channel, "You have sent {} messages.".format(amount))

    if message.content.startswith("!usermessages".casefold()):
        if len(split_message) < 2:
            client.send_message(message.author, "This command requires a user.")
        else:
            for i in range(2,len(split_message)):
                split_message[1] += " " + split_message[i]
            messages_sent = messages.user_message_amount(message, split_message[1].casefold())
            yield from client.send_message(message.channel, messages_sent)


    ##    if "asdfgh" in message.content: #is censoring possible?
    ##        message.content = message.content.replace("asdfgh","memes")#yes, apparently
    ##        yield from client.delete_message(message)
    ##        yield from client.send_message(message.channel, "{}: ".format(message_author) + message.content)
    if message.content.startswith("!songrequest") and len(split_message) >= 2:
        song_added = music.add_song(message)
        yield from client.send_message(message.channel, song_added)

    if message.content.startswith("!songson") or (message.content.startswith("!skipsong") and message.content.user.lower() in mod):
        try:
            voice = yield from client.join_voice_channel(message.author.voice_channel)
        except discord.errors.ClientException:
            pass#voice = yield from client.move_to(message.author.voice_channel)
        #print(songlist)
        songlist = pickle.load(open("{0}/{0}_songlist.txt".format(str(message.server)),"rb"))
        while len(songlist) > 0:
            songlist = pickle.load(open("{0}/{0}_songlist.txt".format(str(message.server)),"rb"))
            player = yield from voice.create_ytdl_player(songlist[0])
            url = songlist[0]
            video = pafy.new(url)
            player.start()
            del songlist[0]
            pickle.dump(songlist,open("{0}/{0}_songlist.txt".format(str(message.server)),"wb"))
            yield from client.send_message(message.channel, "Now playing: **{0}**\nIt is **[{1}]** long.".format(video.title,video.duration[3:len(video.duration)]))
            yield from asyncio.sleep(video.length+1)


    if message.content.startswith("!songlist") or message.content.startswith("!queue"):
        songlist = music.get_queue(message)
        yield from client.send_message(message.channel, songlist)

    if message.content.startswith("!8ball") and len(split_message) > 2:
        bot_message = general_commands.eight_ball(message)
        yield from client.send_message(message.channel, bot_message)

@client.async_event
#Displays login name/id
def on_ready():
    print("Logged in as")
    print(client.user.name)
    print(client.user.id)

client.run("token")
