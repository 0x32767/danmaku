import pygame as pg


class Enemy:
    def __init__(self):
        self.sprite = pg.image.load("./enemy.png")
        self.sprite = pg.transform.scale(self.sprite, (50, 50))

        self.active = False
        self.x = 0
        self.y = 0

    def set_pos(self, x, y):
        self.x = x
        self.y = y
    
    def set_active(self):
        self.active = True

    def set_inactive(self):
        self.active = False

    def render(self, surf):
        if self.active:
            surf.blit(self.sprite, (self.x-25, self.y-25))
