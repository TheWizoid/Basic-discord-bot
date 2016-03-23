# Basic-discord-bot
A bot that currently has the following explicit commands:

!addcom You can add your own commands to the miscellaneous ones I've made (if mod) you can use #touser to direct it at the user who used the command or #user, for anything the user types in. There is also #random[n] where n is an integer, for doing stuff like dicerolling. e.g !addcom !dice #random6

!editcom Edit any existing commands (if mod)

!delcom Delete any commands you don't like (if mod)

!live [stream] let's you check if a livestream on twitch is live. It will return if the stream is online/offline, if there has been an error proccessing your request, or if the stream doesn't exist.

!rps/!rockpaperscissors

!selfdestruct Counts down from 10 and explodes 

This also has a built in chat logger. To opt out of chat logging, simply alter the value in logging_chat.txt to False, or type !chatlogoff

#Requires pip and discord.py
To install pip go to https://pip.pypa.io/en/stable/installing/ and add C:\Python34\Scripts to your path

To install discord.py, simply type ``pip install git+https://github.com/Rapptz/discord.py`` into bash/cmd.
