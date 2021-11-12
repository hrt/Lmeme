import time
import keyboard
from pymem import Pymem
from world import find_objects, find_local_net_id, find_game_time, find_view_proj_matrix, world_to_screen
from champion_stats import ChampionStats
from target import select_lowest_target
from constants import PROCESS_NAME
from orbwalker import OrbWalker


def main():
    mem = Pymem(PROCESS_NAME)
    champion_stats = ChampionStats()
    initial_game_time = champion_stats.game_time
    orb_walker = OrbWalker(initial_game_time)
    blacklist = set()
    while True:
        game_time = find_game_time(mem)
        champions = find_objects(mem, blacklist, champion_stats)
        local_net_id = find_local_net_id(mem)
        active_champion = champions[local_net_id]
        view_proj_matrix, width, height = find_view_proj_matrix(mem)

        target = None
        orb_walk = keyboard.is_pressed(' ')
        if orb_walk:
            target = select_lowest_target(champion_stats, active_champion, champions)

        x, y = None, None
        if target is not None:
            x, y = world_to_screen(view_proj_matrix, width, height, target.x, target.z, target.y)

        if orb_walk:
            orb_walker.walk(champion_stats, active_champion, game_time, x, y)

        time.sleep(0.01)


if __name__ == '__main__':
    main()
