import pygame
import Button

from typing import List, Tuple
from ButtonLogic import ButtonLogic

class Submenu(ButtonLogic):
    def __init__(self, appSize: Tuple[int, int], transitionToTraining, transitionToTesting, transitionToConfig, transitionToMenu):
        self.size = appSize

        # --- Textures ---

        self.buttonUnhover = pygame.image.load("Assets/ButtonUnhover.png").convert_alpha()
        self.buttonHover = pygame.image.load("Assets/ButtonHover.png").convert_alpha()

        # --- Buttons ---

        self.buttons: List[Button.Button] = []
        self.buttons.append(Button.Button((self.size[0] / 2 + 200, 200), self.buttonHover, self.buttonUnhover, (0, 0, 0), 25, "TrainAI", (0, 0), transitionToTraining, False, False))
        self.buttons.append(Button.Button((self.size[0] / 2 - 400, 200), self.buttonHover, self.buttonUnhover, (0, 0, 0), 25, "TestAI", (0, 0), transitionToTesting, False, False))
        self.buttons.append(Button.Button((self.size[0] / 2 - 100, 200), self.buttonHover, self.buttonUnhover, (0, 0, 0), 25, "Config", (0, 0), transitionToConfig, False, False))
        self.buttons.append(Button.Button((self.size[0] / 2 - 100, 350), self.buttonHover, self.buttonUnhover, (0, 0, 0), 25, "Menu", (0, 0), transitionToMenu, False, False))