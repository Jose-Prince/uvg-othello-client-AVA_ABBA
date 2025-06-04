import random

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
        _, best_move = minimax(board, depth=3, maximizing_player=True, player=player)
        return best_move
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






##Minimax chat

import copy

def make_move(board, move, player):
    new_board = copy.deepcopy(board)
    x, y = move
    new_board[x][y] = player
    opponent = -player

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

def evaluate(board, player):
    return sum(cell == player for row in board for cell in row) - \
           sum(cell == -player for row in board for cell in row)


def minimax(board, depth, maximizing_player, player):
    opponent = -player
    current_player = player if maximizing_player else opponent
    valid_moves = valid_movements(board, current_player)

    if depth == 0 or not valid_moves:
        return evaluate(board, player), None

    best_move = None

    if maximizing_player:
        max_eval = float('-inf')
        for move in valid_moves:
            new_board = make_move(board, move, current_player)
            eval_score, _ = minimax(new_board, depth - 1, False, player)
            if eval_score > max_eval:
                max_eval = eval_score
                best_move = move
        return max_eval, best_move
    else:
        min_eval = float('inf')
        for move in valid_moves:
            new_board = make_move(board, move, current_player)
            eval_score, _ = minimax(new_board, depth - 1, True, player)
            if eval_score < min_eval:
                min_eval = eval_score
                best_move = move
        return min_eval, best_move
