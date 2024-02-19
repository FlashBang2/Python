import pygame

from typing import Tuple

class Slider:
    def __init__(self, position: Tuple[int, int], size: Tuple[int, int], initialValue: float, max: int):
        self.position = position
        self.size = size

        self.sliderRect = pygame.Rect(self.position[0] - self.size[0] / 2, self.position[1] - self.size[1] / 2, self.size[0], self.size[1])
        self.buttonRect = pygame.Rect(self.position[0] - self.size[0] / 2, self.position[1] - self.size[1] / 2 + self.size[1] * initialValue, self.size[0], 10)

        self.visible = False
        self.max = max

    def moveSlider(self, mouseposition: Tuple[int, int]):
        self.buttonRect.centery = mouseposition[1]

    def render(self, window: pygame.Surface):
        pygame.draw.rect(window, "darkgray", self.sliderRect)
        pygame.draw.rect(window, "blue", self.buttonRect)

    def getValue(self) -> float:
        return (self.buttonRect.centery - self.sliderRect.top) / self.size[1] * self.max