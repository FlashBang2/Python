import time
import pygame

from typing import Tuple
from enum import Enum

class State(Enum):
    NOTACTIVE = 0
    ACTIVE = 1
    HOVERED = 2

class TextField:
    def __init__(self, position: Tuple[float, float], imageHover: pygame.Surface, imageUnhover: pygame.Surface, caption: str, padding: Tuple[int, int]):
        self.position = position
        self.imageHover = imageHover
        self.imageUnhover = imageUnhover
        self.texture = pygame.image.load("Assets/TextFieldUnhover.png")
        self.font = pygame.font.SysFont("Arial", 25)
        self.caption = self.font.render(caption, True, (192, 192, 192))
        self.captionValue = caption
        self.text = ''
        self.rect = pygame.Rect(position[0], position[1], self.texture.get_width(), self.texture.get_height())
        self.state = State.NOTACTIVE
        self.text_surface = self.font.render(self.text, True, (192, 192, 192))
        self.text_rect = self.text_surface.get_rect(topleft = (self.rect.x + 5, self.rect.y + 5))
        self.cursor_offsets = [position[0] + 5]
        self.cursor_size: Tuple[int, int] = (1, self.text_rect.height)
        self.current_cursor_offset = 0
        self.padding = padding

    def update(self, value: float):
        convertedTuple = list(self.rect.topleft)
        convertedTuple[1] = self.position[1] - value
        self.rect.topleft = tuple(convertedTuple)

    def render(self, window = pygame.Surface):
        window.blit(self.caption, (self.rect.x + self.padding[0], self.rect.y + self.padding[1]))
        window.blit(self.texture, (self.rect.x, self.rect.y))
        window.blit(self.text_surface, (self.rect.x + 5, self.rect.y + 5))
        if time.time() % 1 >= 0.5 and self.state is State.ACTIVE:
            self.cursor = pygame.Rect(self.text_rect.topright, self.cursor_size)
            self.cursor.midleft = (self.cursor_offsets[self.current_cursor_offset], self.text_rect.midleft[1])
            pygame.draw.rect(window, (255, 255, 255), self.cursor)

    def onhover(self):
        if self.state is State.ACTIVE:
            return
        self.state = State.HOVERED
        self.texture = self.imageHover
    
    def onleave(self):
        if self.state is State.ACTIVE:
            return
        self.state = State.NOTACTIVE
        self.texture = self.imageUnhover