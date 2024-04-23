import random

class AutoPlay:
    def __init__(self, game, stars_per_level):
        self.game = game
        self.stars_per_level = stars_per_level

    def auto_play_level(self):
        # Tìm và chọn một cấp độ có số sao ít hơn 3
        selected_level = self.find_level_with_less_than_three_stars()
        if selected_level is not None:
            self.game.level = selected_level
            self.game.run()
        else:
            print("Không có cấp độ nào có số sao ít hơn 3.")

    def find_level_with_less_than_three_stars(self):
        # Tìm và trả về một cấp độ có số sao ít hơn 3
        available_levels = [i + 1 for i, stars in enumerate(self.stars_per_level) if stars < 3]
        if available_levels:
            return random.choice(available_levels)
        else:
            return None  # Trả về None nếu không tìm thấy cấp độ nào có số sao ít hơn 3