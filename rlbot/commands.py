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
    async def addplayer(ctx, name: str, game_name: str, tag: str):
        store_player(name, game_name, tag)
        await ctx.send(f"Player {game_name}#{tag} added as {name}!")

    
    @bot.command()
    async def wardscore(ctx, name: str, tag: str):
        await ctx.send(ward_score(name, tag))

   