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
        _ , alphamove = max_value(board, player, 6, -INFINITY, INFINITY)
        return alphamove
    return None




##Heuristica con alpha prunning
def max_value(board, player, depth, alpha, beta):
    moves = valid_movements(board, player)
    if depth == 0 or not moves:
        return heuristic(board, player), None

    best_score = -INFINITY
    best_move = None
    for move in moves:
        new_board = apply_move(board, move, player)
        score, _ = min_value(new_board, -player, depth - 1, alpha, beta)
        if score > best_score:
            best_score = score
            best_move = move
        if best_score >= beta:
            break
        alpha = max(alpha, best_score)
    return best_score, best_move

def min_value(board, player, depth, alpha, beta):
    moves = valid_movements(board, player)
    if depth == 0 or not moves:
        return heuristic(board, -player), None  # note: use -player here

    best_score = INFINITY
    best_move = None
    for move in moves:
        new_board = apply_move(board, move, player)
        score, _ = max_value(new_board, -player, depth - 1, alpha, beta)
        if score < best_score:
            best_score = score
            best_move = move
        if best_score <= alpha:
            break
        beta = min(beta, best_score)
    return best_score, best_move

INFINITY = float('inf')


def apply_move(board, move, player):
    from copy import deepcopy
    opponent = -player
    x, y = move
    new_board = deepcopy(board)
    new_board[x][y] = player

    for dx, dy in DIRECTIONS:
        i, j = x + dx, y + dy
        path = []

        while in_bounds(i, j) and new_board[i][j] == opponent:
            path.append((i, j))
            i += dx
            j += dy

        if in_bounds(i, j) and new_board[i][j] == player:
            for px, py in path:
                new_board[px][py] = player

    return new_board

def heuristic(board, player):
    # Simple heuristic: difference in number of pieces
    player_count = sum(row.count(player) for row in board)
    opponent_count = sum(row.count(-player) for row in board)
    return player_count - opponent_count

def max_value(board, player, depth, alpha, beta):
    moves = valid_movements(board, player)
    if depth == 0 or not moves:
        return heuristic(board, player), None

    best_score = -INFINITY
    best_move = None
    for move in moves:
        new_board = apply_move(board, move, player)
        score, _ = min_value(new_board, -player, depth - 1, alpha, beta)
        if score > best_score:
            best_score = score
            best_move = move
        if best_score >= beta:
            break
        alpha = max(alpha, best_score)
    return best_score, best_move

def min_value(board, player, depth, alpha, beta):
    moves = valid_movements(board, player)
    if depth == 0 or not moves:
        return heuristic(board, -player), None  # note: use -player here

    best_score = INFINITY
    best_move = None
    for move in moves:
        new_board = apply_move(board, move, player)
        score, _ = max_value(new_board, -player, depth - 1, alpha, beta)
        if score < best_score:
            best_score = score
            best_move = move
        if best_score <= alpha:
            break
        beta = min(beta, best_score)
    return best_score, best_move


