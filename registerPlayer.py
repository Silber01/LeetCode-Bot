import os
from urllib.request import urlopen

import discord
import asyncio
from discord.ext import commands
from lcUtils import *
from setupPlayer import *


async def handleRegister(ctx, leetCodeName, client):
    playerInfo = getPlayer(ctx.author.id)
    embed = getEmbed()
    if not checkIfAccExists(leetCodeName):
        embed.description = f"{leetCodeName} is not a valid LeetCode account! Make sure that you are using the name of your LeetCode account."
        embed.colour = discord.Colour.red()
        await ctx.send(embed=embed)
        return
    if playerInfo is None:
        registerPlayer(ctx, leetCodeName)  # register LeetCode name for player
        embed.description = f"You have successfully registered your LeetCode account as `{leetCodeName}`\n Happy LeetCoding, {ctx.author.name}!"
        embed.colour = discord.Colour.green()
        await ctx.send(embed=embed)
        return
    if playerInfo["LEETCODENAME"] != leetCodeName:
        embed.description = f"Do you want to reregister your LeetCode account as `{leetCodeName}`? WARNING: THIS WILL RESET YOUR DATA! [Y/N]"
        embed.colour = discord.Colour.purple()
        await ctx.send(embed=embed)

        def check(m):
            return m.author == ctx.author
        try:
            msg = await client.wait_for("message", timeout=15, check=check)
        except asyncio.TimeoutError:
            embed.description = "You ran out of time. Try again!"
            embed.colour = discord.Colour.red()
            await ctx.send(embed=embed)
            return
        if msg.content.upper() in ["Y", "YES"]:  # set the new name for the player
            unregisterPlayer(ctx)
            registerPlayer(ctx, leetCodeName)
            embed.description = f"Your LeetCode account is now registered as `{leetCodeName}`"
            embed.colour = discord.Colour.green()
            await ctx.send(embed=embed)
            return
        else:
            embed.description = f"No changes have been made."
            embed.colour = discord.Colour.purple()
            await ctx.send(embed=embed)
            return
    embed.description = f"Your LeetCode account is already \"{leetCodeName}\"!"
    embed.colour = discord.Colour.red()
    await ctx.send(embed=embed)


def registerPlayer(ctx, leetCodeName):
    setUpPlayer(ctx)
    playerInfo = getPlayer(ctx.author.id)
    playerInfo["LEETCODENAME"] = leetCodeName   # register LeetCode name for player
    setPlayer(ctx.author.id, playerInfo)


def unregisterPlayer(ctx):
    os.remove(f"players/{ctx.author.id}.json")


def checkIfAccExists(leetCodeName):
    url = "https://leetcode-stats-api.herokuapp.com/" + leetCodeName
    leetCodeData = json.loads(urlopen(url).read())
    if leetCodeData["status"] != "success":
        return False
    return True
