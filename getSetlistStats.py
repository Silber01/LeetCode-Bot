import json
import os
import discord
from discord.ext import commands
from lcUtils import *

async def getSetlistStats(ctx, setlist):
    embed = getEmbed()

    playerId = str(ctx.author.id)
    player = getPlayer(playerId)
    playerSolved = set(player[f"SOLVED"])

    with open(f"problemSetInfo/{setlist}problems.json", "r") as readFile:
        problems = json.load(readFile)
    leetcodename = player["LEETCODENAME"]
    embed.description = f"**{leetcodename}**'s stats:\n```"
    for i, topic in enumerate(problems):
        index = i+1
        progress = 0
        total = len(problems[topic])
        for problem in problems[topic]:
            # check if the problem is in the topic
            if problem["ID"] in playerSolved:
                # if it is, increment the solved count
                progress += 1
        rate = int((progress / total) * 20)
        progressBar = "█" * rate
        stat = (str(index) + ".").ljust(3)
        name = topic.ljust(22)
        progressNum = f"({progress}/{total})".ljust(7)
        progressBar = f"[{progressBar.ljust(20)}]"
        embed.description += f"{stat} {name} {progressNum} {progressBar}\n"
    embed.description += f"```To see more information about a topic, do `-{setlist} <number>`, where `<number>` is " \
                         f"the number next to the topic name (e.g. `-{setlist} 1` will get the \"Arrays & Hashing\" problems)."
    await ctx.send(embed=embed)
