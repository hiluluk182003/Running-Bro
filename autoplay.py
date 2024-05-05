import threading
import string
import random
import time

class AutoPlay:
    """
    Một lớp để tự động chơi các cấp độ trong trò chơi bằng cách gõ các ký tự.

    Thuộc tính:
        game (Game): Đối tượng trò chơi để tương tác.
        stars_per_level (list): Một danh sách chứa số lượng sao kiếm được cho mỗi cấp độ.
        typing_thread (Thread): Luồng để mô phỏng việc gõ phím.
        window_open (bool): Cờ chỉ trạng thái của cửa sổ trò chơi.
    """

    def __init__(self, game, stars_per_level):
        """
        Khởi tạo đối tượng AutoPlay với trò chơi và số sao mỗi cấp độ được cho.

        Args:
            game (Game): Đối tượng trò chơi để tương tác.
            stars_per_level (list): Một danh sách chứa số lượng sao kiếm được cho mỗi cấp độ.
        """
        self.game = game
        self.stars_per_level = stars_per_level
        self.typing_thread = None  # Biến để lưu trữ luồng gõ phím
        self.window_open = True  # Biến để báo hiệu trạng thái của cửa sổ trò chơi

    def auto_play_level(self):
        """
        Tự động chơi một cấp độ nếu có một cấp độ với ít hơn ba sao.
        """
        selected_level = self.find_level_with_less_than_three_stars()
        if selected_level is not None:
            self.game.level = selected_level
            self.auto_type_characters()

    def find_level_with_less_than_three_stars(self):
        """
        Tìm một cấp độ có ít hơn ba sao.

        Returns:
            int: Số cấp độ có ít hơn ba sao, hoặc None nếu không có cấp độ nào như vậy.
        """
        available_levels = [i + 1 for i, stars in enumerate(self.stars_per_level[:-1]) if stars < 3]
        if available_levels:
            return random.choice(available_levels)
        else:
            return None

    def auto_type_characters(self):
        """
        Mô phỏng việc gõ các ký tự trong trò chơi.
        """
        def auto_typing():
            """
            Hàm để mô phỏng việc gõ các ký tự.
            """
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
