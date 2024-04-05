from letter import Letter

def start_gameplay(letters_list):
    """
    Khởi đầu trò chơi bằng cách tạo ra các chữ cái ban đầu và thêm chúng vào danh sách.

    Args:
        letters_list (list): Danh sách chứa các chữ cái trong trò chơi.
    """
    lanes = [400, 480, 560]
    for lane in lanes:
        letters_list.append(Letter(lane))
