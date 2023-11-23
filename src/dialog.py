from typing import NamedTuple, Literal
import pygame as pg
from var import *


class Message(NamedTuple):
    emotion: Literal["happy", "targeted", "normal"]
    speaker: Literal["player", "enemy", "both"]
    message: str


class DialogBox:
    def __init__(self, text: str, font: pg.font.Font) -> None:
        # the image is unlikley to change so we just render it once, and 
        self._img = font.render(text, False, (255, 255, 255))
    
    def render(self):
        for _ in range(1_000):
            pg.display.get_surface().blit(self._img, TEXT_START)
            yield

class DialogList:
    def __init__(self, messages: list[Message], font: pg.font.Font) -> None:
        self._messages = messages
        self._font = font

    def update(self):
        if len(self._current_message) >= self._message_idx:
            return True # aka, no more text

        for message in self._messages:
            dialog = DialogBox(message.message, self._font)

            # sprite
            if message.speaker == "player":
                character_sprite = pg.image.load(message.speaker+"_"+message.emotion+"_light.png")
            
            else:
                character_sprite = pg.image.load(message.speaker+"_"+message.emotion+"_dark.png")

            # enemy
            if message.speaker == "enemy":
                enemy_sprite = pg.image.load(message.speaker+"_"+message.emotion+"_light.png")

            else:
                enemy_sprite = pg.image.load(message.speaker+"_"+message.emotion+"_dark.png")

            # display the text
            for _ in dialog.render():
                pg.display.get_surface().blit(character_sprite, CHARACTER_LEFT)
                pg.display.get_surface().blit(enemy_sprite, CHARACTER_RIGHT)
