import asyncio
import os
from os.path import exists
import discord
from discord.ext import commands, tasks
from lcUtils import *
import lastACs
import registerPlayer
import getTodaysQuestion
import checkServerExists
import submit

intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix='-', help_command=None, intents=intents)  # sets prefix, deletes default help command, and sets intents

@client.event
async def on_ready():
    print("I'm ready!")
    if not exists("./servers"):                                      
        os.mkdir("./servers")
    if not exists("players"):
        os.mkdir("players")

    while True:
        getTodaysQuestion.dailyQuestion()
        await asyncio.sleep(10)
        # every 10 seconds check if the date from that json file is yesterday

@client.before_invoke
async def common(ctx):
    checkServerExists.checkServerExists(ctx)


@client.command()
async def help(ctx):                            # shows the user what commands the bot has
    embed = getEmbed()
    with open("help.txt", "r") as readFile:     # help text is stored in help.txt
        helpText = readFile.read()              # read text then return in an embedded message
    embed.description = helpText
    embed.colour = discord.Colour.purple()
    await ctx.send(embed=embed)


@client.command()
async def lastSolved(ctx, user, amount=1):      # gets "amount" last questions user has solved
    await lastACs.showLastSolved(ctx, user, amount)


@client.command()
async def getQuestionWithID(ctx, questionID):   # gets LeetCode question with given ID
    await getTodaysQuestion.showQuestion(ctx, questionID)


@client.command()
async def register(ctx, leetCodeName):
    await registerPlayer.handleRegister(ctx, leetCodeName, client)


@client.command()
async def submit(ctx):
    await submit.submit(ctx)



with open("key.txt", "r") as readFile:          # get bot token and run
    bot_token = readFile.readline()
client.run(bot_token)
