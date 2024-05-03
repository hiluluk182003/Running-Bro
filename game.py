import pygame
from pygame.sprite import Group
from character import Character
from letter import Letter
from menu import Menu
import os
import pickle
import random
class Game:
    def __init__(self):
        self.WIDTH = 1000
        self.HEIGHT = 700
        self.GRAY = (150, 150, 150)
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
        self.stars_per_level = [0] * 11  # Khởi tạo số sao đạt được cho mỗi cấp độ
        self.soundlife=pygame.mixer.Sound(r'Sound/life.mp3')
        self.boss = pygame.image.load(r"images/boss.gif")
        self.boss = pygame.transform.scale(self.boss, (300, 200))
        self.rectboss = self.boss.get_rect(topleft=(695, 390))
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
                                self.soundgreenkill = pygame.mixer.Sound(r'Sound/slow.mp3')
                                self.soundgreenkill.play()
                                self.slow_speed()
                            self.letters_group.remove(letter)
                            self.all_sprites.remove(letter)
                            if letter.color == "red":
                                self.soundredkill = pygame.mixer.Sound(r'Sound/boom.mp3')
                                self.soundredkill.play()
                                self.explode(letter)
                            if letter.color == "white":
                                self.soundwhitekill = pygame.mixer.Sound(r'Sound/kill.mp3')
                                self.soundwhitekill.play() 
                            self.letters_group.remove(letter)
                            self.all_sprites.remove(letter)
                            break
            
            if not self.game_over:
                if len(self.letters_group) < 5:
                    if self.level == 11:
                        speed = random.uniform(1, 3)   
                    else:
                        speed = self.level_speeds.get(self.level, 2)
                    new_letter = Letter(self.mbappe.rect, speed, self.letters_group, self.all_sprites, self.level)
                    self.all_sprites.add(new_letter)
                    self.letters_group.add(new_letter)

                hits = pygame.sprite.spritecollide(self.mbappe, self.letters_group, True)
                if hits:
                    self.soundlife.play()
                    self.lives -= 1
                    if self.lives <= 0:
                        self.soundover = pygame.mixer.Sound(r'Sound/gameover.mp3')
                        self.soundover.play()
                        self.game_over = True

                self.all_sprites.update()
                self.window.blit(self.background, (0, 0))
                self.all_sprites.draw(self.window)
                self.draw_text(f"Lives: {self.lives}", self.FONT, self.WHITE, 10, 50)
                self.draw_text(f"Level: {self.level}", self.FONT, self.WHITE, self.WIDTH - 150, 10)
                if self.level != 11:
                    self.draw_text(f"Speed: {self.level_speeds.get(self.level, 2)}", self.FONT, self.WHITE, self.WIDTH - 150, 50)
                else:
                    self.window.blit(self.boss, self.rectboss)
                    for letter in self.letters_group:
                        letter_surface = letter.image
                        position = letter.rect.topleft
                        rotation = random.choice([60, 90, 180])
                        self.transform_letter(letter_surface, position, rotation)
                '''Xử lý khi thua'''
                if self.game_over:
                    self.window.blit(self.game_over_image, (0, 0))
                    pygame.display.flip()
                    pygame.time.delay(3000)
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
                            self.soundwin = pygame.mixer.Sound(r'Sound/win.mp3')
                            self.soundwin.play()
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
        self.running = False  # Dừng luồng tự động gõ phím khi kết thúc trò chơi
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
            self.stars_per_level = game_state.get('stars_per_level', [0] * 11)  # Load lại số sao đạt được cho mỗi cấp độ

            print("Số sao đã tải:", self.stars_per_level)  # Thêm dòng này để kiểm tra dữ liệu đã tải

            # Cập nhật dữ liệu stars_per_level trên menu
            self.menu.stars_per_level = self.stars_per_level
            
            # Kiểm tra mở khóa special level
            self.special_unlocked = self.menu.check_special_unlocked(self.stars_per_level)
            print("Trạng thái mở khóa special level sau khi cập nhật:", self.special_unlocked)

        except FileNotFoundError:
            print("Không tìm thấy trò chơi đã lưu.")


    def handle_auto_typing(self, key):
            for letter in self.letters_group:
                if key.lower() == letter.letter.lower():
                    if letter.color == "green":
                        self.slow_speed()
                    self.letters_group.remove(letter)
                    self.all_sprites.remove(letter)
                    if letter.color == "red":
                        self.explode(letter)
                    break

    def transform_letter(self, letter_surface, position, rotation, rotate_speed=0.3):
        # Xoay chữ cái
        if rotation == 'flip':
            letter_surface = pygame.transform.flip(letter_surface, False, True)
        else:
            letter_surface = pygame.transform.rotate(letter_surface, rotation * rotate_speed)
        
        # Vị trí hiển thị chữ cái
        x, y = position
        if rotation == 90:
            x += letter_surface.get_height() + 20
        elif rotation == 180 or rotation == 'flip':
            y -= letter_surface.get_width() + 20
        else:
            y -= 20

        self.window.blit(letter_surface, (x, y))
