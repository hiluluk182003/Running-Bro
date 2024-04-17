import pygame
import sys
from game import Game

class MainMenu:
    def __init__(self, screen, game):
        self.screen = screen
        self.game = game
        self.WIDTH = screen.get_width()
        self.HEIGHT = screen.get_height()
        self.BG = pygame.image.load(r'images/background.jpg')
        self.play_button = pygame.image.load(r'images/playbutton.PNG')
        self.play_button= pygame.transform.scale(self.play_button, (300, 230))
        self.play_rect = self.play_button.get_rect(center=(500, 300))
        self.clock = pygame.time.Clock()

    def run(self):
        running = True
        while running:
            self.screen.blit(self.BG, (0, 0))
            self.screen.blit(self.play_button, self.play_rect)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    if self.play_rect.collidepoint(x, y):
                        running = False
                        self.game.menu.run()

            pygame.display.flip()
            self.clock.tick(60)