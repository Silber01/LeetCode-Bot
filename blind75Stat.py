import json
import os
import discord
from discord.ext import commands
from lcUtils import *


async def getBlind75Stats(ctx):
    embed = getEmbed()
    progress = {}
    index = 1
    playerId = str(ctx.author.id)

    with open(f"players/{playerId}.json", "r") as readFile:
        player = json.load(readFile)

    playerBlind75Solved = set(player["BLIND75SOLVED"])

    with open("problemSetInfo/blind75problems.json", "r") as readFile:
        blind75problems = json.load(readFile)

    for topic in blind75problems:
        progress[f"{index}. {topic}"] = {"Solved": 0, "Total": len(topic)}
        index += 1

    index = 1

    for topic in blind75problems:                       # loop through the topics
        # loop through the problems in the topic
        for blind75Problem in blind75problems[topic]:
            # check if the problem is in the topic
            if blind75Problem["ID"] in playerBlind75Solved:
                # if it is, increment the solved count
                progress[f"{index}. {topic}"]["Solved"] += 1

        index += 1                               # increment the index
    index = 1                                 # reset the index

    print(progress)

    embed.description = f"**{player['LEETCODENAME']}**'s Blind75 progress: \n "

    for topic in progress:
        rate = int(progress[topic]['Solved'] / progress[topic]['Total']*20)
        progress_bar = "█"*rate
        embed.description += "```{:<27} ({}/{}) [{}]``` \n".format(topic, progress[topic]['Solved'], progress[topic]['Total'], progress_bar.ljust(20))
        # embed.description += f"```{topic} ({progress[topic]['Solved']}/{progress[topic]['Total']}) {progress_bar}``` \n"
        embed.colour = discord.Colour.gold()

    await ctx.send(embed=embed)
