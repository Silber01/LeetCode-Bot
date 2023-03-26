import discord
import json
from lcUtils import getPlayer, getEmbed
import os

async def leaderboard(ctx, page, isGlobal):
    players = []
    if isGlobal:
        players = os.listdir("players")
        serverName = "Global"
    else:
        serverID = ctx.guild.id
        with open(f"servers/{serverID}.json", "r") as readFile:
            serverInfo = json.load(readFile)
        for p in serverInfo["PLAYERS"]:
            players.append(f"{p}.json")
        serverName = f"{serverInfo['NAME']}'s"
    await getLeaderboard(ctx, page, players, serverName)



async def getLeaderboard(ctx, page, players, serverName):
    scores = []
    pageSize = 10
    embed = getEmbed()
    try:
        page = int(page)
    except ValueError:
        embed.color = discord.Colour.red()
        embed.description = "Please insert a value for the page, e.g. `-top 3`."
        await ctx.send(embed=embed)
        return

    start = pageSize * (page-1)

    if start >= len(players):                                       # if start is too big
        embed.color = discord.Colour.red()
        embed.description = "That page does not exist. Try searching for a smaller page."
        await ctx.send(embed=embed)
        return
    if page < 1:                                                    # if start is too small
        embed.color = discord.Colour.red()
        embed.description = "That page does not exist. Try searching for a larger page."
        await ctx.send(embed=embed)
        return
    thisPlayer = getPlayer(ctx.author.id)
    targetPlayer = thisPlayer["NAME"], thisPlayer["SCORE"]
    embed.color = discord.Colour.purple()
    end = min((pageSize * page), len(players))                      # checks to make sure it doesnt overflow
    for p in players:                                               # get all players and add them to the unsorted leaderboard
        with open(f"players/{p}", "r") as readFile:
            playerInfo = json.load(readFile)
        scores.append((playerInfo["NAME"], playerInfo["SCORE"]))
    scores = sorted(scores, key=lambda x: x[1], reverse=True)       # sort the leaderboard
    embed.description = f"**{serverName} Leaderboard:**\n```"
    for i, p in enumerate(scores[start:end]):
        name, score = p
        embed.description += f"{(str(start+i+1)+'.').ljust(4)} {name.ljust(32, '.')}{str(score).rjust(5)} points\n"
    embed.description += f"```\nYou are in position #{scores.index(targetPlayer)+1}\n\n"
    embed.description += f"To view the leaderboard in this server, do `-top <page>`. To see the global leaderboard, do `-gtop <page>`." \
                         f" Note: For a user to be in a server's leaderboard, they must have used at least one LeetCode Bot command in the server."
    await ctx.send(embed=embed)

