import pygame
from gameplay import start_gameplay

# Cài đặt Pygame
pygame.init()

# Khởi tạo cửa sổ và biến chính
screen = pygame.display.set_mode((1000, 700))
pygame.display.set_caption('RunningBro')

# Các biến khác
play_button_img = pygame.image.load(r'image/playbutton.png')
play_button_img = pygame.transform.scale(play_button_img, (300, 200))
background = pygame.image.load(r'image/background.jpg').convert()
background = pygame.transform.scale(background, (1000, 700))
back_button_img = pygame.image.load(r'image/backbutton.png')
back_button_img = pygame.transform.scale(back_button_img, (100, 50))
back_button_rect = back_button_img.get_rect(topleft=(20, 20))
mbappe = pygame.image.load(r"image/mbappe.png").convert_alpha()
mbappe = pygame.transform.scale(mbappe, (300, 200))
show_back_button = False
show_mbappe = False
show_gameplay = False
show_clock = False
clock = pygame.time.Clock()
letters_list = []
lives = 3
speed_increase_interval = 5
speed_increase_amount = 1
speed_update_time = pygame.time.get_ticks() / 1000
last_speed_update = speed_update_time  # Lưu thời điểm cập nhật speed cuối cùng
current_speed = 1  # Tốc độ ban đầu
def main():
    """
    Hàm chính của trò chơi.
    """
    global running
    global play_button_img
    global background
    global show_back_button
    global show_mbappe
    global show_gameplay
    global show_clock
    global lives
    global speed_update_time
    global last_speed_update
    global current_speed
    mbappe_rect = mbappe.get_rect(topleft=(50, 390))
    font = pygame.font.SysFont(None, 50)
    WHITE = (255, 255, 255)

    # Vòng lặp chính
    running = True
    while running:
        # Xử lý sự kiện
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if play_button_img is not None:
                    button_rect = play_button_img.get_rect(topleft=(370, 170))
                    if button_rect.collidepoint(mouse_pos):
                        background_gp = pygame.image.load(r"image/gp.jpg").convert()
                        background = pygame.transform.scale(background_gp, (1000, 700))
                        play_button_img = None
                        show_back_button = True
                        show_mbappe = True
                        show_gameplay = True
                        show_clock = True
                        start_gameplay(letters_list)
                        start_time = pygame.time.get_ticks()
                elif back_button_rect.collidepoint(mouse_pos):
                    background = pygame.image.load(r'image/background.jpg').convert()
                    background = pygame.transform.scale(background, (1000, 700))
                    play_button_img = pygame.image.load(r'image/playbutton.png')
                    play_button_img = pygame.transform.scale(play_button_img, (300, 200))
                    show_back_button = False
                    show_mbappe = False
                    show_gameplay = False
                    show_clock = False
            elif event.type == pygame.KEYDOWN:
                if show_gameplay:
                    for letter in letters_list:
                        if event.unicode.lower() == letter.letter.lower():
                            letters_list.remove(letter)
                            break

        # Vẽ các phần tử lên màn hình
        screen.blit(background, (0, 0))
        if play_button_img:
            screen.blit(play_button_img, (370, 170))
        if show_back_button:
            screen.blit(back_button_img, (20, 20))
        if show_mbappe:
            screen.blit(mbappe, (50, 390))
        if show_gameplay:
            for letter in letters_list:
                letter.update()
                screen.blit(letter.image, letter.rect)
                if letter.rect.colliderect(mbappe_rect):
                    lives -= 1
                    letters_list.remove(letter)
            if len(letters_list) < 3:
                start_gameplay(letters_list)
                # Cập nhật tốc độ cho từng chữ mới
                for letter in letters_list:
                    letter.speed = current_speed
                    print(letter.speed)
            lives_text = font.render(f"Lives: {lives}", True, WHITE)
            screen.blit(lives_text, (900 - lives_text.get_width(), 20))
            if show_clock:
                elapsed_time = (pygame.time.get_ticks() - start_time) // 1000
                clock_text = font.render(f"Time: {elapsed_time}s", True, WHITE)
                screen.blit(clock_text, (500 - clock_text.get_width() // 2, 20))
            # Kiểm tra xem đã đến lúc tăng tốc độ chưa
            current_time = pygame.time.get_ticks() / 1000
            if current_time - last_speed_update >= speed_increase_interval:
                current_speed += speed_increase_amount
                last_speed_update = current_time
                # In ra thông báo về việc tăng tốc độ (có thể loại bỏ sau khi hoàn thành)
                print(f"Speed increased to {current_speed}")
        pygame.display.update()
        clock.tick(60)

if __name__ == "__main__":
    main()
