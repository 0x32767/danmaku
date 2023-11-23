import os

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"

from pygame.locals import *
import pygame as pg

from effectmanager import EffectManager
from stagemanager import StageManager
from player import Player
from var import *

pg.init()
pg.display.init()

pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pg.display.set_caption("danmaku?")

game_over = False
running = True

bullets = pg.sprite.Group()
player = pg.sprite.GroupSingle(Player())
font = pg.font.Font("LePatinMagicien-XB7d.ttf", 20)
effects = EffectManager()
stg_man = StageManager()

stg_man.player = player
stg_man.font = font

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

        if event.type == KEYDOWN and game_over:
            if event.dict["key"] == K_z:
                game_over = False
                
                player.sprite.reset()
                bullets.empty()
                stg_man.reset()

        if event.type == EVENT_PLAYER_IFRAME:
            for _ in range(3):
                effects.add_particle(player.sprite.x, player.sprite.y, min_speed=0.01,  max_speed=0.011,  min_frames=20, max_frames=50)

        if event.type == EVENT_PLAYER_HIT:
            for _ in range(10):
                effects.add_particle(player.sprite.x, player.sprite.y)

        if event.type == EVENT_GAME_OVER:
            game_over = True

    window.fill((000, 000, 000))

    if game_over:
        text = font.render("Game Over!!!", False, (255, 255, 255))
        window.blit(text, (200, 200))
        pg.display.flip()

    if not game_over:
        stg_man.update(bullets)
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

    if not game_over:
        # collisions
        collisions = pg.sprite.spritecollide(
            player.sprite,
            bullets,
            False,
            pg.sprite.collide_circle,
        )
        player.sprite.register_collision(collisions)

    text = font.render(f"Lives: {player.sprite.lives}", False, (255, 255, 255))
    window.blit(text, (PF_END_X+25, PF_START_Y))

    pg.display.flip()

pg.quit()
