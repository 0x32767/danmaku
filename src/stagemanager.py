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
        self.font: pg.font.Font = None
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
                bullets.add(
                    Bullet(
                        x=(PF_START_X + PF_END_X) // 2,
                        y=(PF_START_Y + PF_END_Y) // 2,
                        direction=radians(angle),
                        speed=3,
                        lr=(000, 255, 255),
                    )
                )

            yield from self.wait(10)

            for _ in range(25):
                bullets.add(
                    Bullet(
                        x=(PF_START_X + PF_END_X) // 2,
                        y=(PF_START_Y + PF_END_Y) // 2,
                        direction=radians(randint(0, 360)),
                        speed=uniform(3, 5),
                        lr=(255, 000, 255),
                    )
                )

            yield from self.wait(50)
        yield from self.wait(50)

        # several offset circles
        for offset in range(5):
            for angle in range(0, 360, 20):
                bullets.add(
                    Bullet(
                        x=(PF_START_X + PF_END_X) // 2,
                        y=(PF_START_Y + PF_END_Y) // 2,
                        direction=radians(angle + (offset * 10)),
                        speed=1 + offset,
                        lr=(255, 255, 255),
                    )
                )
            yield from self.wait(50)

        yield from self.wait(50)

        # some basic streaming
        for xx in range(PF_START_X, PF_END_Y // 2):
            player_angle = -degrees(
                atan(
                    radians(
                        (self.player.sprite.x - xx)
                        / (PF_START_X - self.player.sprite.y)
                    )
                )
            )
            bullets.add(Bullet(xx, PF_START_Y, player_angle, 5, lr=(000, 255, 255)))
            yield from self.wait(5)

            bullets.add(
                Bullet(
                    PF_MID_X + randint(-10, 10),
                    PF_MID_Y + randint(-10, 10),
                    randint(0, 360),
                    uniform(1, 5),
                )
            )
            bullets.add(
                Bullet(
                    PF_MID_X + randint(-10, 10),
                    PF_MID_Y + randint(-10, 10),
                    randint(0, 360),
                    uniform(1, 5),
                )
            )

        yield from self.wait(50)

        # a checkerboard of bullets
        for _ in range(10):
            # X
            for xx in range(PF_START_X, PF_END_X, (PF_START_X + PF_END_X) // 10):
                bullets.add(Bullet(xx, PF_START_Y + 10, radians(0), 1))

            # Y
            for yy in range(PF_START_Y, PF_END_Y, (PF_START_Y + PF_END_Y) // 10):
                bullets.add(Bullet(PF_START_X + 10, yy, radians(90), 1))

            yield from self.wait(75)

        # a row of streaming
        for xx in range(PF_START_X, PF_END_X, (PF_START_X + PF_END_X) // 10):
            direction = -degrees(
                atan(
                    radians(
                        (self.player.sprite.x - xx)
                        / (PF_START_X - self.player.sprite.y)
                    )
                )
            )
            bullets.add(Bullet(xx, PF_START_Y, direction, 2, lr=(255, 255, 000)))

        for _ in range(50):
            bullets.add(
                Bullet(
                    randint(PF_START_X, PF_END_X),
                    randint(PF_START_Y, PF_END_Y),
                    degrees(randint(0, 360)),
                    uniform(0.1, 1),
                    lr=(000, 000, 255),
                )
            )

        # continue checkerboard of bullets
        for _ in range(5):
            # X
            for xx in range(PF_START_X, PF_END_X, (PF_START_X + PF_END_X) // 10):
                bullets.add(Bullet(xx, PF_START_Y + 10, radians(0), 1))

            # Y
            for yy in range(PF_START_Y, PF_END_Y, (PF_START_Y + PF_END_Y) // 10):
                bullets.add(Bullet(PF_START_X + 10, yy, radians(90), 1))

            yield from self.wait(75)

        yield from self.wait(225)
        ####################################################################

        # 3 random circles of death
        for _ in range(3):
            for _ in range(100):
                bullets.add(
                    Bullet(
                        x=(PF_START_X + PF_END_X) // 2,
                        y=(PF_START_Y + PF_END_Y) // 2,
                        direction=radians(randint(0, 360)),
                        speed=uniform(4, 6),
                        lr=choice(((255, 000, 000), (000, 255, 000), (000, 000, 255))),
                    )
                )

            yield from self.wait(125)

        # large round circle
        for angle in range(0, 360, 10):
            bullets.add(
                Bullet(
                    x=(PF_START_X + PF_END_X) // 2,
                    y=(PF_START_Y + PF_END_Y) // 2,
                    direction=radians(angle),
                    speed=2,
                )
            )
        yield from self.wait(50)

        # several smaller offset circles
        for speed_inc in range(1, 10):
            for angle in range(0, 360, 20):
                bullets.add(
                    Bullet(
                        x=(PF_START_X + PF_END_X) // 2,
                        y=(PF_START_Y + PF_END_Y) // 2,
                        direction=radians(angle + (speed_inc + 1) * 1.5),
                        speed=speed_inc * 1.2,
                        lr=(255, 000, 000),
                    )
                )
            yield from self.wait(15)

        # random circles
        orientation = (
            (PF_END_X, PF_START_Y),
            (PF_END_X, PF_END_Y),
            (PF_START_X, PF_START_Y),
            (PF_START_X, PF_END_Y),
        )
        for speed_up in range(10):
            pos = choice(orientation)

            for angle in range(0, 360, 10):
                bullets.add(
                    Bullet(
                        x=pos[0],
                        y=pos[1],
                        direction=radians(angle + randint(0, 5)),
                        speed=(speed_up // 5) * uniform(0, 2),
                        lr=(255, 255, 255),
                        ir=(120, 120, 120),
                    )
                )

            yield from self.wait(randint(10, 80))

        # tail
        yield from self.wait(500)
        bullet_x = (PF_END_X + PF_START_X) / 2
        bullet_y = (PF_END_Y + PF_START_Y) / 2
        for _ in range(100):
            bullet_x += randint(-20, 20)
            bullet_y += randint(-20, 20)

            for angle in range(0, 360, 25):
                bullets.add(
                    Bullet(
                        x=bullet_x + randint(-5, 5),
                        y=bullet_y + randint(-5, 5),
                        direction=radians(angle + randint(-5, 5)),
                        speed=1.5,
                    )
                )

            yield from self.wait(15)

        yield from self.wait(35)

        # death rings
        for color in ((255, 000, 000), (000, 255, 000), (255, 255, 000), (000, 000, 255), (255, 000, 255), (000, 255, 255), (255, 255, 255)):
            for angle in range(0, 360, 10):
                for _ in range(randint(3, 5)):
                    bullets.add(Bullet(PF_MID_X, PF_START_Y*1.2, uniform(angle-10, angle+10), uniform(5, 5.5), lr=color))
            
            yield from self.wait(25)

        # aimed massive random blodge
        for _ in range(128):
            direction = -degrees(
                atan(
                    radians(
                        (self.player.sprite.x - xx)
                        / (PF_START_X - self.player.sprite.y)
                    )
                )
            )
            bullets.add(Bullet(xx, PF_START_Y, direction+uniform(-1, 1),uniform(2, 4), lr=(255, 255, 000)))

        # drop a life
        bullets.add(Heart((PF_START_X + PF_END_X) // 2, PF_START_Y + 10, 25))

        # troll the player
        for _ in range(100):
            pg.display.get_surface().blit(self.font.render("You Win!", False, (255, 000, 000)))
            yield

        for _ in range(100):
            pg.display.get_surface().blit(self.font.render("LOL! Problem >;)", False, (255, 000, 000)))
            yield

        while True:
            print("well done")
            yield

    def update(self, bullets):
        if self._stg is None:
            self.reset()

        return self._stg.send(bullets)

    def wait(self, frames):
        for _ in range(frames):
            yield
