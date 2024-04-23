import pygame
from pygame.sprite import Group
from character import Character
from letter import Letter
from menu import Menu
import os
import pickle
class Game:
    def __init__(self):
        self.WIDTH = 1000
        self.HEIGHT = 700
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.FONT = pygame.font.SysFont(None, 36)
        self.window = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Running Bro")
        new_icon = pygame.image.load(r'images/icon.jpg') 
        pygame.display.set_icon(new_icon)
        self.clock = pygame.time.Clock()
        self.all_sprites = Group()
        self.letters_group = Group()
        self.background = pygame.image.load(r"images/gp.jpg").convert()
        self.background = pygame.transform.scale(self.background, (self.WIDTH, self.HEIGHT))
        self.mbappe = Character(self.all_sprites)
        self.all_sprites.add(self.mbappe)
        self.lives = 3
        self.game_over_image = pygame.image.load(r"images/GO.jpg").convert_alpha()
        self.game_over_image = pygame.transform.scale(self.game_over_image, (self.WIDTH, self.HEIGHT))
        self.menu = Menu(self.window, self)
        self.game_over = False
        self.start_time = 0
        self.progress_bar_width = 0
        self.explosion_image = pygame.image.load(r"images/explode.gif")
        self.explosion_rect = self.explosion_image.get_rect()
        self.level_speeds = {
            1: 2,
            2: 2.5,
            3: 3,
            4: 3.5,
            5: 4,
            6: 4.5,
            7: 5,
            8: 5.5,
            9: 6,
            10: 7,
        }
        self.level = 1
        self.stars_per_level = [0] * 10  # Khởi tạo số sao đạt được cho mỗi cấp độ
    def draw_text(self, text, font, color, x, y):
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(topleft=(x, y))
        self.window.blit(text_surface, text_rect)
    def run(self):
        running = True
        while running:
            self.clock.tick(60) 
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    for letter in self.letters_group:
                        if event.unicode.lower() == letter.letter.lower():
                            if letter.color == "green":
                                self.slow_speed()
                            self.letters_group.remove(letter)
                            self.all_sprites.remove(letter)
                            if letter.color == "red":
                                self.explode(letter)
                            self.letters_group.remove(letter)
                            self.all_sprites.remove(letter)
                            break
            
            if not self.game_over:
                if len(self.letters_group) < 5:
                    speed = self.level_speeds.get(self.level, 2)
                    new_letter = Letter(self.mbappe.rect, speed, self.letters_group, self.all_sprites, self.level)
                    self.all_sprites.add(new_letter)
                    self.letters_group.add(new_letter)

                hits = pygame.sprite.spritecollide(self.mbappe, self.letters_group, True)
                if hits:
                    self.lives -= 1
                    if self.lives <= 0:
                        self.game_over = True

                self.all_sprites.update()
                self.window.blit(self.background, (0, 0))
                self.all_sprites.draw(self.window)
                self.draw_text(f"Lives: {self.lives}", self.FONT, self.WHITE, 10, 50)
                self.draw_text(f"Level: {self.level}", self.FONT, self.WHITE, self.WIDTH - 150, 10)
                self.draw_text(f"Speed: {self.level_speeds.get(self.level, 2)}", self.FONT, self.WHITE, self.WIDTH - 150, 50)
                '''Xử lý khi thua'''
                if self.game_over:
                    self.window.blit(self.game_over_image, (0, 0))
                    pygame.display.flip()
                    pygame.time.delay(1000)
                    self.reset_game()
                else:
                    if self.start_time != 0:
                        current_time = pygame.time.get_ticks() #Thời gian từ khi mở game
                        elapsed_time = (current_time - self.start_time) / 1000 # Thời gian trong màn hình game
                        max_time = 30
                        self.progress_bar_width = min(1, elapsed_time / max_time) * self.WIDTH
                        pygame.draw.rect(self.window, self.WHITE, (0, self.HEIGHT - 20, self.progress_bar_width, 20))
                        if elapsed_time >= max_time:
                            stars = min(3, self.lives)
                            self.stars_per_level[self.level - 1] = stars  # Cập nhật số sao đạt được cho mỗi cấp độ
                            self.window.blit(self.background, (0, 0))
                            self.draw_text(f"You've earned {stars} stars!", self.FONT, self.WHITE, 400, 300)
                            pygame.display.flip()
                            pygame.time.delay(3000)
                            self.reset_game()
                    else:
                        self.start_time = pygame.time.get_ticks()

            pygame.display.flip()


    def reset_game(self):
        Letter.red_count_global = 0 
        Letter.green_count_global = 0 
        Letter.green_last_spawn_time = 0 
        Letter.red_last_spawn_time = 0
        self.all_sprites.empty()
        self.letters_group.empty()
        self.mbappe.rect.topleft = (50, 390)
        self.all_sprites.add(self.mbappe)
        self.lives = 3
        self.start_time = 0
        self.game_over = False
        self.menu.run(self.stars_per_level)  # Truyền số sao đạt được cho mỗi cấp độ vào menu
    def slow_speed(self):
        for letter in self.letters_group:
            if letter.color != "green":
                letter.speed = 1
                letter.last_green_typed_time = pygame.time.get_ticks()

    def explode(self, letter):
        self.explosion_rect.center = letter.rect.center
        self.window.blit(self.explosion_image, self.explosion_rect)
        pygame.display.flip()
        pygame.time.delay(100)
        
        self.letters_group.empty()
        self.all_sprites.empty()
        self.mbappe.rect.topleft = (50, 390)
        self.all_sprites.add(self.mbappe)

    def save_game(self):
    # Tạo dictionary chứa trạng thái của game
        game_state = {
            'level': self.level,
            'lives': self.lives,
            'stars_per_level': self.stars_per_level,  # Lưu trạng thái số sao đạt được cho mỗi cấp độ
        }
        # Tạo đường dẫn đến thư mục lưu trữ
        save_directory = "D:\\code\\Running Bro\\savegame"
        # Tạo đường dẫn đến file save_game
        save_path = os.path.join(save_directory, 'game_state.pkl')
        # Mở file và lưu trạng thái của game vào file
        with open(save_path, 'wb') as file:
            pickle.dump(game_state, file)
        print('Đã lưu')
        # Cập nhật dữ liệu stars_per_level trên menu
        self.menu.stars_per_level = self.stars_per_level

    def load_game(self):
        save_directory = "D:\\code\\Running Bro\\savegame"
        save_path = os.path.join(save_directory, 'game_state.pkl')
        try:
            with open(save_path, 'rb') as file:
                game_state = pickle.load(file)
            self.level = game_state['level']
            self.lives = game_state['lives']
            self.stars_per_level = game_state.get('stars_per_level', [0] * 10)  # Load lại số sao đạt được cho mỗi cấp độ
            
            # Reset lại trò chơi
            self.reset_game()
            
            print("Số sao đã tải:", self.stars_per_level)  # Thêm dòng này để kiểm tra dữ liệu đã tải
            # Cập nhật dữ liệu stars_per_level trên menu
            self.menu.stars_per_level = self.stars_per_level
            self.menu.run(self.stars_per_level)  # Thay đổi menu ngay sau khi load game
        except FileNotFoundError:
            print("Không tìm thấy trò chơi đã lưu.")
