import time
import keyboard
from pymem import Pymem
from world import find_champion_pointers, find_minion_pointers, find_game_time, find_local_net_id, find_view_proj_matrix, read_object, world_to_screen
from champion_stats import ChampionStats
from target import select_lowest_target, select_lasthit_target
from constants import PROCESS_NAME
from orbwalker import OrbWalker


def main():
    mem = Pymem(PROCESS_NAME)
    champion_stats = ChampionStats()
    orb_walker = OrbWalker(mem)
    champion_pointers = find_champion_pointers(mem, champion_stats.names())
    minion_pointers = find_minion_pointers(mem)
    previous_game_time = 0
    while True:
        minions = [read_object(mem, pointer) for pointer in minion_pointers]
        champions = [read_object(mem, pointer) for pointer in champion_pointers]
        net_id_to_champion = {c.network_id: c for c in champions}
        local_net_id = find_local_net_id(mem)
        active_champion = net_id_to_champion[local_net_id]
        view_proj_matrix, width, height = find_view_proj_matrix(mem)
        game_time = find_game_time(mem)

        game_time_int = int(game_time)
        if (game_time_int-70) % 30 == 0 and game_time_int != previous_game_time:
            minion_pointers = find_minion_pointers(mem)
            previous_game_time = game_time_int

        target = None
        orb_walk = keyboard.is_pressed(' ')
        if orb_walk:
            target = select_lasthit_target(champion_stats, active_champion, minions)

        x, y = None, None
        if target is not None:
            x, y = world_to_screen(view_proj_matrix, width, height, target.x, target.z, target.y)

        if orb_walk:
            orb_walker.walk(champion_stats, active_champion, x, y, game_time)
        time.sleep(0.08)


if __name__ == '__main__':
    main()
