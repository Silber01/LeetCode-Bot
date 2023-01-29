from lastACs import *
from registerPlayer import *
from randomQuestion import *
import discord
from discord.ext import commands, tasks
from checkServerExists import *

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
        dailyQuestion()
        await asyncio.sleep(10)
        # every 10 seconds check if the date from that json file is yesterday

@client.before_invoke
async def common(ctx):
    checkServerExists(ctx)

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
    await showLastSolved(ctx, user, amount)


@client.command()
async def getQuestionWithID(ctx, questionID):   # gets LeetCode question with given ID
    await showQuestion(ctx, questionID)


@client.command()
async def register(ctx, leetCodeName):
    await handleRegister(ctx, leetCodeName, client)             


with open("key.txt", "r") as readFile:          # get bot token and run
    bot_token = readFile.readline()
client.run(bot_token)
