from __future__ import annotations


import pygame as pg


class MainMenu:
    def __init__(self) -> None:
        self.font: pg.font.Font = None
        self._selected = 0
        self._stage = None

    def render(self, surface: pg.display.Surface):
        if self._stage is not None:
            self._stage.draw(surface)
            return

        surface.fill((000, 000, 000))

        surface.blit(
            self.font.render("Start game", False, (255, 255, 255) if ),
            (20, 50)
        )
