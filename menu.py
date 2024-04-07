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
        self.clock = pygame.time.Clock()
        # Các cấp độ sẽ được lưu trong một danh sách
        self.levels = [
            {"name": "Level 1"},
            {"name": "Level 2"},
            {"name": "Level 3"},
            {"name": "Level 4"},
            {"name": "Level 5"},
            {"name": "Level 6"},
        ]

    def draw_text(self, text, font, color, x, y):
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.topleft = (x, y)
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
                            print(f"Selected level: {i+1}")
                            running = False
                            break

            for i, level in enumerate(self.levels):
                text = f"{level['name']}"
                if i + 1 in range(1, len(self.game.level_status) + 2):
                    stars = self.game.level_status.get(i + 1, 0)
                    text += " " + "★" * stars
                self.draw_text(text, self.FONT, self.WHITE, 50, 50 + 50 * i)

            pygame.display.flip()
            self.clock.tick(60)