
from lastACs import *
from getQuestion import *

import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix='-', help_command=None, intents=intents)  # sets prefix, deletes default help command, and sets intents

botTitle = "LeetCode Bot"


@client.event
async def on_ready():
    print("I'm ready!")


@client.command()
async def help(ctx):                            # shows the user what commands the bot has
    embed = discord.Embed(title=botTitle)
    with open("help.txt", "r") as readFile:     # help text is stored in help.txt
        helpText = readFile.read()              # read text then return in an embedded message
    embed.description = helpText
    embed.colour = discord.Colour.purple()
    await ctx.send(embed=embed)


@client.command()
async def lastSolved(ctx, user, amount=1):      # gets "amount" last questions user has solved
    await showLastSolved(ctx, user, amount)


@client.command()
async def getQuestionWithID(ctx, questionID):   # gets LeetCode question with given ID
    await showQuestion(ctx, questionID)

with open("key.txt", "r") as readFile:          # get bot token and run
    bot_token = readFile.readline()
client.run(bot_token)
