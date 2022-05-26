import sys
import pygame

class MainMenu:
    def __init__(self, screen):
        self.favico = pygame.image.load('assets/favico.PNG')
        # self.screen.fill([106, 210, 255]) 
        self.screen = screen

    def blit(self):
        run = True
        while True:
            self.screen.fill([106, 210, 255])
            self.screen.blit(self.favico, (0, 0))
            for x in pygame.event.get():
                if x.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()