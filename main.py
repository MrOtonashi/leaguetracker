import os
import random
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
    gif_url = random.choice(GIFS)
    title = random.choice(TITLE)
    data = {
        "embeds": [
            {
                "title": title,
                "description": f"😢 MPGGLOL Lost a game! Match ID: `{match_id}`",
                "image": {
                    "url": gif_url
                },
                "color": 16711680  # red
            }
        ]
    }
    requests.post("https://discord.com/api/webhooks/1406092359388889318/NmjS_E3e-EooUGR-EqQGGH75b2KoaRIcs8Av9clzCO4-X156qLUKrhZZbVlv9SvUAp7U", json=data)

GIFS =[
"https://tenor.com/view/jungle-diff-gif-12813900196858187534",
"https://tenor.com/view/viktorarcane-league-of-legends-lolz-lux-gg-ez-gif-23894685",
"https://tenor.com/view/kaoru-gif-22245949",
"https://tenor.com/view/league-of-legends-lol-riot-games-riot-uninstall-gif-18739871",
"https://tenor.com/view/delete-ts-bro-bro-delete-ts-gif-12236641355032177225",
"https://tenor.com/view/trash-gif-26305436",
"https://tenor.com/view/seraphine-anima-squad-quit-league-uninstall-league-sera-lol-gif-5227539488395481688",
"https://tenor.com/view/seraphine-my-beloved-league-of-legends-gif-21116791",
"https://tenor.com/view/seraphine-league-of-legends-dance-dancing-kpop-gif-19003337"
]
TITLE = [
    "Defeat... ",
    "MPGGLOL's Loss",
    "Sad Game",
    "Sad Times",
    "MPGGLOL Delete the game",
    "MPGGLOL Uninstall the game",
    "Get better MPGGLOL"
]

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
    print(f"Logged in as {bot.user}!")

@bot.command()
async def hello(ctx):
    await ctx.send("Hello! I'm alive.")


    

if __name__ == "__main__":
    if not TOKEN:
        raise RuntimeError("DISCORD_TOKEN not set. Put it in .env or your environment.")
    bot.run(TOKEN)
