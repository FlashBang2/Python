import pygame
import re
import Button
import TextField

from typing import Callable, List, Tuple
from ButtonLogic import ButtonLogic
from Slider import Slider

class Config(ButtonLogic):
    def __init__(self, appSize: Tuple[int, int], transitionToSubMenu: Callable):
        self.font = pygame.font.SysFont("Arial", 40)
        self.size = appSize
        self.boardSize = 121
        
        # --- Textures ---

        self.markCheckboxUnhover = pygame.image.load("Assets/MarkCheckboxUnhover.png").convert_alpha()
        self.markCheckboxHover = pygame.image.load("Assets/MarkCheckboxHover.png").convert_alpha()
        self.buttonUnhover = pygame.image.load("Assets/ButtonUnhover.png").convert_alpha()
        self.buttonHover = pygame.image.load("Assets/ButtonHover.png").convert_alpha()
        self.checkboxUnhover = pygame.image.load("Assets/CheckboxUnhover.png").convert_alpha()
        self.checkboxHover = pygame.image.load("Assets/CheckboxHover.png").convert_alpha()
        self.textFieldUnhover = pygame.image.load("Assets/TextFieldUnhover.png").convert_alpha()
        self.textFieldHover = pygame.image.load("Assets/TextFieldHover.png").convert_alpha()
        
        # --- Sliders ---

        self.sliders: List[Slider] = []
        self.sliders.append(Slider((800, 350), (30, 500), 0, 4000))

        # --- Buttons ---

        self.buttons: List[Button.Button] = []
        self.buttons.append(Button.Button((self.size[0] / 2 - 100, 600), self.buttonHover, self.buttonUnhover, (0, 0, 0), 25, "Go Back", (0, 0), transitionToSubMenu, False, False))

        # --- Text Fields ---
        self.textBoxes: List[TextField.TextField] = []

    def update(self, mousePosition: Tuple[int, int]):
        super().update(mousePosition)
        for textbox in self.textBoxes:
            if textbox.state is TextField.State.HOVERED:
                textbox.onleave()
            if textbox.rect.topleft[0] < mousePosition[0] and textbox.rect.topright[0] > mousePosition[0] and\
               textbox.rect.topleft[1] < mousePosition[1] and textbox.rect.bottomleft[1] > mousePosition[1]:
                textbox.onhover()
                continue

    def render(self, window: pygame.Surface):
        window.fill((0,0,0))
        size = self.font.size("-------GAME SETTINGS------")
        window.blit(self.font.render("-------GAME SETTINGS------", True, (255, 255, 255)), (self.size[0] / 2 - size[0] / 2, 125 - self.sliders[0].getValue()))
        size = self.font.size("------NEAT SETTINGS-------")
        window.blit(self.font.render("------NEAT SETTINGS-------", True, (255, 255, 255)), (self.size[0] / 2 - size[0] / 2, 225 + (len(self.gameSettings)) * 75 - self.sliders[0].getValue()))
        size = self.font.size("---EVALUATION SETTINGS----")
        window.blit(self.font.render("---EVALUATION SETTINGS----", True, (255, 255, 255)), (self.size[0] / 2 - size[0] / 2, 275 + (3 + len(self.gameSettings)) * 75 - self.sliders[0].getValue()))
        size = self.font.size("------INPUTS SETTINGS-----")
        window.blit(self.font.render("------INPUTS SETTINGS-----", True, (255, 255, 255)), (self.size[0] / 2 - size[0] / 2, 325 + (3 + len(self.evaluationSettings) + len(self.gameSettings)) * 75 - self.sliders[0].getValue()))
        self.sliders[0].render(window)
        for button in self.buttons:
            button.visible = True
            if button.text == "Go Back":
               continue
            button.render(window)
            button.update(self.sliders[0].getValue())
        for textBox in self.textBoxes:
            textBox.render(window)
            textBox.update(self.sliders[0].getValue())
            textBox.text_surface = textBox.font.render(textBox.text, True, (255, 255, 255))
            textBox.text_rect = textBox.text_surface.get_rect(topleft = (textBox.rect.x + 5, textBox.rect.y + 5))
        pygame.draw.rect(window, (0, 0, 0), (0, 0, 1000, 100))
        pygame.draw.rect(window, (0, 0, 0), (0, self.size[1] - 200, 1000, 200))
        self.buttons[0].render(window)

    def changeButtonState(self, clickedButton: Button.Button):
        if clickedButton.imageUnhover == self.markCheckboxUnhover:
            clickedButton.checked = False
            clickedButton.imageUnhover = self.checkboxUnhover
            clickedButton.imageHover = self.checkboxHover
            if clickedButton.text == "Add Food" or clickedButton.text == "Enemy Snakes":
                self.readInputsSettings(clickedButton.text, clickedButton.checked)
            return
        clickedButton.checked = True
        clickedButton.imageUnhover = self.markCheckboxUnhover
        clickedButton.imageHover = self.markCheckboxHover
        if clickedButton.text == "Add Food" or clickedButton.text == "Enemy Snakes":
            self.readInputsSettings(clickedButton.text, clickedButton.checked)

    def sliderLogic(self, mousePostion: Tuple[int, int]):
        for slider in self.sliders:
            if slider.sliderRect.collidepoint(mousePostion) and pygame.mouse.get_pressed()[0]:
                slider.moveSlider(mousePostion)

    def readSettings(self):

        # -- Reading Files --

        with open("Settings/Game.txt") as f:
            self.gameSettings = f.readlines()
        with open("Settings/NEAT.txt") as f:
            self.neatSettings = f.readlines()
        with open("Settings/Evaluation.txt") as f:
            self.evaluationSettings = f.readlines()
        with open("Settings/Inputs.txt") as f:
            self.inputsSettings = f.readlines()

        # -- Buttons --

        button = self.buttons[0]
        self.buttons = []
        self.buttons.append(button)

        # -- TextBoxes --

        self.textBoxes = []

        # -- Game Settings --

        self.addFoodButtonCheckStatus = None
        self.enemySnakeButtonCheckStatus = None

        for index, line in enumerate(self.gameSettings):
            line = line.replace("\n", "")
            line = line.split(" = ")
            button = Button.Button((self.size[0] / 2 - 25, 125 + (1 + index) * 75), self.checkboxHover, self.checkboxUnhover, (192, 192, 192), 25, line[0], (-450, 7), self.changeButtonState, True, True)
            if line[0] == "Add Food":
                self.addFoodButtonCheckStatus = line[1] == "True"
            if line[0] == "Enemy Snakes":
                self.enemySnakeButtonCheckStatus = line[1] == "True"
            if line[1] == "True":
                button.checked = True
                button.imageUnhover = self.markCheckboxUnhover
                button.imageHover = self.markCheckboxHover
                button.image = button.imageUnhover
            self.buttons.append(button)

        # -- NEAT Settings --

        self.NEATSettingsOffset = 0
        for index, line in enumerate(self.neatSettings):
            line = line.replace('\n', "")
            line = line.split(" = ")
            if line[0].replace(" ", "") == "fitness_threshold":
                textBox = TextField.TextField((self.size[0] / 2 - 25, 225 + (1 + self.NEATSettingsOffset + len(self.gameSettings)) * 75), self.textFieldHover, self.textFieldUnhover, "Fitness Target", (-450, 7))
                for character in line[1]:
                    textBox.text += character
                    textBox.text_surface = textBox.font.render(textBox.text, True, (192, 192, 192))
                    textBox.text_rect = textBox.text_surface.get_rect(topleft = (textBox.rect.x + 5, textBox.rect.y + 5))
                    textBox.cursor_offsets.append(textBox.text_rect.midright[0])
                    textBox.current_cursor_offset += 1
                self.NEATSettingsOffset += 1
                self.textBoxes.append(textBox)
            if line[0].replace(" ", "") == "pop_size":
                textBox = TextField.TextField((self.size[0] / 2 - 25, 225 + (1 + self.NEATSettingsOffset + len(self.gameSettings)) * 75), self.textFieldHover, self.textFieldUnhover, "Population Size", (-450, 7))
                for character in line[1]:
                    textBox.text += character
                    textBox.text_surface = textBox.font.render(textBox.text, True, (192, 192, 192))
                    textBox.text_rect = textBox.text_surface.get_rect(topleft = (textBox.rect.x + 5, textBox.rect.y + 5))
                    textBox.cursor_offsets.append(textBox.text_rect.midright[0])
                    textBox.current_cursor_offset += 1
                self.NEATSettingsOffset += 1
                self.textBoxes.append(textBox)
            if line[0].replace(" ", "") == "initial_connection":
                button = Button.Button((self.size[0] / 2 - 25, 225 + (1 + self.NEATSettingsOffset + len(self.gameSettings)) * 75), self.checkboxHover, self.checkboxUnhover, (192, 192, 192), 25, "Initial Full Connect", (-450, 7), self.changeButtonState, True, True)
                if line[1] == "full":
                    button.checked = True
                    button.imageUnhover = self.markCheckboxUnhover
                    button.imageHover = self.markCheckboxHover
                    button.image = button.imageUnhover
                self.NEATSettingsOffset += 1
                self.buttons.append(button)
                
        # -- Evaluation Settings --
            
        for index, line in enumerate(self.evaluationSettings):
            line = line.replace("\n", "")
            line = re.split(r' // | = ', line)
            textBox = TextField.TextField((self.size[0] / 2 - 25, 275 + (index + 1 + self.NEATSettingsOffset + len(self.gameSettings)) * 75), self.textFieldHover, self.textFieldUnhover, line[0], (-450, 7))
            for character in line[1]:
                textBox.text += character
                textBox.text_surface = textBox.font.render(textBox.text, True, (192, 192, 192))
                textBox.text_rect = textBox.text_surface.get_rect(topleft = (textBox.rect.x + 5, textBox.rect.y + 5))
                textBox.cursor_offsets.append(textBox.text_rect.midright[0])
                textBox.current_cursor_offset += 1
            self.textBoxes.append(textBox)
                                                                
        self.readInputsSettings()
                    
    def readInputsSettings(self, changedButton: str = "", value: bool = False):
        if changedButton == "Add Food":
            self.addFoodButtonCheckStatus = value
        if changedButton == "Enemy Snakes":
            self.enemySnakeButtonCheckStatus = value

        self.buttons = self.buttons[:5:] if len(self.buttons) > 6 else self.buttons
        ordinaryNumber = 0
        for line in self.inputsSettings:
            line = line.replace("\n", "")
            line = re.split(r' // | = ', line)
            if ("Food" in line[0] and not self.addFoodButtonCheckStatus) or ("Enemy" in line[0] and not self.enemySnakeButtonCheckStatus):
                continue
            button = Button.Button((self.size[0] / 2 - 25, 325 + (ordinaryNumber + 1 + self.NEATSettingsOffset + len(self.gameSettings) + len(self.evaluationSettings)) * 75), self.checkboxHover, self.checkboxUnhover, (192, 192, 192), 25, line[0], (-450, 7), self.changeButtonState, True, True)
            if line[1] == "True":
                button.checked = True
                button.imageUnhover = self.markCheckboxUnhover
                button.imageHover = self.markCheckboxHover
                button.image = button.imageUnhover
            self.buttons.append(button)
            ordinaryNumber += 1
        for line in self.inputsSettings:
            line = line.replace("\n", "")
            line = re.split(r' // | = ', line)
            if (not "Food" in line[0] or self.addFoodButtonCheckStatus) and (not "Enemy" in line[0] or self.enemySnakeButtonCheckStatus):
                continue
            button = Button.Button((self.size[0] / 2 - 25, 325 + (ordinaryNumber + 1 + self.NEATSettingsOffset + len(self.gameSettings) + len(self.evaluationSettings)) * 75), self.checkboxHover, self.checkboxUnhover, (192, 192, 192), 25, line[0], (-450, 7), self.changeButtonState, True, True)
            button.checked = False
            button.imageUnhover = self.checkboxUnhover
            button.imageHover = self.checkboxHover
            button.state = Button.State.DISABLED
            button.caption = button.font.render(button.text, True, (192, 0, 0))
            self.buttons.append(button)
            ordinaryNumber += 1

    def saveSettings(self):
        count = 0
        if hasattr(self, "gameSettings"):
            with open("Settings/Game.txt", "w") as f:
                for line in self.gameSettings:
                    for button in self.buttons:
                        if button.text == line.split(" = ")[0]:
                            f.write(button.text + " = " + str(button.checked) + "\n")
        if hasattr(self, "inputsSettings"):
            with open("Settings/Inputs.txt", "w") as f:
                for line in self.inputsSettings:
                    for button in self.buttons:
                        lineSegments = re.split(r' // | = ', line)
                        if button.text == lineSegments[0]:
                            if button.checked and not "Board" in lineSegments[0]:
                                count += 1
                            if button.checked and "Board" in lineSegments[0]:
                                count += self.boardSize
                            if len(lineSegments) > 2:
                                f.write(button.text + " = " + str(button.checked) + " // " + lineSegments[2])
                            else:
                                f.write(button.text + " = " + str(button.checked) + "\n")
        if hasattr(self, "neatSettings"):
            for btn in self.buttons:
                if btn.text == "Initial Full Connect":
                    button = btn
            with open("Settings/NEAT.txt", "w") as f:
                for line in self.neatSettings:
                    lineSegments = re.split(r'= ', line)
                    if lineSegments[0].strip() == "num_inputs":
                        f.write(lineSegments[0] + "= " + str(count) + "\n")
                        continue
                    if lineSegments[0].strip() == 'fitness_threshold':
                        if len(self.textBoxes[0].text) == 0:
                            self.textBoxes[0].text = 0
                        f.write(lineSegments[0] + "= " + str(self.textBoxes[0].text) + "\n")
                        continue
                    if lineSegments[0].strip() == 'pop_size':
                        if len(self.textBoxes[1].text) == 0 or int(self.textBoxes[1].text) < 2:
                            self.textBoxes[1].text = 2
                        f.write(lineSegments[0] + "= " + str(self.textBoxes[1].text) + "\n")
                        continue
                    if lineSegments[0].strip() == 'initial_connection':
                        f.write(lineSegments[0] + "= full\n" if button.checked else lineSegments[0] + "= unconnected\n")
                        continue
                    f.write(line)
        if hasattr(self, "evaluationSettings"):
            with open("Settings/Evaluation.txt", "w") as f:
                for line in self.evaluationSettings:
                    for textBox in self.textBoxes:
                        lineSegments = re.split(r' // | = ', line)
                        if textBox.captionValue == lineSegments[0]:
                            if len(lineSegments) > 2:
                                if len(textBox.text) == 0:
                                    textBox.text = str(0)
                                f.write(textBox.captionValue + " = " + textBox.text + " // " + lineSegments[2])
                            else:
                                if line[1] == "Number Of Games" and (textBox.text == 0 or len(textBox.text) == 0):
                                    textBox.text = str(1)
                                f.write(textBox.captionValue + " = " + textBox.text + "\n")