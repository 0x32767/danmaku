from __future__ import annotations

import pygame as pg
from var import *


class Heart(pg.sprite.Sprite):
    def __init__(self, x: int, y: int, speed: int) -> None:
        super().__init__()

        self.speed = speed / 100
        self.x = x
        self.y = y

        self.image = pg.Surface((10, 13))
        self.rect = pg.Rect(*pg.display.get_surface().get_rect().center, 0, 0).inflate(10, 13)

        pg.draw.rect(self.image, (255, 000, 255), ((0, 0), (10, 17)))

    def update(self) -> None:
        self.y += self.speed
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
