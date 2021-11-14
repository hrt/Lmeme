import time
import mouse
from world import find_game_time


class OrbWalker:
    def __init__(self, mem):
        self.mem = mem
        game_time = find_game_time(self.mem)
        self.can_attack_time = game_time
        self.can_move_time = game_time

    @staticmethod
    def get_attack_time(champion, base_attack_speed):
        attack_speed = min(2.5, champion.attack_speed_multiplier * base_attack_speed)
        return 1. / attack_speed

    @staticmethod
    def get_windup_time(champion, base_attack_speed, windup):
        return OrbWalker.get_attack_time(champion, base_attack_speed) * windup

    def walk(self, stats, champion, x, y):
        mouse.press(mouse.MIDDLE)
        game_time = find_game_time(self.mem)
        if x is not None and y is not None and self.can_attack_time < game_time:
            stored_x, stored_y = mouse.get_position()
            mouse.move(int(x), int(y))
            mouse.right_click()
            time.sleep(0.01)
            attack_speed = stats.get_attack_speed(champion.name)
            windup = stats.get_windup(champion.name)
            game_time = find_game_time(self.mem)
            self.can_attack_time = game_time + OrbWalker.get_attack_time(champion, attack_speed)
            self.can_move_time = game_time + OrbWalker.get_windup_time(champion, attack_speed, windup)
            mouse.move(stored_x, stored_y)
        elif self.can_move_time < game_time:
            mouse.right_click()
            MOVE_CLICK_DELAY = 0.09
            self.can_move_time = game_time + MOVE_CLICK_DELAY
        mouse.release(mouse.MIDDLE)
