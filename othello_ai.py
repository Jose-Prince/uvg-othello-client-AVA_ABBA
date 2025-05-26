import random
import copy

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
 
def ai_move(board, player): 
    valid_moves = valid_movements(board, player)
    if valid_moves:
        def make_move(board, row, col, player):
            new_board = copy.deepcopy(board)
            new_board[row][col] = player
            directions = [(-1,-1), (-1,0), (-1,1),
                          (0,-1),         (0,1),
                          (1,-1), (1,0), (1,1)]
            
            for dr, dc in directions:
                r, c = row +dr, col + dc
                pieces_to_flip = []
                while 0 <= r < 8 and 0 <= c < 8:
                    if new_board[r][c] == -player:
                        pieces_to_flip.append((r, c))
                    elif new_board[r][c] == player:
                        for pr, pc in pieces_to_flip:
                            new_board[pr][pc] = player
                        break
                    else:
                        break
                    r += dr
                    c += dc
            return new_board

        def evaluate(board, player):
            return sum(cell == player for row in board for cell in row) - \
                   sum(cell == player for row in board for cell in row)

        def negamax(board, player, depth):
            if depth == 0:
                return evaluate(board, player), None

            max_score = float("-inf")
            best_move = None
            for move in valid_moves:
                new_board = make_move(board, move[0], move[1], player)
                score, _ = negamax(new_board, -player, depth - 1)
                score = -score
                if score > max_score:
                    max_score = score
                    best_move = move

            if best_move is None:
                return evaluate(board, player), None

            return max_score, best_move

        _, move = negamax(board, player, depth=3)

        if move is None:
            if valid_moves:
                return random.choice(valid_moves)
            else:
                return (0,0)

        return move
        #return random.choice(valid_moves)
    return None
