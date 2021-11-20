import re
import requests
from functools import lru_cache

GAME_DATA_ENDPOINT = 'https://127.0.0.1:2999/liveclientdata/allgamedata'
CHAMPION_INFO_ENDPOINT = 'https://raw.communitydragon.org/latest/game/data/characters/{champion}/{champion}.bin.json'
DEFAULT_RADIUS = 65.
DEFAULT_WINDUP = 0.3


def clean_champion_name(name):
    return name.split('game_character_displayname_')[1].lower()


class ChampionStats():
    def __init__(self):
        game_data = requests.get(GAME_DATA_ENDPOINT, verify=False).json()
        champion_names = [clean_champion_name(player['rawChampionName']) for player in game_data['allPlayers']]
        self.champion_data = {}
        for champion in champion_names:
            champion_response = requests.get(CHAMPION_INFO_ENDPOINT.format(champion=champion)).json()
            # lower case everything for consistency
            self.champion_data[champion] = {k.lower(): v for k, v in champion_response.items()}

    @lru_cache(maxsize=None)
    def get_attack_speed(self, target):
        root_key = 'characters/{}/characterrecords/root'.format(target.lower())
        attack_speed_base = self.champion_data[target.lower()][root_key]['attackSpeed']
        attack_speed_ratio = self.champion_data[target.lower()][root_key]['attackSpeedRatio']
        return attack_speed_base, attack_speed_ratio

    @lru_cache(maxsize=None)
    def get_windup(self, target):
        root_key = 'characters/{}/characterrecords/root'.format(target.lower())
        try:
            windup_time = self.champion_data[target.lower()][root_key]['basicAttack']['mAttackDelayCastOffsetPercent'] + DEFAULT_WINDUP
        except KeyError:
            # todo: for some reason champs like Jinx don't have this
            # maybe it's because she has two different auto attack types?
            windup_time = 0.3
            print("Failed to find windup time for champion {}. Defaulting to inefficient 30%".format(target))
        return windup_time

    @lru_cache(maxsize=None)
    def get_radius(self, target):
        root_key = 'characters/{}/characterrecords/root'.format(target.lower())
        return self.champion_data[target.lower()][root_key].get('overrideGameplayCollisionRadius', DEFAULT_RADIUS)

    def names(self):
        return self.champion_data.keys()

    @lru_cache(maxsize=None)
    def get_spells(self, target):
        # castRange, castFrame, mDataValues
        root_key = 'characters/{}/characterrecords/root'.format(target.lower())
        return [
            self.champion_data[target.lower()]['characters/{}/spells/{}'.format(target.lower(), spell.lower())]['mSpell']
            for spell in self.champion_data[target.lower()][root_key]['spellNames']
        ]

    @lru_cache(maxsize=None)
    def is_melee(self, target):
        root_key = 'characters/{}/characterrecords/root'.format(target.lower())
        identities = self.champion_data[target.lower()][root_key]['purchaseIdentities']
        return any(identity for identity in identities if identity == 'Melee')
