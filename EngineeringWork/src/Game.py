import pygame
import random
import neat
import sys
import glob
import os

from PIL import Image
from typing import List, Callable
from Snake import Snake

class Game:
    def __init__(self):
        with open("Settings/Game.txt") as f:
            self.gameSettings = f.readlines()
            self.settings = {
                'Add Food': False,
                'Randomize Start': False,
                'Enemy Snakes': False
            }
        
        for index, line in enumerate(self.gameSettings):
            line = line.replace("\n", "")
            line = line.split(" = ")
            self.settings[line[0]] = True if line[1] == "True" else False
        
        self.possibleSpawns = [(2, 2), (2, 10), (10, 2), (10, 10), (2, 6), (6, 2), (6, 10), (10, 6)]
        (self.boardWidth, self.boardHeight) = 12, 12
        self.isrunning = True
        spawnPoint = random.choice(self.possibleSpawns)
        self.snakes: List[Snake] = [Snake((255, 255, 255), (2, 2), "Human")] if not self.settings["Randomize Start"] else [Snake((255, 255, 255), spawnPoint, "Human")]
        if self.settings["Enemy Snakes"]:
            if self.settings["Randomize Start"]:
                index = self.possibleSpawns.index(spawnPoint)
                if index < 4:
                    subarray = self.possibleSpawns[:4:]
                    del subarray[subarray.index(self.possibleSpawns[index])]
                    index = subarray.index(random.choice(subarray))
                    self.snakes.append(Snake((255, 0, 0), subarray[index], "Standard AI"))
                    del subarray[index]
                    index = subarray.index(random.choice(subarray))
                    self.snakes.append(Snake((0, 255, 0), subarray[index], "Standard AI"))
                    del subarray[index]
                    self.snakes.append(Snake((255, 255, 0), subarray[0], "Standard AI"))
                else:
                    subarray = self.possibleSpawns[4::]
                    del subarray[subarray.index(self.possibleSpawns[index])]
                    index = subarray.index(random.choice(subarray))
                    self.snakes.append(Snake((255, 0, 0), subarray[index], "Standard AI"))
                    del subarray[index]
                    index = subarray.index(random.choice(subarray))
                    self.snakes.append(Snake((0, 255, 0), subarray[index], "Standard AI"))
                    del subarray[index]
                    self.snakes.append(Snake((255, 255, 0), subarray[0], "Standard AI"))
            else:
                self.snakes.append(Snake((255, 0, 0), (2, 10), "Standard AI"))
                self.snakes.append(Snake((0, 255, 0), (10, 10), "Standard AI"))
                self.snakes.append(Snake((255, 255, 0), (10, 2), "Standard AI"))
        self.gameEnded = False
        self.deadSnakes = 0
        self.turn = 0
        self.FoodTurnSpawn = 0
        self.gameState = self.create2DGameState()
        self.winner = None
        self.hasCreatedGIFForThisGame = False
        self.font = pygame.font.SysFont("Arial", 40)
        if self.settings["Add Food"]:
            self.generateFoodPosition()

    def create2DGameState(self):
        array = [[-1 for i in range(self.boardHeight - 1)] for j in range(self.boardWidth - 1)]
        for snake in self.snakes:
            array[snake.snakeBody[0][0] - 1][snake.snakeBody[0][1] - 1] = 2
        return array

    def handleEvents(self, window: pygame.Surface, Testing, neuralNetworks: List[neat.nn.FeedForwardNetwork], neuralNetworksInputs: List[List[Callable]]):
        from App import MouseButtons
        from Button import State

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                for file in glob.glob("Output/Games/*.png"):
                    os.remove(file)
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and not self.gameEnded:
                if event.key == pygame.K_w and Testing.replaceWithHuman:
                    self.ai(self.snakes[0], 0)
                if event.key == pygame.K_d and Testing.replaceWithHuman:
                    self.ai(self.snakes[0], 1)
                if event.key == pygame.K_s and Testing.replaceWithHuman:
                    self.ai(self.snakes[0], 2)
                if event.key == pygame.K_a and Testing.replaceWithHuman:
                    self.ai(self.snakes[0], 3)
                if event.key == pygame.K_w or\
                   event.key == pygame.K_d or\
                   event.key == pygame.K_a or\
                   event.key == pygame.K_s:
                    for index, snake in enumerate(self.snakes):
                        if snake.dead or (index == 0 and Testing.replaceWithHuman):
                            continue
                        if index - int(Testing.replaceWithHuman) < len(neuralNetworks):
                            output = neuralNetworks[index - int(Testing.replaceWithHuman)].activate(self.getNeuralNetworkValues(snake, neuralNetworksInputs[index - int(Testing.replaceWithHuman)]))
                            decision = output.index(max(output))
                            snake.name = neuralNetworks[index - int(Testing.replaceWithHuman)].snakeName
                            self.ai(snake, decision)
                            continue
                        self.ai(snake, snake.getMove(self))
                        snake.name = "Standard AI"
                    self.update()
                    rect = pygame.Rect(55, 55, 605, 605)
                    sub = window.subsurface(rect)
                    self.currentGifIndex = 0
                    for index, gif in enumerate(glob.glob("Output/Games/*.gif")):
                        self.currentGifIndex = index + 1
                    self.currentGifIndex += 1
                    appendix = ""
                    if self.turn < 10:
                        appendix = "000"
                    if self.turn > 9 and self.turn < 100:
                        appendix = "00"
                    if self.turn > 99 and self.turn < 1000:
                        appendix = "0"
                    if not os.path.isdir("Output/Games/"):
                        os.mkdir("Output/Games/")
                    pygame.image.save(sub, "Output/Games/game" + str(self.currentGifIndex) + appendix + str(self.turn) + ".png")

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == MouseButtons.LEFTMOUSEBUTTON.value: 
                    if Testing.buttons[0].state is State.HOVER:
                        Testing.buttons[0].onclick()
                        self.gameEnded = True
                        Testing.returned = True
                    for frame in glob.glob("Output/Games/game*.png"):
                        os.remove(frame)
                    if Testing.buttons[1].state is State.HOVER:
                        Testing.buttons[1].onclick()

        # -- Creating GIF of Game --

        if self.gameEnded and not self.hasCreatedGIFForThisGame and not Testing.returned:
            self.hasCreatedGIFForThisGame = True
            frames = [Image.open(image) for image in glob.glob("Output/Games/game" + str(self.currentGifIndex) + "*.png")]
            gif = frames[0]
            gif.save("Output/Games/game" + str(self.currentGifIndex) + ".gif", format = "GIF", append_images = frames,
                      save_all=True, duration = 200, loop = 0)
            for frame in glob.glob("Output/Games/game" + str(self.currentGifIndex) + "*.png"):
                os.remove(frame)
 
    def update(self):

        self.turn += 1

        # -- Death Staus Checking --

        snakesHeadPositions = []
        for index, snake in enumerate(self.snakes):
            snake.hasDeleted = False
            snakeHead = [snake.position[0], snake.position[1]]   
            if (not snake.dead) and (snakeHead[0] <= 0 or snakeHead[0] >= self.boardWidth or\
               snakeHead[1] <= 0 or snakeHead[1] >= self.boardHeight or\
               self.gameState[snakeHead[1] - 1][snakeHead[0] - 1] == 1 or\
               self.gameState[snakeHead[1] - 1][snakeHead[0] - 1] == 2 or\
               snake.health == 0):
                if snake.health == 0:
                    snake.deathReason = "Ran out of health on Turn " + str(self.turn)
                if snakeHead[0] <= 0 or snakeHead[0] >= self.boardWidth or\
                   snakeHead[1] <= 0 or snakeHead[1] >= self.boardHeight:
                    snake.deathReason = "Moved out of bounds on Turn " + str(self.turn)
                if snakeHead[0] > 0 and snakeHead[0] < self.boardWidth and\
                   snakeHead[1] > 0 and snakeHead[1] < self.boardHeight:
                    if self.gameState[snakeHead[1] - 1][snakeHead[0] - 1] == 1:
                        for snakeBody in snake.snakeBody:
                            if snakeBody[0] == snakeHead[0] and snakeBody[1] == snakeHead[1]:
                                snake.deathReason = "Collided with itself on Turn " + str(self.turn)
                                break
                        if snake.deathReason is None:
                            for snake2 in self.snakes:
                                for snakeBody in snake2.snakeBody:
                                    if snakeBody[0] == snakeHead[0] and snakeBody[1] == snakeHead[1]:
                                        snake.deathReason = "Collided with " + snake2.name + "\n on Turn " + str(self.turn)
                                    break
                snake.dead = True
                snake.dimColor()
                if snakeHead[0] - snake.snakeBody[-1][0] == 1:
                    if snake.snakeBody[-1][2] == 'Down':
                        snake.headTexture = pygame.transform.flip(snake.headTexture, False, True)
                        snake.headTexture = pygame.transform.rotate(snake.headTexture, 270)
                        snake.headTexture = pygame.transform.scale(snake.headTexture, (50, 55))
                    if snake.snakeBody[-1][2] == 'Up':
                        snake.headTexture = pygame.transform.rotate(snake.headTexture, 270)
                        snake.headTexture = pygame.transform.scale(snake.headTexture, (50, 55))
                if snakeHead[0] - snake.snakeBody[-1][0] == -1:
                    if snake.snakeBody[-1][2] == 'Down':
                        snake.headTexture = pygame.transform.flip(snake.headTexture, False, True)
                        snake.headTexture = pygame.transform.rotate(snake.headTexture, 270)
                        snake.headTexture = pygame.transform.scale(snake.headTexture, (50, 55))
                        snake.headTexture = pygame.transform.flip(snake.headTexture, True, False)
                    if snake.snakeBody[-1][2] == 'Up':
                        snake.headTexture = pygame.transform.rotate(snake.headTexture, 270)
                        snake.headTexture = pygame.transform.scale(snake.headTexture, (50, 55))
                        snake.headTexture = pygame.transform.flip(snake.headTexture, True, False)
                if snakeHead[1] - snake.snakeBody[-1][1] == 1:
                    if snake.snakeBody[-1][2] == 'Left':
                        snake.headTexture = pygame.transform.flip(snake.headTexture, True, False)
                        snake.headTexture = pygame.transform.scale(snake.headTexture, (50, 55))
                        snake.headTexture = pygame.transform.rotate(snake.headTexture, 90)
                        snake.headTexture = pygame.transform.flip(snake.headTexture, False, True)
                    if snake.snakeBody[-1][2] == 'Right':
                        snake.headTexture = pygame.transform.scale(snake.headTexture, (50, 55))
                        snake.headTexture = pygame.transform.rotate(snake.headTexture, 90)
                        snake.headTexture = pygame.transform.flip(snake.headTexture, False, True)
                if snakeHead[1] - snake.snakeBody[-1][1] == -1: 
                    if snake.snakeBody[-1][2] == 'Left':
                        snake.headTexture = pygame.transform.flip(snake.headTexture, True, False)
                        snake.headTexture = pygame.transform.scale(snake.headTexture, (50, 55))
                        snake.headTexture = pygame.transform.rotate(snake.headTexture, 90)
                    if snake.snakeBody[-1][2] == 'Right':
                        snake.headTexture = pygame.transform.scale(snake.headTexture, (50, 55))
                        snake.headTexture = pygame.transform.rotate(snake.headTexture, 90)
                for bodyPart in snake.snakeBody:
                    self.gameState[bodyPart[1] - 1][bodyPart[0] - 1] = -1
            snakesHeadPositions.append(snakeHead)
        for index, head in enumerate(snakesHeadPositions):
            for index2, head2 in enumerate(snakesHeadPositions):
                if (index2 == index) or self.snakes[index].dead or self.snakes[index2].dead:
                    continue
                if head[1] == head2[1] and head[0] == head2[0]:
                    if self.snakes[index].length == self.snakes[index2].length:
                        self.snakes[index].deathReason = "Died due to head-to-head tie on Turn " + str(self.turn)
                        self.snakes[index2].deathReason = "Died due to head-to-head tie on Turn " + str(self.turn)
                        self.snakes[index].dead = True
                        self.snakes[index2].dead = True
                        self.snakes[index].dimColor()
                        self.snakes[index2].dimColor()
                        for bodyPart in self.snakes[index].snakeBody:
                            self.gameState[bodyPart[1] - 1][bodyPart[0] - 1] = -1
                        for bodyPart in self.snakes[index2].snakeBody:
                            self.gameState[bodyPart[1] - 1][bodyPart[0] - 1] = -1
                        snakeHead = [self.snakes[index].position[0], self.snakes[index].position[1]]
                        if snakeHead[0] - self.snakes[index].snakeBody[-1][0] == 1:
                            snakeHead.append("Right")
                        if snakeHead[0] - self.snakes[index].snakeBody[-1][0] == -1:
                            snakeHead.append("Left")
                        if snakeHead[1] - self.snakes[index].snakeBody[-1][1] == 1:
                            snakeHead.append("Down")
                        if snakeHead[1] - self.snakes[index].snakeBody[-1][1] == -1:
                            snakeHead.append("Up")
                        self.snakes[index].snakeBody.append(snakeHead)
                        if len(self.snakes[index].snakeBody) > self.snakes[index].length:
                            self.snakes[index].hasDeleted = True
                            self.gameState[self.snakes[index].snakeBody[0][1] - 1][self.snakes[index].snakeBody[0][0] - 1] = -1
                            del self.snakes[index].snakeBody[0]
                        snakeHead = [self.snakes[index2].position[0], self.snakes[index2].position[1]]
                        if snakeHead[0] - self.snakes[index2].snakeBody[-1][0] == 1:
                            snakeHead.append("Right")
                        if snakeHead[0] - self.snakes[index2].snakeBody[-1][0] == -1:
                            snakeHead.append("Left")
                        if snakeHead[1] - self.snakes[index2].snakeBody[-1][1] == 1:
                            snakeHead.append("Down")
                        if snakeHead[1] - self.snakes[index2].snakeBody[-1][1] == -1:
                            snakeHead.append("Up")
                        self.snakes[index2].snakeBody.append(snakeHead)
                        if len(self.snakes[index2].snakeBody) > self.snakes[index2].length:
                            self.snakes[index2].hasDeleted = True
                            self.gameState[self.snakes[index2].snakeBody[0][1] - 1][self.snakes[index2].snakeBody[0][0] - 1] = -1
                            del self.snakes[index2].snakeBody[0]
                        continue
                    if self.snakes[index].length > self.snakes[index2].length:
                        self.snakes[index2].deathReason = "Died due to head-to-head with\n" + self.snakes[index].name + " on Turn " + str(self.turn)
                        self.snakes[index2].dead = True
                        self.snakes[index2].dimColor()
                        for bodyPart in self.snakes[index2].snakeBody:
                            self.gameState[bodyPart[1] - 1][bodyPart[0] - 1] = -1
                        continue
                    self.snakes[index].deathReason = "Died due to head-to-head with\n" + self.snakes[index2].name + " on Turn " + str(self.turn)
                    self.snakes[index].dead = True
                    self.snakes[index].dimColor()
                    for bodyPart in self.snakes[index].snakeBody:
                        self.gameState[bodyPart[1] - 1][bodyPart[0] - 1] = -1

        # -- Game Ending Conditions --

        for snake in self.snakes:
            if snake.dead:
                self.deadSnakes += 1
            if snake.length == self.boardHeight * self.boardWidth:
                self.gameEnded = True
                self.winner = snake
        if self.deadSnakes == len(self.snakes):
            self.gameEnded = True
        if self.deadSnakes == len(self.snakes) - 1 and self.settings['Enemy Snakes']:
            self.gameEnded = True
            for snake in self.snakes:
                if snake.dead:
                    continue
                self.winner = snake
        self.deadSnakes = 0
            
        # -- Collecting Food --

        if self.settings["Add Food"]:
            for index, snake in enumerate(self.snakes):
                if snake.dead:
                    continue
                snakeHead = [snake.position[0], snake.position[1]]
                if snakeHead[0] == self.foodPositionX and snakeHead[1] == self.foodPositionY:
                    snake.health = 100
                    snake.length += 1
                    self.generateFoodPosition(self.foodPositionY, self.foodPositionX)
                    self.FoodTurnSpawn = self.turn

        # -- Update Snake Position and Game State --

        for snake in self.snakes:
            if snake.dead:
                continue
            snakeHead = [snake.position[0], snake.position[1]]

            if snakeHead[0] - snake.snakeBody[-1][0] == 1:
                snakeHead.append('Right')
                if snake.snakeBody[0][2] == None:
                    snake.snakeBody[0][2] = 'Right'
                    snake.headTexture = pygame.transform.scale(snake.headTexture, (55, 50))
            if snakeHead[0] - snake.snakeBody[-1][0] == -1:
                snakeHead.append('Left')
                if snake.snakeBody[0][2] == None:
                    snake.snakeBody[0][2] = 'Left'
                    snake.headTexture = pygame.transform.scale(snake.headTexture, (55, 50))
                    snake.tailTexture = pygame.transform.flip(snake.tailTexture, True, False)
                    snake.headTexture = pygame.transform.flip(snake.headTexture, True, False)
            if snakeHead[1] - snake.snakeBody[-1][1] == 1:
                snakeHead.append('Down')
                if snake.snakeBody[0][2] == None:
                    snake.snakeBody[0][2] = 'Down'
                    snake.headTexture = pygame.transform.scale(snake.headTexture, (55, 50))
                    snake.tailTexture = pygame.transform.rotate(snake.tailTexture, 90)
                    snake.tailTexture = pygame.transform.flip(snake.tailTexture, False, True)
                    snake.headTexture = pygame.transform.rotate(snake.headTexture, 90)
                    snake.headTexture = pygame.transform.flip(snake.headTexture, False, True)
            if snakeHead[1] - snake.snakeBody[-1][1] == -1:
                snakeHead.append('Up')
                if snake.snakeBody[0][2] == None:
                    snake.snakeBody[0][2] = 'Up'
                    snake.headTexture = pygame.transform.scale(snake.headTexture, (55, 50))
                    snake.tailTexture = pygame.transform.rotate(snake.tailTexture, 90)
                    snake.headTexture = pygame.transform.rotate(snake.headTexture, 90)

            snake.snakeBody.append(snakeHead)

            if len(snake.snakeBody) > snake.length:
                snake.hasDeleted = True
                self.gameState[snake.snakeBody[0][1] - 1][snake.snakeBody[0][0] - 1] = -1
                del snake.snakeBody[0]
            for bodyPart in snake.snakeBody:
                self.gameState[bodyPart[1] - 1][bodyPart[0] - 1] = 1
            self.gameState[snakeHead[1] - 1][snakeHead[0] - 1] = 2

        for snake in self.snakes:
            for index, bodyPart in enumerate(snake.snakeBody):
                if bodyPart[2] == snake.snakeBody[index - 1][2] or snake.dead:
                    continue
                if bodyPart[2] == 'Down' and snake.snakeBody[index - 1][2] == 'Right' and index == len(snake.snakeBody) - 1:
                    snake.headTexture = pygame.transform.rotate(snake.headTexture, 90)
                    snake.headTexture = pygame.transform.flip(snake.headTexture, False, True)
                    continue
                if bodyPart[2] == 'Right' and snake.snakeBody[index - 1][2] == 'Down' and index == len(snake.snakeBody) - 1:
                    snake.headTexture = pygame.transform.flip(snake.headTexture, False, True)
                    snake.headTexture = pygame.transform.rotate(snake.headTexture, 270)
                    continue
                if bodyPart[2] == 'Left' and snake.snakeBody[index - 1][2] == 'Down' and index == len(snake.snakeBody) - 1:
                    snake.headTexture = pygame.transform.flip(snake.headTexture, False, True)
                    snake.headTexture = pygame.transform.rotate(snake.headTexture, 270)
                    snake.headTexture = pygame.transform.flip(snake.headTexture, True, False)
                    continue
                if bodyPart[2] == 'Up' and snake.snakeBody[index - 1][2] == 'Left' and index == len(snake.snakeBody) - 1:
                    snake.headTexture = pygame.transform.flip(snake.headTexture, True, False)
                    snake.headTexture = pygame.transform.rotate(snake.headTexture, 90)
                    continue
                if bodyPart[2] == 'Up' and snake.snakeBody[index - 1][2] == 'Right' and index == len(snake.snakeBody) - 1:
                    snake.headTexture = pygame.transform.rotate(snake.headTexture, 90)
                    continue
                if bodyPart[2] == 'Right' and snake.snakeBody[index - 1][2] == 'Up' and index == len(snake.snakeBody) - 1:
                    snake.headTexture = pygame.transform.rotate(snake.headTexture, 270)
                    continue
                if bodyPart[2] == 'Down' and snake.snakeBody[index - 1][2] == 'Left' and index == len(snake.snakeBody) - 1:
                    snake.headTexture = pygame.transform.flip(snake.headTexture, True, False)
                    snake.headTexture = pygame.transform.rotate(snake.headTexture, 90)
                    snake.headTexture = pygame.transform.flip(snake.headTexture, False, True)
                    continue
                if bodyPart[2] == 'Left' and snake.snakeBody[index - 1][2] == 'Up' and index == len(snake.snakeBody) - 1:
                    snake.headTexture = pygame.transform.rotate(snake.headTexture, 270)
                    snake.headTexture = pygame.transform.flip(snake.headTexture, True, False)
                    continue

            for index, bodyPart in enumerate(snake.snakeBody):
                if index == len(snake.snakeBody) - 1 or not snake.hasDeleted:
                    continue
                if bodyPart[2] == 'Down' and snake.snakeBody[index + 1][2] == 'Right' and index == 0:
                    snake.tailTexture = pygame.transform.flip(snake.tailTexture, False, True)
                    snake.tailTexture = pygame.transform.rotate(snake.tailTexture, 270)
                    continue
                if bodyPart[2] == 'Right' and snake.snakeBody[index + 1][2] == 'Down' and index == 0:
                    snake.tailTexture = pygame.transform.rotate(snake.tailTexture, 90)
                    snake.tailTexture = pygame.transform.flip(snake.tailTexture, False, True)
                    continue
                if bodyPart[2] == 'Left' and snake.snakeBody[index + 1][2] == 'Down' and index == 0:
                    snake.tailTexture = pygame.transform.flip(snake.tailTexture, True, False)
                    snake.tailTexture = pygame.transform.rotate(snake.tailTexture, 90)
                    snake.tailTexture = pygame.transform.flip(snake.tailTexture, False, True)
                    continue
                if bodyPart[2] == 'Up' and snake.snakeBody[index + 1][2] == 'Left' and index == 0:
                    snake.tailTexture = pygame.transform.rotate(snake.tailTexture, 270)
                    snake.tailTexture = pygame.transform.flip(snake.tailTexture, True, False)
                    continue
                if bodyPart[2] == 'Up' and snake.snakeBody[index + 1][2] == 'Right' and index == 0:
                    snake.tailTexture = pygame.transform.rotate(snake.tailTexture, 270)
                    continue
                if bodyPart[2] == 'Right' and snake.snakeBody[index + 1][2] == 'Up' and index == 0:
                    snake.tailTexture = pygame.transform.rotate(snake.tailTexture, 90)
                    continue
                if bodyPart[2] == 'Down' and snake.snakeBody[index + 1][2] == 'Left' and index == 0:
                    snake.tailTexture = pygame.transform.flip(snake.tailTexture, False, True)
                    snake.tailTexture = pygame.transform.rotate(snake.tailTexture, 270)
                    snake.tailTexture = pygame.transform.flip(snake.tailTexture, True, False)
                    continue
                if bodyPart[2] == 'Left' and snake.snakeBody[index + 1][2] == 'Up' and index == 0:
                    snake.tailTexture = pygame.transform.flip(snake.tailTexture, True, False)
                    snake.tailTexture = pygame.transform.rotate(snake.tailTexture, 90)
                    continue

    def render(self, window: pygame.Surface):
        for i in range(1, self.boardWidth):
            for j in range(1, self.boardHeight):
                pygame.draw.rect(window, (65, 65, 65), [55 * i, 55 * j, 50, 50])
        for snake in self.snakes:
            if snake.dead:
                snake.render(window)
        for snake in self.snakes:
            if snake.dead:
                continue
            snake.render(window)
        if self.settings["Add Food"]:
            pygame.draw.circle(window, (128, 0, 32), (25 + 55 * self.foodPositionX, 25 + 55 * self.foodPositionY), 20)

    def ai(self, snake: Snake, decision: int):
        if decision == 0:
            snake.updatePositionY(-1)
        if decision == 1:
            snake.updatePositionX(1)
        if decision == 2:
            snake.updatePositionY(1)
        if decision == 3:
            snake.updatePositionX(-1)
        snake.health -= 1

    def generateFoodPosition(self, positionY: int = None, positionX: int = None):
        (self.foodPositionY, self.foodPositionX) = random.randint(1, self.boardHeight - 1), random.randint(1, self.boardWidth - 1)
        while self.gameState[self.foodPositionY - 1][self.foodPositionX - 1] == 1 or\
              self.gameState[self.foodPositionY - 1][self.foodPositionX - 1] == 2 or\
              self.gameState[self.foodPositionY - 1][self.foodPositionX - 1] == -2:
            (self.foodPositionY, self.foodPositionX) = random.randint(1, self.boardHeight - 1), random.randint(1, self.boardWidth - 1)
        self.gameState[self.foodPositionY - 1][self.foodPositionX - 1] = -2
        if not positionY == None and not positionX == None:
            self.gameState[positionY - 1][positionX - 1] = -1

    def getNeuralNetworkValues(self, snake: Snake, functions: List[Callable]):
        values: List[float] = []
        for function in functions:
            if type(function(snake, self)) == type([]):
                array = function(snake, self)
                for x in range(self.boardWidth - 1):
                    for y in range(self.boardHeight - 1):
                        values.append(array[x][y])
                continue
            values.append(function(snake, self))
        return values