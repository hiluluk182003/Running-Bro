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
        self.clock_image = self.FONT.render("00:00", True, self.WHITE)
        self.clock_rect = self.clock_image.get_rect(center=(500, 50))
        self.level_status = {}  # Trạng thái của các cấp độ
        self.menu = Menu(self.window, self)
        self.time_elapsed = 0
        self.game_over = False  # Biến để kiểm tra trạng thái game over

    def draw_text(self, text, font, color, x, y):
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.topleft = (x, y)
        self.window.blit(text_surface, text_rect)

    def update_clock(self):
        current_time = pygame.time.get_ticks() // 1000
        seconds = current_time % 60
        self.clock_image = self.FONT.render(f"{seconds}S", True, self.WHITE)
        self.clock_rect = self.clock_image.get_rect(center=(500, 50))

    def run(self):
        running = True
        while running:
            dt = self.clock.tick(60) / 1000  # Thời gian trôi qua trong mỗi frame (giây)
            self.time_elapsed += dt
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    for letter in self.letters_group:
                        if event.unicode.lower() == letter.letter.lower():
                            self.letters_group.remove(letter)
                            self.all_sprites.remove(letter)
                            break
            
            if not self.game_over:
                if len(self.letters_group) < 5:
                    speed = len(self.level_status) + 2  # Tốc độ là số vòng + 2
                    new_letter = Letter(self.mbappe.rect, speed, self.letters_group, self.all_sprites)
                    self.all_sprites.add(new_letter)
                    self.letters_group.add(new_letter)

                hits = pygame.sprite.spritecollide(self.mbappe, self.letters_group, True)
                if hits:
                    print("Hit!")
                    self.lives -= 1
                    if self.lives <= 0:
                        self.game_over = True

                self.all_sprites.update()

                self.window.blit(self.background, (0, 0))
                self.all_sprites.draw(self.window)
                
                self.draw_text(f"Lives: {self.lives}", self.FONT, self.WHITE, 10, 50)
                
                if self.game_over:
                    self.window.blit(self.game_over_image, (0, 0))  # Hiển thị hình ảnh "Game Over"
                    pygame.display.flip()  # Hiển thị ngay hình ảnh "Game Over"
                    pygame.time.delay(1000)  # Delay 2 giây trước khi quay lại menu
                    stars = 0  # Đặt số sao thành 0 khi game over
                    self.menu.run(stars)  # Quay lại màn hình Menu
                    self.time_elapsed = 0  # Reset thời gian đã trôi qua
                    self.lives = 3  # Reset số mạng
                    self.game_over = False  # Reset trạng thái game over
                    self.reset_game()  # Khởi tạo lại trò chơi
                elif self.time_elapsed >= 30: 
                    stars = max(0, self.lives)  # Tính số sao dựa trên số mạng còn lại
                    self.menu.run(stars)  # Hiển thị menu và truyền số sao
                    if stars > 0:
                        self.level_status[len(self.level_status) + 1] = stars  # Cập nhật trạng thái số sao cho cấp độ tiếp theo
                    self.time_elapsed = 0  # Reset thời gian đã trôi qua
                    self.lives = 3  # Reset số mạng
                    self.game_over = False  # Reset trạng thái game over
                    self.reset_game()  # Khởi tạo lại trò chơi
                else:
                    self.update_clock()
                    self.window.blit(self.clock_image, self.clock_rect)

                pygame.display.flip()
    
    def reset_game(self):
        self.all_sprites.empty()  # Xoá tất cả các sprite
        self.letters_group.empty()  # Xoá tất cả các chữ
        self.mbappe.rect.topleft = (50, 390)  # Đặt lại vị trí của nhân vật
        self.all_sprites.add(self.mbappe)  # Thêm nhân vật vào nhóm sprite
        self.lives = 3  # Reset số mạng
        self.time_elapsed = 0  # Reset thời gian đã trôi qua
        self.update_clock()