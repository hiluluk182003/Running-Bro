import pygame
import random

class Letter(pygame.sprite.Sprite):
    red_count_global = 0
    green_count_global = 0
    green_last_spawn_time = 0
    red_last_spawn_time = 0
    last_green_typed_time = 0

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

        if 7 <= self.level <= 10:
            red_probability = 0.1
            green_probability = 0.1
        elif 3 <= self.level <= 6:
            red_probability = 0.15
            green_probability = 0.15
        else:
            red_probability = 0
            green_probability = 0

        current_time = pygame.time.get_ticks()
        if Letter.red_last_spawn_time + 8000 < current_time and random.random() < red_probability:
            self.color = "red"
            Letter.red_count_global += 1
            Letter.red_last_spawn_time = current_time
        elif Letter.green_last_spawn_time + 8000 < current_time and random.random() < green_probability:
            self.color = "green"
            Letter.green_count_global += 1
            Letter.green_last_spawn_time = current_time
        else:
            self.color = "white"

        self.image = self.font.render(self.letter, True, self.colors[self.color])
        self.rect = self.image.get_rect(midbottom=(1000, random.choice([400, 480, 560])))
        self.spacing = 20


    def update(self):
        self.rect.x -= self.speed
        if self.rect.right < 0:
            self.kill()

        for letter in self.letters_group:
            if self.rect.colliderect(letter.rect) and self != letter:
                self.rect.right = letter.rect.left - self.spacing
                break