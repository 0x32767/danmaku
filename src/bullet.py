from math import sin, cos, degrees
import pygame as pg

from var import *


class Bullet(pg.sprite.Sprite):
    def __init__(self,
                 x: int, y: int, direction: int, speed: int,
                 ir: tuple[int, int, int] = (255, 255, 255),
                 cr: tuple[int, int, int] = (000, 000, 000),
                 lr: tuple[int, int, int]=(000, 255, 000)) -> None:
        super().__init__()

        self.direction = direction
        self.speed = speed / 100
        self.radius = 4
        self.x = x
        self.y = y

        self.image = pg.Surface((80, 80), pg.SRCALPHA)
        self.rect = pg.Rect(*pg.display.get_surface().get_rect().center, 0, 0).inflate(
            80, 80
        )

        pg.draw.circle(self.image, lr, (40, 40), self.radius + 2)
        pg.draw.circle(self.image, cr, (40, 40), self.radius + 1)
        pg.draw.circle(self.image, ir, (40, 40), self.radius)

    def update(self) -> None:
        self.x += degrees(sin(self.direction)) * self.speed
        self.y += degrees(cos(self.direction)) * self.speed

        self.rect.center = (self.x, self.y)

        if any(
            (
                self.x < PF_START_X,
                self.y < PF_START_Y,
                self.x > PF_END_X,
                self.y > PF_END_Y,
            )
        ):
            self.kill()
