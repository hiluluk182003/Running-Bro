import pygame

class Character(pygame.sprite.Sprite):
    '''
    Khởi tạo nhân vật
    '''
    def __init__(self, all_sprites):
        super().__init__()
        self.image = pygame.image.load(r"images/mbappe.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (300, 200))
        self.rect = self.image.get_rect(topleft=(50, 390))
        self.all_sprites = all_sprites