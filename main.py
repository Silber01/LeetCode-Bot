import asyncio
import os
from os.path import exists
import discord
from discord.ext import commands, tasks
from lcUtils import *
import lastACs
import registerPlayer
import setupPlayer
import getTodaysQuestion
import submit as submitFunc
import setUpServer
import leaderboard
import getStats as getStatsFunc
import getSetlistStats

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
        await getTodaysQuestion.dailyQuestion(client)
        await asyncio.sleep(10)
        # every 10 seconds check if the date from that json file is yesterday

@client.before_invoke
async def common(ctx):
    setupPlayer.setUpPlayer(ctx)

@client.command()
async def help(ctx):                            # shows the user what commands the bot has
    embed = getEmbed()
    with open("help.txt", "r") as readFile:     # help text is stored in help.txt
        helpText = readFile.read()              # read text then return in an embedded message
    embed.description = helpText
    embed.colour = discord.Colour.purple()
    await ctx.send(embed=embed)

# ADMIN COMMANDS
@client.command()
async def setChannel(ctx):
    await setUpServer.setChannel(ctx)

@client.command()
async def setPing(ctx, ping=None):
    await setUpServer.setPing(ctx, ping)

@client.command()
async def lastSolved(ctx, user, amount=1):      # gets "amount" last questions user has solved
    await lastACs.showLastSolved(ctx, user, amount)


@client.command()
async def getQuestionWithID(ctx, questionID):   # gets LeetCode question with given ID
    await getTodaysQuestion.showQuestion(ctx, questionID)


@client.command()
async def register(ctx, leetCodeName=None):
    await registerPlayer.handleRegister(ctx, leetCodeName, client)

@client.command()
async def submit(ctx):
    await submitFunc.submit(ctx)

@client.command()
async def lotd(ctx):
    embed = getEmbed()
    question = getTodayQuestion()
    url = "https://leetcode.com/problems/" + question["QUESTIONSLUG"]
    diff = question["DIFFICULTY"]
    title = question["QUESTIONNAME"]

    embed.description = f"Today's {diff} question: {title} \n {url} \n if you're new, do `-help` to learn how to play"
    embed.colour = discord.Colour.blue()
    await ctx.send(embed=embed)

@client.command()
async def gtop(ctx, page="1"):
    await leaderboard.leaderboard(ctx, page, True)

@client.command()
async def top(ctx, page="1"):
    await leaderboard.leaderboard(ctx, page, False)

@client.command()
async def stats(ctx, *args):
    await getStatsFunc.getStats(ctx, args)

@client.command()
async def blind75(ctx, topic=None):
    if topic is None:
        await getSetlistStats.getSetlistStats(ctx, "blind75")
    else:
        await getSetlistStats.getSetlistTopicStats(ctx, "blind75", topic)


@client.command()
async def neetcode150(ctx, topic=None):
    if topic is None:
        await getSetlistStats.getSetlistStats(ctx, "neetcode150")
    else:
        await getSetlistStats.getSetlistTopicStats(ctx, "neetcode150", topic)

with open("key.txt", "r") as readFile:          # get bot token and run
    bot_token = readFile.readline()
client.run(bot_token)
