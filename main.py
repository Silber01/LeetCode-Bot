import os

from lastACs import *
from getQuestion import *
from registerPlayer import *
from unregisterPlayer import *
from embedMsg import *
from setupPlayer import *
import discord
from discord.ext import commands
from os.path import exists

intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix='-', help_command=None, intents=intents)  # sets prefix, deletes default help command, and sets intents

botTitle = "LeetCode Bot"


@client.event
async def on_ready():
    print("I'm ready!")
    if not exists("./servers"):
        os.mkdir("./servers")
    if not exists("players"):
        os.mkdir("players")

@client.before_invoke
async def common(ctx):
    await setUpPlayer(ctx)


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

@client.command()
async def register(ctx, leetCodeName):
    if getPlayerLCName(ctx) == "null":
        await registerPlayer(ctx, leetCodeName)    # register LeetCode name for player
    elif getPlayerLCName(ctx) != "null" or getPlayerLCName(ctx) != leetCodeName:
        await changeNameEmbed(ctx, leetCodeName)

        try:
            msg = await client.wait_for("message", timeout=15)
        except asyncio.TimeoutError:                           
            await timeoutEmbed(ctx)             
            return

        if msg.content == "Y" or msg.content == "y": # set the new name for the player
            await registerPlayer(ctx, leetCodeName)
        else:
            await changeNameDeclineEmbed(ctx, leetCodeName)      
    

@client.command()
async def unregister(ctx):
  await unregisteringEmbed(ctx)
  try:
      msg = await client.wait_for("message", timeout=15)
  except asyncio.TimeoutError:                           
      await timeoutEmbed(ctx)          
      return

  if msg.content == "Y" or msg.content == "y": 
      await unregisterPlayer(ctx)               # Unregister player
      await unregisteredEmbed(ctx)
  else: 
      pass

with open("key.txt", "r") as readFile:          # get bot token and run
    bot_token = readFile.readline()
client.run(bot_token)
