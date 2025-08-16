import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
import requests

load_dotenv() 
TOKEN = os.getenv("DISCORD_TOKEN")
api_key = os.getenv("RIOT_API_KEY")


if not api_key:
    raise RuntimeError("RIOT_API_KEY not found. Put it in your .env file.")


intents = discord.Intents.default()
intents.message_content = True 

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())


game_name = "MPGGLOL"
tag_line = "KIRYU"
region = "europe"


# Build request
url = f"https://{region}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{game_name}/{tag_line}"
headers = {"X-Riot-Token": api_key}

# Fetch data
response = requests.get(url, headers=headers)



@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}!")

@bot.command()
async def hello(ctx):
    await ctx.send("Hello! I'm alive.")

@bot.command()
async def mpggstats(ctx):
    await ctx.send("Fetching MPGG stats...")
    if response.status_code == 200:
        data = response.json()
        print("Account data:", data)
        await ctx.send(f"Account data: {data}")
    else:
        print(f"Error {response.status_code}: {response.text}")
        await ctx.send(f"Error {response.status_code}: {response.text}")
    

if __name__ == "__main__":
    if not TOKEN:
        raise RuntimeError("DISCORD_TOKEN not set. Put it in .env or your environment.")
    bot.run(TOKEN)
