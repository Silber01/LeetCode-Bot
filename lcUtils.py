import discord
from discord.ext import commands
import json


def getPlayer(playerID):
    try:
        with open(f"players/{playerID}.json", "r") as readFile:
            account = json.load(readFile)
            return account
    except FileNotFoundError:
        return None


def setPlayer(playerID, playerData):
    with open(f"players/{playerID}.json", "w") as writeFile:
        json.dump(playerData, writeFile)

def getEmbed():
    return discord.Embed(title="LeetCode Bot")