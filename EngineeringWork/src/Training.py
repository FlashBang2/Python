import neat
import pickle
import visualize
import re
import pygame
import multiprocessing
import shutil
import os
import sys
import glob

import Button

from typing import List, Callable
from cairosvg import svg2png
from PIL import Image

from Game import Game
from NEATInputs import NEATInputs
from ButtonLogic import ButtonLogic
from CustomThread import CustomThread

class Training(ButtonLogic):
    def __init__(self):
        super().__init__()
        self.NEATInputs = NEATInputs()
        self.population = None
        self.trainingThread = None
        self.numberOfGames = None
        self.survialReward = None
        self.foodPickingReward = None
        self.elimintationReward = None
        self.winningReward = None
        self.penaltyForCollidinWithItself = None
        self.boardSize = 121
        
    def train(self, transitionToSubMenu: Callable, clickedButton: Button.Button, app):
        from App import App

        with open("Settings/Evaluation.txt") as f:
            self.gameSettings = f.readlines()

        for line in self.gameSettings:
            line = line.replace("\n", "")
            line = re.split(r' // | =', line)
            if line[0] == "Penalty For Colliding With Itself":
                self.penaltyForCollidinWithItself = int(line[1])
            if line[0] == "Number Of Games":
                self.numberOfGames = int(line[1])
            if line[0] == "Score Gain Per Survial":
                self.survialReward = int(line[1])
            if line[0] == "Score Gain Per Picking Up Food":
                self.foodPickingReward = int(line[1])
            if line[0] == "Score Per Elimination":
                self.elimintationReward = int(line[1])
            if line[0] == "Score Per Winning":
                self.winningReward = int(line[1])

        self.app: App = app
        self.baseText = "Training"
        self.animationText = "Training"
        self.textInformation= "You can always get best AI trained so Far by pressing button underneath this message"

        self.showInformation = False
        self.animationEvent = pygame.USEREVENT + 1
        self.informationEvent = pygame.USEREVENT + 2
        pygame.time.set_timer(self.animationEvent, 500)
        pygame.time.set_timer(self.informationEvent, 15000, 1)

        self.fontAnimation = pygame.font.SysFont('Arial', 50)
        self.fontInformation = pygame.font.SysFont('Arial', 12)
        font_surface = self.fontAnimation.render(self.animationText, True, (255, 255, 255))
        self.app.window.blit(font_surface, (self.app.size[0] / 2 - self.fontAnimation.size(self.animationText)[0] / 2, self.app.size[1] / 2 - self.fontAnimation.size(self.animationText)[1]))
        pygame.display.update()

        neuralNetworkConfig = neat.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, "Settings/NEAT.txt")

        self.population = neat.Population(neuralNetworkConfig)
        self.population.add_reporter(neat.StdOutReporter(True))
        self.population.add_reporter(neat.StatisticsReporter())

        node_names = {
              0: "up",
              1: "right",
              2: "down",
              3: "left",
        }

        self.getInputsFromFile(node_names)

        self.population.nodeNames = node_names
        self.population.projectDir = os.getcwd().rsplit("\\", 1)[0]
        self.threadedEvaluator = neat.ThreadedEvaluator(multiprocessing.cpu_count(), self.evaluateGenome)
        self.trainingThread = CustomThread(target = self.population.run, args = (self.threadedEvaluator.evaluate, ))
        self.trainingThread.start()
        self.controlTerminationOfTraining()

        winner = self.trainingThread.join()
        self.threadedEvaluator.stop()

        print('\nBest genome:\n{!s}'.format(winner))

        with open("Output/best.pickle", "wb") as f:
            pickle.dump(winner, f)

        if os.path.exists("Output/bestSettings"):
            shutil.rmtree("Output/bestSettings")
        shutil.copytree("Settings", "Output/bestSettings")

        """ appendix = ""
        if self.population.generation < 10:
            appendix = "00000"
        if self.population.generation > 9 and self.population.generation < 100:
            appendix = "0000"
        if self.population.generation > 99 and self.population.generation < 1000:
            appendix = "000"
        if self.population.generation > 999 and self.population.generation < 10000:
            appendix = "00"
        if self.population.generation > 9999 and self.population.generation < 100000:
            appendix = "0" """

        visualize.draw_net(neuralNetworkConfig, winner, False, "Output/Best", node_names = node_names, show_disabled = False)
        """ for svgFile in glob.glob("Output/*.svg"):
            if "FinalTopology" in svgFile:
                continue
            with open(svgFile) as f:
                svgData = "\n".join(f.readlines())
            svgFile = svgFile.replace(".svg", "")
            svg2png(bytestring = svgData, write_to = svgFile + ".png")
        listOfFiles = glob.glob("Output/*.png")
        frames = [Image.open(image) for image in listOfFiles]
        gif = frames[0]
        gif.save("Output/Best.gif", format = "GIF", append_images = frames,
                 save_all=True, duration = 200, loop = 0) """
        
        """  for index, frame in enumerate(listOfFiles):
            if index == len(listOfFiles) - 1:
                if os.path.isfile("Output/FinalTopology.svg"):
                    os.remove("Output/FinalTopology.svg")
                frame = frame.replace(".png", ".svg")
                os.rename(frame, "Output/FinalTopology.svg")
                frame = frame.replace(".svg", ".png")
                os.remove(frame)
                frame = frame.replace(".png", "")
                os.remove(frame)
                break
            os.remove(frame)
            frame = frame.replace(".png", ".svg")
            os.remove(frame)
            frame = frame.replace(".svg", "")
            os.remove(frame)"""
        transitionToSubMenu(clickedButton)

    def evaluateGenome(self, genome: neat.DefaultGenome, config: neat.Config):
        scores: List[int] = []
        for index in range(self.numberOfGames):
            fitness = 0
            game = Game()
            neuralNetwork = neat.nn.FeedForwardNetwork.create(genome, config)
            while True:
                rawValues: List[float] = []
                for function in self.inputs:
                    if type(function(game.snakes[0], game)) == type([]):
                        array = function(game.snakes[0], game)
                        for x in range(game.boardWidth - 1):
                            for y in range(game.boardHeight - 1):
                                rawValues.append(array[x][y])
                        continue
                    rawValues.append(function(game.snakes[0], game))
                output = neuralNetwork.activate(rawValues)
                decision = output.index(max(output))
                for index, snake in enumerate(game.snakes):
                    if snake.dead:
                        continue
                    if index == 0:
                        game.ai(game.snakes[0], decision)
                        continue
                    game.ai(snake, snake.getMove(game))
                game.update()
                if game.gameEnded:
                    if (game.settings["Enemy Snakes"] and game.winner == game.snakes[0]) or\
                       (game.settings["Add Food"] and game.winner == game.snakes[0]):
                        fitness += self.winningReward
                if game.snakes[0].dead or game.gameEnded:
                    if len(game.snakes[0].deathReason) > 0:
                        if "itself" in game.snakes[0].deathReason:
                            fitness -= self.penaltyForCollidinWithItself
                    if game.settings["Add Food"]:
                        fitness += (game.snakes[0].length - game.snakes[0].initialLength) * self.foodPickingReward
                    if game.settings["Enemy Snakes"]:
                        for index, snake in enumerate(game.snakes):
                            if index == 0:
                                continue
                            if snake.dead:
                                if "Human" in snake.deathReason:
                                    fitness += self.elimintationReward
                    break
                fitness += self.survialReward 
            scores.append(fitness)
        return sum(scores) / self.numberOfGames

    def getInputsFromFile(self, node_names: dict[int, str] = None):
        self.inputs: List[Callable] = []

        with open("Settings/Inputs.txt") as f:
            inputsSettings = f.readlines()
        
        key = -1
        for line in inputsSettings:
            line = line.replace("\n", "")
            line = re.split(r' // | = ', line)
            if line[1] == "True":
                self.inputs.append(self.NEATInputs.inputs[line[0]])
                if not node_names == None:
                    if "Board" in line[0]:
                        for x in range(self.boardSize):
                            node_names[key] = "Cell " + str(x + 1) + " " + line[0]
                            key -= 1
                    else:
                        node_names[key] = line[0]
                key -= 1

    def changeAppState(self, clickedButton: Button.Button):
        self.population.terminationFlag = 1
        self.baseText = "Finalizing"
        self.animationText = "Finalizing"
        self.buttons = []
        self.showInformation = False

    def controlTerminationOfTraining(self):
        from App import MouseButtons

        while True:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == MouseButtons.LEFTMOUSEBUTTON.value:
                        self.handleEvents()
                if event.type == pygame.QUIT:
                    self.population.terminationFlag = 1
                    self.animationText = "Finalizing"
                    self.app.window.fill((0, 0, 0))
                    font_surface = self.fontAnimation.render(self.animationText, True,(255, 255, 255))
                    self.app.window.blit(font_surface, ((self.app.size[0] / 2 - self.fontAnimation.size(self.animationText)[0] / 2, self.app.size[1] / 2 - self.fontAnimation.size(self.animationText)[1])))
                    pygame.display.update()
                    self.trainingThread.join()
                    self.threadedEvaluator.stop()
                    """ for file in glob.glob("Output/*.svg"):
                        if "FinalTopology" in file:
                            continue 
                        os.remove(file)
                        file = file.replace(".svg", "")
                        os.remove(file)"""
                    pygame.quit()
                    sys.exit()
                if event.type == self.animationEvent:
                    self.app.window.fill((0, 0, 0))
                    if len(self.animationText) > len(self.baseText) + 2:
                        self.animationText = self.baseText
                    else:
                        self.animationText += "."
                    font_surface = self.fontAnimation.render(self.animationText, True,(255, 255, 255))
                    self.app.window.blit(font_surface, ((self.app.size[0] / 2 - self.fontAnimation.size(self.animationText)[0] / 2, self.app.size[1] / 2 - self.fontAnimation.size(self.animationText)[1])))
                    if self.showInformation:
                        font_surface = self.fontInformation.render(self.textInformation, True, (255, 255, 255))
                        self.app.window.blit(font_surface, (self.app.size[0] / 2 - self.fontInformation.size(self.textInformation)[0] / 2, self.app.size[1] / 2 + 20))
                        button = Button.Button((self.app.size[0] / 2 - self.app.Config.buttonHover.get_width() / 2, self.app.size[1] / 2 + 60), self.app.Config.buttonHover, self.app.Config.buttonUnhover, (0, 0, 0), 25, "STOP", (0, 0), self.changeAppState, True, False)
                        self.buttons.append(button)
                if event.type == self.informationEvent:
                    self.showInformation = True
                self.update(pygame.mouse.get_pos())
                self.render(self.app.window)
                pygame.display.update()
    
            if not self.trainingThread._return is None:
                break