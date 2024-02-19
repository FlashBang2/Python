import Game

from Snake import Snake

class NEATInputs:
    def __init__(self):
        self.inputs = { 
            "Distance To Obstacle Up" : self.getDistanceToObstacleUp,
            "Distance To Obstacle UpLeft" : self.getDistanceToObstacleUpLeft,
            "Distance To Obstacle UpRight" : self.getDistanceToObstacleUpRight,
            "Distance To Obstacle Down" : self.getDistanceToObstacleDown,
            "Distance To Obstacle DownLeft" : self.getDistanceToObstacleDownLeft,
            "Distance To Obstacle DownRight" : self.getDistanceToObstacleDownRight,
            "Distance To Obstacle Right" : self.getDistanceToObstacleRight,
            "Distance To Obstacle Left" : self.getDistanceToObstacleLeft,
            "Above Head Field Value" : self.getAboveHeadFieldValue,
            "Below Head Field Value" : self.getBelowHeadFieldValue,
            "Right Side Head Field Value" : self.getRightSideHeadFieldValue,
            "Left Side Head Field Value" : self.getLeftSideHeadFieldValue,
            "Head-Tail Distance Horizontal" : self.getHead_TailDistanceHorizontal,
            "Head-Tail Distance Vertical" : self.getHead_TailDistanceVertical,
            "Distance From Head to Top Border" : self.getDistanceFromHeadtoTopBorder,
            "Distance From Head to Down Border" : self.getDistanceFromHeadtoDownBorder,
            "Distance From Head to Right Border" : self.getDistanceFromHeadtoRightBorder,
            "Distance From Head to Left Border" : self.getDistanceFromHeadtoLeftBorder,
            "Health" : self.getHealth,
            "Length" : self.getLength,
            "Vertical Distance To Food" : self.getVerticalDistanceToFood,
            "Horizontal Distance To Food" : self.getHorizontalDistanceToFood,
            "Distance To Closest Food Up": self.getDistanceToClosestFoodUp,
            "Distance To Closest Food Down": self.getDistanceToClosestFoodDown,
            "Distance To Closest Food Right": self.getDistanceToClosestFoodRight,
            "Distance To Closest Food Left": self.getDistanceToClosestFoodLeft,
            "Vertical Distnace to Enemy Snake1" : self.getVerticalDistnacetoEnemySnake1,
            "Horizontal Distance to Enemy Snake1" : self.getHorizontalDistancetoEnemySnake1,
            "Vertical Distnace to Enemy Snake2" : self.getVerticalDistnacetoEnemySnake2,
            "Horizontal Distance to Enemy Snake2" : self.getHorizontalDistancetoEnemySnake2,
            "Vertical Distance to Enemy Snake3" : self.getVerticalDistancetoEnemySnake3,
            "Horizontal Distance to Enemy Snake3" : self.getHorizontalDistancetoEnemySnake3,
            "Enemy Snake1 Length" : self.getEnemySnake1Length,
            "Enemy Snake2 Length" : self.getEnemySnake2Length,
            "Enemy Snake3 Length" : self.getEnemySnake3Length,
            "Enemy Snake1 Health" : self.getEnemySnake1Health,
            "Enemy Snake2 Health" : self.getEnemySnake2Health,
            "Enemy Snake3 Health" : self.getEnemySnake3Health,
            "Obstacles Board": self.getObstaclesBoard,
            "Head Position Board": self.getHeadPositionBoard,
            "Food Position Board": self.getFoodPositionBoard,
            "Enemy Head Position Board": self.getEnemyHeadPositionBoard,
        }
    
    def getVerticalDistanceToFood(self, snake: Snake, game: Game.Game):
        distance = game.foodPositionX - snake.position[0]
        return 0 if distance == 0 else -1 if distance < 0 else 1
    
    def getHorizontalDistanceToFood(self, snake: Snake, game: Game.Game):
        distance = game.foodPositionY - snake.position[1]
        return 0 if distance == 0 else -1 if distance < 0 else 1
    
    def getDistanceToObstacleUp(self, snake: Snake, game: Game.Game):
        distance = 0
        if snake.position[1] - 2 < 0:
            return 1
        while game.gameState[snake.position[1] - (2 + distance)][snake.position[0] - 1] == -1 or\
              game.gameState[snake.position[1] - (2 + distance)][snake.position[0] - 1] == -2:
                distance += 1
                if snake.position[1] - (2 + distance) < 0:
                    return 1 / (distance + 1)
        return 1
    
    def getDistanceToObstacleUpLeft(self, snake: Snake, game: Game.Game):
        distance = 0
        if snake.position[0] - 2  < 0 or snake.position[1] - 2 < 0:
            return 1
        while game.gameState[snake.position[1] - (2 + distance)][snake.position[0] - (2 + distance)] == -1 or\
              game.gameState[snake.position[1] - (2 + distance)][snake.position[0] - (2 + distance)] == -2:
                distance += 1
                if snake.position[1] - (2 + distance) < 0 or snake.position[0] - (2 + distance):
                    return 1 / (distance + 1)
        return 1
    
    def getDistanceToObstacleUpRight(self, snake: Snake, game: Game.Game):
        distance = 0
        if snake.position[0] > game.boardWidth - 2 or snake.position[1] - 2 < 0:
            return 1
        while game.gameState[snake.position[1] - (2 + distance)][snake.position[0] + distance] == -1 or\
              game.gameState[snake.position[1] - (2 + distance)][snake.position[0] + distance] == -2:
                distance += 1
                if snake.position[1] - (2 + distance) < 0 or snake.position[0] + distance > game.boardWidth - 2:
                    return 1 / (distance + 1)
        return 1
    
    def getDistanceToObstacleDown(self, snake: Snake, game: Game.Game):
        distance = 0
        if snake.position[1] > game.boardHeight - 2:
            return 1
        while game.gameState[snake.position[1] + distance][snake.position[0] - 1] == -1 or\
              game.gameState[snake.position[1] + distance][snake.position[0] - 1] == -2:
                distance += 1
                if snake.position[1] + distance > game.boardHeight - 2:
                    return 1 / (distance + 1)
        return 1
    
    def getDistanceToObstacleDownLeft(self, snake: Snake, game: Game.Game):
        distance = 0
        if snake.position[0] - 2 < 0 or snake.position[1] > game.boardHeight - 2:
            return 1
        while game.gameState[snake.position[1] + distance][snake.position[0] - (2 + distance)] == -1 or\
              game.gameState[snake.position[1] + distance][snake.position[0] - (2 + distance)] == -2:
                distance += 1
                if snake.position[1] + distance > game.boardHeight - 2 or snake.position[0] - (2 + distance):
                    return 1 / (distance + 1)
        return 1
    
    def getDistanceToObstacleDownRight(self, snake: Snake, game: Game.Game):
        distance = 0
        if snake.position[0] > game.boardWidth - 2 or snake.position[1] > game.boardHeight - 2:
            return 1
        while game.gameState[snake.position[1] + distance][snake.position[0] + distance] == -1 or\
              game.gameState[snake.position[1] + distance][snake.position[0] + distance] == -2:
                distance += 1
                if snake.position[1] + distance > game.boardHeight - 2 or snake.position[0] + distance > game.boardWidth - 2:
                    return 1 / (distance + 1)
        return 1

    def getDistanceToObstacleRight(self, snake: Snake, game: Game.Game):
        distance = 0
        if snake.position[0] > game.boardWidth - 2:
            return 1
        while game.gameState[snake.position[1] - 1][snake.position[0] + distance] == -1 or\
              game.gameState[snake.position[1] - 1][snake.position[0] + distance] == -2:
                distance += 1
                if snake.position[0] + distance > game.boardWidth - 2:
                    return 1 / (distance + 1)
        return 1

    def getDistanceToObstacleLeft(self, snake: Snake, game: Game.Game):
        distance = 0
        if snake.position[0] - 2 < 0:
            return 1
        while game.gameState[snake.position[1] - 1][snake.position[0] - (2 + distance)] == -1 or\
              game.gameState[snake.position[1] - 1][snake.position[0] - (2 + distance)] == -2:
                distance += 1
                if snake.position[0] - (2 + distance) < 0:
                    return 1 / (distance + 1)
        return 1

    def getDistanceToClosestFoodUp(self, snake: Snake, game: Game.Game):
        distance = 0
        if snake.position[1] - 2 < 0:
            return 0
        while not game.gameState[snake.position[1] - (2 + distance)][snake.position[0] - 1] == -2:
                distance += 1
                if snake.position[1] - (2 + distance) < 0:
                    return 1 / (distance + 1)
        return 1

    def getDistanceToClosestFoodDown(self, snake: Snake, game: Game.Game):
        distance = 0
        if snake.position[1] > game.boardHeight - 2:
            return 0
        while not game.gameState[snake.position[1] + distance][snake.position[0] - 1] == -2:
                distance += 1
                if snake.position[1] + distance > game.boardHeight - 2:
                    return 1 / (distance + 1)
        return 1
    
    def getDistanceToClosestFoodRight(self, snake: Snake, game: Game.Game):
        distance = 0
        if snake.position[0] > game.boardWidth - 2:
            return 0
        while not game.gameState[snake.position[1] - 1][snake.position[0] + distance] == -2:
                distance += 1
                if snake.position[0] + distance > game.boardWidth - 2:
                    return 1 / (distance + 1)
        return 1

    def getDistanceToClosestFoodLeft(self, snake: Snake, game: Game.Game):
        distance = 0
        if snake.position[0] - 2 < 0:
            return 0
        while not game.gameState[snake.position[1] - 1][snake.position[0] - (2 + distance)] == -2:
                distance += 1
                if snake.position[0] - (2 + distance) < 0:
                    return 1 / (distance + 1)
        return 1

    def getAboveHeadFieldValue(self, snake: Snake, game: Game.Game):
        if snake.position[1] - 2 < 0:
            return 1
        return game.gameState[snake.position[1] - 2][snake.position[0] - 1]
    
    def getBelowHeadFieldValue(self, snake: Snake, game: Game.Game):
        if snake.position[1] > game.boardHeight - 2:
            return 1
        return game.gameState[snake.position[1]][snake.position[0] - 1]
    
    def getRightSideHeadFieldValue(self, snake: Snake, game: Game.Game):
        if snake.position[0] > game.boardWidth - 2:
            return 1
        return game.gameState[snake.position[1] - 1][snake.position[0]]
    
    def getLeftSideHeadFieldValue(self, snake: Snake, game: Game.Game):
        if snake.position[0] - 2 < 0:
            return 1
        return game.gameState[snake.position[1] - 1][snake.position[0] - 2]
    
    def getHead_TailDistanceHorizontal(self, snake: Snake, game: Game.Game):
        if snake.position[0] == snake.snakeBody[0][0]:
            return -1 if snake.position[1] > snake.snakeBody[0][1] else 1
        return 0 
    
    def getHead_TailDistanceVertical(self, snake: Snake, game: Game.Game):
        if snake.position[1] == snake.snakeBody[0][1]:
            return -1 if snake.position[0] > snake.snakeBody[0][0] else 1
        return 0

    def getDistanceFromHeadtoTopBorder(self, snake: Snake, game: Game.Game):
        return snake.position[1]
    
    def getDistanceFromHeadtoDownBorder(self, snake: Snake, game: Game.Game):
        return (game.boardHeight - 2) - (snake.position[1] - 1)
    
    def getDistanceFromHeadtoRightBorder(self, snake: Snake, game: Game.Game):
        return (game.boardWidth - 2) - (snake.position[0] - 1)
    
    def getDistanceFromHeadtoLeftBorder(self, snake: Snake, game: Game.Game):
        return snake.position[0]
    
    def getHealth(self, snake: Snake, game: Game.Game):
        return 0 if snake.health == 0 else 1 / snake.health
    
    def getLength(self, snake: Snake, game: Game.Game):
        return snake.length
    
    def getVerticalDistnacetoEnemySnake1(self, snake: Snake, game: Game.Game):
        snakeToCompare= None
        for aSnake in game.snakes:
            if snake.position[0] == aSnake.position[0] and snake.position[1] == aSnake.position[1]:
                continue
            snakeToCompare = aSnake
        if snakeToCompare is None:
            return 0
        distance = (snake.position[1] - 1) - (snakeToCompare.position[1] - 1)
        return 0 if distance == 0 else 1 / distance
    
    def getHorizontalDistancetoEnemySnake1(self, snake: Snake, game: Game.Game):
        snakeToCompare = None
        for aSnake in game.snakes:
            if snake.position[0] == aSnake.position[0] and snake.position[1] == aSnake.position[1]:
                continue
            snakeToCompare = aSnake
            break
        if snakeToCompare is None:
            return 0
        distance = (snake.position[0] - 1) - (snakeToCompare.position[0] - 1)
        return 0 if distance == 0 else 1 / distance
    
    def getVerticalDistnacetoEnemySnake2(self, snake: Snake, game: Game.Game):
        counter = 0
        snakeToCompare = None
        for aSnake in game.snakes:
            if snake.position[0] == aSnake.position[0] and snake.position[1] == aSnake.position[1]:
                continue
            if counter >= 1:
                snakeToCompare = aSnake
                break
            counter += 1
        if snakeToCompare is None:
            return 0 
        distance = (snake.position[1] - 1) - (snakeToCompare.position[1] - 1)
        return 0 if distance == 0 else 1 / distance
    
    def getHorizontalDistancetoEnemySnake2(self, snake: Snake, game: Game.Game):
        counter = 0
        snakeToCompare = None
        for aSnake in game.snakes:
            if snake.position[0] == aSnake.position[0] and snake.position[1] == aSnake.position[1]:
                continue
            if counter >= 1:
                snakeToCompare = aSnake
                break
            counter += 1
        if snakeToCompare is None:
            return 0 
        distance = (snake.position[0] - 1) - (snakeToCompare.position[0] - 1)
        return 0 if distance == 0 else 1 / distance
    
    def getVerticalDistancetoEnemySnake3(self, snake: Snake, game: Game.Game):
        counter = 0
        snakeToCompare = None
        for aSnake in game.snakes:
            if snake.position[0] == aSnake.position[0] and snake.position[1] == aSnake.position[1]:
                continue
            if counter >= 2:
                snakeToCompare = aSnake
                break
            counter += 1
        if snakeToCompare is None:
            return 0
        distance = (snake.position[1] - 1) - (snakeToCompare.position[1] - 1)
        return 0 if distance == 0 else 1 / distance
    
    def getHorizontalDistancetoEnemySnake3(self, snake: Snake, game: Game.Game):
        counter = 0
        snakeToCompare = None
        for aSnake in game.snakes:
            if snake.position[0] == aSnake.position[0] and snake.position[1] == aSnake.position[1]:
                continue
            if counter >= 2:
                snakeToCompare = aSnake
                break
            counter += 1
        if snakeToCompare is None:
            return 0
        distance = (snake.position[0] - 1) - (snakeToCompare.position[0] - 1)
        return 0 if distance == 0 else 1 / distance
    
    def getEnemySnake1Length(self, snake: Snake, game: Game.Game):
        snakeToCompare = None
        for aSnake in game.snakes:
            if snake.position[0] == aSnake.position[0] and snake.position[1] == aSnake.position[1]:
                continue
            snakeToCompare = aSnake
            break
        return 0 if snakeToCompare is None else snakeToCompare.length
    
    def getEnemySnake2Length(self, snake: Snake, game: Game.Game):
        counter = 0
        snakeToCompare = None
        for aSnake in game.snakes:
            if snake.position[0] == aSnake.position[0] and snake.position[1] == aSnake.position[1]:
                continue
            if counter >= 1:
                snakeToCompare = aSnake
                break
            counter += 1
        return 0 if snakeToCompare is None else snakeToCompare.length
    
    def getEnemySnake3Length(self, snake: Snake, game: Game.Game):
        counter = 0
        snakeToCompare = None
        for aSnake in game.snakes:
            if snake.position[0] == aSnake.position[0] and snake.position[1] == aSnake.position[1]:
                continue
            if counter >= 2:
                snakeToCompare = aSnake
                break
            counter += 1
        return 0 if snakeToCompare is None else snakeToCompare.length
    
    def getEnemySnake1Health(self, snake: Snake, game: Game.Game):
        snakeToCompare = None
        for aSnake in game.snakes:
            if snake.position[0] == aSnake.position[0] and snake.position[1] == aSnake.position[1]:
                continue
            snakeToCompare = aSnake
            break
        return 0 if snakeToCompare is None or snakeToCompare.health == 0 else 1 / snakeToCompare.health
    
    def getEnemySnake2Health(self, snake: Snake, game: Game.Game):
        counter = 0
        snakeToCompare = None
        for aSnake in game.snakes:
            if snake.position[0] == aSnake.position[0] and snake.position[1] == aSnake.position[1]:
                continue
            if counter >= 1:
                snakeToCompare = aSnake
                break
            counter += 1
        return 0 if snakeToCompare is None or snakeToCompare.health == 0 else 1 / snakeToCompare.health
    
    def getEnemySnake3Health(self, snake: Snake, game: Game.Game):
        counter = 0
        snakeToCompare = None
        for aSnake in game.snakes:
            if snake.position[0] == aSnake.position[0] and snake.position[1] == aSnake.position[1]:
                continue
            if counter >= 2:
                snakeToCompare = aSnake
                break
            counter += 1
        return 0 if snakeToCompare is None or snakeToCompare.health == 0 else 1 / snakeToCompare.health
    
    def getObstaclesBoard(self, _: Snake, game: Game.Game):
        array = [[0 for i in range(game.boardHeight - 1)] for j in range(game.boardWidth - 1)]
        for snake in game.snakes:
            for index, snakeBody in enumerate(snake.snakeBody):
                if index == len(snake.snakeBody) - 1:
                    continue
                array[snakeBody[0] - 1][snakeBody[1] - 1] = 1
        return array
            
    def getHeadPositionBoard(self, snake: Snake, game: Game.Game):
        array = [[0 for i in range(game.boardHeight - 1)] for j in range(game.boardWidth - 1)]
        array[snake.position[0] - 1][snake.position[1] - 1] = 1
        return array

    def getFoodPositionBoard(self, snake: Snake, game: Game.Game):
        array = [[0 for i in range(game.boardHeight - 1)] for j in range(game.boardWidth - 1)]
        array[game.foodPositionX - 1][game.foodPositionY - 1] = 1
        return array

    def getEnemyHeadPositionBoard(self, snake: Snake, game: Game.Game):
        array = [[0 for i in range(game.boardHeight - 1)] for j in range(game.boardWidth - 1)]
        for aSnake in game.snakes:
            if snake.position[0] == aSnake.position[0] and snake.position[1] == aSnake.position[1]:
                continue
            array[aSnake.snakeBody[-1][0] - 1][aSnake.snakeBody[-1][1] - 1] = 1
        return array