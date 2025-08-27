import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import rlbot

# Load environment variables
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# Initialize bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Start
@bot.event
async def on_ready():
    rlbot.commands.__init__(bot)

if __name__ == "__main__":
    bot.run(TOKEN)