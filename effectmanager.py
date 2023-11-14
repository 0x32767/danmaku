from random import uniform, randrange
from math import degrees, sin, cos
from dataclasses import dataclass
import pygame as pg


@dataclass(unsafe_hash=True)
class Effect:
    x: float
    y: float
    speed: float
    heading: float
    frames: int


class EffectManager:
    def __init__(self) -> None:
        self.effects: list[Effect] = []

    def update(self):
        remove_effects = set()

        for effect in self.effects:
            effect.speed *= 0.9
            effect.frames -= 1

            if effect.frames <= 0:
                remove_effects.add(effect)

            effect.x += degrees(sin(effect.heading)) * effect.speed
            effect.y += degrees(cos(effect.heading)) * effect.speed

        for effect in remove_effects:
            self.effects.remove(effect)

    def draw(self, surf):
        for effect in self.effects:
            pg.draw.rect(
                surf,
                (255, 255, 255),
                ((effect.x, effect.y), (effect.frames / 10, effect.frames / 10)),
            )
            pg.draw.rect(
                surf,
                (255, 000, 000),
                (
                    (effect.x - 1, effect.y - 1),
                    ((effect.frames / 10) + 1, (effect.frames / 10) + 1),
                ),
                width=1,
            )

    def clear(self):
        self.effects.clear()

    def add_particle(self, x: int, y: int, min_speed: float=0.1,  max_speed: float=0.11, min_frames: int=100,  max_frames: int=200):
        self.effects.append(
            Effect(x, y, uniform(min_speed, max_speed), uniform(0, 360), randrange(min_frames, max_frames, 10))
        )
