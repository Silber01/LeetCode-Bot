import discord
from discord.ext import commands

embed = discord.Embed(title="LeetCode Bot")
embed.colour = discord.Colour.purple()

async def timeoutEmbed(ctx):
    embed.description="You ran out of time. Try again!"           
    embed.colour = discord.Colour.red()   
    await ctx.send(embed=embed)

async def registeredEmbed(ctx, leetCodeName):
    playerName = str(ctx.author.name)
    embed.description=f"You have successfully registered as `{leetCodeName}`\n Happy LeetCoding {playerName}!"
    embed.colour = discord.Colour.green()   
    await ctx.send(embed=embed)  

async def changeNameEmbed(ctx, leetCodeName):
    embed.description = f"Do you want to change your LeetCode name to `{leetCodeName}`? [Y/N]"
    await ctx.send(embed=embed) 

async def newNameEmbed(ctx, leetCodeName):
    embed.description = f"You are now `{leetCodeName}`"
    embed.colour = discord.Colour.green() 
    await ctx.send(embed=embed)  

async def changeNameDeclineEmbed(ctx,leetCodeName):
    embed.description=f"Your LeetCode name is still `{leetCodeName}`"           
    embed.colour = discord.Colour.red()   
    await ctx.send(embed=embed) 

async def unregisteringEmbed(ctx):
    embed.description= f"Are you sure you want to unregister from LeetCode Bot? [Y/N]"
    await ctx.send(embed=embed)

async def unregisteredEmbed(ctx):
    embed.description= f"You have successfully unregistered\n  Keep LEETCODING!"
    embed.colour = discord.Colour.green() 
    await ctx.send(embed=embed) 

