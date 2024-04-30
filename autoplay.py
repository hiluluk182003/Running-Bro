import threading
import string
import random
import time
import ctypes

class AutoPlay:
    def __init__(self, game, stars_per_level):
        self.game = game
        self.stars_per_level = stars_per_level
        self.typing_thread = None  # Biến để lưu trữ luồng gõ phím
        self.window_open = True  # Biến để báo hiệu trạng thái của cửa sổ game

    def auto_play_level(self):
        selected_level = self.find_level_with_less_than_three_stars()
        if selected_level is not None:
            self.game.level = selected_level
            self.auto_type_characters()

    def find_level_with_less_than_three_stars(self):
        available_levels = [i + 1 for i, stars in enumerate(self.stars_per_level) if stars < 3]
        if available_levels:
            return random.choice(available_levels)
        else:
            return None

    def auto_type_characters(self):
        def auto_typing():
            start_time = time.time()  # Lưu thời gian bắt đầu
            while self.window_open:
                current_time = time.time()
                if current_time - start_time >= 30:  # Kiểm tra nếu đã đủ 30 giây
                    break
                if self.game.game_over:  # Kiểm tra nếu trò chơi đã kết thúc
                    break  # Dừng vòng lặp khi trò chơi kết thúc
                for char in string.ascii_lowercase + string.digits:
                    self.game.handle_auto_typing(char)
                    time.sleep(0.01)

        self.typing_thread = threading.Thread(target=auto_typing)
        self.typing_thread.start()

