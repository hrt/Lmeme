from time import sleep

import keyboard
import mouse

from target import select_lowest_target
from world import find_game_time
from world import world_to_screen

LETHAL_TEMPO = 'ASSETS/Perks/Styles/Precision/LethalTempo/LethalTempo.lua'
HAIL_OF_BLADES = 'ASSETS/Perks/Styles/Domination/HailOfBlades/HailOfBladesBuff.lua'
LETHAL_TEMPO_STACKS_UNCAPPED_RANGED = 30.
LETHAL_TEMPO_STACKS_UNCAPPED_MELEE = 90.


class OrbWalker:
    def __init__(self, mem):
        self.mem = mem
        game_time = find_game_time(self.mem)
        self.can_attack_time = game_time
        self.can_move_time = game_time

    @staticmethod
    def get_attack_time(champion, attack_speed_base, attack_speed_ratio, attack_speed_cap):
        total_attack_speed = min(attack_speed_cap,
                                 (champion.attack_speed_multiplier - 1) * attack_speed_ratio + attack_speed_base)
        return 1. / total_attack_speed

    @staticmethod
    def get_windup_time(champion, attack_speed_base, attack_speed_ratio, windup_percent, windup_modifier,
                        attack_speed_cap):
        # More information at https://leagueoflegends.fandom.com/wiki/Basic_attack#Attack_speed
        attack_time = OrbWalker.get_attack_time(champion, attack_speed_base, attack_speed_ratio, attack_speed_cap)
        base_windup_time = (1 / attack_speed_base) * windup_percent
        windup_time = base_windup_time + ((attack_time * windup_percent) - base_windup_time) * windup_modifier
        return min(windup_time, attack_time)

    @staticmethod
    def get_attack_speed_cap(stats, champion, game_time):
        uncapped = False
        lethal_tempo_buffs = [buff for buff in champion.buffs[LETHAL_TEMPO] if buff.end_time > game_time]
        assert len(lethal_tempo_buffs) <= 1
        if lethal_tempo_buffs:
            lethal_tempo, = lethal_tempo_buffs
            if stats.is_melee(champion.name):
                uncapped |= lethal_tempo.count >= LETHAL_TEMPO_STACKS_UNCAPPED_MELEE
            else:
                uncapped |= lethal_tempo.count >= LETHAL_TEMPO_STACKS_UNCAPPED_RANGED
        uncapped |= any([buff.end_time > game_time for buff in champion.buffs[HAIL_OF_BLADES]])
        if uncapped:
            return 90.
        return 2.5

    def walk(self, stats, champion, x, y, game_time):
        mouse.press(mouse.MIDDLE)
        attack_speed_cap = OrbWalker.get_attack_speed_cap(stats, champion, game_time)
        if x is not None and y is not None and self.can_attack_time < game_time:
            stored_x, stored_y = mouse.get_position()
            mouse.move(int(x), int(y))
            mouse.right_click()
            sleep(0.01)
            game_time = find_game_time(self.mem)
            attack_speed_base, attack_speed_ratio = stats.get_attack_speed(champion.name)
            windup_percent, windup_modifier = stats.get_windup(champion.name)
            self.can_attack_time = game_time + OrbWalker.get_attack_time(champion, attack_speed_base,
                                                                         attack_speed_ratio, attack_speed_cap)
            self.can_move_time = game_time + OrbWalker.get_windup_time(champion, attack_speed_base, attack_speed_ratio,
                                                                       windup_percent, windup_modifier,
                                                                       attack_speed_cap)
            mouse.move(stored_x, stored_y)
        elif self.can_move_time < game_time:
            mouse.right_click()
            move_click_delay = 0.05
            self.can_move_time = game_time + move_click_delay
        mouse.release(mouse.MIDDLE)

    def cast(self, x, y, spell):
        mouse.press(mouse.MIDDLE)
        if x is not None and y is not None:
            stored_x, stored_y = mouse.get_position()
            mouse.move(int(x), int(y))
            keyboard.press_and_release('w')
            sleep(0.01)
            game_time = find_game_time(self.mem)
            self.can_attack_time = game_time + 0.25
            self.can_move_time = game_time + 0.25
            mouse.move(stored_x, stored_y)
        mouse.release(mouse.MIDDLE)

    def run(self, champion_stats, active_champion, champions, view_proj_matrix, width, height, game_time):
        target = None
        orb_walk = keyboard.is_pressed(' ')
        if orb_walk:
            target = select_lowest_target(champion_stats, active_champion, champions)

        x, y = None, None
        if target is not None:
            x, y = world_to_screen(view_proj_matrix, width, height, target.x, target.z, target.y)

        if orb_walk:
            self.walk(champion_stats, active_champion, x, y, game_time)
