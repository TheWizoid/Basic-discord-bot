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
#Loads a dictionary of all the points
def load_points(message, user):

    user = user.lower()
    try:
        points = pickle.load(open("{0}points.txt".format(message.server),"rb"))
    except FileNotFoundError:
        points = {user: 0}
        pickle.dump(points, open("{0}points.txt".format(message.server),"wb"))
    except EOFError:
        points = {user: 0}
        pickle.dump(points, open("{0}points.txt".format(message.server),"wb"))

    return points



#Point interaction
def add_points(message):
    """
    Every time someone sends a message, they gain one point.
    This is because any time based ones would result in mobile users having
    the same amount of each, due to idling.
    """
    split_message = message.content.split()

    message.author.name = message.author.name.lower()
    points = load_points(message, message.author.name)
    message_amount = messages.load_messages(message, message.author.name)

    non_trigger = ["!points","!roulette","!userpoints","!givepoints","!barryroulette"]
    non_message_trigger = ["!usermessages","!messages"]

    if message.author.name not in message_amount:
        message_amount[message.author.name] = 0
    elif split_message[0] not in non_message_trigger:
        message_amount[message.author.name] += 1

    if message.author.name not in points:
        points[message.author.name] = 0
    elif split_message[0] not in non_trigger:
        points[message.author.name] += 1

    pickle.dump(points, open("{0}points.txt".format(message.server),"wb"))
    pickle.dump(message_amount, open("{0}_messages.txt".format(message.server),"wb"))
    return True

#Sets emotes in points, is its own function due to me using it twice.
def set_emote(message, points):

    if points[message.author.name] == 0:
        emote = "FeelsEmoMan"
    elif points[message.author.name] > 9000:
        emote = "forsenSS"
    elif points[message.author.name] >= 1000:
        emote = "PogChamp"
    elif points[message.author.name] == 420:
        emote = "CiGrip"
    else:
        emote = "FeelsGoodMan"

    return emote


#See your own points
def see_points(message):
    points = load_points(message, message.author.name.lower())

    emote = set_emote(message, points)

    if points[message.author.name] != 1:
        pickle.dump(points, open("{0}points.txt".format(message.server),"wb"))
        return "{}: You have {} points {}".format(message.author,points[message.author.name],emote)
    else:
        pickle.dump(points, open("{0}points.txt".format(message.server),"wb"))
        return "{}: You have {} point {}".format(message.author,points[message.author.name],emote)



#!roulette
def bet_points(message):
    split_message = message.content.split()

    user = message.author.name
    points = load_points(message, user)

    if len(split_message) < 2:
        return "You must roulette *something*."
    else:
        try:
            if split_message[1] == "all".casefold():
                if message.author.name not in points:
                    points[message.author.name] = 0
                    amount = 0
                else:
                    amount = points[message.author.name]

            else:
                amount = int(split_message[1])
            if amount == 0 and points[message.author.name] == 0:
                return "You don't have any points FeelsEmoMan"
            elif amount == 0:
                return "You must roulette *something*."
            elif amount < 0:
                return "You cannot roulette negative points. "
            else:
                if amount > points[message.author.name]:
                    return "You don't have enough points FeelsEmoMan"
                else:
                    random_integer = randint(0,3)
                    if random_integer < 2:
                        outcome = "wins"
                        points[message.author.name] += amount
                        emote = "FeelsGoodMan"
                    else:
                        outcome = "loses"
                        points[message.author.name] -= amount
                        emote = "FeelsEmoMan"
                    pickle.dump(points, open("{0}points.txt".format(message.server),"wb"))
                    return"{} {} {} points! {}\nYou now have {} points.".format(message.author, outcome, amount, emote, points[message.author.name])
        except ValueError:
            return "Invalid amount."




#See someone else's points
def user_points(message, user):

    user = user.lower()
    points = load_points(message, user)
    list_of_users = []

    for member in message.server.members:
        list_of_users.append(member.name.lower())
    #print(list_of_users)

    if user not in points and user not in list_of_users:
        return "That user doesn't exist."
    elif user in points:
        emote = set_emote(message, points)
    elif user in list_of_users:
        emote = "FeelsEmoMan"
        points[user] = 0

    pickle.dump(points, open("{0}points.txt".format(message.server),"wb"))
    return "{} has {} points {}".format(user, emote)


#Allows mods to give users points
def give_points(message):
    modlist = open("modlist.txt","r")
    mod = modlist.read()#List of mods on 1 line, edit at your pleasure
    mod = mod.split(";")
    modlist.close()

    split_message = message.content.split()

    amount = split_message[1]
    user = split_message[2].lower()

    points = load_points(message, user)


    if len(split_message) < 3:
        return "Invalid parameters"
    elif len(split_message) > 3:
        for i in range(3,len(split_message)):
            user += " " + split_message[i].lower()
    try:
        amount = int(amount)
        amount = abs(amount)
    except ValueError:
        return "The 1st term must be a whole number."

    if message.author.name.lower() in mod:
        try:
            points[user] += amount
            return "{} was just given {} points by {}, and now has {} points!".format(user,amount,message.author,points[user])
        except KeyError:
            return "That user doesn't exist."
    else:
        points[message.author.name.lower()] -= amount
        if points[message.author.name.lower()] < 0:
            return "You don't have enough points to give away."
            points[message.author.name.lower()] += amount
        else:
            points[user] += amount
            pickle.dump(points, open(message.server+"points.txt","wb"))
            return "{} was just given {} points by {}, and now has {} points!".format(user,amount,message.author,points[user])
