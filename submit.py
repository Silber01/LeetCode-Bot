import json
import discord
import asyncio
from discord.ext import commands
from lastACs import getLastACs
from lcUtils import *


async def submit(ctx):
    embed = getEmbed()
    try:                                                            # get player's info
        player = getPlayer(ctx.author.id)
    except FileNotFoundError:                                       # if player does not exist, ask to register and return
        embed.colour = discord.Colour.red()
        embed.description = "You need to register your leetcode account! Do `-register <leetcode_name>` to register!"
        await ctx.send(embed=embed)
        return
    embed.colour = discord.Colour.purple()
    embed.description = "Checking..."                               # since checking can take some time, have a temporary message and edit later
    msg = await ctx.send(embed=embed)
    msgContent = ""                                                 # since multiple things can be submitted at once, stack messages in this variable and send at the end
    qotd = getTodayQuestion()                                       # done here to prevent calling multiple times throughout code
    if checkLOTD(player, qotd):                                     # checks if player did LOTD
        if player["HASSOLVEDTODAY"]:                                # checks if player has already submitted before
            msgContent += "You have already submitted today!"
            embed.colour = discord.Colour.red()
        else:                                                       # reward points based on difficulty, set hasdone to true, and congratulate
            difficulty = qotd["DIFFICULTY"]
            name = qotd["QUESTIONNAME"]
            msgContent += f"Congratulations! You have earned **{giveLOTDPoints(ctx.author.id, player, difficulty)}** points" \
                          f" for solving **{name}**!\n\n"

    if msgContent == "":                                            # if string is empty, there were no valid submissions
        msgContent = "You do not have any valid submissions. Please do `-lotd` to see the LeetCode of the Day " \
                     "question or `-blind75` or `-neetcode150` to see valid questions for those problem sets."
        embed.colour = discord.Colour.red()
    embed.description = msgContent
    await msg.edit(embed=embed)                                     # edit the "Checking..." message with the new information


def checkLOTD(player, question):
    lastSubmits = getLastACs(player["NAME"], 10)                    # gets the last 10 submissions
    qotd = question["QUESTIONSLUG"]                                 # uses question slugs to identify if LOTD slug is in player submissions
    for sub in lastSubmits:
        if sub["titleSlug"] == qotd:                                # for every submission, if a title slug matched LOTD slug, return True
            return True
    return False                                                    # return false if no submissions have LOTD slug


def giveLOTDPoints(playerID, player, difficulty):
    EASYLOTDSCORE = 4
    MEDIUMLOTDSCORE = 6
    HARDLOTDSCORE = 10
    if difficulty == "Easy":                                        # give out score based on difficulty
        player["SCORE"] += EASYLOTDSCORE
        pointsGiven = EASYLOTDSCORE
    elif difficulty == "Medium":
        player["SCORE"] += MEDIUMLOTDSCORE
        pointsGiven = MEDIUMLOTDSCORE
    else:
        player["SCORE"] += HARDLOTDSCORE
        pointsGiven = HARDLOTDSCORE
    player["HASSOLVEDTODAY"] = True                                 # set HASSOLVEDTODAY to true, done last to reduce chance of multiple submissions (race condition)
    setPlayer(playerID, player)                                     # save data
    return pointsGiven                                              # returns pointsGiven to be used in the congratulation message, reduces recomputation a little
