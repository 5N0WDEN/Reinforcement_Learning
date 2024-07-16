import pygame
import time
import random
import os
import numpy as np

'''
Encountering a initial case when sanke can go to four different directions but after the first move it can only move in the three directions
For solving this case, I am spawning the snake 2 blocks in inside with random direction so that it will not collide but will get a direction
'''

class Snake:
    def __init__(self, screen, gridSize):
        self.screen, self.length = screen, gridSize
        self.speed = gridSize # Change this value to 1 for better transition of the snake on the grid
        self.numberOfBlockes = (700 - self.length * 4) // self.length
        self.xChange, self.yChange, self.direction = 1, 0, "Right"
        self.snakeBodyPart = [[self.snakeSpawn(), self.snakeSpawn(), self.xChange, self.yChange, self.direction]]
        self.gameOver = False
        self.font = pygame.font.Font('freesansbold.ttf', 20)
        self.path = os.path.abspath(__file__)[:-12]
        self.foodApple = pygame.image.load(self.path + "apple.png")
        self.xpos, self.ypos = 0, 0
        self.foodPosition()
        self.frame_iteration = 0
        self.reward = 0
        self.clock = pygame.time.Clock()

    def randomSpawn(self):
        return (random.randint(self.length * 2, self.length * (self.numberOfBlockes + 1)) // self.length) * self.length
    
    def snakeSpawn(self):
        return (random.randint(self.length * 4, self.length * (self.numberOfBlockes - 1)) // self.length) * self.length
    
    def drawSnake(self):
        for i, body in enumerate(self.snakeBodyPart):
            #print(i, self.snakeBodyPart)
            if i == 0:
                color = (78,124,246)
                if body[2] == 1:
                    snakeEye1 = (body[0] + self.length - (self.length / 5), body[1] + (self.length / 3))
                    snakeEye2 = (body[0] + self.length - (self.length / 5), body[1] + (self.length / 3) * 2)
                elif body[2] == -1:
                    snakeEye1 = (body[0] + (self.length / 5), body[1] + (self.length / 3))
                    snakeEye2 = (body[0] + (self.length / 5), body[1] + (self.length / 3) * 2)
                elif body[3] == 1:
                    snakeEye1 = (body[0] + (self.length / 3), body[1] + self.length - (self.length / 5))
                    snakeEye2 = (body[0] + (self.length / 3) * 2, body[1] + self.length - (self.length / 5))
                elif body[3] == -1:
                    snakeEye1 = (body[0] + (self.length / 3), body[1] + (self.length / 5))
                    snakeEye2 = (body[0] + (self.length / 3) * 2, body[1] + (self.length / 5))
                elif body[2] == 0 and body[3] == 0:
                    snakeEye1 = (-1, -1)
                    snakeEye2 = (-1, -1) 
                pygame.draw.rect(self.screen, color, (body[0], body[1], self.length, self.length))
                pygame.draw.circle(self.screen, (255, 100, 100), snakeEye1, self.length / 15)
                pygame.draw.circle(self.screen, (255, 100, 100), snakeEye2, self.length / 15)
            else:
                color = (66,111,227)
                pygame.draw.rect(self.screen, color, [body[0], body[1], self.length, self.length])

    def backgroundDraw(self):
        self.screen.fill((87,138,52))
        rect = [self.length * 2, self.length * 2, self.length * self.numberOfBlockes, self.length * self.numberOfBlockes]
        pygame.draw.rect(self.screen, ((170,215,81)), rect)
        dimension = [self.length * 2, self.length * 2, self.length, self.length]
        color, i = (162,209,73), 2
        score = self.font.render(f'SCORE: {len(self.snakeBodyPart) - 1}', True, (255, 255, 255))
        self.screen.blit(score, (550, 50))
        while i < (self.numberOfBlockes + 2):
            j = 2
            while j < (self.numberOfBlockes + 2):
                if i % 2 == 0 and j % 2 == 0:
                    dimension[0] = self.length * i
                    dimension[1] = self.length * j
                    pygame.draw.rect(self.screen, color, dimension)
                if i % 2 != 0 and j % 2 != 0:
                    dimension[0] = self.length * i
                    dimension[1] = self.length * j
                    pygame.draw.rect(self.screen, color, dimension)
                j += 1
            i += 1
        # Drawing food on the background.
        self.screen.blit(self.foodApple, (self.food[0][0], self.food[0][1]))

    def update(self):
        #Checks whether the snake is inside or outside
        if self.snakeBodyPart[0][0] > self.length * (self.numberOfBlockes + 1) or self.snakeBodyPart[0][0] < self.length * 2 or self.snakeBodyPart[0][1] > self.length * (self.numberOfBlockes + 1) or self.snakeBodyPart[0][1] < self.length * 2:
            self.gameOver = True
        # Starting from last each element gets value of previous element
        if not self.gameOver:
            i = len(self.snakeBodyPart) - 1
            while i >= 0:
                nextBodyPart = list(self.snakeBodyPart.pop(i))
                if i == 0:
                    nextBodyPart[2], nextBodyPart[3], nextBodyPart[4] = self.xChange, self.yChange, self.direction
                else:
                    nextBodyPart[2], nextBodyPart[3], nextBodyPart[4] = self.snakeBodyPart[i - 1][2], self.snakeBodyPart[i - 1][3], self.snakeBodyPart[i - 1][4]
                nextBodyPart[0] += nextBodyPart[2] * self.speed
                nextBodyPart[1] += nextBodyPart[3] * self.speed
                self.snakeBodyPart.insert(i, tuple(nextBodyPart))
                i -= 1

    def controls(self):
        if self.snakeBodyPart[0][0] % self.length == 0 and self.snakeBodyPart[0][1] % self.length == 0:
            if self.yChange != 1 and self.direction == "Up":
                self.xChange, self.yChange = 0, -1
            if self.yChange != -1 and self.direction == "Down":
                self.xChange, self.yChange = 0, 1
            if self.xChange != 1 and self.direction == "Left":
                self.xChange, self.yChange = -1, 0
            if self.xChange != -1 and self.direction == "Right":
                self.xChange, self.yChange = 1, 0
            self.frame_iteration += 1

    def reset(self):
        if self.gameOver:
            self.__init__(self.screen, self.length)
            self.gameOver = False
    
    def foodPosition(self):
        newPosition = [(self.randomSpawn(), self.randomSpawn())]
        while any((newPosition[0][0] == body[0] and newPosition[0][1] == body[1]) for body in self.snakeBodyPart):
           newPosition = [(self.randomSpawn(), self.randomSpawn())]
        self.food = newPosition
    
    def checkGameStatus(self): # Checks wheather player is playing or he has completed the game
        if len(self.snakeBodyPart) + 1 == self.numberOfBlockes * self.numberOfBlockes:
            print("You have completed the game.")
            self.gameOver = True
            #self.reward += 10

    def checkCollision(self):
        if self.snakeBodyPart[0][0] == self.food[0][0] and self.snakeBodyPart[0][1] == self.food[0][1]:
            self.reward += 10
            self.checkGameStatus()
            if not self.gameOver:
                self.foodPosition()
            #print(self.snakeBodyPart)
            if self.snakeBodyPart[-1][2] == -1 or self.snakeBodyPart[-1][2] == 1:
                new = [self.snakeBodyPart[-1][0] - (self.length * self.snakeBodyPart[-1][2]), self.snakeBodyPart[-1][1], self.snakeBodyPart[-1][2], 0, self.snakeBodyPart[-1][4]]
            elif self.snakeBodyPart[-1][3] == -1 or self.snakeBodyPart[-1][3] == 1:
                new = [self.snakeBodyPart[-1][0], self.snakeBodyPart[-1][1] - (self.length * self.snakeBodyPart[-1][3]), 0, self.snakeBodyPart[-1][3], self.snakeBodyPart[-1][4]]
            self.snakeBodyPart.append(tuple(new))
        if len(self.snakeBodyPart) > 0 and self.gameOver != True:
            collisionWithBody = any((body[0] == self.snakeBodyPart[0][0] and body[1] == self.snakeBodyPart[0][1]) for body in self.snakeBodyPart[1::])
            if collisionWithBody:
                self.gameOver = True
                self.reward -= 10
        if self.frame_iteration >= 100 * len(self.snakeBodyPart):
            self.gameOver = True
            self.reward -= 10


    #taging them on the basis of the turn like left turn or right turn or going down
    #iterating in self.snakeBodyPart when len of that list is greater than the 2
    #   (1, 0), (-1, 0), (0, 1), (0, -1)
    # Reinforcement Learning
    # Action, Reward +10, 0, -10, check the condition if nothing happens for a long time 
    # self.frame_iteration > 100 * len(self.snakeBodyPart)

    def step(self, action): # action a list [forward, left turn, right turn] respective values can only be 1 or 0
        self.reward = 0
        self.backgroundDraw()
        if self.snakeBodyPart[0][0] % self.length == 0 and self.snakeBodyPart[0][1] % self.length == 0:
            print(f"food->{self.food} snake->{self.snakeBodyPart[0]}")
            '''number = input("Enter something: ")
            action = [int(number[0]), int(number[1]), int(number[2])]'''
            action = self.decisionMaking()
            print(action)
            time.sleep(0.2)
            direction = ["Right", "Down", "Left", "Up"]
            if np.array_equal(action, [0, 1, 0]):
                if self.direction == "Right":
                    self.direction = "Up"
                else:
                    self.direction = direction[direction.index(self.direction) - 1]
            elif np.array_equal(action, [0, 0, 1]):
                if self.direction == "Up":
                    self.direction = "Right"
                else:
                    self.direction = direction[direction.index(self.direction) + 1]
        self.controls()
        self.update()
        self.drawSnake()
        self.checkCollision()
        return self.reward, self.gameOver, len(self.snakeBodyPart) - 1
    
    def decisionMaking(self):
        #CHECKING FOR THE INITIAL DISTANCE BETWEEN HEAD AND FOOD
        xabs = abs(self.food[0][0] - self.snakeBodyPart[0][0])
        yabs = abs(self.food[0][1] - self.snakeBodyPart[0][1])
        
        # CHECKING FOR THE LEFT OR RIGHT TURN
        if self.snakeBodyPart[0][2] == 0:

            xright = abs(self.food[0][0] - self.snakeBodyPart[0][0] + 1 * self.speed)
            yright = abs(self.food[0][1] - self.snakeBodyPart[0][1] + 0 * self.speed)
            if xright < xabs or yright < yabs:
                if self.snakeBodyPart[0][4] == 'Up':
                    return [0, 1, 0]
                else:
                    return [0, 0, 1]
                
            xleft = abs(self.food[0][0] - self.snakeBodyPart[0][0] + ((-1) * self.speed))
            yleft = abs(self.food[0][1] - self.snakeBodyPart[0][1] + 0 * self.speed)
            if xleft < xabs or yleft < yabs:
                if self.snakeBodyPart[0][4] == 'Up':
                    return [0, 0, 1]
                else:
                    return [0, 1, 0]

        if self.snakeBodyPart[0][3] == 0:
            
            xup = abs(self.food[0][0] - self.snakeBodyPart[0][0] + 0 * self.speed)
            yup = abs(self.food[0][1] - self.snakeBodyPart[0][1] + ((-1) * self.speed))
            if xup < xabs or yup < yabs:
                if self.snakeBodyPart[0][4] == 'Right':
                    return [0, 0, 1]
                else:
                    return [0, 1, 0]
                
            xdown = abs(self.food[0][0] - self.snakeBodyPart[0][0] + 0 * self.speed)
            ydown = abs(self.food[0][1] - self.snakeBodyPart[0][1] + 1 * self.speed)
            if xdown < xabs or ydown < yabs:
                if self.snakeBodyPart[0][4] == 'Right':
                    return [0, 1, 0]
                else:
                    return [0, 0, 1]
                
        # FORWARD
        xforward = abs(self.food[0][0] - self.snakeBodyPart[0][0] + self.snakeBodyPart[0][2] * self.speed)
        yforward = abs(self.food[0][1] - self.snakeBodyPart[0][1] + self.snakeBodyPart[0][3] * self.speed)
        if xforward < xabs or yforward < yabs:
            return [1, 0, 0]

    
'''pygame.init()
snake = Snake(40)
moves = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
while True:
    reward, gameOver, score = snake.step(random.choice(moves))
    if reward != 0:
        print(f"Reward is {reward} offered for the action.")
        time.sleep(1)
    if gameOver == True:
        snake.reset()'''

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((700, 700))
    pygame.display.set_caption("Snake Game")
    gridSize = 40 # Change this value for different resolution of grid and snake
    snake = Snake(screen, gridSize)
    moves = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
    run = True
    while run:
        reward, isOver, score = snake.step(random.choice(moves))
        if reward != 0:
            print(f"{reward}pts as REWARD offered for the action.")
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
        if isOver:
            snake.reset()
        #time.sleep(1)
        pygame.display.update()


# Need to create a function which will take list as an arg [Forward, Left, Right] 
# while true:
#   action -> function -> will return reward, isOver, score
#   
# Once we get the isOver = True then use reset() function to reset game 
# and run while loop again 
#