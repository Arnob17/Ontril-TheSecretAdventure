import pygame, json

class end:

    X_POS = 80
    Y_POS = 200

    def __init__(self):

        self.texts = ['Ontril: The Secret Adventure', 'The game has been finished', 'I know.. this is pretty small', 'But I will comeback!', 'Thanks for playing.', 'Bye..']

        self.letter_index = 0

        self.text_index = 0

        self.font = pygame.font.Font('dialogs/dialog_font.ttf', 18)

        self.reading = False

        self.toggle = False

    def execute (self) :
        if self.reading:
            self.next_text()
        else:
            self.reading = True
            self.text_index = 0

    
    def render (self, screen) :

        if self.reading:
            self.letter_index += 1

            if self.letter_index >= len(self.texts[self.text_index]):
                self.letter_index = self.letter_index
                pygame.mixer.Channel(5).stop()

            screen.fill([0, 0, 0])

            text = self.font.render(self.texts[self.text_index][0:self.letter_index], False, (255, 255, 255))
    
            screen.blit(text, (self.X_POS + 60, self.Y_POS + 30))

        if self.toggle:
            self.letter_index += 1

            if self.letter_index >= len(self.texts[self.text_index]):
                self.letter_index = self.letter_index
                pygame.mixer.Channel(5).stop()

            screen.fill([0, 0, 0])

            text = self.font.render(self.texts[self.text_index][0:self.letter_index], False, (255, 255, 255))
    
            screen.blit(text, (self.X_POS + 60, self.Y_POS + 30))

    def next_text ( self ):
        self.text_index += 1
        self.letter_index = 0
        if self.text_index >= len(self.texts):
            # self.text_index = 0
            self.reading = False
            self.toggle = False

    def musicPlay(self):
        if self.reading:
            pygame.mixer.Channel(3).play(pygame.mixer.Sound('assets/typing.wav'))
        else:
            pygame.mixer.Channel(3).stop()