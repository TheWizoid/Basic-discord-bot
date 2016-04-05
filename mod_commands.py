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


#Adding commands
def add_command(message):

    commands = pickle.load(open("commands.txt","rb"))
    commands_array = pickle.load(open("commands_array.txt","rb"))
    """
    Hypothetically, I could have the bot add commands to itself. What a world.
    """
    valid = True
    adding_command = message.content.split()
    adding_command[1] = adding_command[1].lower()
    if len(adding_command) < 3:
        return "Invalid amount of parameters"
    elif adding_command[1] in commands:
        return "That command already exists"
    else:
        if message.content.find("#random") != -1:
            try:
                number = int(message.content[message.content.find("#random")+7])
            except ValueError:
                return "Invalid #random value"
            except IndexError:
                return "Invalid #random value"
        command = adding_command[1]
        if "#" in command:
            command = command.replace("#", " ")
        if len(adding_command) == 3:
            pass
        else:
            for i in range(3,len(adding_command)):
                adding_command[2] += " " + adding_command[i]

        command_text = adding_command[2]
        commands[command] = command_text
        commands_array.append(command)

        pickle.dump(commands, open("commands.txt", "wb"))
        pickle.dump(commands_array, open("commands_array.txt", "wb"))
        return "Command added"


#Deleting commands
def delete_command(message, command):

    commands = pickle.load(open("commands.txt","rb"))
    commands_array = pickle.load(open("commands_array.txt","rb"))
    """
    There are times I may want to delete a command, when the user hasn't specified so.
    E.g. if a user creates an invalid command (such as using #random without a number), it will be deleted.
    """
    message.content = message.content.lower()
    if "#" in command:
        command = command.replace("#", " ")
    if command not in commands:
        yield from client.send_message(message.channel, "Command does not exist.")
    else:
        del commands[command]
        commands_array.remove(command)
        pickle.dump(commands, open("commands.txt", "wb"))
        pickle.dump(commands_array, open("commands_array.txt", "wb"))


#Editing/replacing commands
def edit_command(message):

    commands = pickle.load(open("commands.txt","rb"))
    commands_array = pickle.load(open("commands_array.txt","rb"))
    """
    Consistency with the command addition/deletion features.
    """
    rep_command = message.content.split()
    if rep_command[1] not in commands:
        return "That command does not exist to be replaced"
    else:
        if len(rep_command) < 3:
            return "Invalid amount of parameters"
        else:
            command = rep_command[1]
            if len(rep_command) == 3:
                pass
            else:
                for i in range(3,len(rep_command)):
                    rep_command[2] += " " + rep_command[i]

            command_text = rep_command[2]
            commands[command] = command_text

            pickle.dump(commands, open("commands.txt", "wb"))
            pickle.dump(commands_array, open("commands_array.txt", "wb"))

            return "Command replaced"
