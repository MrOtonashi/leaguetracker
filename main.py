import os
from dotenv import load_dotenv
import discord
from discord.ext import commands

load_dotenv() 
TOKEN = os.getenv("DISCORD_TOKEN")


intents = discord.Intents.default()
intents.message_content = True 

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}!")

@bot.command()
async def hello(ctx):
    await ctx.send("Hello! I'm alive.")

if __name__ == "__main__":
    if not TOKEN:
        raise RuntimeError("DISCORD_TOKEN not set. Put it in .env or your environment.")
    bot.run(TOKEN)
