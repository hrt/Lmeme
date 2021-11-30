import pygame
import win32gui
import win32api
import win32con

from math import floor
from time import sleep
from keyboard import register_hotkey
from world import world_to_screen
from target import is_alive


class Colors:
    trans = (255, 0, 128)
    red = (255, 0, 0)
    yellow = (255, 255, 100)
    blue = (0, 0, 255)
    green = (0, 255, 0)
    white = (255, 255, 255)
    black = (0, 0, 0)
    silver = (192, 192, 192)


class Settings:
    def __init__(self):
        self.menu = True
        self.orb_walker = False
        self.show_enemy_spell_cd = False

        register_hotkey("F1", self.set_menu)
        register_hotkey("F2", self.set_show_enemy_spell_cd)
        register_hotkey("F3", self.set_orb_walker)

    def set_menu(self):
        self.menu = False if self.menu else True

    def set_orb_walker(self):
        self.orb_walker = False if self.orb_walker else True

    def set_show_enemy_spell_cd(self):
        self.show_enemy_spell_cd = False if self.show_enemy_spell_cd else True


def game_menu(overlay, sets):
    menu_font = pygame.font.SysFont("Courier", 12)
    blank_line = menu_font.render("", False, Colors.trans)
    overlay_gui_text = [
        menu_font.render("[F1] Menu", False, Colors.yellow),
        blank_line,
        menu_font.render("[F2] Enemy Spell CD", False, Colors.green if sets.show_enemy_spell_cd else Colors.white),
        blank_line,
        menu_font.render("[F3] Orb Walker", False, Colors.green if sets.orb_walker else Colors.white),
    ]
    y = 200
    for line in overlay_gui_text:
        overlay.blit(line, (15, y))
        y += 16


def get_game_window(hwnd_name="League of Legends (TM) Client"):
    while True:
        try:
            hwnd = win32gui.FindWindow(None, hwnd_name)
            window_rect = win32gui.GetWindowRect(hwnd)
            x = window_rect[0] - 5
            y = window_rect[1]
            width = window_rect[2] - x
            height = window_rect[3] - y
            return x, y, width, height, hwnd
        except:
            pass
        sleep(0.5)


def create_overlay(game_window):
    pygame.event.set_blocked(pygame.MOUSEMOTION)
    pygame.mouse.set_visible(False)
    screen = pygame.display.set_mode((game_window[2], game_window[3]), pygame.NOFRAME | pygame.DOUBLEBUF)
    hwnd = pygame.display.get_wm_info()["window"]
    win32gui.SetWindowLong(
        hwnd, win32con.GWL_EXSTYLE, win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED
    )
    win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(*Colors.trans), 0, win32con.LWA_COLORKEY)
    return screen


def reset_overlay(game_window):
    win32gui.SetWindowPos(pygame.display.get_wm_info()["window"], -1, game_window[0], game_window[1], 0, 0, 0x0001)


def draw_enemy_spell_cd(overlay, active_champion, champions, view_proj_matrix, width, height, game_time):
    cd_font = pygame.font.SysFont("Comic Sans MS", 16)
    for champion in champions:
        if champion.network_id == active_champion.network_id:
            continue
        x, y = world_to_screen(view_proj_matrix, width, height, champion.x, champion.z, champion.y)
        if champion.visibility and is_alive(champion) and x is not None and y is not None:
            if 0 < x < width and 0 < y < width:
                index = 0
                spell_x = x - 150
                spell_y = y + 50
                for spell in champion.spells:
                    cd = get_cd(spell.cooldown_expire, game_time)
                    color = Colors.yellow if spell.level == 0 else Colors.green
                    if cd > 0:
                        color = Colors.red
                    name = {
                        0: "Q",
                        1: "W",
                        2: "E",
                        3: "R",
                        4: "D",
                        5: "F"
                    }

                    overlay.blit(cd_font.render("{}:{}".format(name.get(index), cd), False, color), (spell_x, spell_y))
                    index += 1
                    spell_x += 50


def get_cd(spell_time, game_time):
    cd = floor(spell_time - game_time)
    return cd if cd > 0 else 0
