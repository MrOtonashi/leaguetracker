import discord
from discord.ext import commands as cmd
from rlbot.league import *

def __init__(bot):
    general(bot)

def general(bot):
    @bot.command()
    async def hello(ctx):
        await ctx.send("Hello! I'm alive.")


    @bot.command()
    async def tea(ctx):
        file = discord.File("images/tea.jpg", filename="tea.jpg")
        await ctx.send(file=file)

    @bot.command()
    async def bonk(ctx):
        file = discord.File("images/bonk.png", filename="bonk.png")
        await ctx.send(file=file)

    @bot.command()
    async def toxicscore(ctx, name: str, tag: str):
        await ctx.send(toxic_score(name, tag))