import re
import requests

GAME_DATA_ENDPOINT = 'https://127.0.0.1:2999/liveclientdata/allgamedata'
CHAMPION_INFO_ENDPOINT = 'https://raw.communitydragon.org/latest/game/data/characters/{champion}/{champion}.bin.json'
DEFAULT_RADIUS = 65.
DEFAULT_WINDUP = 0.3


def clean_champion_name(name):
    return re.sub(r'[^a-zA-Z]', '', name).lower()


class ChampionStats():
    def __init__(self):
        game_data = requests.get(GAME_DATA_ENDPOINT, verify=False).json()
        self.game_time = game_data['gameData']['gameTime']
        champion_names = [clean_champion_name(player['championName']) for player in game_data['allPlayers']]
        self.champion_data = {}
        for champion in champion_names:
            champion_response = requests.get(CHAMPION_INFO_ENDPOINT.format(champion=champion)).json()
            # lower case everything for consistency
            champion_response = {k.lower(): v for k, v in champion_response.items()}
            self.champion_data[champion] = champion_response['characters/{}/characterRecords/root'.format(champion)]
            self.champion_data[champion]['radius'] = self.champion_data[champion].get('overrideGameplayCollisionRadius', DEFAULT_RADIUS)
            try:
                self.champion_data[champion]['windup'] = self.champion_data[champion]['basicAttack']['mAttackDelayCastOffsetPercent'] + DEFAULT_WINDUP
            except KeyError:
                # for some reason champs like Jinx don't have this
                # maybe it's because she has two different auto attack types?
                # skip for now - wont work if user is playing a champ like this
                continue

    def get(self, name):
        return self.champion_data[name.lower()]

    def names(self):
        return self.champion_data.keys()
