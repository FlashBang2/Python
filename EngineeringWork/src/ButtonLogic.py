import pygame
import Button

from typing import List, Tuple

class ButtonLogic:
    def __init__(self):
        self.buttons: List[Button.Button] = []

    def render(self, window: pygame.Surface):
        if len(self.buttons) > 0:
            for button in self.buttons:
                button.render(window)
                button.visible = True

    def update(self, mousePosition: Tuple[int, int]):
        if len(self.buttons) > 0:
            for button in self.buttons:
                if button.rect.topleft[0] < mousePosition[0] and button.rect.topright[0] > mousePosition[0] and\
                   button.rect.topleft[1] < mousePosition[1] and button.rect.bottomleft[1] > mousePosition[1] and button.visible:
                    button.onhover()
                    continue
                if button.state is Button.State.HOVER:
                    button.onleave()

    def handleEvents(self):
        if len(self.buttons) > 0:
            for button in self.buttons:
                if button.state is Button.State.HOVER:
                    button.onclick()

    def reset(self, window: pygame.Surface):
        window.fill((0, 0, 0))
        if len(self.buttons) > 0:
            for button in self.buttons:
                button.visible = False