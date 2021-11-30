import sys
import pygame
import win32gui
import gui

from urllib3 import disable_warnings
from time import sleep
from pymem import Pymem
from world import find_champion_pointers, find_game_time, find_local_net_id, find_view_proj_matrix, read_object
from champion_stats import ChampionStats
from constants import PROCESS_NAME
from orbwalker import OrbWalker


def main():
    disable_warnings()
    pygame.display.init()
    pygame.font.init()

    overlay = gui.create_overlay(gui.get_game_window())
    win32gui.BringWindowToTop(gui.get_game_window()[4])
    pygame.event.set_grab(True)

    mem = Pymem(PROCESS_NAME)
    champion_stats = ChampionStats()
    orb_walker = OrbWalker(mem)
    champion_pointers = find_champion_pointers(mem, champion_stats.names())

    settings = gui.Settings()

    while True:
        try:
            champions = [read_object(mem, pointer) for pointer in champion_pointers]
            net_id_to_champion = {c.network_id: c for c in champions}
            local_net_id = find_local_net_id(mem)
            active_champion = net_id_to_champion[local_net_id]
            view_proj_matrix, width, height = find_view_proj_matrix(mem)
            game_time = find_game_time(mem)

            game_window = gui.get_game_window()
            window_focused = game_window[4] == win32gui.GetForegroundWindow()
            overlay.fill(gui.Colors.trans)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    break
            if window_focused:
                if settings.menu:
                    gui.game_menu(overlay, settings)

                if settings.orb_walker:
                    orb_walker.run(champion_stats, active_champion, champions, view_proj_matrix, width, height, game_time)

                if settings.show_enemy_spell_cd:
                    gui.draw_enemy_spell_cd(overlay, active_champion, champions, view_proj_matrix, width, height, game_time)

            gui.reset_overlay(game_window)
            pygame.display.flip()
            sleep(0.01)
        except KeyboardInterrupt:
            sys.exit("Bye")
        except UnicodeDecodeError:
            pass


if __name__ == '__main__':
    main()
