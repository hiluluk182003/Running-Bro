from letter import *
import pygame

class AI:
    def __init__(self):
        self.font = pygame.font.SysFont(None, 50)  # Font cho chữ cái hiển thị

    def get_displayed_letter(self, game):
        # Lấy chữ cái đang hiển thị trên màn hình
        displayed_letter = None
        for sprite in game.all_sprites:
            if isinstance(sprite, Letter):
                displayed_letter = sprite.letter
                break
        return displayed_letter

    def type_correct_letter(self, game):
        # Tìm kiếm và gõ đúng chữ cái hiển thị
        displayed_letter = self.get_displayed_letter(game)
        if displayed_letter:
            # Xác định mã ASCII của chữ cái
            letter_ascii = ord(displayed_letter.upper())
            # Kiểm tra khi nào phím tương ứng được nhấn
            keys = pygame.key.get_pressed()
            if keys[letter_ascii]:
                # Gửi mã phím đó đến trò chơi
                game.handle_key_press(displayed_letter)
