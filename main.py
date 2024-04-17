import pygame
from game import Game
from main_menu import MainMenu

def main():
    pygame.init()
    game = Game()
    main_menu = MainMenu(pygame.display.set_mode((1000, 700)), game)
    main_menu.run()
    game.run()  # Bắt đầu chơi game sau khi chọn level từ menu
    pygame.quit()

if __name__ == "__main__":
    main()
