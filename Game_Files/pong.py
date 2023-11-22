import pygame, sys, random, threading

#Initial set up of the ball. Ball size, co-ords, and speed.
class Ball:
    def __init__(self):             
        self.width = 30
        self.height = 30
        self.x = (screenWidth / 2 - 15)
        self.y = (screenHeight / 2 - 15)
        self.ballSpeedX = 0
        self.ballSpeedY = 0
        self.player1Score = 0
        self.player2Score = 0
    
    # Getter function to return ballRect
    def getBallRect(self):
        ballRect = pygame.Rect(self.x, self.y, self.width, self.height) 
        return ballRect

    #Draws the ball onto surface    
    def draw(self):                 
        ballRect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.ellipse(screen,(229, 230, 228), ballRect)
    

    #makes the ball move
    def movement(self):
        self.x += self.ballSpeedX
        self.y += self.ballSpeedY

    #Resets ball's position
    def restart(self):                              
        self.x = (screenWidth / 2 - 15)
        self.y = (screenHeight / 2 - 15)
        self.ballSpeedX = 0
        self.ballSpeedY = 0
        t = threading.Timer(2, self.delay)
        t.start()

    #Collision checks
    def checkCollision(self):     
        #side wall
        if self.x <= 0:
            self.player1Score += 1
            self.restart()
                        
        #top wall
        elif self.y <= 0:
            self.ballSpeedY = self.ballSpeedY * -1

        #side wall
        elif self.x >= (screenWidth -30):
            self.player2Score += 1
            self.restart()
                       
        #bottom wall
        elif self.y >= (screenHeight-30):
            self.ballSpeedY = self.ballSpeedY * -1

    # delays restart of the game
    def delay(self): 
        self.ballSpeedX = 8 * random.choice((1,-1))
        self.ballSpeedY = 8 * random.choice((1,-1))
            
#player class
class Player:      
    def __init__(self, playerNo):
        self.playerNo = playerNo
        self.x1 = (screenWidth -20)    #Player 1 x and y
        self.y1 = (screenHeight/2 - 70)
        self.x2 = 10                    #PLayer 2 x and y
        self.y2 = (screenHeight / 2 - 70)
        self.playerSpeed = 0
        
    #Getter function for PlayerRects
    def getPlayerRect(self):                  
        if self.playerNo == "1":
            playerRect = pygame.Rect(self.x1, self.y1 , 10, 140)
            return playerRect
        elif self.playerNo == "2":
            playerRect = pygame.Rect(self.x2, self.y2, 10, 140)
            return playerRect

    #Draws players onto screen
    def draw(self):                             
        if self.playerNo == "1":
            playerRect = pygame.Rect(self.x1, self.y1, 10, 140)
            pygame.draw.rect(screen, (229, 230, 228), playerRect)
        elif self.playerNo == "2":
            playerRect = pygame.Rect(self.x2, self.y2, 10, 140)
            pygame.draw.rect(screen, (229, 230, 228), playerRect)

    #Prevents players from going off screen
    def wallCollision(self):                    
        if self.y1 <= 0:
            self.y1 = 0
        elif self.y1 >= screenHeight-140:
            self.y1 = screenHeight - 140
        if self.y2 <= 0:
            self.y2 = 0
        elif self.y2 >= screenHeight -140:
            self.y2 = screenHeight -140 
           

class GAME:
    def __init__(self):
        self.ball = Ball()
        self.player1 = Player("1")
        self.player2 = Player("2")
    
    def ballCollision(self):
        ball = self.ball.getBallRect()
        player1 = self.player1.getPlayerRect()
        player2 = self.player2.getPlayerRect()
        if ball.colliderect(player1) or ball.colliderect(player2):
            self.ball.ballSpeedX = self.ball.ballSpeedX * -1     

    #calls every method to make the game run 
    def update(self):
        self.ball.draw()
        self.ball.movement()
        self.player1.draw()
        self.player2.draw()
        self.player1.wallCollision()
        self.player2.wallCollision()
        self.ball.checkCollision()
        self.ballCollision()

        


#General set up
pygame.init()
clock = pygame.time.Clock()
screenWidth = 1280
screenHeight = 960
screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("Pong")


SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 125)
mainGame = GAME()

#game variables
gameFont = pygame.font.Font("freesansbold.ttf", 32)
dscrptFont = pygame.font.Font(None, 24)
t = threading.Timer(3, mainGame.ball.delay)
t.start()

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

#button objects
playButton = button((14, 20, 40),((screenWidth)/2 - 125),((screenHeight)/2 - 250), 250, 150, "Play Pong")
instructionButton = button((14, 20, 40), ((screenWidth)/2 - 125), ((screenHeight)/2 - 50), 250, 150, "Instructions")

#creates a pause menu // new game loop
def pause():
    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            #checks if the player is quiting or continuing
            if event.type == pygame.KEYDOWN:    
                if event.key == pygame.K_c:
                    paused = False 
                elif event.key == pygame.K_q:
                    menu()

        screen.fill((58, 64, 90))
        msg1 = gameFont.render("The game is paused", True, (229, 230, 228))
        msg2 = gameFont.render("Press C to continue or Q to quit", True,(229, 230, 228)) 
        screen.blit(msg1, (screenWidth/2 -200, screenHeight/2 -75 ))
        screen.blit(msg2,(screenWidth/2 -300, screenHeight/2 -25 ) )
        pygame.display.update()
        clock.tick(5)
    
#menu screen // creates a new game loop
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

        screen.fill((59, 112, 128))
        playButton.draw(screen)
        instructionButton.draw(screen)
        pygame.display.flip()
        clock.tick(60)

#creates instructions screeen // new game loop
def instructions():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    menu()
        
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

# main game loop
def main():  
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                #Player 1 Movement          
                if event.key == pygame.K_DOWN:          
                    mainGame.player1.playerSpeed += 7
                elif event.key == pygame.K_UP:
                    mainGame.player1.playerSpeed -= 7
                
                #Player 2 Movement   
                elif event.key == pygame.K_w:           
                    mainGame.player2.playerSpeed -= 7
                elif event.key == pygame.K_s:
                    mainGame.player2.playerSpeed += 7

                #pause checks
                elif event.key == pygame.K_ESCAPE:
                    pause()
                elif event.key == pygame.K_p:
                    pause()

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    mainGame.player1.playerSpeed -= 7
                elif event.key == pygame.K_UP:
                    mainGame.player1.playerSpeed += 7
                
                if event.key == pygame.K_w:
                    mainGame.player2.playerSpeed += 7
                elif event.key == pygame.K_s:
                    mainGame.player2.playerSpeed -= 7

            
        # Visual
        screen.fill((58, 64, 90))
        pygame.draw.aaline(screen,(229, 230, 228),(screenWidth / 2, 0),(screenWidth / 2, screenHeight))
        mainGame.update()
        mainGame.player1.y1 += mainGame.player1.playerSpeed 
        mainGame.player2.y2 += mainGame.player2.playerSpeed

        player1Text = gameFont.render(f"{mainGame.ball.player1Score}", True, (229, 230, 228))
        screen.blit(player1Text, (660, 470))
        player2Text = gameFont.render(f"{mainGame.ball.player2Score}", True, (229, 230, 228))
        screen.blit(player2Text, (600, 470))

        #Updating window
        pygame.display.flip()
        clock.tick(60)

# menu()
# if __name__ == "__main__":
#     main()
