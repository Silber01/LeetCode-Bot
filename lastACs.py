import requests
import json
import discord
from datetime import datetime


async def showLastSolved(ctx, user, amount):
    embed = discord.Embed(title="LeetCode Bot")
    embed.colour = discord.Colour.purple()
    embed.description = "Retrieving Data..."
    waitMsg = await ctx.send(embed=embed)
    acs = getLastACs(user, amount)                                      # calls method to get last AC's (all clears)
    print(acs)
    if acs == "INVALID":                                                # returns this if user doesnt exist
        embed.colour = discord.Colour.red()
        embed.description = "Sorry, that user does not exist."
        await ctx.send(embed=embed)
        return
    embed.description = f"Here are the last questions **{user}** solved:"
    for i in range(len(acs)):
        ac = dict(acs[i])                                               # goes through each dict in list and returns info
        name = ac["title"]
        date = datetime.fromtimestamp(int(ac["timestamp"]))
        embed.description += f"\n\n**Name**: {name}\n **Date**: {date}"
    await waitMsg.edit(embed=embed)


def getLastACs(user, amount):
    amount = min(1000, amount)                                # limits amount of questions to 10 to prevent overworking
    query = f"""query recentAcSubmissions($username: String!) {{
        recentAcSubmissionList(username: $username) {{
          id
          title
          titleSlug
          timestamp
        }}
      }}"""
    params = f"""{{
          "username": "{user}"
      }}"""
    url = 'https://leetcode.com/graphql'                    # sends query and params to this url in a post request

    r = requests.post(url, json={'query': query, 'variables': params})
    if "User matching query does not exist" in str(json.loads(r.text)): # this is returned when a user doesnt exist
        return "INVALID"
    return (r.json())["data"]["recentAcSubmissionList"]


