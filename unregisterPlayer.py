import os
import discord
import json
from os.path import exists
import asyncio

async def unregisterPlayer(ctx): 
    playerID = str(ctx.author.id)

    with open(f"./players/{playerID}.json") as readFile:
        playerInfo = json.load(readFile)
        
    playerInfo["LEETCODENAME"] = 'null'   # unregister player from the bot

    with open(f"./players/{playerID}.json", "w") as writeFile:  # save player info
        json.dump(playerInfo, writeFile)
    