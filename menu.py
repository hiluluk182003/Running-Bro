import pygame
import sys

class Menu:
    def __init__(self, screen, game):
        self.screen = screen
        self.game = game
        self.WIDTH = screen.get_width()
        self.HEIGHT = screen.get_height()
        self.BG = pygame.image.load(r'images/background.jpg')
        self.WHITE = (255, 255, 255)
        self.FONT = pygame.font.SysFont(None, 36)
        self.STAR_IMAGE = pygame.image.load(r'images/star.png')
        self.clock = pygame.time.Clock()
        self.levels = [
            {"name": "Level 1"},
            {"name": "Level 2"},
            {"name": "Level 3"},
            {"name": "Level 4"},
            {"name": "Level 5"},
            {"name": "Level 6"},
            {"name": "Level 7"},
            {"name": "Level 8"},
            {"name": "Level 9"},
            {"name": "Level 10"},
        ]

    def draw_text(self, text, font, color, x, y):
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(topleft=(x, y))
        self.screen.blit(text_surface, text_rect)

    def run(self, stars=0):
        running = True
        while running:
            self.screen.blit(self.BG, (0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    for i, level in enumerate(self.levels):
                        level_rect = pygame.Rect(50, 50 + 50 * i, 200, 40)
                        if level_rect.collidepoint(x, y):
                            running = False
                            break
            
            # Vẽ các cấp độ lên màn hình
            for i, level in enumerate(self.levels):
                self.draw_text(level["name"], self.FONT, self.WHITE, 50, 50 + 50 * i)

            pygame.display.flip()
            self.clock.tick(60)

        # Gọi phương thức display_stars với số sao tương ứng
        self.display_stars(stars)

    def display_stars(self, stars):
        self.screen.blit(self.BG, (0, 0))
        self.draw_text(f"You've earned {stars} stars!", self.FONT, self.WHITE, 350, self.HEIGHT // 2)
        # Vẽ số sao tương ứng
        star_width = self.STAR_IMAGE.get_width()
        for i in range(stars):
            self.screen.blit(self.STAR_IMAGE, (self.WIDTH // 2 + i * (star_width + 10), self.HEIGHT // 2 + 50))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                return
