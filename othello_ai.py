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
    if not valid_moves:
        return None
    
    # Pesos estratégicos para posiciones del tablero
    POSITION_WEIGHTS = [
        [100, -20, 10,  5,  5, 10, -20, 100],
        [-20, -50, -2, -2, -2, -2, -50, -20],
        [ 10,  -2, -1, -1, -1, -1,  -2,  10],
        [  5,  -2, -1, -1, -1, -1,  -2,   5],
        [  5,  -2, -1, -1, -1, -1,  -2,   5],
        [ 10,  -2, -1, -1, -1, -1,  -2,  10],
        [-20, -50, -2, -2, -2, -2, -50, -20],
        [100, -20, 10,  5,  5, 10, -20, 100]
    ]
    
    def make_move(board, row, col, player):
        new_board = copy.deepcopy(board)
        new_board[row][col] = player
        
        for dr, dc in DIRECTIONS:
            r, c = row + dr, col + dc
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
    
    def count_pieces(board):
        player_count = sum(row.count(player) for row in board)
        opponent_count = sum(row.count(-player) for row in board)
        empty_count = sum(row.count(0) for row in board)
        return player_count, opponent_count, empty_count
    
    def evaluate_position(board, player):
        score = 0
        player_count, opponent_count, empty_count = count_pieces(board)
        
        # 1. Evaluación por pesos posicionales (muy importante en early/mid game)
        position_score = 0
        for i in range(8):
            for j in range(8):
                if board[i][j] == player:
                    position_score += POSITION_WEIGHTS[i][j]
                elif board[i][j] == -player:
                    position_score -= POSITION_WEIGHTS[i][j]
        
        # 2. Movilidad (número de movimientos válidos)
        player_mobility = len(valid_movements(board, player))
        opponent_mobility = len(valid_movements(board, -player))
        mobility_score = (player_mobility - opponent_mobility) * 10
        
        # 3. Estabilidad de esquinas (esquinas son muy valiosas)
        corner_score = 0
        corners = [(0,0), (0,7), (7,0), (7,7)]
        for r, c in corners:
            if board[r][c] == player:
                corner_score += 50
            elif board[r][c] == -player:
                corner_score -= 50
        
        # 4. Penalizar posiciones adyacentes a esquinas vacías
        corner_penalty = 0
        for r, c in corners:
            if board[r][c] == 0:  # Esquina vacía
                # Penalizar estar en posiciones adyacentes
                adjacent_positions = []
                if r == 0 and c == 0:  # Esquina superior izquierda
                    adjacent_positions = [(0,1), (1,0), (1,1)]
                elif r == 0 and c == 7:  # Esquina superior derecha
                    adjacent_positions = [(0,6), (1,7), (1,6)]
                elif r == 7 and c == 0:  # Esquina inferior izquierda
                    adjacent_positions = [(6,0), (7,1), (6,1)]
                elif r == 7 and c == 7:  # Esquina inferior derecha
                    adjacent_positions = [(7,6), (6,7), (6,6)]
                
                for ar, ac in adjacent_positions:
                    if board[ar][ac] == player:
                        corner_penalty -= 25
                    elif board[ar][ac] == -player:
                        corner_penalty += 25
        
        # 5. En endgame, priorizar número de fichas
        if empty_count <= 16:  # Endgame
            piece_score = (player_count - opponent_count) * 5
            score = piece_score * 2 + position_score * 0.5 + mobility_score + corner_score
        else:  # Early/Mid game
            piece_score = (player_count - opponent_count)
            score = position_score + mobility_score * 2 + corner_score + corner_penalty + piece_score
        
        return score
    
    def negamax_alpha_beta(board, player, depth, alpha, beta, maximizing_player):
        if depth == 0:
            return evaluate_position(board, player if maximizing_player else -player), None
        
        moves = valid_movements(board, player)
        if not moves:
            # Si no hay movimientos, evaluar directamente
            return evaluate_position(board, player if maximizing_player else -player), None
        
        best_move = None
        
        if maximizing_player:
            max_eval = float('-inf')
            for move in moves:
                new_board = make_move(board, move[0], move[1], player)
                eval_score, _ = negamax_alpha_beta(new_board, -player, depth - 1, alpha, beta, False)
                
                if eval_score > max_eval:
                    max_eval = eval_score
                    best_move = move
                
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break  # Poda alpha-beta
            
            return max_eval, best_move
        else:
            min_eval = float('inf')
            for move in moves:
                new_board = make_move(board, move[0], move[1], player)
                eval_score, _ = negamax_alpha_beta(new_board, -player, depth - 1, alpha, beta, True)
                
                if eval_score < min_eval:
                    min_eval = eval_score
                    best_move = move
                
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break  # Poda alpha-beta
            
            return min_eval, best_move
    
    # Determinar profundidad basada en el estado del juego
    empty_squares = sum(row.count(0) for row in board)
    
    if empty_squares > 50:  # Early game
        search_depth = 4
    elif empty_squares > 20:  # Mid game
        search_depth = 5
    else:  # End game
        search_depth = 6
    
    # Si queda muy poco tiempo del juego, búsqueda más profunda
    if empty_squares <= 12:
        search_depth = min(empty_squares, 8)
    
    try:
        _, best_move = negamax_alpha_beta(board, player, search_depth, float('-inf'), float('inf'), True)
        
        if best_move is None:
            # Fallback: elegir el movimiento que capture más fichas
            best_score = -1
            for move in valid_moves:
                new_board = make_move(board, move[0], move[1], player)
                captured = sum(row.count(player) for row in new_board) - sum(row.count(player) for row in board)
                if captured > best_score:
                    best_score = captured
                    best_move = move
        
        return best_move if best_move else random.choice(valid_moves)
    
    except:
        # En caso de error, usar estrategia simple
        return random.choice(valid_moves)