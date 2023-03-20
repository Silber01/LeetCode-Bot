import json
import discord
import asyncio
from discord.ext import commands
from lastACs import getLastACs
from lcUtils import *


async def submit(ctx):
    embed = getEmbed()
    player = getPlayer(ctx.author.id)
    oldScore = player["SCORE"]
    if not player["LEETCODENAME"]:
        embed.description = "You have not registered your Leetcode name yet. Use `-register <LeetCode name>` to register."
        embed.colour = discord.Colour.red()
        await ctx.send(embed=embed)
        return
    embed.colour = discord.Colour.purple()
    embed.description = "Checking..."                               # since checking can take some time, have a temporary message and edit later
    msg = await ctx.send(embed=embed)
    msgContent = ""                                                 # since multiple things can be submitted at once, stack messages in this variable and send at the end
    qotd = getTodayQuestion()                                       # done here to prevent calling multiple times throughout code
    lastSubmits = getLastACs(player["LEETCODENAME"], 1000)                    # gets the last 20 submissions
    if lastSubmits == "INVALID":                                                # returns this if user doesnt exist
        embed.colour = discord.Colour.red()
        embed.description = "Sorry, that user does not exist."
        await msg.edit(embed=embed)
        return
    if checkLOTD(qotd, lastSubmits):                        # checks if player did LOTD
        if player["HASSOLVEDTODAY"]:                                # checks if player has already submitted before
            msgContent += "You have already submitted for LeetCode of the day today!\n\n"
            embed.colour = discord.Colour.red()
        else:                                                       # reward points based on difficulty, set hasdone to true, and congratulate
            difficulty = qotd["DIFFICULTY"]
            name = qotd["QUESTIONNAME"]
            msgContent += f"Congratulations! You have earned **{givePoints(player, difficulty, True)}** points" \
                          f" for solving **{name}**!\n\n"

    newSolved = checkSetlists(player, lastSubmits)                  # checks for setlists problems
    if len(newSolved) > 0:
        msgContent += "You have completed these setlist problems:\n"
        embed.colour = discord.Colour.purple()
    for n in newSolved:                                             # iterates through setlist solutions, appends to solved, and awards points
        problemID, problemName, problemDifficulty, isInBlind75 = n  # gets information from tuple provided
        player["SOLVED"].append(int(problemID))
        msgContent += f"- **{problemName}**, a {'Blind 75 and Neetcode 150' if isInBlind75 else 'Neetcode 150'} problem " \
                      f"worth **{givePoints(player, problemDifficulty, False)} points!**\n\n"

    if msgContent == "":                                            # if string is empty, there were no valid submissions
        msgContent = "You do not have any valid submissions. Please do `-lotd` to see the LeetCode of the Day " \
                     "question or `-blind75` or `-neetcode150` to see valid questions for those problem sets."
        embed.colour = discord.Colour.red()
    elif player["SCORE"] - oldScore != 0:                           # if score has changed, announce new points earned
        msgContent += f"You just earned {player['SCORE'] - oldScore} points! You now have a total of {player['SCORE']} points!"
    embed.description = msgContent
    setPlayer(ctx.author.id, player)                                # save data
    await msg.edit(embed=embed)                                     # edit the "Checking..." message with the new information


def checkLOTD(question, lastSubmits):
    qotd = question["QUESTIONSLUG"]                                 # uses question slugs to identify if LOTD slug is in player submissions
    for sub in lastSubmits:
        if sub["titleSlug"] == qotd:                                # for every submission, if a title slug matched LOTD slug, return True
            return True
    return False                                                    # return false if no submissions have LOTD slug

def checkSetlists(player, lastSubmits):                             # checks if any of the last submissions are in the blind75 or neetcode150 setlists
    with open("problemSetInfo/setlistProblemIDs.json", "r") as readFile:
        setlist = json.load(readFile)
    nameToID = setlist["NAME"]
    IDtoProblem = setlist["ID"]
    alreadySolved = set(player["SOLVED"])
    newSolutions = []
    for sub in lastSubmits:
        titleSlug = sub["titleSlug"]
        if titleSlug in nameToID:                                   # if it is in nameToID, it is in a setlist
            probID = int(nameToID[titleSlug])
            if probID not in alreadySolved:                         # make sure the problem isnt already submitted by the player
                problemInfo = IDtoProblem[str(probID)]
                name = problemInfo["TITLE"]
                difficulty = problemInfo["DIFFICULTY"]
                isBlind75 = problemInfo["INBLIND75"]
                newSolutions.append((probID, name, difficulty, isBlind75))  # tuples have the problem's ID, name, difficulty, and whether it is in the blind75.
    return newSolutions                                             # returns list of tuples




def givePoints(player, difficulty, isLOTD):
    EASYLOTDSCORE = 2
    MEDIUMLOTDSCORE = 3
    HARDLOTDSCORE = 5
    multiplier = 1                                                  # LOTD multiplies the score given by 2
    if isLOTD:
        multiplier = 2
    if difficulty == "Easy":                                        # give out score based on difficulty
        player["SCORE"] += (EASYLOTDSCORE * multiplier)
        pointsGiven = (EASYLOTDSCORE * multiplier)
    elif difficulty == "Medium":
        player["SCORE"] += (MEDIUMLOTDSCORE * multiplier)
        pointsGiven = (MEDIUMLOTDSCORE * multiplier)
    else:
        player["SCORE"] += (HARDLOTDSCORE * multiplier)
        pointsGiven = (HARDLOTDSCORE * multiplier)
    player["HASSOLVEDTODAY"] = True                                 # set HASSOLVEDTODAY to true, done last to reduce chance of multiple submissions (race condition)
    return pointsGiven                                              # returns pointsGiven to be used in the congratulation message, reduces recomputation a little
