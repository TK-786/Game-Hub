from multiprocessing.connection import wait
import pygame
import sys
import random, threading
from pygame.math import Vector2
from os import path

screenWidth = 800
screenHeight = 800

pygame.init()
screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("Snake")
clock = pygame.time.Clock()

cellSize = 40
cellNum = 20
def gridPattern():
    grassColour = (25, 235, 14)
    for row in range(cellNum):
        if row % 2 == 0:
            for col in range(cellNum):
                if col % 2 == 0:
                    grass_rect = pygame.Rect(col * cellSize, row * cellSize, cellSize, cellSize)
                    pygame.draw.rect(screen, grassColour, grass_rect)
        else:
            for col in range(cellNum):
                if col % 2 != 0:
                    grass_rect = pygame.Rect(col * cellSize, row * cellSize, cellSize, cellSize)
                    pygame.draw.rect(screen, grassColour, grass_rect)

class Food:
    def __init__(self):
        self.randomPos()

    def draw(self):
        foodRect = pygame.Rect(self.pos.x * cellSize,
                               self.pos.y * cellSize, cellSize, cellSize)
        screen.blit(food, foodRect)

    def randomPos(self):
        self.x = random.randint(0, cellNum - 1)
        self.y = random.randint(0, cellNum - 1)
        self.pos = Vector2(self.x, self.y)

class Snake:
    def __init__(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(0, 0)
        self.newBlock = False
        # self.eatSound = pygame.mixer.Sound("Programming Project/Sounds/eat.wav")
        # self.deathSound = pygame.mixer.Sound("Programming Project/Sounds/deathSound.wav")
        self.scoreValue = 0
        self.loadHighScore()
        self.highscoreTxt = ""
        self.food = Food()

    def loadHighScore(self): # method to load highscore value from external file
        #self.dir = path.dirname(__file__) #creates a variable to store path of hihgscore file
        with open(path.join("Game_Files\Highscore", "highscore"), "r") as f:
            try: #reads highscore file
                self.highscore = int(f.read())
            except: #if its unable to set to 0
                self.highscore = 0

    def draw(self):
        for block in self.body:
            blockRect = pygame.Rect(block.x * cellSize, block.y * cellSize, cellSize, cellSize)
            pygame.draw.rect(screen, (2, 62, 138), blockRect,0,5)

    def movement(self):
        if self.direction != Vector2((0,0)):
            if self.newBlock == False:
                bodyCopy = self.body[:-1]
                bodyCopy.insert(0, bodyCopy[0] + self.direction)
                self.body = bodyCopy
            else:
                bodyCopy = self.body[:]
                bodyCopy.insert(0, bodyCopy[0] + self.direction)
                self.body = bodyCopy
                self.newBlock = False

    def grow(self):
        self.newBlock = True

    def checkCollision(self):
        if self.food.pos == self.body[0]:
            self.food.randomPos()
            snake.grow()
            self.scoreValue += 1
            # snake.playEatSound()
        
        for block in self.body:
            if block == self.food.pos:
                self.food.randomPos()

        if not 0 <= self.body[0].x < cellNum:
            # self.playDeathSound()
            self.gameOver()
        elif not 0 <= self.body[0].y < cellNum:
            # self.playDeathSound()
            self.gameOver()

        for body in self.body[1:]:
            if body == self.body[0]:
                self.gameOver()

    def gameOver(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(0, 0)
        if self.scoreValue > self.highscore:
            self.drawHighScore()
            self.highscore = self.scoreValue
            with open(path.join("Game_Files\Highscore", "highscore"), "w") as f:
                f.write(str(self.scoreValue))

        self.scoreValue = 0
        
    def drawScore(self):
        scoreTxt = ("Score: "+ str(self.scoreValue))
        scoreSurface = font.render(scoreTxt, True, (30, 30, 36))
        screen.blit(scoreSurface, [10,10]) 
    
    def drawHighScore(self):
        self.highscoreTxt = ("Well done you set a new highscore!")
        highscoreSurface = font.render(self.highscoreTxt, True, (30, 30, 36))
        screen.blit(highscoreSurface, (100, 300))
    


pygame.time.set_timer(pygame.USEREVENT, 130)
snake =Snake() #snake

font = pygame.font.Font(None, 40)
dscrptFont = pygame.font.Font(None, 24)
gameFont = pygame.font.Font("freesansbold.ttf", 42)
food = pygame.image.load("Game_Files/Graphics/apple.png")

class button:
    def __init__(self, colour, x, y, width, height, text=""):
        self.color = colour
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self, win, outline=None):
        # Call this method to draw the button on the screen
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
        # Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True

        return False



menuPlayButton = button((14, 20, 40),((cellSize*cellNum)/2 - 125),((cellSize*cellNum)/2 - 250), 250, 150, "Play Snake")
instructionButton = button((14, 20, 40), ((cellSize*cellNum)/2 - 125), ((cellSize*cellNum)/2 - 50), 250, 150, "Instructions")
snakeButton = button((20, 17, 15), 100, 300, 200, 100, "Play Snake")
pongButton = button((20, 17, 15), 500, 300,200, 100, "Play Pong")
pongMenuButton = button((14, 20, 40),((1280)/2 - 125),((960)/2 - 250), 250, 150, "Play Pong")
instructionButton2 = button((14, 20, 40),((1280)/2 - 125),((960)/2 - 50), 250, 150, "Instruction")

def menu():
    running = True
    pygame.display.set_caption("Snake")
    while running:
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if menuPlayButton.isOver(pos):
                    main()
                if instructionButton.isOver(pos):
                    instructions()
        
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    mainGame()

        screen.fill((12, 250, 0))
        menuPlayButton.draw(screen)
        instructionButton.draw(screen)
        pygame.display.flip()
        clock.tick(60)

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


def pause1():
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

        msg1 = font.render("The game is paused", True, (229, 230, 228))
        msg2 = font.render("Press C to continue or", True,(229, 230, 228)) 
        msg3 = font.render("Q to quit to the main menu", True,(229, 230, 228))
        screen.blit(msg1, (800/2 -200 + 10, 800/2 - 100))
        screen.blit(msg2,(800/2 -200, 800/2 -70 ))
        screen.blit(msg3,(800/2 -200, 800/2 - 40 ))
        pygame.display.update()


def main():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()  
            if event.type == pygame.USEREVENT:
                snake.movement()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    if snake.direction.y != 1:
                        snake.direction = Vector2(0, -1)
                        snake.movement()
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    if snake.direction.x != -1:
                        snake.direction = Vector2(1, 0)
                        snake.movement()
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    if snake.direction.y != -1:
                        snake.direction = Vector2(0, 1)
                        snake.movement()
                elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    if snake.direction.x != 1:
                        snake.direction = Vector2(-1, 0)
                        snake.movement()

                if event.key == pygame.K_p or event.key == pygame.K_ESCAPE:
                    pause1()
                
                
        screen.fill((12, 250, 0))
        gridPattern()
        snake.draw()
        snake.food.draw()
        snake.checkCollision()
        snake.drawScore()
        pygame.display.flip()
        clock.tick(60)
#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////

class Ball:
    def __init__(self):             #Initial set up of the ball. Ball size, co-ords, and speed.
        self.width = 30
        self.height = 30
        self.x = (1280 / 2 - 15)
        self.y = (960 / 2 - 15)
        self.ballSpeedX = random.randint(6,9) * random.choice((1,-1))
        self.ballSpeedY = random.randint(6,9) * random.choice((1,-1))
        self.player1Score = 0
        self.player2Score = 0
    
    def draw(self):                 #Draws the ball onto surface
        ballRect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.ellipse(screen,(229, 230, 228), ballRect)

    def movement(self):
        self.x += self.ballSpeedX
        self.y += self.ballSpeedY

    def checkCollision(self):     #Collision checks
        if self.x <= 0:
            self.restart()
            self.player1Score += 1

        elif self.x >= (1280 -30):  
            self.restart()
            self.player2Score += 1
            
        elif self.y <= 0:
            self.ballSpeedY = self.ballSpeedY * -1

        elif self.y >= (960-30):
            self.ballSpeedY = self.ballSpeedY * -1

    def restart(self):      #Resets ball's position
        self.x = (1280 / 2 - 15)
        self.y = (960 / 2 - 15)
        self.ballSpeedX = 0
        self.ballSpeedY = 0
        t = threading.Timer(2, self.delay)
        t.start()
        
    def getBallRect(self):
        ballRect = pygame.Rect(self.x, self.y, self.width, self.height) # Getter function to return ballRect
        return ballRect

    def delay(self): # delays restart of the game
        self.ballSpeedX = 8 * random.choice((1,-1))
        self.ballSpeedY = 8 * random.choice((1,-1))
    

class Player:       #player class
    def __init__(self, playerNo, x, y):
        self.playerNo = playerNo
        self.x = x
        self.y = y
        self.playerSpeed = 0

    def draw(self):                             #Draws players onto screen
        playerRect = pygame.Rect(self.x, self.y, 10, 140)
        pygame.draw.rect(screen, (229, 230, 228), playerRect)
    
    def wallCollision(self):            #Prevents players from going off screen
        if self.y <= 0:
            self.y = 0
        elif self.y >= 960-140:
            self.y = 960 - 140
    
    def getPlayerRect(self):                  #Getter function for PlayerRects
        playerRect = pygame.Rect(self.x, self.y , 10, 140)
        return playerRect

        

pongBall = Ball()
player1 = Player("1",(1280 -20), (960/2 - 70))
player2 = Player("2",10, (960/2 - 70))

def ballCollision():
    ball = pongBall.getBallRect()
    playerOne = player1.getPlayerRect()
    playerTwo = player2.getPlayerRect()
    if ball.colliderect(playerOne) or ball.colliderect(playerTwo):
        pongBall.ballSpeedX = pongBall.ballSpeedX * -1     

def pongMenu():
    pygame.display.set_caption("Pong")
    screen = pygame.display.set_mode((1280, 960))
    running = True
    while running:
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pongMenuButton.isOver(pos):
                    pongMain()
                if instructionButton2.isOver(pos):
                    instructions2()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    mainGame()
        
        screen.fill((59, 112, 128))
        pongMenuButton.draw(screen)
        instructionButton2.draw(screen)
        pygame.display.flip()
        clock.tick(60)

def instructions2():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pongMenu()
        
        screen.fill((59, 112, 128))
        writeInstruction()
        msg = dscrptFont.render("The aim of the game is to get points by hitting", True, (0,0,0))
        msg1 = dscrptFont.render("the ball behind the other player",True, (0,0,0))
        msg2 = dscrptFont.render("Player 1 use W and S, Player 2 use Up and Down keys.",True, (0,0,0))
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


def pause2():
    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:    #checks if the player is quiting or continuing
                if event.key == pygame.K_c:
                    paused = False 
                elif event.key == pygame.K_q:
                    pongMenu()

        screen.fill((58, 64, 90))
        msg1 = gameFont.render("The game is paused", True, (229, 230, 228))
        msg2 = gameFont.render("Press C to continue or Q to quit", True,(229, 230, 228)) 
        screen.blit(msg1, (1290/2 -200, 980/2 -75 ))
        screen.blit(msg2,(1290/2 -300, 960/2 -25 ) )
        pygame.display.update()
        clock.tick(5)


def pongMain():  # main game loop pong
    screen = pygame.display.set_mode((1280, 960))
    pygame.display.set_caption("Pong")
    t = threading.Timer(2, pongBall.delay)
    t.start()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:          
                if event.key == pygame.K_DOWN:          #Player 1 Movement
                    player1.playerSpeed += 7
                elif event.key == pygame.K_UP:
                    player1.playerSpeed -= 7

                elif event.key == pygame.K_w:           #Player 2 movement
                    player2.playerSpeed -= 7
                elif event.key == pygame.K_s:
                    player2.playerSpeed += 7

                if event.key == pygame.K_ESCAPE or event.key == pygame.K_p:
                    pause2()

            elif event.type == pygame.KEYUP:    #checks if key has been let go
                if event.key == pygame.K_DOWN:
                    player1.playerSpeed -= 7
                elif event.key == pygame.K_UP:
                    player1.playerSpeed += 7

                if event.key == pygame.K_w:
                    player2.playerSpeed += 7
                elif event.key == pygame.K_s:
                    player2.playerSpeed -= 7
        
        screen.fill((58, 64, 90))
        pygame.draw.aaline(screen,(229, 230, 228),(1280 / 2, 0),(1280 / 2, 960))
        pongBall.draw()
        player1.draw()
        player2.draw()
        pongBall.movement()
        pongBall.checkCollision()
        player1.wallCollision()
        player2.wallCollision()
        ballCollision()

        player1Text = gameFont.render(f"{pongBall.player1Score}", True, (229, 230, 228))
        screen.blit(player1Text, (660, 460))
        player2Text = gameFont.render(f"{pongBall.player2Score}", True, (229, 230, 228))
        screen.blit(player2Text, (600, 460))


        player1.y += player1.playerSpeed 
        player2.y += player2.playerSpeed

        pygame.display.flip()
        clock.tick(60)
    

def mainGame(): #GAME HUB
    pygame.display.set_caption("Game Hub")
    screen = pygame.display.set_mode((1280, 960))
    while True:
        pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if snakeButton.isOver(pos):
                    screen = pygame.display.set_mode((800,800))
                    menu()
                elif pongButton.isOver(pos):
                    pongMenu()
                

        screen.fill((255,255,255))
        snakeButton.draw(screen)
        pongButton.draw(screen)

        pygame.draw.rect(screen, (0,0,0), (73, 498, 350, 155))
        pygame.draw.rect(screen, (0,0,0), (478, 498, 275,155))

        snakeDescription = dscrptFont.render("Snake is a video game where ", True, (255,255,255))
        snakeDescription1 = dscrptFont.render("the player maneuvers a growing ", True, (255,255,255))
        snakeDescription2 = dscrptFont.render("line that becomes a primary obstacle to itself.", True, (255,255,255))
        snakeDescription3 = dscrptFont.render("The aim of the game is to get", True, (255,255,255))
        snakeDescription4 = dscrptFont.render("as many points as possible", True, (255,255,255))
        snakeDescription5 = dscrptFont.render("by eating all the food items.", True, (255,255,255))

        pongDescription = dscrptFont.render("Pong is a two-dimensional game",True, (255,255,255))
        pongDescription1 = dscrptFont.render("that simulates table tennis.",True, (255,255,255))
        pongDescription2 = dscrptFont.render("The player controls an in-game",True, (255,255,255))
        pongDescription3 = dscrptFont.render("paddle by moving it vertically",True, (255,255,255))
        pongDescription4 = dscrptFont.render("across the left or right side",True, (255,255,255))

        screen.blit(snakeDescription, (75,500))
        screen.blit(snakeDescription1, (75,525))
        screen.blit(snakeDescription2, (75,550))
        screen.blit(snakeDescription3, (75,575))
        screen.blit(snakeDescription4, (75,600))
        screen.blit(snakeDescription5, (75,625))

        screen.blit(pongDescription, (480,500))
        screen.blit(pongDescription1, (480,525))
        screen.blit(pongDescription2, (480,550))
        screen.blit(pongDescription3, (480,575))
        screen.blit(pongDescription4, (480,600))

        pygame.display.update()
        clock.tick(60)





    
mainGame()
# pongMain()
# pongMenu()