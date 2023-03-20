import json
import os
import discord
from discord.ext import commands
from lcUtils import *

async def getSetlistStats(ctx, setlist):
    embed = getEmbed()
    player = getPlayer(ctx.author.id)
    if not player["LEETCODENAME"]:
        embed.description = "You have not registered your Leetcode name yet. Use `-register <LeetCode name>` to register."
        embed.colour = discord.Colour.red()
        await ctx.send(embed=embed)
        return
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

async def getSetlistTopicStats(ctx, setlist, ind):
    embed = getEmbed()
    player = getPlayer(ctx.author.id)
    if not player["LEETCODENAME"]:
        embed.description = "You have not registered your Leetcode name yet. Use `-register <LeetCode name>` to register."
        embed.colour = discord.Colour.red()
        await ctx.send(embed=embed)
        return
    playerSolved = set(player[f"SOLVED"])

    with open(f"problemSetInfo/{setlist}problems.json", "r") as readFile:
        problems = json.load(readFile)
    try:
        ind = int(ind) - 1
    except ValueError:
        embed.color = discord.Colour.red()
        embed.description = f"Please type in a number, e.g. `-{setlist} 1`."
        await ctx.send(embed=embed)
        return
    if ind >= len(problems):
        embed.color = discord.Colour.red()
        embed.description = f"Please type in a number from 1 to {len(problems)}."
        await ctx.send(embed=embed)
        return
    topicList = ["Arrays & Hashing", "Two Pointers", "Sliding Window", "Stack", "Binary Search", "Linked List",
                 "Trees", "Tries", "Heap / Priority Queue", "Backtracking", "Graphs", "1D Dynamic Programming",
                 "2D Dynamic Programming", "Greedy", "Intervals", "Math & Geometry", "Bit Manipulation"]
    if setlist == "neetcode150":
        topicList.insert(11, "Advanced Graphs")
    topic = topicList[ind]
    problems = problems[topic]
    leetcodename = player["LEETCODENAME"]
    with open(f"problemSetInfo/problemIDtoTutorial.json", "r") as readFile:
        tutorials = json.load(readFile)
    embed.description = f"**{leetcodename}**'s Progress for **{topic}** (for {'Blind 75' if setlist == 'blind75' else 'Neetcode 150'}):\n\n"
    for p in problems:
        problemTitle = p["TITLE"]
        problemURL = p["URL"]
        questionSolved = "✓" if p["ID"] in playerSolved else "✘"
        questionTutorial = tutorials[str(p["ID"])]
        problemDifficulty = p["DIFFICULTY"]
        embed.description += f"{questionSolved} [{problemTitle}]({problemURL}) ({problemDifficulty}), ([Solution]({questionTutorial}))\n"
    embed.description += "\n✓ = Solved, ✘ = Not Solved. Click on the problem's name to see its page on LeetCode."
    await ctx.send(embed=embed)

