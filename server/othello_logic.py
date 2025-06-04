DIRECTIONS = [
    (-1, -1),  # UP-LEFT
    (-1, 0),   # UP
    (-1, 1),   # UP-RIGHT
    (0, -1),   # LEFT
    (0, 1),    # RIGHT
    (1, -1),   # DOWN-LEFT
    (1, 0),    # DOWN
    (1, 1)     # DOWN-RIGHT
]

def in_bounds(x, y):
    return 0 <= x < 8 and 0 <= y < 8

def valid_movements(board, player):
    opponent = -player
    valid_moves = []

    for x in range(8):
        for y in range(8):
            if board[x][y] != 0:
                continue

            for dx, dy in DIRECTIONS:
                i, j = x + dx, y + dy
                found_opponent = False

                while in_bounds(i, j) and board[i][j] == opponent:
                    i += dx
                    j += dy
                    found_opponent = True

                if found_opponent and in_bounds(i, j) and board[i][j] == player:
                    valid_moves.append((x, y))
                    break

    return valid_moves

def move(board, player, x, y):
    if (x, y) not in valid_movements(board, player):
        return None  # Invalid move

    board[x][y] = player
    opponent = -player

    for dx, dy in DIRECTIONS:
        i, j = x + dx, y + dy
        path = []

        while in_bounds(i, j) and board[i][j] == opponent:
            path.append((i, j))
            i += dx
            j += dy

        if path and in_bounds(i, j) and board[i][j] == player:
            for px, py in path:
                board[px][py] = player

    return board

def check_board_status(board):
    black_valid = valid_movements(board, -1)
    white_valid = valid_movements(board, 1)

    if not black_valid and not white_valid:
        black_count = sum(row.count(-1) for row in board)
        white_count = sum(row.count(1) for row in board)
        if black_count > white_count:
            winner = 'black'
        elif white_count > black_count:
            winner = 'white'
        else:
            winner = 'draw'
        return {
            "status": "ended",
            "winner": winner,
            "black": black_count,
            "white": white_count
        }
    
    return { "status": "ongoing" }
