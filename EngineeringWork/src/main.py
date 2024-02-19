import os

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

import pygame

from App import App

if __name__ == "__main__":

    pygame.init()

    application = App((1000, 800))

    application.run()