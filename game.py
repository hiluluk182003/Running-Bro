import pygame
from pygame.sprite import Group
from character import Character
from letter import Letter
from menu import Menu

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
        self.start_time = 0  # Thời gian bắt đầu chơi
        self.progress_bar_width = 0  # Chiều rộng của thanh tiến trình
        # Load hình ảnh hoặc gif cho hiệu ứng nổ
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
            # Thêm các cấp độ khác ở đây
        }
        self.level = 1  # Đặt cấp độ mặc định là 1 khi khởi tạo game

    def draw_text(self, text, font, color, x, y):
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(topleft=(x, y))
        self.window.blit(text_surface, text_rect)

    def run(self):
        running = True
        while running:
            dt = self.clock.tick(60) / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    for letter in self.letters_group:
                        if event.unicode.lower() == letter.letter.lower():
                            if letter.color == "green":
                                self.slow_speed()  # Gọi phương thức slow_speed() khi gõ đúng chữ xanh lá
                            self.letters_group.remove(letter)
                            self.all_sprites.remove(letter)
                            if letter.color == "red":
                                self.explode(letter)  # Gọi phương thức explode() khi gõ đúng chữ đỏ
                            self.letters_group.remove(letter)
                            self.all_sprites.remove(letter)
                            break
            
            if not self.game_over:
                if len(self.letters_group) < 5:
                    speed = self.level_speeds.get(self.level, 2)  # Sử dụng tốc độ mặc định là 2 nếu không có tốc độ được đặt cho cấp độ hiện tại
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
                
                # Hiển thị cấp độ và tốc độ ở góc phải màn hình
                self.draw_text(f"Level: {self.level}", self.FONT, self.WHITE, self.WIDTH - 150, 10)
                self.draw_text(f"Speed: {self.level_speeds.get(self.level, 2)}", self.FONT, self.WHITE, self.WIDTH - 150, 50)
                
                if self.game_over:
                    self.window.blit(self.game_over_image, (0, 0))
                    pygame.display.flip()
                    pygame.time.delay(1000)
                    stars = 0
                    self.menu.run(stars)
                    self.reset_game()
                else:
                    if self.start_time != 0:  # Chỉ tính thời gian khi đã bắt đầu chơi
                        current_time = pygame.time.get_ticks() # Thời gian trôi qua khi bắt đầu game
                        elapsed_time = (current_time - self.start_time) / 1000
                        max_time = 30  # Thời gian tối đa cho mỗi cấp độ
                        self.progress_bar_width = min(1, elapsed_time / max_time) * self.WIDTH  # Tính toán chiều rộng của thanh tiến trình
                        pygame.draw.rect(self.window, self.WHITE, (0, self.HEIGHT - 20, self.progress_bar_width, 20))  # Vẽ thanh tiến trình
                        if elapsed_time >= max_time:
                            stars = min(3, self.lives)
                            self.window.blit(self.background, (0, 0))
                            self.draw_text(f"You've earned {stars} stars!", self.FONT, self.WHITE, 400, 300)
                            pygame.display.flip()
                            pygame.time.delay(3000)
                            self.menu.run(stars)
                            self.reset_game()
                    else:  # Nếu chưa bắt đầu chơi, gán giá trị cho start_time
                        self.start_time = pygame.time.get_ticks()

            pygame.display.flip()

    def reset_game(self):
        # Reset các thuộc tính liên quan đến việc đếm số lần xuất hiện của chữ màu đỏ và xanh
        Letter.red_count_global = 0
        Letter.green_count_global = 0
        Letter.green_last_spawn_time = 0
        Letter.red_last_spawn_time = 0

        self.all_sprites.empty()
        self.letters_group.empty()
        self.mbappe.rect.topleft = (50, 390)
        self.all_sprites.add(self.mbappe)
        self.lives = 3
        self.start_time = 0  # Đặt lại thời gian bắt đầu khi reset game
        self.game_over = False

    def slow_speed(self):
        for letter in self.letters_group:
            if letter.color != "green":
                letter.speed = 1
                letter.last_green_typed_time = pygame.time.get_ticks()
    def explode(self, letter):
            # Đặt vị trí hiệu ứng nổ ở vị trí của chữ đỏ và phát nổ
            self.explosion_rect.center = letter.rect.center
            self.window.blit(self.explosion_image, self.explosion_rect)
            pygame.display.flip()
            pygame.time.delay(100)  # Delay  hiệu ứng nổ hoàn thành
            
            # Xóa chữ đỏ và tất cả các chữ khác
            self.letters_group.empty()
            self.all_sprites.empty()
            self.mbappe.rect.topleft = (50, 390)
            self.all_sprites.add(self.mbappe)