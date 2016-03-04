#It works!
import asyncio
import csv
import discord
import json
import os
import pickle
from datetime import datetime
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
        server = str(message.server)
        
        if server == "r00kieboys":
            chatlog = open("r00kie_chatlog.txt","a")
        elif server == "need for pleb":
            chatlog = open("lads_chatlog.txt","a")
        elif server == "Bot test":
            chatlog = open("test_chatlog.txt","a")
            
        time = str(datetime.now())
        
        chatlog.write("["+time[0:19]+"]"+message.author.name+":"+message.content+"\n")#slicing the string is easier than importing gmtime and specifying hh:mm:ss lol
        chatlog.close()
        
    commands = pickle.load(open("commands.txt","rb"))
    commands_array = pickle.load(open("commands_array.txt","rb"))

    
    for i in commands_array:
        if str(message.content[0:len(i)]) == i.casefold():
            yield from client.send_message(message.channel, commands[i])
            break
        
    #Adding commands
    if message.content.startswith("!addcom".casefold()) and message.author.name in mod:
        adding_command = str(message.content).split()
        if len(adding_command) < 3:
            yield from client.send_message(message.channel, "Invalid amount of parameters")
        else:
            command = adding_command[1]
            if len(adding_command) == 3:
                command_text = adding_command[2]
            else:
                for i in range(3,len(adding_command)):
                    adding_command[2] += " " + adding_command[i]
                    command_text = adding_command[2]
                
            commands[command] = command_text
            commands_array.append(command)
            pickle.dump(commands, open("commands.txt", "wb"))
            pickle.dump(commands_array, open("commands_array.txt", "wb"))
            yield from client.send_message(message.channel, "Command added")

    #Deleting commands
    if message.content.startswith("!delcom".casefold()) and message.author.name in mod:
        del_command = str(message.content).split()
        if len(del_command) < 2:
            yield from client.send_message(message.channel, "Invalid amount of parameters")
        else:
            command = del_command[1]
            if command not in commands:
                yield from client.send_message(message.channel, "Command does not exist.")
            else:
                del commands[command]
                commands_array.remove(command)
                pickle.dump(commands, open("commands.txt", "wb"))
                pickle.dump(commands_array, open("commands_array.txt", "wb"))
                yield from client.send_message(message.channel, "Command successfully deleted")
      
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
        if message.author.name in mod: 
            yield from client.send_message(message.channel, "Barry Bot going down BibleThump /")
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
