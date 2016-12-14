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

import messages
import general_commands
import mod_commands
import chat_logging
import points_stuff
#this block is for privacy :>
accinfo = open("name_and_pass.txt", "r") #opens txt of username;password
info = accinfo.read().split(";") #splits up username and password
accinfo.close()
#this block is for privacy :>

#Checks if the command is valid
def command_check(message):
    """
    Checks if a command is present at the beginning of a message.
    If it is in the array of commands, but not the dictionary (i.e there's no key which would cause an error)
    it is deleted. Otherwise, it simply checks if #user, #touser, #random, or #authorrandom are present in the command text.
    If #touser is present, it will direct the message towards the user, by mentioning their username.
    If #user is present, the second word will replace it. If there is more than one word after the command,
    all are included. If #user has not been entered, the bot will send a private message to the author: "Invalid parameters".
    If #random is present, a random number between 1 and the previously assigned value inclusive (e.g. !roll is #random6).
    If #random is present, but the command was added without a number (e.g. if !roll was simply #random, instead of #random6),
    it will send a message to the user stating that the command is not valid, as it does not contain a number to randomise.
    The command will then be deleted.
    Similar to how #random has a moderator defined maximum, #authorrandom has an author defined one.
    E.g. a moderator may type !addcom !random #authorrandom.
    This would allow anyone to type !random 6 and receive a number between 1 and 6 (inclusive), !random 900 to receive a random number
    between 1 and 900 etc.
    """
    try:
        commands = pickle.load(open("{}/commands.txt".format(str(message.server)),"rb"))
    except:
        #just a placeholder/default command to create the dictionary successfully
        commands = {"!memeschool":"https://www.youtube.com/watch?v=fJdA7dwx6-4"}
        pickle.dump(commands,open("{}/commands.txt".format(str(message.server)),"wb"))
    try:
        commands_array = pickle.load(open("{}/commands_array.txt".format(str(message.server)),"rb"))
    except:
        commands_array = []
        for i in commands:
            commands_array.append(i)
        pickle.dump(commands_array,open("{}/commands_array.txt".format(str(message.server)),"wb"))
    for i in commands_array:
        if message.content.lower().startswith(i):
            if i not in commands:
                commands_array.remove(i)
                pickle.dump(commands_array,open("{}/commands_array.txt".format(str(message.server)),"wb"))
            else:
                command_info = commands[i]
                list_message = message.content.split()
                if "<" not in command_info:
                    return commands[i]
                
                if "<user>" in command_info:
                    try:
                        for i in range(1,len(list_message)):
                            if i > 1:
                                list_message[1] += " " + list_message[i]
                        command_info = command_info.replace("<user>", list_message[1])
                    except IndexError:
                        command_info = command_info.replace("<user>", message.author.name)
                    return command_info

                if "<touser>" in command_info:
                    try:
                        command_info = command_info.replace("<touser>", str(message.author.name))
                        return  command_info
                    except IndexError:
                        return send_message(message.author, "Invalid parameters")


                if "<random>" in command_info:
                    try:
                        random_number = command_info[command_info.find("<random>")+7]
                        command_info = command_info.replace("<random>", str(randint(1,int(random_number))))
                        command_info = command_info.replace(random_number, "")
                        return  command_info
                        break
                    except IndexError:
                        delete_command(message, i)
                        return "The way this command was created is not valid, it has been deleted."

                if "<authorrandom>" in command_info:
                    try:
                        max_num = int(list_message[1])
                        command_info = command_info.replace("<authorrandom>", str(randint(1, max_num)))
                        return command_info
                    except ValueError:
                        return "That must be a number"
                    except IndexError:
                        return "Invalid parameters"


                


def list_commands(message):

    commands = pickle.load(open("{}/commands.txt".format(str(message.server)),"rb"))
    commands_array = pickle.load(open("{}/commands_array.txt".format(str(message.server)),"rb"))
    list_of_commands = []
    str_of_commands = ""
    for i in commands_array:
        try:
            list_of_commands.append(i)
        except KeyError:
            pass

    list_of_commands = sorted(list_of_commands)

    for i in list_of_commands:
        if "*" in i:
            edited = i.replace("*","\*")
            str_of_commands += edited + ", "
        elif "<user>" in commands[i]:
            str_of_commands += i + " <user>, "
        elif "<touser>" in commands[i]:
            str_of_commands += i +" <author>, "
        else:
            str_of_commands += i + ", "

    str_of_commands += "!givepoints, !points, !userpoints, !roulette, !messages, !usermessages <messages>, !commandinfo, !live <stream>, !rps/!rockpaperscissors, !selfdestruct, !kill\*, !addcom\*, !delcom\*, !editcom\* and !commands."
    return  "The following commands are available (* means mod only): " + str_of_commands


def command_info(message):
    commands = pickle.load(open("{}/commands.txt".format(str(message.server)),"rb"))
    commands_array = pickle.load(open("{}/commands_array.txt".format(str(message.server)),"rb"))
    split_message = message.content.split()
    if len(split_message) < 2:
        return "Invalid amount of parameters"
    else:
        command = split_message[1]
        if command not in commands:
            if command.startswith("!commands"):
                return "Displays a list of commands."

            elif command.startswith("!commandinfo"):
                return "Displays the info of the command, i.e what you're looking at now :P"

            elif command.startswith("!selfdestruct"):
                return "Counts down from 10 and selfdestructs."
            elif "points" in command:
                return "Point interaction"
            elif command.startswith("!addcom") or command.startswith("!delcom")\
             or command.startswith("!editcom") or command.startswith("!repcom"):
                alters_by = "add"
                if command[1] in "re": #replace/edit; r/e
                    alters_by = "replace"
                elif command[1] == "d":
                    alters_by = "delete"
                return "Mods can use this to {} commands.".format(alters_by)

            elif command.startswith("!rps") or command.startswith("!rockpaperscissors"):
                return "Used for playing a game of rock, paper, scissors."

            elif command.startswith("!kill"):
                return "Kills the bot."

            else:
                return "Command does not exist."

        elif commands[command].startswith("http://i.imgur"):
            return "Displays an image"
        else:
            return commands[command]

def rock_paper_scissors(message, user):

    if len(message.content.split()) == 1:
        return "Invalid choice"
    else:
        temp_message = message.content.split()
        choice = temp_message[1].lower()

        if choice == "stone":
            choice = "rock"
        elif choice == "scissor":
            choice = "scissors"

        if choice == "rock" or choice == "paper" or choice == "scissors":
            if len(message.content.split()) >= 3:
                try:
                    points_bet = int(message.content.split()[2])
                except:
                    if message.content.split()[2].lower() == "all":
                        points_bet = True
            else:
                points_bet = False

            bot_choice = randint(0,2)
            bc_array = ["rock","paper","scissors"]

            #Goes through all the combinations
            if bc_array[bot_choice] == choice:
                outcome = "\nTie"
            elif bot_choice == 0 and choice == "paper":
                outcome = "\nYou win!"
            elif bot_choice == 0 and choice == "scissors":
                outcome = "\nYou lose..."
            elif bot_choice == 1 and choice == "rock":
                outcome = "\nYou lose..."
            elif bot_choice == 1 and choice == "scissors":
                outcome = "\nYou win!"
            elif bot_choice == 2 and choice == "rock":
                outcome = "\nYou win!"
            elif bot_choice == 2 and choice == "paper":
                outcome = "\nYou lose..."
            points_message = ""
            if points_bet:
                points = points_stuff.load_points(message, user)
                if message.content.split()[2].lower() == "all":
                    points_bet = points[user]
                if points[user] - points_bet < 0:
                    return "You don't have enough points to bet FeelsEmoMan"
                if outcome == "\nYou win!":
                    points[user] += points_bet
                elif outcome == "\nTie":
                    pass
                else:
                    points[user] = points[user] - points_bet
                points_message = "\nYou now have {} points.".format(points[user])
                pickle.dump(points, open("{0}/{0}_points.txt".format(str(message.server)),"wb"))
            return "I choose " + bc_array[bot_choice] + outcome + points_message
        else:
            return "Invalid choice."


#Checking if a livestream on twitch is live
def stream_live_check(stream):

    url = "https://api.twitch.tv/kraken/streams/{}".format(stream.lower())

    try:
        contents = json.loads(urllib.request.urlopen(url).read().decode("utf-8"))
        if contents["stream"] == None:
            status = "offline"
            bot_message = "{} is offline.".format(stream)
        else:
            #print(contents)
            name = contents["stream"]["channel"]["name"]
            title = contents["stream"]["channel"]["status"]
            game = contents["stream"]["channel"]["game"]
            viewers = contents["stream"]["viewers"]
            bot_message = "{0} is online.\n{0}'s title is: {1} \n{0} is playing {2} \nThere are {3} viewers \n".format(name,title,game,viewers)

    except urllib.error.URLError as e:
        if e.reason == "Not found" or e.reason == "Unprocessable Entity":
            bot_message = "That stream doesn't exist."
        else:
            bot_message = "There was an error proccessing your request."

    return bot_message

def eight_ball():
    response = [
    "It is certain",
    "It is decidedly so",
    "Without a doubt",
    "Yes, definitely",
    "You may rely on it",
    "As I see it, yes",
    "Most likely",
    "Yes",
    "Signs point to yes",
    "Don't count on it",
    "My reply is no",
    "My sources say no",
    "Very doubtful"]
    index = randint(0,12)
    return response[index]
