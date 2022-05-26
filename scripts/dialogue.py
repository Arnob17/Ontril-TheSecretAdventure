import pygame

class DialogueBox:

    X_POS = 60
    Y_POS = 470

    def __init__(self):
        self.box = pygame.image.load('dialogs/dialog_box.png')

        self.box = pygame.transform.scale(self.box, (700, 100))

        self.texts = ['what is your name?', 'My name is Arnob', 'How are you?']

        self.letter_index = 0

        self.text_index = 0

        self.font = pygame.font.Font('dialogs/dialog_font.ttf', 18)

        self.reading = False

    def execute (self, dialog=[]) :
        if self.reading:
            self.next_text()
        else:
            self.reading = True
            self.text_index = 0
            self.texts = dialog
    
    def render (self, screen) :

        if self.reading:
            self.letter_index += 1

            if self.letter_index >= len(self.texts[self.text_index]):
                self.letter_index = self.letter_index
                pygame.mixer.Channel(4).stop()

            screen.blit(self.box, (self.X_POS, self.Y_POS))

            text = self.font.render(self.texts[self.text_index][0:self.letter_index], False, (0, 0, 0))
    
            screen.blit(text, (self.X_POS + 60, self.Y_POS + 30))

    def next_text ( self ):
        self.text_index += 1
        self.letter_index = 0
        if self.text_index >= len(self.texts):
            # self.text_index = 0
            self.reading = False

    def musicPlayer(self):
        if self.reading:
            pygame.mixer.Channel(4).play(pygame.mixer.Sound('assets/typing.wav'))
        else:
            pygame.mixer.Channel(4).stop()