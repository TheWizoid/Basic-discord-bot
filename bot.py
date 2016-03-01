#It works!

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


@client.async_event
class special_commands:
    @client.async_event
    def on_message(message):
    #General stuff
        if message.content.startswith("!online".casefold()):
            yield from client.send_message(message.channel, "Barry Bot is online")
    
        if message.content.startswith("!memeschool".casefold()):
            yield from client.send_message(message.channel, "https://www.youtube.com/watch?v=fJdA7dwx6-4")
        
        if message.content.startswith("!commands") or message.content.startswith("!command".casefold()):
            yield from client.send_message(message.channel, "A list of current commands: you really expect to list all these? Bloody hell.")

        if message.content.startswith("!hello".casefold()):
            yield from client.send_message(message.channel, "Hello " + message.author.name)
        
        if message.content.startswith("!bye".casefold()):
            yield from client.send_message(message.channel, "Bye " + message.author.name)
        
        if message.content.startswith("!g4g".casefold()):
            yield from client.send_message(message.channel, "http://www.gamingforgood.net/s/r00kieoftheyear#donate MingLee")
            
        if message.content.startswith("!itis".casefold()):
            number = randint(1,10)
            if number % 3 == 0:
                yield from client.send_message(message.channel, "Is it?")
            else:
                yield from client.send_message(message.channel, "It isn't")
            
        if message.content.startswith("!kek".casefold()) or message.content.startswith("!topkek".casefold()):
            yield from client.send_message(message.channel, "top kek xD")
        
        if message.content.startswith("!selfdestruct".casefold()):
            for i in range(10,-1,-1):
                if i == 0:
                    yield from client.send_message(message.channel, ":boom: ANELE :boom: ")
                    break
                yield from asyncio.sleep(1)
                yield from client.send_message(message.channel, "{}".format(i))
    
        if message.content.startswith("!age".casefold()):
            yield from client.send_message(message.channel, "PedoBear")
            
        if message.content.startswith("xD".casefold()) or message.content.startswith("!xD".casefold()):
            yield from client.send_message(message.channel, "xD")
        
    #People
        
        if message.content.startswith("!chris".casefold()):
            yield from client.send_message(message.channel, "Abusive uncle chris DansGame")
        
        if message.content.startswith("!eladia".casefold()):
            yield from client.send_message(message.channel, "We miss you BibleThump")
        
        if message.content.startswith("!kieran".casefold()):
            yield from client.send_message(message.channel, "http://i.imgur.com/37274Z1.jpg oi oi kieran")
        
        if message.content.startswith("!nick".casefold()):
            yield from client.send_message(message.channel, "NIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIICK! Kreygasm")
        
        if message.content.startswith("!sogyoh".casefold()):
            yield from client.send_message(message.channel, "TriHard I am so fucking zooted right now CiGrip")
            
    #GIFs
            
        if message.content.startswith("!flex".casefold()):
            yield from client.send_message(message.channel, "http://i.imgur.com/YdCl7E8.gif")
            
        if message.content.startswith("!fuckingmental".casefold()):
            yield from client.send_message(message.channel, "http://i.imgur.com/GiG4nPn.gif")
        
        if message.content.startswith("!rarelola".casefold()):
            yield from client.send_message(message.channel, "http://i.imgur.com/yz6c2RE.gif")
        
        if message.content.startswith("!sigma".casefold()):
            yield from client.send_message(message.channel, "http://pastebin.com/mM6x75TE")

        if message.content.startswith("!shoe".casefold()):
            yield from client.send_message(message.channel, "http://i.imgur.com/qEMJJTP.gif")

    
    #kill (only available to bot operator)
        if message.content.startswith("!kill".casefold()):
##        if discord.Role(message.author) == "mod": #need to figure out how to get message author role
##            yield from client.send_message(message.channel, "Barry Bot going down BibleThump /")
            if message.author.name == "TheWizoid": #and message.author.id == "99916696600461312":
                yield from client.send_message(message.channel, "Barry Bot going down BibleThump /")
                os._exit(5)

    #Rock, paper, scissors
        if message.content.startswith("!rps".casefold()) or message.content.startswith("!rockpaperscissors".casefold()):
            temp = open("temp.txt", "w")
            temp.write(message.content)
            temp.close()
            
            temp = open("temp.txt", "r")
            new_message = temp.read().lower()
            temp.close()

            #Tries to find the choice
            if message.content.startswith("!rps"):
                locator = 4 #!rps is shorter than !rockpaperscissors (obvious but w/e)
            else:
                locator = 18
                
            choice_index = new_message.find("rock",locator)
            choice = "rock"
            
            if choice_index == -1:
                choice = "paper"
                choice_index = new_message.find("paper",locator)
                if choice_index == -1:
                    choice_index = new_message.find("scissor",locator)#if someone types scissor over scissors, it gets processed correctly
                    choice = "scissors"
                    if choice_index == -1:
                        choice_index = new_message.find("stone",locator) #some people prefer stone over rock
                        choice = "rock"
                        if choice_index == -1:
                            choice = "invalid"
                        
            if choice == "rock" or choice == "paper" or choice == "scissors":
                
                bot_choice = randint(0,2)
                bc_array = ["rock","paper","scissors"]
                
                yield from client.send_message(message.channel, "I choose "+bc_array[bot_choice])
                
                #Goes through all the combinations
                if bc_array[bot_choice] == choice:
                    yield from client.send_message(message.channel, "Tie")
                elif bot_choice == 0 and choice == "paper":
                    yield from client.send_message(message.channel, "You win!")
                elif bot_choice == 0 and choice == "scissors":
                    yield from client.send_message(message.channel, "You lose...")
                elif bot_choice == 1 and choice == "rock":
                    yield from client.send_message(message.channel, "You lose")
                elif bot_choice == 1 and choice == "scissors":
                    yield from client.send_message(message.channel, "You win!")
                elif bot_choice == 2 and choice == "rock":
                    yield from client.send_message(message.channel, "You win")
                elif bot_choice == 2 and choice == "paper":
                    yield from client.send_message(message.channel, "You lose...")
                
            else:
                yield from client.send_message(message.channel, "Invalid choice.")
            
            
@client.async_event
#Displays login name/id
def on_ready():
    print("Logged in as")
    print(client.user.name)
    print(client.user.id)
    
    
client.run(info[0], info[1]) #0 is username, 1 is password.
