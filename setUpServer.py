import os
import json
import discord
from lcUtils import getEmbed
from discord.ext import commands


async def setChannel(ctx):
    embed = getEmbed()
    if ctx.author.guild_permissions.administrator:
        serverId = str(ctx.guild.id)
        channelId = ctx.channel.id

        with open(f"./servers/{serverId}.json", "r") as readFile:
            server = json.load(readFile)
        server["LOTDCHANNEL"] = channelId
        with open(f"./servers/{serverId}.json", "w") as writeFile:
            json.dump(server, writeFile)
        embed.color = discord.Colour.green()
        embed.description = f"LeetCode of the Day will now be posted to \"{ctx.channel.name}.\""
        await ctx.send(embed=embed)
    else:
        embed.color = discord.Colour.green()
        embed.description = f"You need to be an administrator to do this."
        await ctx.send(embed=embed)

async def setPing(ctx, ping):
    embed = getEmbed()
    if ping is None or not ping.startswith("<@"):
        embed.color = discord.Colour.red()
        embed.description = "Invalid ping. Syntax: `-setping @role`."
        await ctx.send(embed=embed)
        return
    if ctx.author.guild_permissions.administrator:
        serverId = str(ctx.guild.id)
        with open(f"./servers/{serverId}.json", "r") as readFile:
            server = json.load(readFile)
        server["LOTDPING"] = ping
        with open(f"./servers/{serverId}.json", "w") as writeFile:
            json.dump(server, writeFile)
        embed.color = discord.Colour.green()
        embed.description = f"LeetCode of the Day will now ping {ping}."
        await ctx.send(embed=embed)
    else:
        embed.color = discord.Colour.green()
        embed.description = f"You need to be an administrator to do this."
        await ctx.send(embed=embed)
