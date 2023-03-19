import json
import os
import discord
from discord.ext import commands
from lcUtils import *


async def getNeetcode150Stats(ctx):
    embed = getEmbed()
    progress = {}
    index = 1
    playerId = str(ctx.author.id)

    with open(f"players/{playerId}.json", "r") as readFile:
        player = json.load(readFile)

    playerNeetcode150Solved = set(player["NEETCODE150SOLVED"])

    with open("problemSetInfo/neetcode150problems.json", "r") as readFile:
        neetcode150problems = json.load(readFile)

    for topic in neetcode150problems:
        progress[f"{index}. {topic}"] = {"Solved": 0, "Total": len(topic)}
        index += 1

    index = 1

    for topic in neetcode150problems:                       # loop through the topics
      # loop through the problems in the topic
      for problem in neetcode150problems[topic]:
          # check if the problem is in the topic
          if problem["ID"] in playerNeetcode150Solved:
              # if it is, increment the solved count
              progress[f"{index}. {topic}"]["Solved"] += 1

      index += 1                               # increment the index
    index = 1                                 # reset the index

    print(progress)

    embed.description = f"**{player['LEETCODENAME']}**'s Neetcode150 progress: \n "

    for topic in progress:
        rate = int(progress[topic]['Solved'] / progress[topic]['Total']*20)
        progress_bar = "█"*rate
        embed.description += "```{:<27} ({}/{}) [{}]``` \n".format(topic, progress[topic]['Solved'], progress[topic]['Total'], progress_bar.ljust(20))
        # embed.description += f"```{topic} ({progress[topic]['Solved']}/{progress[topic]['Total']}) {progress_bar}``` \n"
        embed.colour = discord.Colour.gold()

    await ctx.send(embed=embed)
