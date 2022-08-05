import pygame

class Toggle:

    X_POS = 0
    Y_POS = 0

    def __init__(self):
        self.box = pygame.image.load('dialogs/dialog_box.png')

        self.text = ''

        self.text_index = 0

        self.reading = False

        self.font = pygame.font.Font('dialogs/dialog_font.ttf', 13)
        
        self.letter_index = 0

        self.open = False

    def executeText(self, text=[]):
        if self.reading:
            self.next_text()
        else:
            self.reading = True
            self.text_index = 0
            self.texts = text

    def execture_map(self):
        if self.open:
            self.open = False
        else:
            self.open = True

    def render (self, screen) :

        if self.reading:
            self.letter_index += 1

            if self.letter_index >= len(self.texts[self.text_index]):
                self.letter_index = self.letter_index

            screen.blit(self.box, (self.X_POS, self.Y_POS))

            text = self.font.render(self.texts[self.text_index][0:self.letter_index], False, (0, 0, 0))
    
            screen.blit(text, (self.X_POS + 30, self.Y_POS + 15))

        if self.open:

            east = self.font.render('East', False, (255, 255, 25))
            west = self.font.render('West', False, (255, 255, 25))
            south = self.font.render('South', False, (255, 255, 25))
            north = self.font.render('North', False, (255, 255, 25))

            screen.fill([0, 0, 0])

            screen.blit(pygame.image.load('assets/MINI-map.PNG'), (400, 185))
            screen.blit(east, (500, 50))
            screen.blit(west, (500, 550))
            screen.blit(north, (200, 300))
            screen.blit(south, (800, 300))

    def next_text ( self ):
        self.text_index += 1
        self.letter_index = 0
        if self.text_index >= len(self.texts):
            # self.text_index = 0
            self.reading = False