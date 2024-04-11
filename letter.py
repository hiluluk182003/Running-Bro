import pygame
import random
'''
Khởi tạo các chữ
'''
class Letter(pygame.sprite.Sprite):
    def __init__(self, mbappe_rect, speed, letters_group, all_sprites):
        super().__init__()
        self.letters_group = letters_group
        self.all_sprites = all_sprites
        self.mbappe_rect = mbappe_rect
        self.speed = speed
        self.letter = random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
        self.font = pygame.font.SysFont(None, 50)
        self.WHITE = (255, 255, 255)
        self.image = self.font.render(self.letter, True, self.WHITE)
        self.ranged = random.choice([400, 480, 560])
        self.rect = self.image.get_rect(midbottom=(1000, self.ranged))
        self.spacing = 20  # Khoảng cách giữa các chữ cái

    def update(self):
        self.rect.x -= self.speed
        if self.rect.right < 0:
            self.kill()

        # Kiểm tra va chạm với các chữ cái khác và xử lý vị trí
        for letter in self.letters_group:
            if self.rect.colliderect(letter.rect) and self != letter:
                # Đặt vị trí của chữ cái hiện tại ngay sau chữ cái khác
                self.rect.right = letter.rect.left - self.spacing
                break
