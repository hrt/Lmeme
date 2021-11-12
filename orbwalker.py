import time
import mouse


class OrbWalker:
    def __init__(self, game_time):
        self.can_attack_time = game_time
        self.can_move_time = game_time

    @staticmethod
    def get_attack_time(champion, stats):
        attack_speed = min(2.5, champion.AtkSpeedMulti * stats['attackSpeed'])
        return 1. / attack_speed

    @staticmethod
    def get_windup_time(champion, stats):
        return OrbWalker.get_attack_time(champion, stats) * stats['windup']

    def walk(self, stats, champion, game_time, x, y):
        if x is not None and y is not None and self.can_attack_time < game_time:
            stored_x, stored_y = mouse.get_position()
            mouse.move(int(x), int(y))
            mouse.right_click()
            time.sleep(0.01)
            champion_stats = stats.get(champion.Name)
            self.can_attack_time = game_time + OrbWalker.get_attack_time(champion, champion_stats)
            self.can_move_time = game_time + OrbWalker.get_windup_time(champion, champion_stats)
            mouse.move(stored_x, stored_y)
        elif self.can_move_time < game_time:
            mouse.right_click()
            MOVE_CLICK_DELAY = 0.09
            self.can_move_time = game_time + MOVE_CLICK_DELAY
