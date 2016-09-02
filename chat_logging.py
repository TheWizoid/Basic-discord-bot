import asyncio
import discord
import json
import os
import pickle
import sys
import time
from datetime import datetime
from random import randint
import unicodedata
import urllib
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
        try:
            logging_consent = open("{0}/{0}_logging_chat.txt".format(message.server),"w", encoding="utf-8")
        except FileNotFoundError:
            os.mkdir("{}".format(message.server))
        logging_consent = open("{0}/{0}_logging_chat.txt".format(message.server),"w",encoding="utf-8")
        logging_consent.write("False")
        logging_consent.close()
        return "Chatlogging off"

    if message.content.startswith("!chatlogon".casefold()) and message.author.name in mod:
        try:
            logging_consent = open("{0}/{0}_logging_chat.txt".format(message.server),"w",encoding="utf-8")
        except FileNotFoundError:
            os.mkdir("{}".format(message.server))
        logging_consent = open("{0}/{0}_logging_chat.txt".format(message.server),"w",encoding="utf-8")
        logging_consent.write("True")
        logging_consent.close()
        return "Chatlogging on"


#Checks if logging is allowed on the message.server
def logging_consent(message):
    try:
        logging_consent = open("{0}/{0}_logging_chat.txt".format(message.server),"r",)
        for i in logging_consent:
            if i == "":
                raise FileNotFoundError
    except:
        try:
            os.mkdir("{}".format(message.server))
        except:
            pass
        logging_consent = open("{0}/{0}_logging_chat.txt".format(message.server),"w",encoding="utf-8")
        logging_consent.write("True")

    logging_consent.close()
    logging_consent = open("{0}/{0}_logging_chat.txt".format(message.server),"r",)
    logging_chat = logging_consent.read()
    logging_consent.close()

    if logging_chat == "True":
        chatlog = open("{0}/{0}_chatlog.txt".format(message.server),"a",encoding="utf-8")
        try:
            message.content += (" " + str(message.attachments[0]["url"]))
            url = str(message.attachments[0]["url"])
            file_name = url.split('/')[-1]
            response = urllib.request.urlopen("{}".format(url))
            #Discord doesn't allow me to download files?
            response_temp = response.read()
        except:
            pass
        print("[{}]{}:{}".format(message.server,message.author.name,message.content))
        try:
            start = int("1f1e6", 16)
            end = int("1f93f", 16)
            emoji_dict = pickle.load(open("{}/emoji_amount.txt".format(str(message.server)),"rb"))
        except:
            pickle.dump({},open("{}/emoji_amount.txt".format(str(message.server)),"wb"))
            emoji_dict = pickle.load(open("{}/emoji_amount.txt".format(str(message.server)),"rb"))

            for i in range(start,end):
                emoji_dict[i] = 0
        """
        unicode_message_content = str.encode(message.content,"utf-8")
        print(unicode_message_content)
        if bytes(128515) in unicode_message_content:
            print("PogChamp")
        print(bytes(128515))
        print(bytes("64",encoding="utf-8"))

        for i in range(start,end):#still doesn't work
            temp = int(str.lower(hex(i)),16)
            if bytes(temp) in unicode_message_content:
                emoji_dict[temp] += 1

        print(emoji_dict)
        #print(emoji_dict["0x1f604"])

        pickle.dump(emoji_dict,open("{}/emoji_amount.txt".format(str(message.server)),"wb"))
        """
        chatlog.write("[" +str(message.timestamp)[0:19]+ "]"+ message.author.name + ":" + message.content + "\n")
        chatlog.close()
