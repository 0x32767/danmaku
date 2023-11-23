import pygame as pg

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480

PF_START_X = 10
PF_START_Y = 10
PF_START = (PF_START_X, PF_START_Y)

PF_END_X = 400
PF_END_Y = 450
PF_END = (PF_END_X, PF_END_Y)

PF_MID_X = (PF_START_X + PF_END_X)//2
PF_MID_Y = (PF_START_Y + PF_END_Y)//2


EVENT_PLAYER_HIT = pg.USEREVENT + 1
EVENT_GAME_OVER = pg.USEREVENT + 2
EVENT_PLAYER_IFRAME = pg.USEREVENT + 3

TEXT_START = (PF_END_Y-75, PF_START_X+10)

CHARACTER_LEFT = ()
CHARACTER_RIGHT = ()
