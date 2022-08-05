import pygame, sys, pytmx, pyscroll
from scripts.dialogue import DialogueBox
from scripts.map import MapManager

from scripts.player import Player
from scripts.storyTeller import StoryTell
from scripts.toggleMap import Toggle
from scripts.endScreen import end

class Game:
    def __init__(self):
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((1000, 600), pygame.RESIZABLE)
        pygame.display.set_caption('Ontril: The Secret Adventure')
        pygame.display.set_icon(pygame.image.load('assets/favIco.PNG'))
        self.player = Player()

        self.map_manager = MapManager(self.screen, self.player)

        self.dialog_box = DialogueBox()

        self.storyTell = StoryTell()

        self.end = end()

        self.toggle = Toggle()

    def handle_input(self):
        pressed = pygame.key.get_pressed()

        if pressed[pygame.K_UP] or pressed[pygame.K_w]:
            self.player.move_up()

        elif pressed[pygame.K_DOWN] or pressed[pygame.K_s]:
            self.player.move_down()

        elif pressed[pygame.K_RIGHT] or pressed[pygame.K_d]:
            self.player.move_right()

        elif pressed[pygame.K_LCTRL] and pressed[pygame.K_RIGHT]:
            self.player.boost_move_right()

        elif pressed[pygame.K_LEFT] or pressed[pygame.K_a]:
            self.player.move_left()

    def update(self):
        self.map_manager.update()

    def run(self):

        clock = pygame.time.Clock()
        pygame.mixer.Channel(1).set_volume(0.10)
        pygame.mixer.Channel(0).play(pygame.mixer.Sound('assets/wave.mp3'), -1)
        pygame.mixer.Channel(1).play(pygame.mixer.Sound('assets/rexaa.wav'), -1)
        run = True
        while True:
            self.player.save_location()
            self.handle_input()
            self.update()
            self.map_manager.draw()
            self.dialog_box.render(self.screen)
            self.storyTell.render(self.screen)
            self.toggle.render(self.screen)
            self.end.render(self.screen)
            pygame.display.flip()

            for events in pygame.event.get():
                if events.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif events.type == pygame.KEYDOWN:
                    if events.key == pygame.K_SPACE:
                        self.map_manager.check_npc_collision(self.dialog_box)
                    if events.key == pygame.K_SPACE:
                        self.storyTell.execute()
                        self.storyTell.musicPlay()
                    if events.key == pygame.K_ESCAPE:
                        self.toggle.executeText(text=[
                            "Press 'e' for CutScene",
                            "Press 'm' for see MAP",
                            "Use HeadPhones!",
                            'Enjoy!',
                        ])
                    if events.key == pygame.K_m:
                        self.toggle.execture_map()
                    if self.map_manager.current_map == 'samirland' and events.key == pygame.K_SPACE:
                        point = self.map_manager.get_object('endingscreen')
                        rect = pygame.Rect(point.x, point.y, point.width, point.height)
                        if self.player.feet.colliderect(rect):
                            self.end.execute()

            clock.tick(60)
    
    def main_menu(self):
        pygame.mixer.Channel(5).play(pygame.mixer.Sound('assets/rexaa.wav'), -1)
        font = pygame.font.Font('dialogs/dialog_font.ttf', 17)
        run = True
        while True:
            self.screen.fill([0, 0, 0])
            text = font.render('Press Space', False, (255, 255, 255))
            self.screen.blit(pygame.image.load('assets/favico.PNG'), (0, 0))
            self.screen.blit(text, (300, 300))
            press = pygame.key.get_pressed()

            if press[pygame.K_SPACE]:
                pygame.mixer.Channel(5).stop()
                self.run()

            for xy in pygame.event.get():
                if xy.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.flip()
