import os
import json
import discord
from discord.ext import commands

async def getChannel(ctx):
  if (ctx.author.guild_permissions.administrator):
    serverId = str(ctx.guild.id)
    channelId = ctx.channel.id

    with open(f"./servers/{serverId}.json", "r") as readFile:
      server = json.load(readFile)
    server["LOTDCHANNEL"] = channelId
    with open(f"./servers/{serverId}.json", "w") as writeFile:
      json.dump(server, writeFile)
    await ctx.send("Channel is set!")
  else:
    await ctx.send("You don't have permission to do that!")
