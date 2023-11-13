import os

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"

from pygame.locals import *
import pygame as pg
import random

from effectmanager import EffectManager
from player import Player
from bullet import Bullet
from var import *

pg.init()
pg.display.init()

pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pg.display.set_caption("danmaku?")

game_over = False
running = True
bullets = pg.sprite.Group(
    [
        Bullet((PF_START_X + PF_END_X) // 2, (PF_START_Y + PF_END_Y) // 2, i, 1)
        for i in range(360)
    ]
)
player = pg.sprite.GroupSingle(Player())
effects = EffectManager()

font = pg.font.Font("LePatinMagicien-XB7d.ttf")

window = pg.display.get_surface()
clock = pg.time.Clock()

while running:
    delta = clock.tick(60)

    for event in pg.event.get():
        if event.type == QUIT:
            running = False

        if event.type == KEYUP:
            player.sprite.send_keyup(event.dict["key"])

        if event.type == KEYDOWN:
            player.sprite.send_keydown(event.dict["key"])

        if event.type == EVENT_PLAYER_HIT:
            for _ in range(10):
                effects.add_particle(player.sprite.x, player.sprite.y)

        if event.type == EVENT_GAME_OVER:
            for _ in range(10):
                effects.add_particle(player.sprite.x, player.sprite.y)

            game_over = True

    window.fill((000, 000, 000))

    if game_over:
        continue

    bullets.update()
    player.update()
    effects.update()

    player.draw(window)
    bullets.draw(window)
    effects.draw(window)

    pg.draw.rect(
        window,
        (255, 255, 255),
        (PF_START, PF_END),
        5,
    )

    # collisions
    collidions = pg.sprite.spritecollide(
        player.sprite,
        bullets,
        False,
        pg.sprite.collide_circle,
    )

    player.sprite.register_collision(collidions)

    pg.display.flip()

pg.quit()
