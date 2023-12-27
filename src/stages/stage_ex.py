from __future__ import annotations

from random import randint, uniform, choice
from math import radians, degrees, atan, sin, cos
from bullet import Bullet
from heart import Heart
import pygame as pg
from var import *


class StageManagerEX:
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

        pg.event.post(pg.event.Event(EVENT_SHOW_ENEMY))
        pg.event.post(pg.event.Event(EVENT_ENEMY_POSITION, {"x": (PF_START_X + PF_END_X) // 2, "y": (PF_START_Y + PF_END_Y) // 2}))

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

        bullets.add(Bullet(PF_MID_X, PF_MID_Y, 0, 0, radius=10))
        # some basic streaming
        for xx in range(PF_START_X, PF_END_Y // 2):
            pg.event.post(pg.event.Event(EVENT_ENEMY_POSITION, {"x": xx, "y": PF_START_Y + 25}))

            player_angle = -degrees(
                atan(
                    radians(
                        (self.player.sprite.x - xx)
                        / (PF_START_X - self.player.sprite.y)
                    )
                )
            )
            bullets.add(Bullet(xx, PF_START_Y, player_angle, 5, lr=(000, 255, 255)))
            yield from self.wait(6)

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
        bullets.empty()

        bullets.add(Heart((PF_START_X + PF_END_X) // 2, PF_START_Y + 10, 25))

        # spinning ring
        offset = 100
        for _ in range(3):
            pg.event.post(pg.event.Event(EVENT_ENEMY_POSITION, {"x": PF_MID_X, "y": PF_MID_Y}))

            for _ in range(100):
                # create a static circle
                for angle in range(0, 360, 10):
                    bullets.add(
                        Bullet(
                            PF_MID_X + (2 * degrees(cos(radians(angle + offset)))),
                            PF_MID_Y + (2 * degrees(sin(radians(angle + offset)))),
                            angle,
                            0,
                        )
                    )

                offset -= uniform(1, 2)

                if offset < 2:
                    offset = 100

                else:
                    if offset > 25:
                        yield from self.wait(1)

                    elif offset > 10:
                        yield from self.wait(2)

                    else:
                        positions = []
                        # shoot bullets out
                        for bullet in bullets.sprites():
                            positions.append((bullet.x, bullet.y, bullet.direction))

                        yield from self.wait(20)

                        for x, y, heading in positions:
                            pg.event.post(pg.event.Event(EVENT_ENEMY_POSITION, {"x": x, "y": y}))

                            bullets.add(
                                Bullet(
                                    x,
                                    y,
                                    heading,
                                    speed=0,
                                    ir=(255, 000, 000),
                                    lr=(255, 255, 255),
                                ),
                                Bullet(
                                    x,
                                    y,
                                    heading + uniform(-10, 10),
                                    speed=0,
                                    ir=(255, 000, 000),
                                    lr=(255, 255, 255),
                                ),
                            )

                            yield from self.wait(2)

                        for bullet in bullets.sprites():
                            bullet.speed = 0.01 + uniform(0.01, 0.05)
                            bullet.direction = bullet.direction + uniform(-10, 10)

                        yield from self.wait(50)

                        bullets.add(*[Bullet(PF_MID_X, PF_MID_Y, radians(randint(0, 360)), speed=2.5, lr=(000, 000, 255)) for _ in range(100)])

                        yield from self.wait(150)

                        offset = 100

                bullets.empty()

        for xx in range(PF_START_X, PF_END_X, (PF_START_X + PF_END_X) // 5):
            pg.event.post(pg.event.Event(EVENT_ENEMY_POSITION, {"x": xx, "y": PF_START_Y + 10}))
            pg.event.post(pg.event.Event(EVENT_SHOW_ENEMY))
            yield from self.wait(15)

        # a checkerboard of bullets
        for _ in range(10):
            # X
            for xx in range(PF_START_X, PF_END_X, (PF_START_X + PF_END_X) // 5):
                bullets.add(Bullet(xx + 15, PF_START_Y + 10, radians(0), 1))

            # Y
            for yy in range(PF_START_Y, PF_END_Y, (PF_START_Y + PF_END_Y) // 5):
                bullets.add(Bullet(PF_START_X + 10, yy + 15, radians(90), 1))

            yield from self.wait(75)

        # a row of streaming
        for idx, xx in enumerate(range(PF_START_X, PF_END_X, 10)):
            pg.event.post(pg.event.Event(EVENT_ENEMY_POSITION, {"x": xx, "y": PF_START_Y + 25}))

            direction = -degrees(
                atan(
                    radians(
                        (self.player.sprite.x - xx)
                        / (PF_START_X - self.player.sprite.y)
                    )
                )
            )
            bullets.add(Bullet(xx, PF_START_Y, direction, 2, lr=(255, 255, 000)))

            yield from self.wait(5)

            # continue the checkerboard of bullets
            if (idx % 15) == 0:
                # X
                for xx in range(PF_START_X, PF_END_X, (PF_START_X + PF_END_X) // 5):
                    bullets.add(Bullet(xx + 15, PF_START_Y + 10, radians(0), 1))

                # Y
                for yy in range(PF_START_Y, PF_END_Y, (PF_START_Y + PF_END_Y) // 5):
                    bullets.add(Bullet(PF_START_X + 10, yy + 15, radians(90), 1))

        # random bulets
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
            for xx in range(PF_START_X, PF_END_X, (PF_START_X + PF_END_X) // 5):
                bullets.add(Bullet(xx + 15, PF_START_Y + 10, radians(0), 1))

            # Y
            for yy in range(PF_START_Y, PF_END_Y, (PF_START_Y + PF_END_Y) // 5):
                bullets.add(Bullet(PF_START_X + 10, yy + 15, radians(90), 1))

            yield from self.wait(75)

        yield from self.wait(225)
        ####################################################################

        # 3 random circles of death
        pg.event.post(pg.event.Event(EVENT_ENEMY_POSITION, {"x": PF_MID_X, "y": PF_MID_Y}))

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

            yield from self.wait(225)

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
            (PF_END_X - 10, PF_START_Y + 10),
            (PF_END_X - 10, PF_END_Y - 10),
            (PF_START_X + 10, PF_START_Y + 10),
            (PF_START_X + 10, PF_END_Y - 10),
        )
        for speed_up in range(10):
            
            pos = choice(orientation)
            pg.event.post(pg.event.Event(EVENT_ENEMY_POSITION, {"x": pos[0], "y": pos[1]}))

            yield from self.wait(randint(10, 60))

            for angle in range(0, 360, 5):
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

            yield from self.wait(randint(10, 20))

        bullets.add(Heart((PF_START_X + PF_END_X) // 2, PF_START_Y + 10, 25))

        # tail
        yield from self.wait(500)
        bullet_x = (PF_END_X + PF_START_X) / 2
        bullet_y = (PF_END_Y + PF_START_Y) / 2
        for i in range(100):
            bullet_x += randint(-20, 20)
            bullet_y += randint(-20, 20)

            pg.event.post(pg.event.Event(EVENT_ENEMY_POSITION, {"x": bullet_x, "y": bullet_y}))

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

            if (i % 10) == 0:
                for angle in range(0, 360, 20):
                    bullets.add(
                        Bullet(
                            bullet_x,
                            bullet_y,
                            direction=radians(angle),
                            speed=2,
                            ir=(000, 000, 000),
                            lr=(255, 255, 255),
                        )
                    )

        yield from self.wait(35)

        # death rings
        for color in (
            (255, 000, 000),
            (000, 255, 000),
            (255, 255, 000),
            (000, 000, 255),
            (255, 000, 255),
            (000, 255, 255),
            (255, 255, 255),
        ):
            for angle in range(0, 360, 10):
                for _ in range(randint(3, 5)):
                    bullets.add(
                        Bullet(
                            PF_MID_X,
                            PF_START_Y * 1.2,
                            uniform(angle - 10, angle + 10),
                            uniform(5, 5.5),
                            lr=color,
                        )
                    )

            yield from self.wait(75)

        yield from self.wait(150)

        # drop a life
        bullets.add(Heart((PF_START_X + PF_END_X) // 2, PF_START_Y + 10, 25))

        for _ in range(20):
            plant_x = self.player.sprite.x
            plant_y = self.player.sprite.y
            pg.event.post(pg.event.Event(EVENT_ENEMY_POSITION, {"x": plant_x, "y": plant_y}))
            yield from self.wait(50)
            pg.event.post(pg.event.Event(EVENT_MAKE_PARTICLE, {"x": plant_x, "y": plant_y}))
            yield from self.wait(20)
            bullets.add(Bullet(
                x=plant_x,
                y=plant_y,
                speed=0,
                direction=0,
                radius=25,
                ir=(255, 000, 000),
                cr=(000, 000, 000),
                lr=(255, 000, 000)
            ))

            for _ in range(20):
                bullets.add(Bullet(
                    x=plant_x,
                    y=plant_y,
                    direction=radians(randint(0, 360)),
                    speed=uniform(1, 2)
                ))

            yield from self.wait(55)

        yield from self.wait(45)

        pg.event.post(pg.event.Event(EVENT_ENEMY_POSITION, {"x": (PF_START_X + PF_END_X) // 2, "y": (PF_START_Y + PF_END_Y) // 2}))
        for offset in range(360):
            for angle in range(360):
                if (angle % 72):
                    continue

                bullets.add(Bullet(PF_MID_X, PF_MID_Y, direction=radians(angle+offset), speed=10))

            yield from self.wait(5)

        while True:
            yield

    def update(self, bullets):
        if self._stg is None:
            self.reset()

        return self._stg.send(bullets)

    def wait(self, frames):
        for _ in range(frames):
            yield
