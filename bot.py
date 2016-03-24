#It works!
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


#Checks if the command is valid
def command_check(message):
    """
    Checks if a command is present at the beginning of a message.
    If it is in the array of commands, but not the dictionary (i.e there's no key which would cause an error)
    it is deleted. Otherwise, it simply checks if #user, #touser, or #random are present in the command text.
    If #touser is present, it will direct the message towards the user, by mentioning their username.
    If #user is present, the second word will replace it. If there is more than one word after the command,
    all are included. If #user has not been entered, the bot will send a private message to the author: "Invalid parameters".
    If #random is present, a random number between 1 and the previously assigned value inclusive (e.g. !dice is #random6).
    If #random is present, but the command was added without a number (e.g. if !dice was simply #random, instead of #random6),
    it will send a message to the user stating that the command is not valid, as it does not contain a number to randomise.
    The command will then be deleted.
    Similar to how #random has a moderator defined maximum, #authorrandom has an author defined one, that is to say
    that the author defines the maximum value. E.g. a moderator may type !addcom !random #authorrandom.
    This would allow anyone to type !random 6 and receive a number between 1 and 6, !random 900 to receive a random number
    between 1 and 900 etc. Also it should be noted that it is simply called #authorrandom isntead of #userrandom, due to
    annoying interactions with #user that I can't be bothered to fix.
    """
    for i in commands_array:
        if str(message.content[0:len(i)+1]).casefold() == i.casefold() or message.content[0:len(i)+1] == (i+" ").casefold():
            if i not in commands:
                commands_array.remove(i)
                pickle.dump(commands_array,open("commands_array.txt","wb"))
            else:
                command_info = commands[i]
                list_message = message.content.split()
                if "#touser" in command_info:
                    try:
                        command_info = command_info.replace("#touser", str(message.author.name))
                        yield from client.send_message(message.channel, command_info)
                    except IndexError:
                        yield from client.send_message(message.author, "Invalid parameters")
                    break

                if "#user" in command_info:
                    try:
                        for i in range(1,len(list_message)):
                            if i > 1:
                                list_message[1] += " " + list_message[i]
                        command_info = command_info.replace("#user", list_message[1])
                        yield from client.send_message(message.channel, command_info)
                    except IndexError:
                        yield from client.send_message(message.author, "Invalid parameters")
                    break

                if "#random" in command_info:
                    try:
                        random_number = command_info[command_info.find("#random")+7]
                        command_info = command_info.replace("#random", str(randint(1,int(random_number))))
                        command_info = command_info.replace(random_number, "")
                        yield from client.send_message(message.channel, command_info)
                        break
                    except IndexError:
                        yield from client.send_message(message.author, "The way this command was created is not valid, it is being deleted.")
                        yield from delete_command(i)
                        yield from client.send_message(message.author, "The command has been deleted.")

                if "#authorrandom" in command_info:
                    try:
                        max_num = int(list_message[1])
                        command_info = command_info.replace("#authorrandom", str(randint(1, max_num)))
                        yield from client.send_message(message.channel, command_info)
                    except ValueError:
                        yield from client.send_message(message.author, "That must be a number")
                    except IndexError:
                        yield from client.send_message(message.author, "Invalid parameters")
                    break

                if "#" not in command_info:
                    yield from client.send_message(message.channel, commands[i])


def list_commands(message):
    list_of_commands = []
    str_of_commands = ""
    for i in commands_array:
        try:
            list_of_commands.append(i)
        except KeyError:
            pass

    list_of_commands = sorted(list_of_commands)

    for i in list_of_commands:
        if "#user" in commands[i]:
            str_of_commands += i + " <user>, "
        elif "#touser" in commands[i]:
            str_of_commands += i +" <author>, "
        else:
            str_of_commands += i + ", "

    str_of_commands += "!commandinfo, !live, !rps/!rockpaperscissors, !selfdestruct, !kill\*, !addcom\*, !delcom\*, !repcom\* and !commands."
    yield from client.send_message(message.channel, "The following commands are available (* means mod only): " + str_of_commands)


def command_info(message):
    if len(split_message) < 2:
        yield from client.send_message(message.channel, "Invalid amount of parameters")
    else:
        command = split_message[1]
        if command not in commands:
            if command.startswith("!commands"):
                yield from client.send_message(message.channel, "Displays a list of commands.")

            elif command.startswith("!commandinfo"):
                yield from client.send_message(message.channel, "Displays the info of the command, i.e what you're looking at now :P")

            elif command.startswith("!selfdestruct"):
                yield from client.send_message(message.channel, "Counts down from 10 and selfdestructs.")

            elif command.startswith("!addcom") or command.startswith("!delcom")\
             or command.startswith("!editcom") or command.startswith("!repcom"):
                alters_by = "add"
                if command[1] in "re": #replace/edit; r/e
                    alters_by = "replace"
                elif command[1] == "d":
                    alters_by = "delete"
                yield from client.send_message(message.channel, "Mods can use this to {} commands.".format(alters_by))

            elif command.startswith("!rps") or command.startswith("!rockpaperscissors"):
                yield from client.send_message(message.channel, "Used for playing a game of rock, paper, scissors.")

            elif command.startswith("!kill"):
                yield from client.send_message(message.channel, "Kills the bot.")

            else:
                yield from client.send_message(message.channel, "Command does not exist.")

        elif commands[command].startswith("http://i.imgur"):
            yield from client.send_message(message.channel, "Displays an image")
        else:
            yield from client.send_message(message.channel, commands[command])


#Adding commands
def add_command(message):
    """
    Hypothetically, I could have the bot add commands to itself. What a world.
    """
    valid = True
    adding_command = message.content.split()
    if len(adding_command) < 3:
        yield from client.send_message(message.channel, "Invalid amount of parameters")
    elif adding_command[1] in commands:
        yield from client.send_message(message.channel, "That command already exists")
    else:
        if message.content.find("#random") != -1:
            try:
                number = int(message.content[message.content.find("#random")+7])
            except ValueError:
                yield from client.send_message(message.author, "Invalid #random value")
                valid = False
            except IndexError:
                yield from client.send_message(message.author, "Invalid #random value")
                valid = False
        if valid == True:
            command = adding_command[1]
            if "#" in command:
                command = command.replace("#", " ")
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


#Deleting commands
def delete_command(command):
    """
    There are times I may want to delete a command, when the user hasn't specified so.
    E.g. if a user creates an invalid command (such as using #random without a number), it will be deleted.
    """
    if "#" in command:
        command = command.replace("#", " ")
    if command not in commands:
        yield from client.send_message(message.channel, "Command does not exist.")
    else:
        del commands[command]
        commands_array.remove(command)
        pickle.dump(commands, open("commands.txt", "wb"))
        pickle.dump(commands_array, open("commands_array.txt", "wb"))


#Editing/replacing commands
def edit_command(message):
    """
    Consistency with the command addition/deletion features.
    """
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



def logging_config(message):
    if message.content.startswith("!chatlogoff".casefold()) and message.author.name in mod:
        yield from client.send_message(message.channel, "Chatlogging off" )
        logging_consent = open(server + "_logging_chat.txt","w")
        logging_consent.write("False")
        logging_consent.close()

    if message.content.startswith("!chatlogon".casefold()) and message.author.name in mod:
        yield from client.send_message(message.channel, "Chatlogging on")
        logging_consent = open(server + "_logging_chat.txt","w")
        logging_consent.write("True")
        logging_consent.close()


#Checks if logging is allowed on the server
def logging_consent(message):
    #Chat logger Doesn't work with uploads (displays as a space after the name)
    try:
        logging_consent = open(server + "_logging_chat.txt","r")
    except FileNotFoundError:
        logging_consent = open(server + "_logging_chat.txt","w")
        logging_consent.write("True")
        logging_consent.close()
        logging_consent = open(server + "_logging_chat.txt","r")

    logging_chat = logging_consent.read()
    logging_consent.close()

    if logging_chat == "True":

        if server == "r00kieboys":
            chatlog = open("r00kie_chatlog.txt","a")
        elif server == "need for pleb":
            chatlog = open("lads_chatlog.txt","a")
        elif server == "Bot test":
            chatlog = open("test_chatlog.txt","a")
        elif server == "The Study of The Blade":
            chatlog = open("sam_chatlog.txt","a")
        else:
            chatlog = open(server+"_server_chatlog.txt","a")

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


#WIP
def avatar_finder(message):
    ##    if message.content.startswith("!avatar".casefold()):
    ##        try:
    ##            user = split_message[1]
    ##            user_avatar = user
    ##            user_avatar = user_avatar.avatar#_url
    ##            yield from client.send_message(message.channel, "This user's avatar is " + user_avatar)
    ##        except IndexError:
    ##            user_avatar = ""
    ##            yield from client.send_message(message.channel, "Invalid user")
    ##        #user_avatar = avatar(user_avatar)
    pass


def rock_paper_scissors(message):
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


#Checking if a livestream on twitch is live
def stream_live_check(stream):
    url = "https://api.twitch.tv/kraken/streams/{}".format(stream.lower())

    try:
        contents = json.loads(urllib.request.urlopen(url).read().decode("utf-8"))
        if contents["stream"] == None:
            status = "offline"
            bot_message = "{} is offline".format(stream)
        else:
            #print(contents)
            name = contents["stream"]["channel"]["name"]
            title = contents["stream"]["channel"]["status"]
            game = contents["stream"]["channel"]["game"]
            viewers = contents["stream"]["viewers"]
            bot_message = "{0} is online.\n{0}'s title is: {1} \n{0} is playing {2} \nThere are {3} viewers \n".format(name,title,game,viewers)

    except urllib.error.URLError as e:
        if e.reason == "Not found" or e.reason == "Unprocessable Entity":
            bot_message = "That stream doesn't exist."
        else:
            bot_message = "There was an error proccessing your request."

    return bot_message


def points(message):
    """
    Every time someone sends a message, they gain one point.
    This is because any time based ones would result in mobile users having
    the same amount of points each, due to idling.
    """

    try:
        points = pickle.load(open(server+"points.txt","rb"))
    except FileNotFoundError:
        points = {message.author: 0}
        pickle.dump(points, open(server+"points.txt","wb"))


    if message.author not in points:
        points[message.author] = 0
    elif split_message[0] != "!points" and split_message[0] != "!roulette":
        points[message.author] += 1

    if message.content.startswith("!points"):
        if points[message.author] == 0:
            emote = "FeelsEmoMan"
        elif points[message.author] >= 1000:
            emote = "PogChamp"
        else:
            emote = "FeelsGoodMan"

        if points[message.author] != 1:
            yield from client.send_message(message.channel, "You have {} points {}".format(points[message.author],emote))
        else:
            yield from client.send_message(message.channel, "You have {} point {}".format(points[message.author],emote))

    if message.content.startswith("!roulette"):
        if len(split_message) < 2:
            yield from client.send_message(message.author, "You must roulette *something*.")
        else:
            try:
                if split_message[1] == "all".casefold():
                    amount = points[message.author]
                else:
                    amount = int(split_message[1])
                if amount == 0 and points[message.author] == 0:
                    yield from client.send_message(message.author, "You don't have any points FeelsEmoMan")
                elif amount == 0:
                    yield from client.send_message(message.author, "You must roulette *something*.")
                else:
                    if amount > points[message.author]:
                        yield from client.send_message(message.author, "You don't have enough points FeelsEmoMan")
                    else:
                        random_integer = randint(0,3)
                        if random_integer < 2:
                            outcome = "win"
                            points[message.author] += amount
                            emote = "FeelsGoodMan"
                        else:
                            outcome = "lost"
                            points[message.author] -= amount
                            emote = "FeelsEmoMan"

                        yield from client.send_message(message.channel, "You {} {} points! {}\nYou now have {} points.".format(outcome, amount, emote, points[message.author]))
            except ValueError:
                yield from client.send_message(message.author, "Invalid amount.")

    pickle.dump(points, open(server+"points.txt","wb"))


#Main Body
@client.async_event
def on_message(message):
    global commands
    global commands_array
    global server
    global split_message

    split_message = message.content.split()
    server = str(message.server)

    yield from points(message)

    logging_consent(message)
    yield from logging_config(message)

    commands = pickle.load(open("commands.txt","rb"))
    commands_array = pickle.load(open("commands_array.txt","rb"))

    #General Commands
    yield from command_check(message)

    #Adding commands
    if message.content.startswith("!addcom".casefold()) and message.author.name in mod:
        yield from add_command(message)

    #Replacing commands
    if message.content.startswith("!repcom".casefold()) or message.content.startswith("!editcom".casefold()) and message.author.name in mod:
        yield from edit_command(message)

    #Deleting commands
    if message.content.startswith("!delcom".casefold()) and message.author.name in mod:
        del_command = message.content.split()
        if len(del_command) < 2:
            yield from client.send_message(message.channel, "Invalid amount of parameters")
        else:
            yield from delete_command(del_command[1])
            yield from client.send_message(message.channel, "Successfully deleted.")

    #Command info
    if message.content.startswith("!commandinfo".casefold()):
        yield from command_info(message)

    #!commands
    if message.content.startswith("!commands".casefold()):
        yield from list_commands(message)

    #is it?
    if message.content.startswith("!itis".casefold()):
        number = randint(1,10)
        if number % 4 == 0:
            yield from client.send_message(message.channel, "Is it?")
        else:
            yield from client.send_message(message.channel, "It isn't")

    #Checking if a stream is live using urllib and json
    if message.content.startswith("!live"):
        try:
            bot_message = stream_live_check(message.content.split()[1])
        except IndexError:
            bot_message = "Invalid parameters"
        yield from client.send_message(message.channel, bot_message)

    if message.content.startswith("!selfdestruct".casefold()):
        for i in range(10,-1,-1):
            if i == 0:
                yield from client.send_message(message.channel, ":boom: :man_with_turban: :boom: ")
                break
            yield from asyncio.sleep(1)
            yield from client.send_message(message.channel, "{}".format(i))

    #kill (only available to mods)
    if message.content.startswith("!kill".casefold()):
        if message.author.name in mod:
            yield from client.send_message(message.channel, "Barry Bot going down BibleThump /")
            os._exit(5)
        else:
            yield from client.send_message(message.channel, "You do not have permission to perform that command.")

    #Rock, paper, scissors
    if message.content.startswith("!rps".casefold()) or message.content.startswith("!rockpaperscissors".casefold()):
        yield from rock_paper_scissors(message)

    ##    if "asdfgh" in message.content: #is censoring possible?
    ##        message.content = message.content.replace("asdfgh","memes")#yes, apparently
    ##        yield from client.delete_message(message)
    ##        yield from client.send_message(message.channel, "{}: ".format(message.author.name) + message.content)

@client.async_event
#Displays login name/id
def on_ready():
    print("Logged in as")
    print(client.user.name)
    print(client.user.id)

client.run(info[0], info[1]) #0 is username, 1 is password.
