from __future__ import annotations

from random import randint, uniform, choice
from math import radians, degrees, atan
from bullet import Bullet
from heart import Heart
import pygame as pg
from var import *


class StageManager:
    def __init__(self) -> None:
        self.bullets: list[Bullet] = []
        self.player = None
        self._stg = None

    def reset(self):
        self._stg = self.stage_gen()
        self._stg.send(None)

    def stage_gen(self):
        bullets: pg.sprite.Group = yield

        yield from self.wait(100)

        # 3 basic rings with a bit of randomness
        for _ in range(3):
            for angle in range(0, 360, 20):
                bullets.add(Bullet(
                    x=(PF_START_X+PF_END_X)//2,
                    y=(PF_START_Y+PF_END_Y)//2,
                    direction=radians(angle),
                    speed=3,
                    lr=(000, 255, 255),
                ))

            yield from self.wait(10)

            for _ in range(25):
                bullets.add(Bullet(
                    x=(PF_START_X+PF_END_X)//2,
                    y=(PF_START_Y+PF_END_Y)//2,
                    direction=radians(randint(0, 360)),
                    speed=uniform(3, 5),
                    lr=(255, 000, 255)
                ))

            yield from self.wait(50)
        yield from self.wait(50)

        # several offset circles
        for offset in range(5):
            for angle in range(0, 360, 20):
                bullets.add(Bullet(
                    x=(PF_START_X+PF_END_X)//2,
                    y=(PF_START_Y+PF_END_Y)//2,
                    direction=radians(angle+(offset*10)),
                    speed=1+offset,
                    lr=(255, 255, 255),
                ))
            yield from self.wait(50)

        yield from self.wait(50)

        # some basic streaming
        for xx in range(PF_START_X, PF_END_Y//2):
            player_angle = -degrees(atan(radians((self.player.sprite.x - xx) / (PF_START_X - self.player.sprite.y))))
            bullets.add(Bullet(xx, PF_START_Y, player_angle, 5, lr=(000, 255, 255)))
            yield from self.wait(5)

            bullets.add(Bullet(PF_MID_X + randint(-10, 10), PF_MID_Y+randint(-10, 10), randint(0, 360), uniform(1, 5)))
            bullets.add(Bullet(PF_MID_X + randint(-10, 10), PF_MID_Y+randint(-10, 10), randint(0, 360), uniform(1, 5)))

        yield from self.wait(500)

        ####################################################################

        # 3 random circles of death
        for _ in range(3):
            for _ in range(100):
                bullets.add(Bullet(
                    x=(PF_START_X+PF_END_X)//2,
                    y=(PF_START_Y+PF_END_Y)//2,
                    direction=radians(randint(0, 360)),
                    speed=uniform(5, 7)
                ))

            yield from self.wait(50)

        # large round circle
        for angle in range(0, 360, 5):
            bullets.add(Bullet(
                    x=(PF_START_X+PF_END_X)//2,
                    y=(PF_START_Y+PF_END_Y)//2,
                    direction=radians(angle),
                    speed=2
            ))
        yield from self.wait(50)

        # several smaller offset circles
        for speed_inc in range(1, 10):
            for angle in range(0, 360, 20):
                bullets.add(Bullet(
                    x=(PF_START_X+PF_END_X)//2,
                    y=(PF_START_Y+PF_END_Y)//2,
                    direction=radians(angle + (speed_inc+1) * 1.5),
                    speed=speed_inc+2
            ))
            yield from self.wait(10)

        # random circles
        orientation = ((PF_END_X, PF_START_Y), (PF_END_X, PF_END_Y), (PF_START_X, PF_START_Y), (PF_START_X, PF_END_Y))
        for _ in range(10):
            pos = choice(orientation)

            for angle in range(0, 360, 10):
                bullets.add(Bullet(
                        x=pos[0],
                            y=pos[1],
                            direction=radians(angle+randint(0, 5)),
                            speed=0.5
                        ))

            yield from self.wait(randint(10, 80))

        # tail
        yield from self.wait(500)
        bullet_x = (PF_END_X+PF_START_X)/2
        bullet_y = (PF_END_Y+PF_START_Y)/2
        for _ in range(100):
            bullet_x += randint(-20, 20)
            bullet_y += randint(-20, 20)

            for angle in range(0, 360, 20):
                bullets.add(Bullet(
                    x=bullet_x+randint(-5, 5),
                    y=bullet_y+randint(-5, 5),
                    direction=radians(angle+randint(-5, 5)),
                    speed=1.5
                ))

            yield from self.wait(10)

        # drop a life
        bullets.add(Heart((PF_START_X+PF_END_X)//2, PF_START_Y+10, 5))

        while True:
            yield

    def update(self, bullets):
        if self._stg is None:
            self.reset()

        return self._stg.send(bullets)

    def wait(self, frames):
        for _ in range(frames):
            yield
