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
        if "&" in song:
            return "No playlist or time links"
        songlist.append(song)
    else:
        return "Invalid song request"
    for i in range(len(songlist)):
        songlist[i] = str(songlist[i])
    pickle.dump(songlist, open("{0}/{0}_songlist.txt".format(str(message.server)), "wb"))
    #json = simplejson.load(urllib.urlopen(song))
    return "Your song has been added"

#I'll fix it sometime soon 
def get_queue(message):
    bot_message = "The current queue is:\n"
    songlist = pickle.load(open("{0}/{0}_songlist.txt".format(str(message.server)),"rb"))
    id_list = []
    for i in range(len(songlist)):
        id_list += songlist[i][len(songlist[i])-11:len(songlist[i])]
    print(id_list)
    for i in range(len(id_list)):
        song_id = songlist[i][len(songlist[i])-11:len(songlist[i])]
        url = 'https://youtube.com/watch?v={0}'.format(song_id)
        video = pafy.new(url)
        title = video.title
        bot_message += "**{}**\n".format(title)
    return bot_message
