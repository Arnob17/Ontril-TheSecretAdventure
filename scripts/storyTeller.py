import pygame, json

class StoryTell:

    X_POS = 80
    Y_POS = 200

    def __init__(self):

        self.texts = ['Many days ago...', 'A boy was with his 6 friends..', 'They were spending their time well..BUT', 'Something goes wrong.. AND', 'They get separated', 'Welcome to the Ontril: The secret adventure!', 'FIND THE MYSTERY!', 'ENJOY!']

        self.letter_index = 0

        self.text_index = 0

        self.font = pygame.font.Font('dialogs/dialog_font.ttf', 18)

        self.reading = True

        self.toggle = False

        data = {
            'reading' : "true"
        }
    

        with open('data.txt', 'r') as data_file:
            data = json.load(data_file)
            if data['reading'] == 'true':
                self.reading = False

        data['reading'] = 'true'

        with open('data.txt', 'w') as data_files:
            json.dump(data, data_files)

    def execute (self) :
        if self.reading:
            self.next_text()
        else:
            # self.reading = True
            self.text_index = 0


    def execute_toggle(self, texts=[]):
        if self.toggle:
            self.next_text()
        else:
            self.toggle = True
            self.texts = texts
            self.letter_index = 0
    
    def render (self, screen) :

        if self.reading:
            self.letter_index += 1

            if self.letter_index >= len(self.texts[self.text_index]):
                self.letter_index = self.letter_index
                pygame.mixer.Channel(3).stop()

            screen.fill([0, 0, 0])

            text = self.font.render(self.texts[self.text_index][0:self.letter_index], False, (255, 255, 255))
    
            screen.blit(text, (self.X_POS + 60, self.Y_POS + 30))

        if self.toggle:
            self.letter_index += 1

            if self.letter_index >= len(self.texts[self.text_index]):
                self.letter_index = self.letter_index
                pygame.mixer.Channel(3).stop()

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