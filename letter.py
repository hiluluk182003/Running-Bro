import pygame
import random

class Letter(pygame.sprite.Sprite):
    red_count_global = 0  # Khai báo thuộc tính red_count_global
    green_count_global = 0  # Khai báo thuộc tính green_count_global
    green_last_spawn_time = 0  # Biến lớp để theo dõi thời gian giữa các lần xuất hiện của chữ xanh
    red_last_spawn_time = 0  # Biến lớp để theo dõi thời gian giữa các lần xuất hiện của chữ đỏ

    def __init__(self, mbappe_rect, speed, letters_group, all_sprites, level):
        super().__init__()
        self.letters_group = letters_group
        self.all_sprites = all_sprites
        self.mbappe_rect = mbappe_rect
        self.speed = speed
        self.letter = random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
        self.font = pygame.font.SysFont(None, 50)
        self.colors = {
            "white": (255, 255, 255),
            "red": (255, 0, 0),
            "green": (0, 255, 0)
        }
        self.level = level

        # Xác định xác suất xuất hiện của màu đỏ và xanh tùy theo vòng hiện tại
        if 7 <= self.level <= 10:
            red_probability = 0.1 if Letter.red_count_global == 0 else 0
            green_probability = 0.1 if Letter.green_count_global < 2 else 0
        elif 3 <= self.level <= 6:
            red_probability = 0 if Letter.red_count_global > 0 else 0.1
            green_probability = 0 if Letter.green_count_global == 2 else 0.1
        else:
            red_probability = 0
            green_probability = 0

        # Kiểm tra xem đã đủ thời gian chưa để tạo mới chữ xanh hoặc đỏ
        current_time = pygame.time.get_ticks()
        if Letter.red_last_spawn_time + 5000 < current_time and random.random() < red_probability:
            self.color = "red"
            Letter.red_count_global += 1
            Letter.red_last_spawn_time = current_time
        elif Letter.green_last_spawn_time + 5000 < current_time and random.random() < green_probability:
            self.color = "green"
            Letter.green_count_global += 1
            Letter.green_last_spawn_time = current_time
        else:
            self.color = "white"

        self.image = self.font.render(self.letter, True, self.colors[self.color])
        self.rect = self.image.get_rect(midbottom=(1000, random.choice([400, 480, 560])))
        self.spacing = 20  # Khoảng cách giữa các chữ cái 

    def update(self):
        self.rect.x -= self.speed
        if self.rect.right < 0:
            self.kill()
# Kiểm tra va chạm với các chữ cái khác và xử lý vị trí
        for letter in self.letters_group:
            if self.rect.colliderect(letter.rect) and self != letter:
                self.rect.right = letter.rect.left - self.spacing
                break
