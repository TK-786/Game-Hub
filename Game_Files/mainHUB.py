import pygame, sys #importing modules
import snake #importing games
import pong

#initialising pygame
pygame.init() 
clock = pygame.time.Clock()
fps = 60

#screen variables
screenWidth = 1280  
screenHeight = 960
screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("Game Hub")

#button class
class button:
    def __init__(self, colour, x, y, width, height, text=""):
        self.color = colour
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    #This method draw the button on the screen
    def draw(self, win, outline=None):
        if outline:
            pygame.draw.rect(win, outline, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)

        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height), 0)

        if self.text != "":
            font = pygame.font.SysFont("comicsans", 30)
            text = font.render(self.text, 1, (251, 245, 243))
            win.blit(text, 
                    (
                    self.x + (self.width / 2 - text.get_width() / 2),
                    self.y + (self.height / 2 - text.get_height() / 2))
                    )

    #this method checks if button has been clicked
    def isOver(self, pos):
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True

        return False

#creating the button objects for each game
snakeButton = button((20, 17, 15), 100, 300, 200, 100, "Play Snake")
pongButton = button((20, 17, 15), 500, 300,200, 100, "Play Pong")

#main game loop
while True:
    for event in pygame.event.get():
        pos = pygame.mouse.get_pos()

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if snakeButton.isOver(pos):
                screen = pygame.display.set_mode((800,800))
                pygame.display.update()
                pygame.display.set_caption("Snake")
                snake.menu()
            elif pongButton.isOver(pos):
                pong.menu()
                
    screen.fill((255,255,255))
    snakeButton.draw(screen)
    pongButton.draw(screen)
    pygame.display.update()
    clock.tick(fps)