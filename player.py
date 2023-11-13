from pygame.locals import *
import pygame as pg

from var import *


class Player(pg.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()
        self.keys = {
            "up": False,
            "down": False,
            "left": False,
            "right": False,
            "focus": False,
            "shoot": False,
        }
        self.i_frames = 0
        self.last_hit = 0

        self.x = (PF_START_X + PF_END_X) // 2
        self.y = PF_END_Y - 20

        self.radius = 5
        self.image = pg.Surface((80, 80), pg.SRCALPHA)
        pg.draw.circle(self.image, (255, 0, 0), (40, 40), self.radius)
        self.rect = pg.Rect(*pg.display.get_surface().get_rect().center, 0, 0).inflate(
            80, 80
        )

        self.lives = 2

    def send_keyup(self, key):
        if key == K_UP:
            self.keys["up"] = False

        elif key == K_DOWN:
            self.keys["down"] = False

        elif key == K_LEFT:
            self.keys["left"] = False

        elif key == K_RIGHT:
            self.keys["right"] = False

        elif key == K_LSHIFT:
            self.keys["focus"] = False

        elif key == K_z:
            self.keys["shoot"] = False

    def send_keydown(self, key):
        if key == K_UP:
            self.keys["up"] = True

        elif key == K_DOWN:
            self.keys["down"] = True

        elif key == K_LEFT:
            self.keys["left"] = True

        elif key == K_RIGHT:
            self.keys["right"] = True

        elif key == K_LSHIFT:
            self.keys["focus"] = True

        elif key == K_z:
            self.keys["shoot"] = True

    def update(self) -> None:
        # player movement
        move_speed = 5

        if self.keys["focus"]:
            move_speed //= 2.5

        if self.keys["left"]:
            self.x -= move_speed

            if self.x < PF_START_X + self.radius * 2:
                self.x = PF_START_X + self.radius * 2

        if self.keys["right"]:
            self.x += move_speed

            if self.x > PF_END_X:
                self.x = PF_END_X

        if self.keys["up"]:
            self.y -= move_speed

            if self.y < PF_START_Y + self.radius * 2:
                self.y = PF_START_Y + self.radius * 2

        if self.keys["down"]:
            self.y += move_speed

            if self.y > PF_END_Y:
                self.y = PF_END_Y

        self.rect.center = (self.x, self.y)

    def register_collision(self, collisions):
        if not collisions:
            return

        self.die()
        return True

    def die(self):
        self.x = (PF_START_X + PF_END_X) // 2
        self.y = PF_END_Y - 20

        self.lives -= 1

        if self.lives < 0:
            pg.event.post(pg.event.Event(EVENT_GAME_OVER))
            return

        pg.event.post(pg.event.Event(EVENT_PLAYER_HIT))
