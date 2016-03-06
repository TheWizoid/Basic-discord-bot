#It works!
import asyncio
import discord
import os
import pickle
import sys
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
        elif server == "The Study of The Blade":
            chatlog = open("sam_chatlog.txt","a")
            
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
            
    commands = pickle.load(open("commands.txt","rb"))
    commands_array = pickle.load(open("commands_array.txt","rb"))
    for i in commands_array:
        if str(message.content[0:len(i)+1]) == i.casefold() or message.content[0:len(i)+1] == (i+" ").casefold():
            if i not in commands:
                commands_array.remove(i)
                pickle.dump(commands_array,open("commands_array.txt","wb"))
            else:
                command_info = commands[i]
                list_message = message.content.split()
                if command_info.find("#touser") != -1 or command_info.find("#user") != -1 or command_info.find("#random") != -1:
                    if command_info.find("#touser") != -1:
                        try:
                            command_info = command_info.replace("#touser", str(message.author.name))
                            yield from client.send_message(message.channel, command_info)
                            break
                        except IndexError:
                            yield from client.send_message(message.channel, "Invalid parameters")
                    
                    if command_info.find("#user") != -1:
                        try:
                            command_info = command_info.replace("#user", list_message[1])
                            yield from client.send_message(message.channel, command_info)
                            break
                        except IndexError:
                            yield from client.send_message(message.channel, "Invalid parameters")

                    if command_info.find("#random") != -1:
                        try:
                            random_number = command_info[command_info.find("#random")+7]
                            command_info = command_info.replace("#random", str(randint(1,int(random_number))))
                            command_info = command_info.replace(random_number, "")
                            yield from client.send_message(message.channel, command_info)
                            break
                        except IndexError:
                            yield from client.send_message(message.channel, "Invalid parameters")
                else:
                    yield from client.send_message(message.channel, commands[i])

    #Adding commands
    if message.content.startswith("!addcom".casefold()) and message.author.name in mod:
        adding_command = message.content.split()
        if len(adding_command) < 3:
            yield from client.send_message(message.channel, "Invalid amount of parameters")
        elif adding_command[1] in commands:
            yield from client.send_message(message.channel, "That command already exists")
        else:
            command = adding_command[1]
            if len(adding_command) == 3:
                pass
            else:
                for i in range(3,len(adding_command)):
                    adding_command[2] += " " + adding_command[i]
                    
            command_text = adding_command[2]    
            commands[command] = command_text
            commands_array.append(command)
            
            pickle.dump(commands, open("commands.txt", "wb"))
            pickle.dump(commands_array, open("commands_array.txt", "wb"))
            yield from client.send_message(message.channel, "Command added")
            
    #Replacing commands
    if message.content.startswith("!repcom".casefold()) and message.author.name in mod:
        rep_command = message.content.split()
        if rep_command[1] not in commands:
            yield from client.send_message(message.channel, "That command does not exist to be replaced")
        else:
            if len(rep_command) < 3:
                yield from client.send_message(message.channel, "Invalid amount of parameters")
            else:
                command = rep_command[1]
                if len(rep_command) == 3:
                    pass
                else:
                    for i in range(3,len(rep_command)):
                        rep_command[2] += " " + rep_command[i]
                        
                command_text = rep_command[2]
                commands[command] = command_text
                
                pickle.dump(commands, open("commands.txt", "wb"))
                pickle.dump(commands_array, open("commands_array.txt", "wb"))
                
                yield from client.send_message(message.channel, "Command replaced")
    #Deleting commands
    if message.content.startswith("!delcom".casefold()) and message.author.name in mod:
        del_command = message.content.split()
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
    list_of_commands = []
    str_of_commands = ""
    if message.content.startswith("!commands".casefold()):
        for i in commands_array:
            try:
                list_of_commands.append(i)
            except KeyError:
                pass
        #temp_list_of_commands += "!selfdestruct, !rps/!rockpaperscissors, !kill\*, !addcom\*, !delcom\*, !repcom\* and !commands."
        list_of_commands = sorted(list_of_commands)
        for i in list_of_commands:
            str_of_commands += i + ", "
        str_of_commands += "!selfdestruct, !rps/!rockpaperscissors, !kill\*, !addcom\*, !delcom\*, !repcom\* and !commands."
        yield from client.send_message(message.channel, "The following commands are available (* means mod only): " + str_of_commands)
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
        else:
            yield from client.send_message(message.channel, "You do not have permission to perform that command.")

    
        
    #Rock, paper, scissors
    if message.content.startswith("!rps".casefold()) or message.content.startswith("!rockpaperscissors".casefold()):
        if len(message.content.split()) == 1:
            yield from client.send_message(message.channel, "Invalid choice")
        else:
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
