#It works!
import asyncio
import discord
import json
import os
import pickle
import sys
import time
from datetime import datetime
from random import randint
import urllib.request
import urllib.response
import urllib.error

import points_stuff
import messages
import general_commands
import mod_commands
import chat_logging

#this block is for privacy :>
accinfo = open("name_and_pass.txt", "r") #opens txt of username;password
info = accinfo.read().split(";") #splits up username and password
accinfo.close()
#this block is for privacy :>

client = discord.Client()
client.login("username","password")

modlist = open("modlist.txt","r")
mod = modlist.read()#List of mods on 1 line, edit at your pleasure
mod = mod.split(";")
modlist.close()

#Main Body
@client.async_event
def on_message(message):
    global commands
    global commands_array
    global server
    global split_message
    global path

    split_message = message.content.split()
    server = str(message.server)
    path = server+"/{0}/".format(server)

    chat_logging.logging_consent(message)
    if "!chatlog" in message.content.lower():
        logging_chat = chat_logging.logging_config(message)
        if logging_chat != None:
            yield from client.send_message(message.author, logging_chat)
    
    adding_points = points_stuff.add_points(message)
    if adding_points != True:
        print("An error has occurred.")


    commands = pickle.load(open("commands.txt","rb"))
    commands_array = pickle.load(open("commands_array.txt","rb"))

    #General Commands
    result = general_commands.command_check(message)
    if result != None:
        yield from client.send_message(message.channel, result)

    #Adding commands
    if message.content.startswith("!addcom".casefold()):
        if message.author.name.lower() in mod:
            added_command = mod_commands.add_command(message)
            yield from client.send_message(message.channel, added_command)
        else:
            yield from client.send_message(message.author, "You do not have permission to perform that command.")

    #Replacing commands
    if message.content.startswith("!repcom".casefold()) or message.content.startswith("!editcom".casefold()):
        if message.author.name.lower() in mod:
            edited_command = mod_commands.edit_command(message)
            yield from client.send_message(message.channel, edited_command)
        else:
            yield from client.send_message(message.author, "You do not have permission to perform that command.")

    #Deleting commands
    if message.content.startswith("!delcom".casefold()):
        if message.author.name.lower() in mod:
            if len(split_message) < 2:
                yield from client.send_message(message.author, "Invalid amount of parameters")
            else:
                yield from mod_commands.delete_command(message,split_message[1])
                yield from client.send_message(message.channel, "Successfully deleted.")
        else:
            yield from client.send_message(message.author, "You do not have permission to perform that command.")

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
    if message.content.startswith("!live"):
        try:
            bot_message = general_commands.stream_live_check(message.content.split()[1])
        except IndexError:
            bot_message = general_commands.stream_live_check("r00kieoftheyear")
        yield from client.send_message(message.channel, bot_message)

    if message.content.startswith("!selfdestruct".casefold()):
        for i in range(10,-1,-1):
            if i == 0:
                yield from client.send_message(message.channel, ":boom: :man_with_turban: :boom: ")
                break
            yield from asyncio.sleep(1)
            yield from client.send_message(message.channel, "{}".format(i))

    #kill (only available to mods)
    if message.content.startswith("!kill".casefold()):
        if message.author.name.lower() in mod:
            yield from client.send_message(message.channel, "Barry Bot going down BibleThump /")
            os._exit(5)
        else:
            yield from client.send_message(message.author, "You do not have permission to perform that command.")

    #Rock, paper, scissors
    if message.content.startswith("!rps".casefold()) or message.content.startswith("!rockpaperscissors".casefold()):
        yield from general_commands.rock_paper_scissors(message)

    #!userpoints
    if message.content.startswith("!userpoints".casefold()):
        if len(split_message) < 2:
            client.send_message(message.author, "This command requires a user.")
        else:
            for i in range(2,len(split_message)):
                split_message[1] += " " + split_message[i]
            amount = points_stuff.user_points(message, split_message[1].casefold())
            yield from client.send_message(message.channel, amount)

    #!points
    if message.content.startswith("!points".casefold()):
        amount = points_stuff.see_points(message)
        yield from client.send_message(message.channel, amount)

    #!roulette
    if message.content.startswith("!roulette".casefold()):
        roulette_result = points_stuff.bet_points(message)
        yield from client.send_message(message.channel, roulette_result)

    #Lets perople give each other their points
    if message.content.startswith("!givepoints".casefold()):
        if len(split_message) >= 3:
            amount_given = points_stuff.give_points(message)
            yield from client.send_message(message.channel, amount_given)
        else:
            yield from client.send_message(message.author, "Invalid parameters")

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
    ##        yield from client.send_message(message.channel, "{}: ".format(message.author.name) + message.content)




@client.async_event
#Displays login name/id
def on_ready():
    print("Logged in as")
    print(client.user.name)
    print(client.user.id)

client.run(info[0],info[1])#0 is username, 1 is password.
