import os

import discord
import json
from os.path import exists

async def setUpPlayer(ctx):
    playerID = str(ctx.author.id)
    playerName = str(ctx.author.name)
    playerDiscriminator = str(ctx.author.discriminator)
    serverID = str(ctx.guild.id)
    serverName = str(ctx.guild.name)
    if not exists(f"./servers/{serverID}.json"):                    # if the server has never been initialized, make it
        with open("./initFiles/server.json", "r") as readFile:
            serverInfo = json.load(readFile)
        serverInfo["NAME"] = serverName
    else:
        with open(f"./servers/{serverID}.json", "r") as readFile:   # if server info exists, retrieve it
            serverInfo = json.load(readFile)
    if playerID not in serverInfo["PLAYERS"]:                       # if player is not registered as a member of the server
        serverInfo["PLAYERS"].append(playerID)
        with open(f"./servers/{serverID}.json", "w") as writeFile:  # save server info (also works for initializing
            json.dump(serverInfo, writeFile)                        # because player will always not be in the server if it didnt exist)
    if not exists(f"./players/{playerID}.json"):                    # if player has never registered, set up profile
        with open(f"initFiles/player.json", "r") as readFile:
            playerInfo = json.load(readFile)
        playerInfo["NAME"] = playerName
        playerInfo["DISCRIMINATOR"] = playerDiscriminator
        with open(f"./players/{playerID}.json", "w") as writeFile:  # save player info
            json.dump(playerInfo, writeFile)
