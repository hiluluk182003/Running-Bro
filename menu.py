import pygame
import sys
from autoplay import AutoPlay

class Menu:
    def __init__(self, screen, game):
        self.screen = screen
        self.game = game
        self.WIDTH = screen.get_width()
        self.HEIGHT = screen.get_height()
        self.BG = pygame.image.load(r'images/background.jpg')
        self.WHITE = (255, 255, 255)
        self.GRAY = (150, 150, 150)
        self.FONT = pygame.font.SysFont(None, 36)
        self.bigFONT = pygame.font.SysFont(None, 60)
        self.clock = pygame.time.Clock()
        self.auto_play = False  # Thêm thuộc tính để đánh dấu chế độ autoplay
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
    def set_auto_play(self, value):
                self.auto_play = value
    def run(self, stars_per_level):
        special_unlocked = self.check_special_unlocked(stars_per_level)  # Kiểm tra trạng thái mở khóa của Special level
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
                                continue  # Bỏ qua việc chọn Special level nếu chưa mở khóa
                            else:
                                self.game.level = i + 1
                                if self.auto_play:
                                    return  # Trả về mà không chạy trò chơi
                                else:
                                    self.game.run()  # Chạy trò chơi sau khi chọn cấp độ
                                return stars_per_level  # Trả về stars_per_level sau khi chọn level
                    if self.load_button_rect.collidepoint(x, y):
                        self.game.load_game()
                        # Cập nhật lại stars_per_level sau khi load game
                        stars_per_level = self.game.stars_per_level
                    elif self.save_button_rect.collidepoint(x, y):
                        self.game.save_game()
                    elif self.AI_button.collidepoint(x, y):
                        # Gọi chức năng AutoPlay khi nhấp vào nút AutoPlay
                        ai = AutoPlay(self.game, stars_per_level, self.auto_play)
                        ai.auto_play_level()
                        return stars_per_level
            for i, level in enumerate(self.levels):
                level_name = level["name"]
                stars = stars_per_level[i] if i < len(stars_per_level) else 0
                color = self.WHITE if special_unlocked or level_name != "Special!!!" else self.GRAY  # Chọn màu sắc
                self.draw_text(f"{level_name} - Star: {stars}", self.FONT, color, 50, 50 + 50 * i)
            self.load_button_rect = pygame.Rect(450, 320, 100, 40)
            self.save_button_rect = pygame.Rect(450, 260, 100, 40)
            self.draw_text("Load", self.bigFONT, self.WHITE, 450, 320)
            self.draw_text("Save", self.bigFONT, self.WHITE, 450, 260)
            self.AI_button = pygame.Rect(450, 380, 100, 40)
            self.draw_text("AutoPlay", self.bigFONT, self.WHITE, 450, 380)
            pygame.display.flip()
            self.clock.tick(60)

    def check_special_unlocked(self, stars_per_level):
        # Kiểm tra điều kiện để mở cấp độ đặc biệt
        completed_levels = len([stars for stars in stars_per_level if stars == 3])
        return completed_levels >= 10  # Mở cấp độ đặc biệt nếu đã hoàn thành 10 level với mỗi level đạt 3 sao
