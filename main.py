import time
import keyboard
import twitch
from pymem import Pymem
from world import find_champion_pointers, find_game_time, find_local_net_id, find_view_proj_matrix, read_object, world_to_screen
from champion_stats import ChampionStats
from target import select_lowest_target
from constants import PROCESS_NAME
from orbwalker import OrbWalker


def main():
    mem = Pymem(PROCESS_NAME)
    champion_stats = ChampionStats()
    orb_walker = OrbWalker(mem)
    champion_pointers = find_champion_pointers(mem, champion_stats.names())
    while True:
        champions = [read_object(mem, pointer) for pointer in champion_pointers]
        net_id_to_champion = {c.network_id: c for c in champions}
        local_net_id = find_local_net_id(mem)
        active_champion = net_id_to_champion[local_net_id]
        view_proj_matrix, width, height = find_view_proj_matrix(mem)
        game_time = find_game_time(mem)

        target = None
        orb_walk = keyboard.is_pressed(' ')
        if orb_walk:
            target = select_lowest_target(champion_stats, active_champion, champions)

        x, y = None, None
        if target is not None:
            x, y = world_to_screen(view_proj_matrix, width, height, target.x, target.z, target.y)

        if orb_walk:
            orb_walker.walk(champion_stats, active_champion, x, y, game_time)
        time.sleep(0.005)


if __name__ == '__main__':
    main()
