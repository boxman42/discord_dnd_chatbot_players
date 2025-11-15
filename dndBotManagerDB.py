import discord
from discord.ext import commands
import characterDerectory as cd
import random
import asyncio
#import a generic discord bot that can use various language modles 
from lmDiscordBot import lmBot
#langauge models
from models.blenderBot import blenderBot
from models.godelBot import godelBot
from rnnBot import rnnBot

#bot preliminary setup
TOKEN = '' #bot token
BOT_PREFIX = './'
intents = discord.Intents.default()
intents.members = True
intents.message_content = True

#tracked variables
activeModel = 0 #0 or 1. 0 is the baseline model, 1 is the advenced model
activeGame = -1 #this is a 10 digit number denoting the id of the session.

#comands
helpCMD = f"{BOT_PREFIX}help"
newCharacterCMD = f"{BOT_PREFIX}new_character"
getCharacterCMD = f"{BOT_PREFIX}get_character"
startBotsCMD = f"{BOT_PREFIX}start_bots"
startGameCMD = f"{BOT_PREFIX}start_game"

# Create an instance of the bot
bot = commands.Bot(command_prefix=BOT_PREFIX, intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.event
async def on_message(message):
    phrase = message.content
    author = message.author.id
    print(f"{author} : {phrase}")
    #i dont know whay i have to do this, but it makes everything work corectly
    global processes
    global botPaths

    if message.author != bot.user: #only processes information that comes from players, not the bot
        if phrase.startswith(helpCMD):
            await message.channel.send(f"comands:\n"\
                                       f"\n{newCharacterCMD} - create a new dnd character. give a character name and class. ex. {newCharacterCMD} gandolf sorcerer."\
                                       f"\n{getCharacterCMD} - print the information of that users character"\
                                       f"\n{startGameCMD} - start a new game or give session ID (10 digit number) to continue a game."\
                                       f"\n{startBotsCMD} - start the language model bots"\
                                       "\nYou may also send plain text promts and they will be interperted by the NLP model."\
                                        "\nIt is recommended that you create a character and select a model before starting a new game.")

        elif phrase.startswith(newCharacterCMD): #creta a new character
            phraseSplit = phrase.split()
            cd.creatNewCharacter(author, phraseSplit[1], phraseSplit[2])
            await message.channel.send(cd.getCharacter(author))

        elif phrase.startswith(startGameCMD): #this function can start a new dnd session or recall a passed one
            sessionParams = phrase.split() #[0] - the start_game comand. [1] - the id of the session to continue
            if len(sessionParams) <= 1: #if only the start_game comand is used, start a new game
                activeGame = random.randint(1000000000, 9999999999) #creat a new session ID whenever starting a new game
                await message.channel.send(f"your game id is: {activeGame}. You should pin this")

            else: #if a game id is passed in
                activeGame = sessionParams[1]
                cd.loadSession(activeGame)
                await message.channel.send(f"active game: {activeGame}")
                pass
        
        elif phrase.startswith(getCharacterCMD): #this will send the character information of the user that sent the comand  
            await message.channel.send(cd.getCharacter(author))
        elif phrase.startswith(startBotsCMD):
            #build discord bots
            print("initalize bots")
            bots = [asyncio.create_task(lmBot(godelBot(), "MTE4Mzg1NTI3MDYzNjU2NDY2Mw.GSbBL2.7ZnwdaLO2HSCOGIcIQxkyEgXC2UEGzQdYJaLJs", 'g/').run()), 
                    asyncio.create_task(lmBot(blenderBot(), "MTE4Mzg3NTYxNDQ3NDc2ODUyNQ.GnwsRq._oTQe77dU2yEZdRjafD0mKz8f69PWOoXWcMXY0", "b/").run()), 
                    asyncio.create_task(lmBot(rnnBot("fbRnnAdomModel"), "MTE4NDU1MDU2NTUwNjcxNTczOA.G3_016.qdBug5GbqFoXLNkttGNfuJ6n54I6cShdh-4dBE", "r/").run())]
            for dbot in bots:
                asyncio.run(asyncio.gather(*bots)) 
                print(dbot)
#     if activeModel == 1: #if active model is the advanced model
#         cd.chatHistory.append(phrase) #at the end of every message, add new messages to chat history
#     cd.saveSession(activeGame) #save all the text that was genereated during this interaction


# print(f"active model: {activeModel}")
bot.run(TOKEN)