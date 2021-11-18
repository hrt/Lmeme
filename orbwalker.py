import time
import mouse
import keyboard
from world import find_game_time

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
    def get_attack_time(champion, base_attack_speed, attack_speed_cap):
        attack_speed = min(attack_speed_cap, champion.attack_speed_multiplier * base_attack_speed)
        return 1. / attack_speed

    @staticmethod
    def get_windup_time(champion, base_attack_speed, windup, attack_speed_cap):
        return OrbWalker.get_attack_time(champion, base_attack_speed, attack_speed_cap) * windup

    @staticmethod
    def get_attack_speed_cap(stats, champion, game_time):
        uncapped = False
        lethal_tempo_buffs =  [buff for buff in champion.buffs[LETHAL_TEMPO] if buff.end_time > game_time]
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
            time.sleep(0.01)
            game_time = find_game_time(self.mem)
            attack_speed = stats.get_attack_speed(champion.name)
            windup = stats.get_windup(champion.name)
            self.can_attack_time = game_time + OrbWalker.get_attack_time(champion, attack_speed, attack_speed_cap)
            self.can_move_time = game_time + OrbWalker.get_windup_time(champion, attack_speed, windup, attack_speed_cap)
            mouse.move(stored_x, stored_y)
        elif self.can_move_time < game_time:
            mouse.right_click()
            MOVE_CLICK_DELAY = 0.05
            self.can_move_time = game_time + MOVE_CLICK_DELAY
        mouse.release(mouse.MIDDLE)

    def cast(self, x, y, spell):
        mouse.press(mouse.MIDDLE)
        if x is not None and y is not None:
            stored_x, stored_y = mouse.get_position()
            mouse.move(int(x), int(y))
            keyboard.press_and_release('w')
            time.sleep(0.01)
            game_time = find_game_time(self.mem)
            self.can_attack_time = game_time + 0.25
            self.can_move_time = game_time + 0.25
            mouse.move(stored_x, stored_y)
        mouse.release(mouse.MIDDLE)
