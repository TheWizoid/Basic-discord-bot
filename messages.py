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
import general_commands
import points_stuff

def load_messages(message, user):

    user = user.lower()
    try:
        messages = pickle.load(open("{0}/{0}_messages.txt".format(message.server),"rb"))
    except FileNotFoundError:
        try:
            os.mkdir("{}".format(message.server))
        except FileExistsError:
            temp_messages = open("{0}/{0}_messages.txt".format(str(message.server)),"w")
            temp_messages.close()
        messages = {user: 0}
        pickle.dump(messages, open("{0}/{0}_messages.txt".format(message.server),"wb"))
    except EOFError:
        messages = {user: 0}
        pickle.dump(messages, open("{0}/{0}_messages.txt".format(message.server),"wb"))

    return messages

def message_amount(message):

    message.author.name = message.author.name.lower()
    messages = load_messages(message, message.author.name)

    pickle.dump(messages, open("{0}/{0}_messages.txt".format(message.server),"wb"))
    
    return messages[message.author.name]

def user_message_amount(message, user):

    user = user.lower()
    messages = load_messages(message, user)
    list_of_users = []

    for member in message.server.members:
        list_of_users.append(member.name.lower())

    if user not in messages and user not in list_of_users:
        return "That user doesn't exist."
    elif user in messages:
        return "{} has sent {} messages.".format(user, messages[user])
    elif user in list_of_users:
        messages[user] = 0
        return "{} has sent 0 messsages.".format(user)
