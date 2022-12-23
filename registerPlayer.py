import os
import discord
import json
from os.path import exists
import asyncio
from discord.ext import commands
from embedMsg import *

async def registerPlayer(ctx, leetCodeName): 
    playerID = str(ctx.author.id)

    with open(f"./players/{playerID}.json") as readFile:
        playerInfo = json.load(readFile)

    playerInfo["LEETCODENAME"] = leetCodeName   # register LeetCode name for player
    await registeredEmbed(ctx, leetCodeName)

    with open(f"./players/{playerID}.json", "w") as writeFile:  # save player info
        json.dump(playerInfo, writeFile)

def getPlayerLCName(ctx):
    playerID = str(ctx.author.id)
    with open(f"./players/{playerID}.json") as readFile:
        playerInfo = json.load(readFile)
    
    return playerInfo["LEETCODENAME"]