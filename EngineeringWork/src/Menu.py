import pygame

import Button

from typing import List, Tuple

from ButtonLogic import ButtonLogic

class Menu(ButtonLogic):
    def __init__(self, appSize: Tuple[int, int], quitApplication, transitionToSubMenu):
        self.size = appSize
        self.titleFont = pygame.font.SysFont("Arial", 80)
        self.font = pygame.font.SysFont("Arial", 40)

        # --- Textures ---

        self.buttonUnhover = pygame.image.load("Assets/ButtonUnhover.png").convert_alpha()
        self.buttonHover = pygame.image.load("Assets/ButtonHover.png").convert_alpha()

        # --- Buttons ---
        
        self.buttons: List[Button.Button] = []
        self.buttons.append(Button.Button((self.size[0] / 2 - 100, 250), self.buttonHover, self.buttonUnhover, (0, 0, 0), 25, "Play", (0, 0), transitionToSubMenu, True, False))
        self.buttons.append(Button.Button((self.size[0] / 2 - 100, 400), self.buttonHover, self.buttonUnhover, (0, 0, 0), 25, "Quit", (0, 0), quitApplication, True, False))

    def render(self, window: pygame.Surface):
        super().reset(window)
        super().render(window)
        window.blit(self.titleFont.render("Snake AI Trainer", True, (255, 255, 255)), (self.size[0] / 2 - 275, 75))
        window.blit(self.font.render("1.0", True, (255, 255, 255)), (940, 750))