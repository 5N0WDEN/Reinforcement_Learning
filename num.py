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
        self.xChange, self.yChange = 1, 0
        self.direction = "Right"
        self.snakeBodyPart = np.array([[self.snakeSpawn(), self.snakeSpawn(), self.xChange, self.yChange]], dtype="i")
        self.snakeBodyDirection = np.array(["Right"], dtype="S")
        self.gameOver = False
        self.font = pygame.font.Font('freesansbold.ttf', 20)
        self.path = os.path.abspath(__file__)[:-6]
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
        rect = np.array([self.length * 2, self.length * 2, self.length * self.numberOfBlockes, self.length * self.numberOfBlockes])
        pygame.draw.rect(self.screen, ((170,215,81)), rect)
        dimension = np.array([self.length * 2, self.length * 2, self.length, self.length])
        color, i = (162,209,73), 2
        score = self.font.render(f'SCORE: {len(self.snakeBodyPart) - 1}', True, (255, 255, 255))
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
        # Drawing food and score on the background.
        self.screen.blit(self.foodApple, (self.food[0, 0], self.food[0, 1]))
        self.screen.blit(score, (550, 50))

    def update(self):
        # CHECKING WHETHER THE SNAKE IS INSIDE OR OUTSIDE OF THE PLAYING AREA
        if self.snakeBodyPart[0, 0] > self.length * (self.numberOfBlockes + 1) or self.snakeBodyPart[0, 0] < self.length * 2 or self.snakeBodyPart[0, 1] > self.length * (self.numberOfBlockes + 1) or self.snakeBodyPart[0, 1] < self.length * 2:
            self.gameOver = True
        if not self.gameOver:
            self.snakeBodyDirection = np.insert(self.snakeBodyDirection, 0, self.direction)
            self.snakeBodyDirection = np.delete(self.snakeBodyDirection, -1)
            new_head = [self.snakeBodyPart[0, 0] + self.xChange * self.speed, self.snakeBodyPart[0, 1] + self.yChange * self.speed, self.xChange, self.yChange]
            self.snakeBodyPart = np.insert(self.snakeBodyPart, 0, [new_head], axis = 0)
            self.snakeBodyPart = np.delete(self.snakeBodyPart, -1, axis = 0)

    def controls(self):
        if self.snakeBodyPart[0, 0] % self.length == 0 and self.snakeBodyPart[0, 1] % self.length == 0:
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
        newPosition = np.array([(self.randomSpawn(), self.randomSpawn())], dtype='i')
        while any((newPosition[0][0] == body[0] and newPosition[0][1] == body[1]) for body in self.snakeBodyPart):
           newPosition = np.array([(self.randomSpawn(), self.randomSpawn())], dtype='i')
        self.food = newPosition
    
    def checkGameStatus(self): # Checks wheather player is playing or he has completed the game
        if len(self.snakeBodyPart) + 1 == self.numberOfBlockes * self.numberOfBlockes:
            print("You have completed the game.")
            self.gameOver = True
            #self.reward += 10

    def checkCollision(self):
        if self.snakeBodyPart[0, 0] == self.food[0, 0] and self.snakeBodyPart[0, 1] == self.food[0, 1]:
            self.reward += 10
            self.checkGameStatus()
            if not self.gameOver:
                self.foodPosition()
            if self.snakeBodyPart[-1, 2] == -1 or self.snakeBodyPart[-1, 2] == 1:
                new = [self.snakeBodyPart[-1, 0] - (self.length * self.snakeBodyPart[-1, 2]), self.snakeBodyPart[-1, 1], self.snakeBodyPart[-1, 2], 0]
            elif self.snakeBodyPart[-1, 3] == -1 or self.snakeBodyPart[-1, 3] == 1:
                new = [self.snakeBodyPart[-1, 0], self.snakeBodyPart[-1, 1] - (self.length * self.snakeBodyPart[-1, 3]), 0, self.snakeBodyPart[-1, 3]]
            self.snakeBodyDirection = np.append(self.snakeBodyDirection, self.snakeBodyDirection[-1])
            self.snakeBodyPart = np.append(self.snakeBodyPart, [new], axis=0)
        if len(self.snakeBodyPart) > 0 and any((body[0] == self.snakeBodyPart[0, 0] and body[1] == self.snakeBodyPart[0, 1]) for body in self.snakeBodyPart[1::]):
            self.gameOver = True
            self.reward -= 10
        if self.frame_iteration >= 10000 * len(self.snakeBodyPart):
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
        if self.snakeBodyPart[0, 0] % self.length == 0 and self.snakeBodyPart[0, 1] % self.length == 0:
            '''number = input("Enter something: ")
            action = [int(number[0]), int(number[1]), int(number[2])]'''
            action = self.decisionMaking()
            direction = ["Right", "Down", "Left", "Up"]
            if np.array_equal(action, [0, 1, 0]): # NUMPY ARRAYS ARE 50x FASTER THAN PYTHON LISTS
                self.direction = direction[(direction.index(self.direction) - 1) % 4]
            elif np.array_equal(action, [0, 0, 1]):
                self.direction = direction[(direction.index(self.direction) + 1) % 4]
        self.controls()
        self.update()
        self.drawSnake()
        self.checkCollision()
        return self.reward, self.gameOver, len(self.snakeBodyPart) - 1

    def decisionMaking(self):
        #CHECKING FOR THE INITIAL DISTANCE BETWEEN HEAD AND FOOD

        directioncheck = np.array(["Right", "Down", "Left", "Up"], dtype="S")

        xabs = abs(self.food[0, 0] - self.snakeBodyPart[0, 0])
        yabs = abs(self.food[0, 1] - self.snakeBodyPart[0, 1])

        # CHECKING FOR THE LEFT OR RIGHT TURN
        if self.snakeBodyPart[0, 2] == 0: # MOVING IN Y AXIS

            # RIGHT SIDE MEANS POSITIVE X DIRECTION 
            xright = abs(self.food[0, 0] - self.snakeBodyPart[0, 0] + 1 * self.speed)
            yright = abs(self.food[0, 1] - self.snakeBodyPart[0, 1] + 0 * self.speed)
            if xright < xabs or yright < yabs:
                if np.array_equal(self.snakeBodyDirection[0], directioncheck[3]):
                    return np.array([0, 1, 0], dtype='i') # LEFT TURN 
                else:
                    return np.array([0, 0, 1], dtype='i') # RIGHT TURN 

            # LEFT SIDE MEANS NEGATIVE X DIRECTION
            xleft = abs(self.food[0, 0] - self.snakeBodyPart[0, 0] + ((-1) * self.speed))
            yleft = abs(self.food[0, 1] - self.snakeBodyPart[0, 1] + 0 * self.speed)
            if xleft < xabs or yleft < yabs:
                if np.array_equal(self.snakeBodyDirection[0], directioncheck[3]):
                    return np.array([0, 0, 1], dtype='i') # RIGHT TURN
                else:
                    return np.array([0, 1, 0], dtype='i') # LEFT TURN
                
        # CHECKING FOR THE UP OR DOWN
        if self.snakeBodyPart[0, 3] == 0: # MOVING IN X AXIX
            
            # UP SIDE MEANS NEGATIVE Y DIRECTION
            xup = abs(self.food[0, 0] - self.snakeBodyPart[0, 0] + 0 * self.speed)
            yup = abs(self.food[0, 1] - self.snakeBodyPart[0, 1] + ((-1) * self.speed))
            if xup < xabs or yup < yabs:
                if np.array_equal(self.snakeBodyDirection[0], directioncheck[0]):
                    return np.array([0, 0, 1], dtype='i') # RIGHT TURN 
                else:
                    return np.array([0, 1, 0], dtype='i') # LEFT TURN 
  
            # DOWN SIDE MEANS POSITIVE Y DIRECTION
            xdown = abs(self.food[0, 0] - self.snakeBodyPart[0, 0] + 0 * self.speed)
            ydown = abs(self.food[0, 1] - self.snakeBodyPart[0, 1] + 1 * self.speed)
            if xdown < xabs or ydown < yabs:
                if np.array_equal(self.snakeBodyDirection[0], directioncheck[0]):
                    return np.array([0, 1, 0], dtype='i') # LEFT TURN 
                else:
                    return np.array([0, 0, 1], dtype='i') # RIGHT TURN

        # FORWARD POINT CHECK
        xforward = abs(self.food[0, 0] - self.snakeBodyPart[0, 0] + self.snakeBodyPart[0, 2] * self.speed)
        yforward = abs(self.food[0, 1] - self.snakeBodyPart[0, 1] + self.snakeBodyPart[0, 3] * self.speed)
        if xforward < xabs or yforward < yabs:
            return np.array([1, 0, 0], dtype='i') # CONTINUING IN SAME DIRECTION

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((700, 700))
    pygame.display.set_caption("Snake Game")
    gridSize = 5 # Change this value for different resolution of grid and snake
    snake = Snake(screen, gridSize)
    moves = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
    clock = pygame.time.Clock()
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
        pygame.display.update()
        print(clock.get_fps())
        clock.tick(60)

# Need to create a function which will take list as an arg [Forward, Left, Right] 
# while true:
#   action -> function -> will return reward, isOver, score
#   
# Once we get the isOver = True then use reset() function to reset game 
# and run while loop again 
