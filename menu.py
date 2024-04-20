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
        self.bigFONT = pygame.font.SysFont(None, 60)
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

    def run(self, stars_per_level):
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
                            self.game.level = i + 1
                            running = False
                            break
                        # Kiểm tra nếu nhấn vào nút Load
                    if self.load_button_rect.collidepoint(x, y):
                            self.game.load_game()  # Gọi phương thức load_game từ Game
                            print("Số sao đã tải:", stars)
                        # Kiểm tra nếu nhấn vào nút Save
                    elif self.save_button_rect.collidepoint(x, y):
                            self.game.save_game()  # Gọi phương thức save_game từ Game
            for i, level in enumerate(self.levels):
                level_name = level["name"]
                stars = stars_per_level[i] if i < len(stars_per_level) else 0  # Số sao tương ứng với cấp độ
                self.draw_text(f"{level_name} - Star: {stars}", self.FONT, self.WHITE, 50, 50 + 50 * i)
            self.load_button_rect = pygame.Rect(450, 320, 100, 40)
            self.save_button_rect = pygame.Rect(450, 260, 100, 40)       
            self.draw_text("Load", self.bigFONT, self.WHITE, 450, 320)
            self.draw_text("Save", self.bigFONT, self.WHITE, 450, 260)
            pygame.display.flip()
            self.clock.tick(60)

        return stars_per_level
