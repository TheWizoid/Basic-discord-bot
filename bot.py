#It works!

import logging
import datetime
import discord
import asyncio
import os
from random import randint


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

@client.async_event
def on_message(message):
    #Chat logger Doesn't work with uploads (displays as a space after the name)
    
    logging_consent = open("logging_chat.txt","r")
    logging_chat = logging_consent.read()
    logging_consent.close()
    #print(message.server) #prints the server name, for adding servers and their logfiles/debugging
    if message.content.startswith("!chatlogoff".casefold()) and message.author.name in mod: 
        yield from client.send_message(message.channel, "Chatlogging off" )
        logging_consent = open("logging_chat.txt","w")
        logging_consent.write("False")
        logging_consent.close()
        
    if message.content.startswith("!chatlogon".casefold()) and message.author.name in mod:
        yield from client.send_message(message.channel, "Chatlogging on")
        logging_consent = open("logging_chat.txt","w")
        logging_consent.write("True")
        logging_consent.close()
        
    if logging_chat == "True":
        message.server = str(message.server)
        
        if message.server == "r00kieboys":
            chatlog = open("r00kie_chatlog.txt","a")
        elif message.server == "need for pleb":
            chatlog = open("lads_chatlog.txt","a")
        elif message.server == "Bot test":
            chatlog = open("test_chatlog.txt","a")
            
        time = str(datetime.datetime.now())
        
        chatlog.write("["+time[0:19]+"]"+message.author.name+":"+message.content+"\n")#slicing the string is easier than importing gmtime and specifying hh:mm:ss lol
        chatlog.close()
        
    #General stuff

    commands = {
        #General
        "!online": "Barry bot is online",
        "!memeschool": "https://www.youtube.com/watch?v=fJdA7dwx6-4",
        "!command": "you really expect me to list all these? Bloody hell",
        "!mod": "Never mod FeelsBadMan",
        "!g4g": "http://www.gamingforgood.net/s/r00kieoftheyear#donate MingLee",
        "!kek": "top kek xD",
        "!topkek": "top kek xD",
        "!age": "PedoBear",
        #People
        "!chris": "Abusive uncle Chris DansGame",
        "!eladia": "We miss you BibleThump",
        "!kieran": "http://i.imgur.com/37274Z1.jpg oi oi kieran",
        "!nick": "NIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIICK! Kreygasm",
        "!sogyoh": "TriHard I am so fucking zooted right now CiGrip",
        #GIFS
        "!flex": "http://i.imgur.com/YdCl7E8.gif",
        "!fuckingmental": "http://i.imgur.com/GiG4nPn.gif",
        "!girlstreamer": "http://i.imgur.com/2Xm93C5.gif",
        "!lolachamp": "http://i.imgur.com/hsBcxLo.gif",
        "!rarelola": "http://i.imgur.com/yz6c2RE.gif",
        "!roastme": "https://www.reddit.com/r/RoastMe/comments/45h19g/i_dont_get_attention_from_my_boyfriend_so_i/",
        "!sigma": "http://pastebin.com/mM6x75TE",
        "!shoe": "http://i.imgur.com/qEMJJTP.gif",
        "!wave": " http://i.imgur.com/9lIIaiT.gif",
        "!wutface": "http://i.imgur.com/MH60h6v.gif"
        }
    
    commands_array = ["!online","!memeschool","!command","!mod","!g4g","!kek","!topkek",\
                      "!age","!chris","!eladia","!kieran","!nick","!sogyoh","!flex", "!fuckingmental",\
                      "!girlstreamer","!lolachamp","!rarelola","!roastme","!sigma","!shoe","!wave","!wutface"]
    
    for i in commands_array:
        if str(message.content[0:len(i)]) == i.casefold():
            yield from client.send_message(message.channel, commands[i])
            break
        
    #Slightly more complex commands than printing in chat        
    if message.content.startswith("!hello".casefold()):
        yield from client.send_message(message.channel, "Hello " + message.author.name)
        
    if message.content.startswith("!bye".casefold()):
        yield from client.send_message(message.channel, "Bye " + message.author.name)
            
    if message.content.startswith("!itis".casefold()):
        number = randint(1,10)
        if number % 4 == 0:
            yield from client.send_message(message.channel, "Is it?")
        else:
            yield from client.send_message(message.channel, "It isn't")
        
    if message.content.startswith("!selfdestruct".casefold()):
        for i in range(10,-1,-1):
            if i == 0:
                yield from client.send_message(message.channel, ":boom: :man_with_turban: :boom: ")
                break
            yield from asyncio.sleep(1)
            yield from client.send_message(message.channel, "{}".format(i))

    
    #kill (only available to bot operator)
    if message.content.startswith("!kill".casefold()):
        if message.author.name in mod: #need to figure out how to get message author role
            yield from client.send_message(message.channel, "Barry Bot going down BibleThump /")
            #yield from client.send_message(message.channel, "Barry Bot going down BibleThump /")
            os._exit(5)

    #Rock, paper, scissors
    if message.content.startswith("!rps".casefold()) or message.content.startswith("!rockpaperscissors".casefold()):
        
        temp_message = message.content.split()
        choice = temp_message[1].lower()
        
        if choice == "stone":
            choice = "rock"
        elif choice == "scissor":
            choice = "scissors"
            
        if choice == "rock" or choice == "paper" or choice == "scissors":
                
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
                outcome = "\nYou lose"
            elif bot_choice == 1 and choice == "scissors":
                outcome = "\nYou win!"
            elif bot_choice == 2 and choice == "rock":
                outcome = "\nYou win"
            elif bot_choice == 2 and choice == "paper":
                outcome = "\nYou lose..."
                
            yield from client.send_message(message.channel, "I choose " + bc_array[bot_choice] + outcome)    
        else:
            yield from client.send_message(message.channel, "Invalid choice.")
            
            
@client.async_event
#Displays login name/id
def on_ready():
    print("Logged in as")
    print(client.user.name)
    print(client.user.id)
    
    
client.run(info[0], info[1]) #0 is username, 1 is password.
