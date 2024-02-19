import pygame

import Button

from typing import List, Tuple

from ButtonLogic import ButtonLogic


class TestingOptionMenu(ButtonLogic):
    def __init__(self, appSize: Tuple[int, int], transitionToTestingWithHuman, transitionToTestingWithAI):
        self.size = appSize
        self.font = pygame.font.SysFont("Arial", 40)

        # --- Textures ---

        self.buttonUnhover = pygame.image.load("Assets/ButtonUnhover.png").convert_alpha()
        self.buttonHover = pygame.image.load("Assets/ButtonHover.png").convert_alpha()

        # --- Buttons ---

        self.buttons: List[Button.Button] = []
        self.buttons.append(Button.Button((self.size[0] / 2, self.size[1] / 2 - 100), self.buttonHover, self.buttonUnhover, (0, 0, 0), 25, "I want to play", (0, 0), transitionToTestingWithHuman, True, False))
        self.buttons.append(Button.Button((self.size[0] / 2 - 210, self.size[1] / 2 - 100), self.buttonHover, self.buttonUnhover, (0, 0, 0), 25, "Let AI play", (0, 0), transitionToTestingWithAI, True, False))