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

def logging_config(message):
    modlist = open("modlist.txt","r")
    mod = modlist.read()
    mod = mod.split(";")
    modlist.close()

    if message.content.startswith("!chatlogoff".casefold()) and message.author.name in mod:
        logging_consent = open("{0}_logging_chat.txt".format(message.server),"w")
        logging_consent.write("False")
        logging_consent.close()
        return "Chatlogging off"

    if message.content.startswith("!chatlogon".casefold()) and message.author.name in mod:
        logging_consent = open("{0}_logging_chat.txt".format(message.server),"w")
        logging_consent.write("True")
        logging_consent.close()
        return "Chatlogging on"


#Checks if logging is allowed on the message.server
def logging_consent(message):

    #Chat logger Doesn't work with uploads (displays as a space after the name)
    try:
        logging_consent = open("{0}_logging_chat.txt".format(message.server),"r")

    except FileNotFoundError or OSError:
        logging_consent = open("{0}_logging_chat.txt".format(message.server),"w")
        logging_consent.write("True")
        logging_consent.close()
        logging_consent = open("{0}_logging_chat.txt".format(message.server),"r")

    logging_chat = logging_consent.read()
    logging_consent.close()

    if logging_chat == "True":
        chatlog = open("{0}_chatlog.txt".format(message.server),"a")

        time = str(datetime.now())
        try:
            chatlog.write("[" +time[0:19]+ "]"+ message.author.name + ":" + message.content + "\n")#slicing the string is easier than specifying hh:mm:ss lol
        except UnicodeEncodeError: #If an emoji is present, it adds one to the amount of that emoji in a dictionary.
            ##DOESN'T WORK YET
            ##DOESN'T WORK YET
            emoji_dict = pickle.load(open("emoji_amount.txt","rb"))
            start = int("1f1e6", 16)
            end = int("1f93f", 16) #1 higher than actual end for easier formatting
            for i in range(start,end):
                temp = str.lower(hex(i)[4:10])
                if temp in message.content:
                    value = hex(i)
                    emoji_dict[value] += 1
                    break
            non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)
            print(emoji_dict["0x1f603"])
            print(emoji_dict["0x1f604"])

            pickle.dump(emoji_dict,open("emoji_amount.txt","wb"))
            replaced = str(message.content).translate(non_bmp_map)#should replace the emoji with a placeholder char, but doesn't?
            chatlog.write("[" +time[0:19]+ "]"+ message.author.name + ":" + replaced + "\n")

        chatlog.close()#emojis cause an error, as they are inputted as text, but don't make a unicode character
