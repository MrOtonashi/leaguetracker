import os
from discord.ext import commands
import requests
from dotenv import load_dotenv

env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path=env_path)


API_KEY = os.getenv("RIOT_API_KEY")
headers = {"X-Riot-Token": API_KEY}

region = "europe"



def get_puuid(game_name, tag_line):
    """
    Function to get the PUUID for a given game name and tag line.
    """
    url = f"https://{region}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{game_name}/{tag_line}"
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        return data.get("puuid")
    else:
        print(f"Error {response.status_code}: {response.text}")
        return None

# count parameter for how many matches you want to get
def get_recent_match_ids(count, puuid):
    url = f"https://{region}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids"
    params = {"count": count}
    response = requests.get(url, headers=headers, params=params)
    return response.json()

def get_match_data(match_id):
    url = f"https://{region}.api.riotgames.com/lol/match/v5/matches/{match_id[0]}"
    response = requests.get(url, headers=headers)
    return response.json()

def get_target(game_name, tag_line):

    try:
        puuid = get_puuid(game_name, tag_line)
        match = get_match_data(get_recent_match_ids(1, puuid))
        
        count = 0
        for participant in match["metadata"]["participants"]:
            if participant == puuid:
                break
            count += 1
        
        target = match["info"]["participants"][count]
        return target
    
    except:
        return "Error, name or tag might be wrong dummy"

def wardscore(game_name, tag_line):

    target = get_target(game_name, tag_line)

    if type(target) is str:
        message = target
        return message

    missing_ping = target["enemyMissingPings"]
    vision_ping = target["enemyVisionPings"]

    message = f"Last match {game_name} toxic pings: \n" \
    f"Vision ping: {vision_ping} times \n" \
    f"Missing ping: {missing_ping} times"
    
    return message


__all__ = [
    "get_puuid",
    "get_recent_match_ids",
    "get_match_data",
    "toxic_score",
    "API_KEY",
    "region",
]
