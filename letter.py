import pygame
import random

class Letter:
    """
    Class đại diện cho mỗi chữ cái trong trò chơi.
    """

    def __init__(self, lane):
        """
        Khởi tạo một đối tượng Letter với lane và tốc độ di chuyển.
        """
        self.letters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
        self.font = pygame.font.SysFont(None, 50)
        self.WHITE = (255, 255, 255)
        self.letter_images = {letter: self.font.render(letter, True, self.WHITE) for letter in self.letters}
        self.letter = random.choice(self.letters)
        self.image = self.letter_images[self.letter]
        self.speed = 1
        self.lane = lane
        self.rect = self.image.get_rect(midbottom=(1000, self.lane))

    def update(self):
        """
        Cập nhật vị trí của chữ cái dựa trên tốc độ di chuyển.
        """
        self.rect.x -= self.speed
