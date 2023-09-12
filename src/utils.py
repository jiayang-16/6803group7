import math

import pygame as pg
import os

# fire event, trigger when player shoot
FIRE_EVENT = pg.USEREVENT + 1
# spawn event, trigger when enemy spawn
SPAWN_EVENT = pg.USEREVENT + 2
# pause event, trigger when game paused
PAUSE_EVENT = pg.USEREVENT + 3
# resume event, trigger when game resumed
RESUME_EVENT = pg.USEREVENT + 4
# restart event, trigger when game restart
RESTART_EVENT = pg.USEREVENT + 5
# boss event, trigger when boss appear
BOSS_EVENT = pg.USEREVENT + 6

END_EVENT = pg.USEREVENT + 7

START_EVENT = pg.USEREVENT + 8

# game state
IDLE = 0
PAUSE = 1
RUNNING = 2
QUIT = 3
END = 4
START = 5
# fall speed of enemies and buffs
FALL_SPEED = 5
# spawn time of enemies
SPAWN_TIME = 1000
# screen size
WIDTH, HEIGHT = 480, 720
# boss respawn time
BOSS_TIME = 50000

# bullet type
BLT_AMMO = 0
BLT_BLADE = 1

main_dir = os.path.abspath(__file__)
res_dir = os.path.join(os.path.dirname(os.path.dirname(main_dir)), "res")
assets = {}
masks = {}
music = {}


# tool to load assets, avoid loading the same asset multiple times
def load_asset(name):
    if name in assets:
        return assets[name]
    else:
        assets[name] = pg.image.load(os.path.join(res_dir, name)).convert_alpha()
        return assets[name]

def load_music(name):
    if name in music:
        return music[name]
    else:
        music[name] = pg.mixer.Sound(os.path.join(res_dir, name))
        music[name].set_volume(0.4)
        return music[name]


def format_number(n):
    suffixes = ['k', 'm', 'b', 't']  # 后缀，可根据需要扩展
    if isinstance(n, float):
        n = math.ceil(n)
    if n < 1000:
        return str(n)
    for i, suffix in enumerate(suffixes):
        magnitude = 1000 ** (i + 1)
        if n < magnitude * 1000:
            return '{:.1f}{}'.format(n / magnitude, suffix)
    return str(n)
