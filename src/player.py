from pygame.locals import *
import pygame as pg

from heart import Heart
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

        self.x = (PF_START_X + PF_END_X) // 2
        self.y = PF_END_Y - 20

        self.radius = 4
        self.image = pg.Surface((80, 80), pg.SRCALPHA)
        pg.draw.circle(self.image, (255, 0, 0), (40, 40), self.radius)
        self.rect = pg.Rect(*pg.display.get_surface().get_rect().center, 0, 0).inflate(
            80, 80
        )

        self.lives = 10

    def send_keyup(self, key):
        if key == K_UP:
            self.keys["up"] = False

        if key == K_DOWN:
            self.keys["down"] = False

        if key == K_LEFT:
            self.keys["left"] = False

        if key == K_RIGHT:
            self.keys["right"] = False

        if key == K_LSHIFT:
            self.keys["focus"] = False

        if key == K_z:
            self.keys["shoot"] = False

    def send_keydown(self, key):
        if key == K_UP:
            self.keys["up"] = True

        if key == K_DOWN:
            self.keys["down"] = True

        if key == K_LEFT:
            self.keys["left"] = True

        if key == K_RIGHT:
            self.keys["right"] = True

        if key == K_LSHIFT:
            self.keys["focus"] = True

        if key == K_z:
            self.keys["shoot"] = True

    def update(self) -> None:
        if self.i_frames > 0:
            pg.event.post(pg.event.Event(EVENT_PLAYER_IFRAME))
            self.i_frames -= 1

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

        if self.i_frames > 0:
            return

        for collision in collisions:
            if isinstance(collision, Heart):
                self.lives += 1
                collision.kill()

            else:
                self.die()

        if self.i_frames > 0:
            return True

    def die(self):
        if isinstance(self.lives, str):
            self.lives = 10

        self.x = (PF_START_X + PF_END_X) // 2
        self.y = PF_END_Y - 20

        self.lives -= 1

        if self.lives < 0:
            self.lives = "You ran out!"

            pg.event.post(pg.event.Event(EVENT_GAME_OVER))
            return

        pg.event.post(pg.event.Event(EVENT_PLAYER_HIT))

        self.i_frames = 100

    def reset(self):
        self.lives = 0

        self.i_frames = 0

        self.x = (PF_START_X + PF_END_X) // 2
        self.y = PF_END_Y - 20

        self.lives = 100
