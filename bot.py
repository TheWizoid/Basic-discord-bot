#Runs perfectly fine MingLee
import discord
import asyncio

accinfo = open("name_and_pass.txt", "r") #opens txt of username;password
info = accinfo.read().split(";")
accinfo.close()

client = discord.Client()
client.login("username","password")

@client.async_event
def on_message(message):
    #General stuff
    if message.content.startswith("!command") or message.content.startswith("!commands".casefold()):
        yield from client.send_message(message.channel, "A list of current commands: you really expect to list all these? Bloody hell.")
    if message.content.startswith("!hello".casefold()):
        yield from client.send_message(message.channel, "Hello " + message.author.name)
    if message.content.startswith("!bye".casefold()):
        yield from client.send_message(message.channel, "Bye " + message.author.name)
    if message.content.startswith("!meme".casefold()):
        yield from client.send_message(message.channel, "Dank memes")
    if message.content.startswith("!kek".casefold()) or message.content.startswith("!topkek".casefold()):
        yield from client.send_message(message.channel, "top kek xD")
    if message.content.startswith("!itis".casefold()):
        if counter % 3 == 0 and counter != 0:
            yield from client.send_message(message.channel, "Is it?")
        yield from client.send_message(message.channel, "It isn't")
        counter += 1
    
    if message.content.startswith("!age".casefold()):
        yield from client.send_message(message.channel, "PedoBear")
    #People
    if message.content.startswith("!chris".casefold()):
        yield from client.send_message(message.channel, "Abusive uncle chris DansGame")
    if message.content.startswith("!eladia".casefold()):
        yield from client.send_message(message.channel, "We miss you BibleThump")
    if message.content.startswith("!kieran".casefold()):
        yield from client.send_message(message.channel, "http://i.imgur.com/37274Z1.jpg oi oi kieran")
    if message.content.startswith("!sogyoh".casefold()):
        yield from client.send_message(message.channel, "TriHard I am so fucking zooted right now CiGrip")
    if message.content.startswith("!g4g".casefold()):
        yield from client.send_message(message.channel, "http://www.gamingforgood.net/s/r00kieoftheyear#donate MingLee")
    if message.content.startswith("!selfdestruct".casefold()):
        for i in range(10,-1,-1):
            if i == 0:
                yield from client.send_message(message.channel, ":boom: ANELE :boom: ")
                break
            yield from asyncio.sleep(1)
            yield from client.send_message(message.channel, "{}".format(i))
            
    #GIFs
    if message.content.startswith("!flex".casefold()):
        yield from client.send_message(message.channel, "http://i.imgur.com/YdCl7E8.gif")
    if message.content.startswith("!rarelola".casefold()):
        yield from client.send_message(message.channel, "http://i.imgur.com/yz6c2RE.gif")
    if message.content.startswith("!fuckingmetal".casefold()):
        yield from client.send_message(message.channel, "http://i.imgur.com/GiG4nPn.gif)
    
    
    #ad infinitum
        
@client.async_event
def on_ready():
    print("logged in as")
    print(client.user.name)
    print(client.user.id)
    client.accept_invite("https://discord.gg/0qRxlLO5ywXH4ejB")
    
client.run(info[0], info[1])
