import pygame
from game import Game

def main():
    pygame.init()
    game = Game()
    game.menu.run()  # Hiển thị menu khi bắt đầu chương trình
    game.run()  # Bắt đầu chơi game sau khi chọn level từ menu
    pygame.quit()

if __name__ == "__main__":
    main()
