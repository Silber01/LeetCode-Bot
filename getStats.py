import json
import os
import discord
from discord.ext import commands
from lcUtils import *

async def getStats(ctx):
  embed = getEmbed()
  playerId = str(ctx.author.id)

  with open(f"players/{playerId}.json", "r") as readFile:
    player = json.load(readFile)

  if not player["LEETCODENAME"]:
    embed.description = "You have not registered your Leetcode name yet. Use `-register <LeetCode name>` to register."
    embed.colour = discord.Colour.red()

  else:
    if player["HASSOLVEDTODAY"]:
      status = "Solved"
    else:
      status = "Not Solved"

    embed.description = f"**{player['LEETCODENAME']}**'s stats:"
    embed.add_field(name="Current Score:", value=player["SCORE"], inline=False)
    embed.add_field(name="Total LOTD Solved:", value=player["LOTDSSOLVED"], inline=False)
    embed.add_field(name="Today's LOTD Status:", value=status, inline=False)
    embed.add_field(name="Blind 75 Solved:", value=len(player["BLIND75SOLVED"]), inline=False)
    embed.add_field(name="NeetCode 150 Solved:", value=len(player["NEETCODE150SOLVED"]), inline=False)
    embed.colour = discord.Colour.gold()

  await ctx.send(embed=embed)