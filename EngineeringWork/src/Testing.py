import neat
import pickle
import pygame
import shutil
import os
import glob

import Button

from Game import Game
from Training import Training
from ButtonLogic import ButtonLogic

class Testing(ButtonLogic):
    def __init__(self, transitionToSubMenu, transitionToTesting):
        super().__init__()

        self.buttons.append(Button.Button((800, 700), pygame.image.load("Assets/ButtonHover.png").convert_alpha(), pygame.image.load("Assets/ButtonUnhover.png").convert_alpha(), (0, 0, 0), 25, "Go Back", (0, 0),  transitionToSubMenu, True, False))
        self.buttons.append(Button.Button((590, 700), pygame.image.load("Assets/ButtonHover.png").convert_alpha(), pygame.image.load("Assets/ButtonUnhover.png").convert_alpha(), (0, 0, 0), 25, "Another Game", (0, 0), transitionToTesting, True, False))
        
        self.font = pygame.font.SysFont("Arial", 40)
        self.deathMessageFont = pygame.font.SysFont("Arial", 20)
        self.Training = Training()
        self.setupNeuralNetwork = True
        self.returned = False
    
    def render(self, window: pygame.Surface, game: Game):
        super().render(window)
        window.blit(self.font.render("Turn " + str(game.turn), True, (255, 255, 255)), (775, 25))
        adjust = 0
        currentHeight = 0
        for index, snake in enumerate(game.snakes):
            if snake.dead:
                adjust += 1
                continue
            currentHeight = 125 + (100 * (index - adjust))
            window.blit(self.font.render(snake.name, True, (255, 255, 255)), (675, currentHeight - 45, 100 ,50))
            window.blit(self.font.render(str(snake.length), True, (255, 255, 255)), (675 + 250, currentHeight - 45, 100 ,50))
            pygame.draw.rect(window, (65, 65, 65), (675, currentHeight, 300, 50), 0, 16)
            pygame.draw.rect(window, snake.color, (675, currentHeight, 300 * (snake.health / 100), 50), 0, 16)
            window.blit(self.font.render(str(snake.health), True, (0, 0, 0)), (675, currentHeight, 100, 50))
        for index, snake in enumerate(game.snakes):
            if not snake.dead:
                continue
            currentHeight += 100
            window.blit(self.font.render(snake.name, True, (255, 255, 255)), (675, currentHeight - 45, 100 ,50))
            window.blit(self.font.render(str(snake.length), True, (255, 255, 255)), (675 + 250, currentHeight - 45, 100 ,50))
            if "\n" in snake.deathReason:
                window.blit(self.deathMessageFont.render(snake.deathReason.split("\n")[0], True, (255, 255, 255)), (675, currentHeight, 300, 50))
                window.blit(self.deathMessageFont.render(snake.deathReason.split("\n")[1], True, (255, 255, 255)), (675, currentHeight + 25, 300, 50))
                continue
            window.blit(self.deathMessageFont.render(snake.deathReason, True, (255, 255, 255)), (675, currentHeight, 300, 50))

    def reset(self, window: pygame.Surface):
        window.fill((0, 0, 0))
        pygame.display.update()

    def test(self, window: pygame.Surface, replaceWithHuman: bool):
        self.replaceWithHuman = replaceWithHuman
        self.returned = False

        neuralNetworks = []
        neuralNetworksInputs = []    
        
        game = None

        counter = 0
        os.chdir("Output")
        for file in glob.glob("*.pickle"):
            file = file.replace(".pickle", "")
            if os.path.exists(file + "Settings"):
                if game is None:
                    shutil.rmtree("../Settings")
                    shutil.copytree(file + "Settings", "../Settings")
                    os.chdir("../")
                    game = Game()
                    os.chdir("Output")
                with open(file + "Settings/Game.txt") as f:
                    neuralNetworkEnviroment = f.readlines()
                notSuitableForCurrentEnviroment = False
                for line in neuralNetworkEnviroment:
                    line = line.replace("\n", "")
                    line = line.split(" = ")
                    if not line[1] == str(game.settings[line[0]]):
                        notSuitableForCurrentEnviroment = True
                        break
                if notSuitableForCurrentEnviroment:
                    continue    
            if game is None:
                os.chdir("../")
                game = Game()
                os.chdir("Output")
            if not game.settings['Enemy Snakes'] and counter == 1:
                break
            if counter == 3:
                break
            with open(file + ".pickle", "rb") as f:
                genome = pickle.load(f)
            shutil.rmtree("../Settings")
            shutil.copytree(file + "Settings", "../Settings")  
            neuralNetworkConfig = neat.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, "../Settings/NEAT.txt")
            os.chdir("../")
            self.Training.getInputsFromFile()
            os.chdir("Output")
            neuralNetwork = neat.nn.FeedForwardNetwork.create(genome, neuralNetworkConfig)
            neuralNetwork.snakeName = file
            neuralNetworks.append(neuralNetwork)
            neuralNetworksInputs.append(self.Training.inputs)
            counter += 1
        os.chdir("../")

        if game is None:
            game = Game()

        while True:
            game.handleEvents(window, self, neuralNetworks, neuralNetworksInputs)
            window.fill((0, 0, 0))
            game.render(window)
            self.render(window, game)
            pygame.display.update()
            self.update(pygame.mouse.get_pos())
            if self.returned:
                break
        window.fill((0, 0, 0))
        pygame.display.update()