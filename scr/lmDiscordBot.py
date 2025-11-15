import discord
from discord.ext import commands

"""
This class acts as the basic framework for a discord bot that utilizes one of the language models
"""
class lmBot:
    def __init__(self, model, token:str, prefex:str) -> None:
        """
        Arguments:
        model = one of the text generation language models
        token = discord bot token
        prefex = the prefex of the cammands the bot will use. a secondary prefix is automaticaly created when the bot is strated. This is @bot name
        """
        self.BOT_PREFIX = prefex
        self.secondaryPrefix = ""
        self.TOKEN = token
        self.model = model #this is one of the text generation language models
        #paramaters on what the bot can and cant do
        intents = discord.Intents.default()
        intents.members = True
        intents.message_content = True
        self.bot = commands.Bot(command_prefix=self.BOT_PREFIX, intents=intents)
        #other important information
        self.botName = ""
        self.secondaryPrefix = ""
        #comands
        self.helpCMD = f"{self.BOT_PREFIX}help"
        
        @self.bot.event
        async def on_ready():
            self.botName = self.bot.user.name
            self.secondaryPrefix = f"<@{self.bot.user.id}>" #use @bot name when talking to the bot and BOT_PREFIX when using its comands
            print(f'Logged in as {self.botName}:{self.secondaryPrefix}')
        
        @self.bot.event
        async def on_message(message):
            phrase = message.content
            author = message.author.id
            print(self.secondaryPrefix)
            print(f"{author} : {phrase}")
            self.model.readInUtterance(phrase) #add phrase to the lm so it can process it and continue process
            if message.author != self.bot.user: #only processes information that comes from players, not the bot
                if phrase.startswith(self.helpCMD):
                    await message.channel.send(f"This bot acts as a dnd player and only uses basic comands."\
                                            f" If you would like to have it talk back to you, @ it lie you would a normal user. ex. {self.secondaryPrefix}")
                if phrase.startswith(self.secondaryPrefix):
                    response = self.model.generateResponse()
                    await message.channel.send(response)
    def __repr__(self) -> str:
        return f"{self.botName} : {self.BOT_PREFIX}"
    
    async def run(self):
        await self.bot.start(self.TOKEN)