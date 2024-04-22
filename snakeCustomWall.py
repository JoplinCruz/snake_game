

def wall(width: int | None=52, heigth: int | None=20) -> list:
    if not (10 < width < 100):
        width = 10 if width < 10 else 100
    if not (6 < heigth < 24):
        heigth = 6 if heigth < 6 else 24
    
    brick = [1,1]
    h_wall = [1] * width
    h_board = [0] * width
    wall_line = brick + h_wall + brick
    board_line = brick + h_board + brick
    board = [board_line] * heigth
    
    wall = [wall_line] + board + [wall_line]
    
    return wall
    