import pygame
import re
import sys

import TextField
import Button

from typing import Tuple
from enum import Enum

from Config import Config
from Menu import Menu
from Training import Training
from Submenu import Submenu
from Testing import Testing
from TestingOptionMenu import TestingOptionMenu

class MouseButtons(Enum):
    LEFTMOUSEBUTTON = 1
    MIDDLEMOUSEUBTTON = 2
    RIGHTCLICK = 3
    SCROLLUP = 4
    SCROLLDOWN = 5

class State(Enum):
    MENU = 1
    SUBMENU = 2
    GAME = 3
    CONFIG = 4
    TRAINING = 5
    GAMEOPTIONS = 6

class App:
    def __init__(self, size: Tuple[int, int]):
        self.state = State.MENU
        self.size = size[0], size[1]
        self.window = pygame.display.set_mode(self.size)
        
        self.Menu = Menu(self.size, self.quitApplication, self.transitionToSubMenu)
        self.Submenu = Submenu(self.size, self.transitionToTraining, self.transitionToTestingOptions, self.transitionToConfig, self.transitionToMenu)
        self.Config = Config(self.size, self.transitionFromConfigToSubMenu)
        self.Training = Training()
        self.TestingOptionMenu = TestingOptionMenu(self.size, self.transitionToTestingWithHuman, self.transitionToTestingWithAI)

        pygame.key.set_repeat(500, 100)
        pygame.display.set_caption("SnakeAITrainner")

    def run(self):
        while True:
            self.mousePosition = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == MouseButtons.LEFTMOUSEBUTTON.value:
                        if self.state is State.MENU:
                            self.Menu.handleEvents()
                            continue
                        if self.state is State.SUBMENU:
                            self.Submenu.handleEvents()
                            continue
                        if self.state is State.GAMEOPTIONS:
                            self.TestingOptionMenu.handleEvents()
                        if self.state is State.CONFIG:
                            self.Config.handleEvents()
                            for textBox in self.Config.textBoxes:
                                if textBox.state is TextField.State.ACTIVE:
                                   textBox.state = TextField.State.NOTACTIVE
                                   textBox.onleave()
                                if textBox.state is TextField.State.HOVERED:
                                    textBox.state = TextField.State.ACTIVE
                            continue
                    if event.button == MouseButtons.SCROLLUP.value:
                        if self.state is State.CONFIG:
                            self.Config.sliders[0].buttonRect.centery -= 10
                            if self.Config.sliders[0].buttonRect.centery < 100:
                                self.Config.sliders[0].buttonRect.centery = 100
                    if event.button == MouseButtons.SCROLLDOWN.value:
                        if self.state is State.CONFIG:
                            self.Config.sliders[0].buttonRect.centery += 10
                            if self.Config.sliders[0].buttonRect.centery > 599:
                                self.Config.sliders[0].buttonRect.centery = 599
                if event.type == pygame.KEYDOWN and self.state is State.CONFIG:
                    for textBox in self.Config.textBoxes:
                        if textBox.state == TextField.State.NOTACTIVE:
                            continue
                        if event.key == pygame.K_LEFT:
                            if textBox.current_cursor_offset > 0:
                                textBox.current_cursor_offset -= 1
                        if event.key == pygame.K_RIGHT:
                            if textBox.current_cursor_offset < len(textBox.cursor_offsets) - 1:
                                textBox.current_cursor_offset += 1
                        if event.key == pygame.K_BACKSPACE:
                            if len(textBox.cursor_offsets) > 1 and textBox.current_cursor_offset > 0:
                                textBox.text = textBox.text[:textBox.current_cursor_offset - 1] + textBox.text[textBox.current_cursor_offset:]
                                textBox.text_surface = textBox.font.render(textBox.text, True, (255, 255, 255))
                                textBox.text_rect = textBox.text_surface.get_rect(topleft = (textBox.rect.x + 5, textBox.rect.y + 5))
                                textBox.cursor_offsets = textBox.cursor_offsets[:-1]
                                textBox.current_cursor_offset -= 1
                        character = re.findall('[0-9]', event.unicode)
                        if len(character) > 0 and len(textBox.text) < 7:
                            textBox.text = textBox.text[:textBox.current_cursor_offset] + character[0] + textBox.text[textBox.current_cursor_offset:]
                            textBox.text_surface = textBox.font.render(textBox.text, True, (255, 255, 255))
                            textBox.text_rect = textBox.text_surface.get_rect(topleft = (textBox.rect.x + 5, textBox.rect.y + 5))
                            textBox.cursor_offsets.append(textBox.text_rect.midright[0])
                            textBox.current_cursor_offset += 1
                   
            if self.state is State.MENU:
                self.Menu.render(self.window)
                self.Menu.update(self.mousePosition)
            if self.state is State.SUBMENU:
                self.Submenu.render(self.window)
                self.Submenu.update(self.mousePosition)
            if self.state is State.CONFIG:
                self.Config.render(self.window)
                self.Config.update(self.mousePosition)
                self.Config.sliderLogic(self.mousePosition)
            if self.state is State.GAMEOPTIONS:
                self.TestingOptionMenu.render(self.window)
                self.TestingOptionMenu.update(self.mousePosition)
            pygame.display.update()

    def transitionFromConfigToSubMenu(self, clickedButton: Button.Button):
        self.Config.saveSettings()
        self.transitionToSubMenu(clickedButton)

    def transitionToSubMenu(self, clickedButton: Button.Button):
        self.state = State.SUBMENU
        clickedButton.state = Button.State.NONE
        self.Menu.reset(self.window)
        self.Config.reset(self.window)

    def transitionToTraining(self, clickedButton: Button.Button):
        self.state = State.TRAINING
        clickedButton.state = Button.State.NONE 
        self.Training.reset(self.window)
        self.Training.train(self.transitionToSubMenu, clickedButton, self)

    def transitionToTestingOptions(self, clickedButton: Button.Button):
        self.state = State.GAMEOPTIONS
        clickedButton.state = Button.State.NONE
        self.Submenu.reset(self.window)

    def transitionToTestingWithHuman(self, clickedButton: Button.Button):
        self.state = State.GAME
        clickedButton.state = Button.State.NONE
        self.Testing = Testing(self.transitionToSubMenu, self.transitionToTestingWithHuman)
        self.Testing.reset(self.window)
        self.Testing.test(self.window, True)
    
    def transitionToTestingWithAI(self, clickedButton: Button.Button):
        self.state = State.GAME
        clickedButton.state = Button.State.NONE
        self.Testing = Testing(self.transitionToSubMenu, self.transitionToTestingWithAI)
        self.Testing.reset(self.window)
        self.Testing.test(self.window, False)

    def transitionToConfig(self, clickedButton: Button.Button):
        self.state = State.CONFIG
        clickedButton.state = Button.State.NONE
        self.Config.readSettings()
        self.Submenu.reset(self.window)

    def transitionToMenu(self, clickedButton: Button.Button):
        self.state = State.MENU
        clickedButton.state = Button.State.NONE
        self.Submenu.reset(self.window)

    def quitApplication(self, clickedButton: Button.Button):
        pygame.quit()
        sys.exit()