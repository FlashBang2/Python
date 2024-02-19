import pygame
import random

from typing import Tuple

class Snake:
    def __init__(self, color: Tuple[int, int, int], position: Tuple[int, int], name: str):
        self.position = position
        self.color = color
        self.headTexture = self.adjustTextureColor(pygame.image.load("Assets/HeadSnakeTexture.png"))
        self.tailTexture = self.adjustTextureColor(pygame.image.load("Assets/TailSnakeTexture.png"))
        self.snakeBody = [[self.position[0], self.position[1], None]]
        self.initialLength = 3
        self.length = self.initialLength
        self.health = 100
        self.dead = False
        self.deathReason = ""
        self.horizontalPosition = 55
        self.verticalPosition = 55
        self.hasDeleted = False
        self.name = name

    def render(self, gameWindow: pygame.Surface):
        for index, bodyPart in enumerate(self.snakeBody):
            if index == len(self.snakeBody) - 1:
                if bodyPart[2] == 'Right':
                    gameWindow.blit(self.headTexture, (self.horizontalPosition * bodyPart[0] - 5, self.verticalPosition * bodyPart[1]))
                if bodyPart[2] == 'Left':
                    gameWindow.blit(self.headTexture, (self.horizontalPosition * bodyPart[0], self.verticalPosition * bodyPart[1]))
                if bodyPart[2] == 'Up':
                    gameWindow.blit(self.headTexture, (self.horizontalPosition * bodyPart[0], self.verticalPosition * bodyPart[1]))
                if bodyPart[2] == 'Down':
                    gameWindow.blit(self.headTexture, (self.horizontalPosition * bodyPart[0], self.verticalPosition * bodyPart[1] - 5))
                if bodyPart[2] == None:
                    gameWindow.blit(self.headTexture, (self.horizontalPosition * bodyPart[0], self.verticalPosition * bodyPart[1]))
                continue
            if index == 0 and len(self.snakeBody) > 1:
                gameWindow.blit(self.tailTexture, (self.horizontalPosition * bodyPart[0], self.verticalPosition * bodyPart[1]))
                continue
            if bodyPart[2] == "Right":
                pygame.draw.rect(gameWindow, self.color, [self.horizontalPosition * bodyPart[0] - 5, self.verticalPosition * bodyPart[1], 55, 50])
                continue
            if bodyPart[2] == "Left":
                pygame.draw.rect(gameWindow, self.color, [self.horizontalPosition * bodyPart[0], self.verticalPosition * bodyPart[1], 55, 50])
                continue
            if bodyPart[2] == "Up":
                pygame.draw.rect(gameWindow, self.color, [self.horizontalPosition * bodyPart[0], self.verticalPosition * bodyPart[1], 50, 55])
                continue
            if bodyPart[2] == "Down":
                pygame.draw.rect(gameWindow, self.color, [self.horizontalPosition * bodyPart[0], self.verticalPosition * bodyPart[1] - 5, 50, 55])
                continue
            
    def updatePositionX(self, value: int):
        self.position = list(self.position)
        self.position[0] += value
        self.position = tuple(self.position)
    
    def updatePositionY(self, value: int):
        self.position = list(self.position)
        self.position[1] += value
        self.position = tuple(self.position)

    def adjustTextureColor(self, surface: pygame.Surface):
        w, h = surface.get_size()
        for x in range(w):
            for y in range(h):
                a = surface.get_at((x, y))[3]
                color = list(self.color)
                color.append(a)
                surface.set_at((x, y), color)
        return surface
    
    def dimColor(self):
        color = []
        color.append(list(self.color)[0] * 0.2)
        color.append(list(self.color)[1] * 0.2)
        color.append(list(self.color)[2] * 0.2)
        self.color = tuple(color)
        self.headTexture = self.adjustTextureColor(self.headTexture)
        self.tailTexture = self.adjustTextureColor(self.tailTexture)

    def getMove(self, game):
        from Game import Game

        self.game: Game = game 

        safeMoves = {
            'Up': True,
            'Right': True,
            'Down': True,
            'Left': True
        }

        if self.position[1] <= 0:
            safeMoves['Up'] = False
        if self.position[1] >= self.game.boardHeight:
            safeMoves['Down'] = False
        if self.position[0] <= 0:
            safeMoves['Left'] = False
        if self.position[0] >= self.game.boardWidth:
            safeMoves['Righ'] = False

        if self.position[1] - 2 < 0:
            safeMoves['Up'] = False
        if self.position[1] > self.game.boardHeight - 2:
            safeMoves['Down'] = False
        if self.position[0] - 2 < 0:
            safeMoves['Left'] = False
        if self.position[0] > self.game.boardWidth - 2:
            safeMoves['Right'] = False

        if safeMoves['Up']:
            if self.game.gameState[self.position[1] - 2][self.position[0] - 1] == 1 or\
               self.game.gameState[self.position[1] - 2][self.position[0] - 1] == 2:
                safeMoves['Up'] = False
        if safeMoves['Down']:
            if self.game.gameState[self.position[1]][self.position[0] - 1] == 1 or\
               self.game.gameState[self.position[1]][self.position[0] - 1] == 2:
                safeMoves['Down'] = False
        if safeMoves['Left']:
            if self.game.gameState[self.position[1] - 1][self.position[0] - 2] == 1 or\
               self.game.gameState[self.position[1] - 1][self.position[0] - 2] == 2:
                safeMoves['Left'] = False
        if safeMoves['Right']:
            if self.game.gameState[self.position[1] - 1][self.position[0]] == 1 or\
               self.game.gameState[self.position[1] - 1][self.position[0]] == 2:
                safeMoves['Right'] = False

        countNotAvailableMoves = 0
        for value in safeMoves.values():
            if not value:
                countNotAvailableMoves += 1
        if countNotAvailableMoves == 4:
            return random.choice([0, 1, 2, 3])
        
        move = random.choice(list(safeMoves))
        while not safeMoves[move]:
            move = random.choice(list(safeMoves))

        if move == 'Up':
            return 0
        if move == 'Right':
            return 1
        if move == 'Down':
            return 2
        if move == 'Left':
            return 3