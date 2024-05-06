import pygame
import sys
from autoplay import AutoPlay

class Menu:
    """
    Lớp Menu đại diện cho menu trong trò chơi.

    Attributes:
        screen (Surface): Màn hình trò chơi.
        game (Game): Đối tượng trò chơi.
        WIDTH (int): Độ rộng của màn hình trò chơi.
        HEIGHT (int): Độ cao của màn hình trò chơi.
        BG (Surface): Hình nền của menu.
        WHITE (tuple): Màu trắng.
        GRAY (tuple): Màu xám.
        hover (tuple): Màu sắc khi nút được hover qua.
        FONT (Font): Font chữ cho văn bản.
        bigFONT (Font): Font chữ lớn cho văn bản tiêu đề.
        clock (Clock): Đồng hồ để kiểm soát tốc độ khung hình.
        levels (list): Danh sách các cấp độ trong trò chơi.
    """
    def __init__(self, screen, game):
        """
        Khởi tạo menu.

        Args:
            screen (Surface): Màn hình trò chơi.
            game (Game): Đối tượng trò chơi.
        """
        self.screen = screen
        self.game = game
        self.WIDTH = screen.get_width()
        self.HEIGHT = screen.get_height()
        self.BG = pygame.image.load(r'images/background.jpg')
        self.WHITE = (255, 255, 255)
        self.GRAY = (150, 150, 150)
        self.hover = (200,200,200)
        self.FONT = pygame.font.SysFont(None, 36)
        self.bigFONT = pygame.font.SysFont(None, 60)
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
            {"name": "Special!!!"},  # Đặt tên cấp độ đặc biệt
        ]

    def draw_text(self, text, font, color, x, y):
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(topleft=(x, y))
        self.screen.blit(text_surface, text_rect)
    def run(self, stars_per_level):
        """
        Chạy menu.

        Args:
            stars_per_level (list): Số sao đạt được cho mỗi cấp độ.
        """
        special_unlocked = self.check_special_unlocked(stars_per_level)
        while True:
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
                            if level["name"] == "Special!!!" and not special_unlocked:
                                continue
                            else:
                                self.game.level = i + 1
                                return stars_per_level
                    if self.load_button_rect.collidepoint(x, y):
                        self.game.load_game()
                        stars_per_level = self.game.stars_per_level
                        special_unlocked = self.check_special_unlocked(stars_per_level)
                    elif self.save_button_rect.collidepoint(x, y):
                        self.soundok = pygame.mixer.Sound(r'Sound/save.mp3')
                        self.soundok.play()
                        self.game.save_game()
                    elif self.AI_button.collidepoint(x, y):
                        ai = AutoPlay(self.game, stars_per_level)
                        ai.auto_play_level()
                        return stars_per_level

            # Vẽ các nút và kiểm tra hover
            for i, level in enumerate(self.levels):
                level_name = level["name"]
                stars = stars_per_level[i] if i < len(stars_per_level) else 0
                color = self.WHITE if special_unlocked or level_name != "Special!!!" else self.GRAY
                # Kiểm tra khi nào chuột di chuyển qua nút và cập nhật màu sắc
                level_rect = pygame.Rect(50, 50 + 50 * i, 200, 40)
                if level_rect.collidepoint(pygame.mouse.get_pos()):
                    color = self.hover  # Màu sắc khi hover qua
                self.draw_text(f"{level_name} - Star: {stars}", self.FONT, color, 50, 50 + 50 * i)

            self.load_button_rect = pygame.Rect(450, 320, 100, 40)
            self.save_button_rect = pygame.Rect(450, 260, 100, 40)
            self.AI_button = pygame.Rect(450, 380, 100, 40)
            self.draw_text("Load", self.bigFONT, self.hover if self.load_button_rect.collidepoint(pygame.mouse.get_pos()) else self.WHITE, 450, 320)
            self.draw_text("Save", self.bigFONT, self.hover if self.save_button_rect.collidepoint(pygame.mouse.get_pos()) else self.WHITE, 450, 260)
            self.draw_text("AutoPlay", self.bigFONT, self.hover if self.AI_button.collidepoint(pygame.mouse.get_pos()) else self.WHITE, 450, 380)

            pygame.display.flip()
            self.clock.tick(60)



    def check_special_unlocked(self, stars_per_level):
        """Kiểm tra điều kiện để mở cấp độ đặc biệt"""
        completed_levels = len([stars for stars in stars_per_level if stars == 3])
        return completed_levels >= 10  # Mở cấp độ đặc biệt nếu đã hoàn thành 10 level với mỗi level đạt 3 sao
