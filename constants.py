#!/usr/bin/env python
import os
import json

API_KEY = os.environ['LOL_API_KEY']
URLS = {
        'NAME_TO_ID' : 'https://na1.api.riotgames.com/lol/summoner/v3/summoners/by-name/{name}',
        'ID_TO_NAME' : 'https://na1.api.riotgames.com/lol/summoner/v3/summoners/by-account/{id}',
        'MATCHES_BY_ID' : 'https://na1.api.riotgames.com/lol/match/v3/matchlists/by-account/{id}?season=8',
        'RECENT_MATCHES_BY_ID' : 'https://na1.api.riotgames.com/lol/match/v3/matchlists/by-account/{id}/recent',
        'MATCH_INFO': 'https://na1.api.riotgames.com/lol/match/v3/matches/{id}', 
        'RECENT_TEN' : 'https://na.api.riotgames.com/api/lol/NA/v1.3/game/by-summoner/{summonerId}/recent',
        }
HEADERS = {'X-Riot-Token' : API_KEY}

CHAMP_BY_ID = {}
with open('champ_by_id.json') as f:
    CHAMP_BY_ID = json.load(f)

CHAMP_BY_NAME = {}
with open('champ_by_name.json') as f:
    CHAMP_BY_NAME = json.load(f)


print(CHAMP_BY_ID['data']['236'])
#"queue": 2 or 400
