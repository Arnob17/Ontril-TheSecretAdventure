import pygame

from scripts.run import Game

if __name__ == '__main__':
    pygame.init()
    game = Game()
    game.main_menu()