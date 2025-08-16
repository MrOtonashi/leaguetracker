import os
from wsgiref import headers
from dotenv import load_dotenv
import discord
from discord.ext import commands
import requests

# Loading environment variables
load_dotenv() 
TOKEN = os.getenv("DISCORD_TOKEN")
API_KEY = os.getenv("RIOT_API_KEY")


# Discord bot setup
intents = discord.Intents.default()
intents.message_content = True 
bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

# Mohanad Account Info
game_name = "MPGGLOL"
tag_line = "KIRYU"
region = "asia"


# Functions

# Function to get the PUUID for a given game name and tag line
def get_puuid():
    """
    Function to get the PUUID for a given game name and tag line.
    """
    url = f"https://{region}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{game_name}/{tag_line}"
    headers = {"X-Riot-Token": API_KEY}
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        return data.get("puuid")
    else:
        print(f"Error {response.status_code}: {response.text}")
        return None

# Function to get recent match IDs using the PUUID
def get_recent_match_ids():
    url = f"https://{region}.api.riotgames.com/lol/match/v5/matches/by-puuid/{get_puuid()}/ids"
    params = {"count": 1}
    response = requests.get(url, headers=headers, params=params)
    return response.json()

# Function to check if the latest match is a loss
def is_loss(match_id):
    url = f"https://{region}.api.riotgames.com/lol/match/v5/matches/{match_id}"
    response = requests.get(url, headers=headers)
    match_data = response.json()
    for p in match_data["info"]["participants"]:
        if p["puuid"] == get_puuid():
            return not p["win"]
    return False

# Function to send a message alerting it in discord
def send_to_discord(match_id):
    data = {
        "content": f"😢 MPGGLOL Lost a game! Match ID: {match_id}\nhttps://www.op.gg/summoners/REGION/SUMMONER_NAME"
    }
    requests.post("https://discord.com/api/webhooks/1406092359388889318/NmjS_E3e-EooUGR-EqQGGH75b2KoaRIcs8Av9clzCO4-X156qLUKrhZZbVlv9SvUAp7U", json=data)



# Function to check when MPGG gets a loss
def check_losses(match_history):
    """
    Function to check when MPGG gets a loss.
    """
    losses = []
    for match_id in match_history:
        url = f"https://{region}.api.riotgames.com/lol/match/v5/matches/{match_id}"
        headers = {"X-Riot-Token": API_KEY}
        
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            match_data = response.json()
            participants = match_data.get("info", {}).get("participants", [])
            for participant in participants:
                if participant.get("puuid") == get_puuid():
                    if participant.get("win") is False:
                        losses.append(match_id)
        else:
            print(f"Error {response.status_code}: {response.text}")
    
    return losses


@bot.event
async def on_ready():
    try:
        await bot.tree.sync()
        print(f"✅ Logged in as {bot.user}. Slash commands synced.")
    except Exception as e:
        print("Slash command sync failed:", e)

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


@bot.tree.command(name="tea", description="yoda tea")
async def tea(interaction: discord.Interaction):
    file = discord.File("images/tea.jpg", filename="tea.jpg")
    await interaction.response.send_message(file=file)


if __name__ == "__main__":
    if not TOKEN:
        raise RuntimeError("DISCORD_TOKEN not set. Put it in .env or your environment.")
    bot.run(TOKEN)
