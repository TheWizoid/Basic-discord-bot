import asyncio
import discord
import simplejson
import os
import pafy
import pickle
import sys
import time
from datetime import datetime
from random import randint
import urllib.request
import urllib.response
import urllib.error
import urllib
import youtube_dl

import points_stuff
import messages
import general_commands
import mod_commands
import chat_logging

modlist = open("modlist.txt","r")
mod = modlist.read()#List of mods on 1 line, edit at your pleasure
mod = mod.split(";")
modlist.close()

def add_song(message):
    split_message = message.content.split()
    song = split_message[1]
    try:
        songlist = pickle.load(open("{0}/{0}_songlist.txt".format(str(message.server)),"rb"))
    except EOFError:
        songlist = []
        pickle.dump(songlist, open("{0}/{0}_songlist.txt".format(str(message.server)),"wb"))
    except FileNotFoundError:
        try:
            os.mkdir("{}".format(message.server))
        except FileExistsError:
            songlist = open("{0}/{0}_songlist.txt".format(str(message.server)),"wb")
            songlist.close()
        songlist = pickle.load(open("{0}/{0}_songlist.txt".format(str(message.server)),"rb"))
    if "youtu.be/" in song or "youtube.com" in song:
        video = pafy.new(song)
        if video.length <= 600:
            songlist.append(song)
        else:
            return "Songs must 10 minutes or less"
    else:
        return "Invalid song request"
    for i in range(len(songlist)):
        songlist[i] = str(songlist[i])
    pickle.dump(songlist, open("{0}/{0}_songlist.txt".format(str(message.server)), "wb"))

    return "Your song has been added"

#Fixed
def get_queue(message):
    bot_message = "The current queue is:\n"
    songlist = pickle.load(open("{0}/{0}_gachilist.txt".format(str(message.server)),"rb"))
    print(songlist)
    for i in songlist:
        video = pafy.new(i)
        title = video.title
        bot_message += "**{}**\n".format(title)
    return bot_message
