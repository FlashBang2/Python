import pygame

from enum import Enum
from typing import Callable, Tuple

class State(Enum):
    NONE = 1
    HOVER = 2
    DISABLED = 3

class Button:
    def __init__(self, position: Tuple[int, int], imageHover: pygame.Surface, imageUnhover: pygame.Surface, fontColor: Tuple[int, int, int], fontSize: int, caption: str, padding: Tuple[int, int], function: Callable, visibility: bool, isCheckBox: bool):
        self.imageHover = imageHover
        self.imageUnhover = imageUnhover
        self.image = self.imageUnhover
        self.rect = self.image.get_rect()
        self.rect.topleft = position
        self.position = position
        self.padding = padding
        self.font = pygame.font.SysFont("Arial", fontSize)
        self.text = caption
        self.fontSize = self.font.size(self.text)
        self.caption = self.font.render(self.text, True, fontColor)
        self.state = State.NONE
        self.function = function
        self.visible = visibility
        self.checked = False
        self.isCheckBox = isCheckBox

    def render(self, window: pygame.Surface):
        if not self.state == State.DISABLED:
            window.blit(self.image, (self.rect.x, self.rect.y))
        if self.isCheckBox:
             window.blit(self.caption, (self.rect.x + self.padding[0], self.rect.y + self.padding[1]))
        else:   
            window.blit(self.caption, (self.rect.center[0] - self.fontSize[0] / 2 + self.padding[0], self.rect.center[1] - self.fontSize[1] / 2 + self.padding[1]))

    def onleave(self):
        if self.state is State.DISABLED:
            return
        self.state = State.NONE
        self.image = self.imageUnhover
    
    def onhover(self):
        if self.state is State.DISABLED:
            return
        self.state = State.HOVER
        self.image = self.imageHover

    def onclick(self):
        return self.function(self)
    
    def update(self, value: float):
        convertedTuple = list(self.rect.topleft)
        convertedTuple[1] = self.position[1] - value
        self.rect.topleft = tuple(convertedTuple)   