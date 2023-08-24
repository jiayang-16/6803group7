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

# fall speed of enemies and buffs
FALL_SPEED = 3
# spawn time of enemies
SPAWN_TIME = 2000
# screen size
WIDTH, HEIGHT = 480, 720
main_dir = os.path.abspath(__file__)
res_dir = os.path.join(os.path.dirname(os.path.dirname(main_dir)), "res")
assets = {}


# tool to load assets, avoid loading the same asset multiple times
def load_asset(name):
    if name in assets:
        return assets[name]
    else:
        assets[name] = pg.image.load(os.path.join(res_dir, name))
        return assets[name]
