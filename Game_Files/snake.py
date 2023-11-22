import pygame 
import sys
import random
from pygame.math import Vector2
from os import path
#importing modules


#food class
class Food:
    def __init__(self):
        self.randomPos()

    #draw method
    def draw(self):
        foodRect = pygame.Rect(self.pos.x * cellSize,
                               self.pos.y * cellSize, cellSize, cellSize)
        screen.blit(food, foodRect)

    #generate random postion 
    def randomPos(self):
        self.x = random.randint(0, cellNum - 1)
        self.y = random.randint(0, cellNum - 1)
        self.pos = Vector2(self.x, self.y)

#snake class
class Snake:
    #creates the snake 
    def __init__(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(0, 0)
        self.newBlock = False
        self.eatSound = pygame.mixer.Sound("Game_Files/Sounds/eat.wav")
        self.deathSound = pygame.mixer.Sound("Game_Files/Sounds/deathSound.wav")

    #draw snake onto screen
    def draw(self):
        for block in self.body:
            blockRect = pygame.Rect(
                block.x * cellSize, block.y * cellSize, cellSize, cellSize)
            if block == self.body[0]:
                if self.direction.x == 1 or self.direction.x == 0:
                    pygame.draw.rect(screen, (2, 62, 138),
                                     blockRect, 0, 5, 0, 5, 0, 5)
                elif self.direction.x == -1:
                    pygame.draw.rect(screen, (2, 62, 138),
                                     blockRect, 0, 5, 5, 0, 5, 0)
                elif self.direction.y == 1:
                    pygame.draw.rect(screen, (2, 62, 138),
                                     blockRect, 0, 5, 0, 0, 5, 5)
                elif self.direction.y == -1:
                    pygame.draw.rect(screen, (2, 62, 138),
                                     blockRect, 0, 5, 5, 5, 5, 5)
            elif block == self.body[-1]:
                if self.direction.x == 1 or self.direction.x == 0:
                    pygame.draw.rect(screen, (2, 62, 138),
                                     blockRect, 0, 5, 5, 0, 5, 0)
                elif self.direction.x == -1:
                    pygame.draw.rect(screen, (2, 62, 138),
                                     blockRect, 0, 5, 0, 5, 0, 5)
                elif self.direction.y == 1:
                    pygame.draw.rect(screen, (2, 62, 138),
                                     blockRect, 0, 5, 5, 5, 0, 0)
                elif self.direction.y == -1:
                    pygame.draw.rect(screen, (2, 62, 138),
                                     blockRect, 0 , 5, 0, 0, 5, 5)
            else:
                pygame.draw.rect(screen, (2, 62, 138), blockRect)

    #movement of snake
    def movement(self):
        if self.newBlock == False:
            bodyCopy = self.body[:-1]
            bodyCopy.insert(0, bodyCopy[0] + self.direction)
            self.body = bodyCopy
        else:
            bodyCopy = self.body[:]
            bodyCopy.insert(0, bodyCopy[0] + self.direction)
            self.body = bodyCopy
            self.newBlock = False

    #makes snake grow
    def grow(self):
        self.newBlock = True

    #plays sounds
    def playEatSound(self):
        self.eatSound.play()
    
    def playDeathSound(self):
        self.deathSound.play()
       
class GAME:
    def __init__(self):
        self.apple = Food()
        self.snake = Snake()
        self.scoreValue = 0
        self.loadHighScore()
    

    def loadHighScore(self):
        # self.dir = path.dirname(__file__)
        # print(self.dir)
        with open(path.join("Game_Files\Highscore", "highscore"), "r") as f:
            try:
                self.highscore = int(f.read())
            except:
                self.highscore = 0

        print(self.highscore)
            

    #call all methods to make game run
    def update(self):
        self.snake.movement()
        self.checkCollision()
        self.deathStates()

    #calls all draw methods
    def drawElements(self):
        self.gridPattern()
        self.apple.draw()
        self.snake.draw()
        self.drawScore()

    #collision checks
    def checkCollision(self):
        if self.apple.pos == self.snake.body[0]:
            self.apple.randomPos()
            self.snake.grow()
            self.scoreValue += 1
            self.snake.playEatSound()
        
        for block in self.snake.body:
            if block == self.apple.pos:
                self.apple.randomPos()
    
    #resets snake
    def reset(self):
        self.snake.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.snake.direction = Vector2(0, 0)
        self.scoreValue = 0

    def gameOver(self):
        self.reset()
        if self.scoreValue > self.highscore:
            self.highscore = self.scoreValue
            with open("Game_Files\Highscore", "highscore") as f:
                f.write(str(self.scoreValue))
            print(self.scoreValue)

    #checks if snake is dead
    def deathStates(self):
        if not 0 <= self.snake.body[0].x < cellNum:
            self.snake.playDeathSound()
            self.gameOver()
        elif not 0 <= self.snake.body[0].y < cellNum:
            self.snake.playDeathSound()
            self.gameOver()

        for body in self.snake.body[1:]:
            if body == self.snake.body[0]:
                self.gameOver()

    #creates grid
    def gridPattern(self):
        grassColour = (25, 235, 14)
        for row in range(cellNum):
            if row % 2 == 0:
                for col in range(cellNum):
                    if col % 2 == 0:
                        grass_rect = pygame.Rect(
                            col * cellSize, row * cellSize, cellSize, cellSize)
                        pygame.draw.rect(screen, grassColour, grass_rect)
            else:
                for col in range(cellNum):
                    if col % 2 != 0:
                        grass_rect = pygame.Rect(
                            col * cellSize, row * cellSize, cellSize, cellSize)
                        pygame.draw.rect(screen, grassColour, grass_rect)
    
    #creates score
    def drawScore(self):
        scoreTxt = ("Score: "+ str(self.scoreValue))
        scoreSurface = font.render(scoreTxt, True, (30, 30, 36))
        screen.blit(scoreSurface, [10,10]) 

#button class
class button:
    def __init__(self, colour, x, y, width, height, text=""):
        self.color = colour
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self, win, outline=None):
        if outline:
            pygame.draw.rect(win, outline, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)

        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height), 0)

        if self.text != "":
            font = pygame.font.SysFont("comicsans", 30)
            text = font.render(self.text, 1, (255,255,255))
            win.blit(text, 
                    (
                    self.x + (self.width / 2 - text.get_width() / 2),
                    self.y + (self.height / 2 - text.get_height() / 2))
                    )

    def isOver(self, pos):
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True

        return False

#initalising pgame
pygame.init()
cellSize = 40
cellNum = 20

#game variables
screen = pygame.display.set_mode((cellSize*cellNum, cellSize*cellNum))
pygame.display.set_caption("Snake")
clock = pygame.time.Clock()
food = pygame.image.load("Game_Files/Graphics/apple.png")
font = pygame.font.Font(None, 40)
gameFont = pygame.font.Font("freesansbold.ttf", 32)
dscrptFont = pygame.font.Font(None, 24)

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 125)

mainGame = GAME() 

#button objects
playButton = button((14, 20, 40),((cellSize*cellNum)/2 - 125),((cellSize*cellNum)/2 - 250), 250, 150, "Play Snake")
instructionButton = button((14, 20, 40), ((cellSize*cellNum)/2 - 125), ((cellSize*cellNum)/2 - 50), 250, 150, "Instructions")

#menu screen // new game loop
def menu():
    running = True
    while running:
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if playButton.isOver(pos):
                    main()
                if instructionButton.isOver(pos):
                    instructions()
        
        screen.fill((12, 250, 0))
        playButton.draw(screen)
        instructionButton.draw(screen)
        pygame.display.flip()
        clock.tick(60)

#instructions screen // new game loop
def instructions():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    menu()
        
        screen.fill((12, 250, 0))
        writeInstruction()
        msg = dscrptFont.render("The aim of the game is to get points by eating the food item.", True, (0,0,0))
        msg1 = dscrptFont.render("Use W,A,S,D to move or instead the arrow keys.",True, (0,0,0))
        msg2 = dscrptFont.render(" Don't hit the wall or yourself!",True, (0,0,0))
        msg3 = dscrptFont.render("To pause, press P or the Escape button", True, (0,0,0))
        msg4 = dscrptFont.render("To leave, press Escape.", True, (0,0,0))

        screen.blit(msg,(250, 260))
        screen.blit(msg1, (250,295))
        screen.blit(msg2, (250,330))
        screen.blit(msg3, (250,365))
        screen.blit(msg4, (250,400))

        pygame.display.flip()
        clock.tick(60)

def writeInstruction():
    textRect = pygame.Rect(250,250, 500, 200)
    pygame.draw.rect(screen, (14, 20, 40), (250-2, 250-2, 504, 204 ), 0)
    pygame.draw.rect(screen, (255,255,255),textRect)

#pause menu // creates new game loop
def pause():
    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    paused = False 
                elif event.key == pygame.K_q:
                    menu()

        msg1 = gameFont.render("The game is paused", True, (229, 230, 228))
        msg2 = gameFont.render("Press C to continue or", True,(229, 230, 228)) 
        msg3 = gameFont.render("Q to quit to the main menu", True,(229, 230, 228))
        screen.blit(msg1, (800/2 -200 + 10, 800/2 - 100))
        screen.blit(msg2,(800/2 -200, 800/2 -70 ))
        screen.blit(msg3,(800/2 -200, 800/2 - 40 ))
        pygame.display.update()

#main game loop
def main():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == SCREEN_UPDATE:
                mainGame.update()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    if mainGame.snake.direction.y != 1:
                        mainGame.snake.direction = Vector2(0, -1)
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    if mainGame.snake.direction.x != -1:
                        mainGame.snake.direction = Vector2(1, 0)
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    if mainGame.snake.direction.y != -1:
                        mainGame.snake.direction = Vector2(0, 1)
                elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    if mainGame.snake.direction.x != 1:
                        mainGame.snake.direction = Vector2(-1, 0)
                
                elif event.key == pygame.K_ESCAPE:
                    pause()
                elif event.key == pygame.K_p:
                    pause()

        screen.fill((12, 250, 0))
        mainGame.drawElements()
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
