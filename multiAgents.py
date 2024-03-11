
from GameStatus import GameStatus


def max_value(game_state: GameStatus, alpha, beta):
    if game_state.is_terminal():
        return game_state.get_score(True)
    print(game_state.get_moves())

    v = float('-inf')
    for move in game_state.get_moves():
        v = max(v, min_value(game_state.get_new_state(move), alpha, beta))
        alpha = max(alpha, v)
        if v >= beta:
            return v
    return v


def min_value(game_state: GameStatus, alpha, beta):
    if game_state.is_terminal():
        return game_state.get_score(True)
    print(game_state.get_moves())

    v = float('inf')
    for move in game_state.get_moves():
        v = min(v, max_value(game_state.get_new_state(move), alpha, beta))
        beta = min(beta, v)
        if v <= alpha:
            return v
    return v


def super_minimax(game_state: GameStatus, depth: int, maximizingPlayer: bool, alpha=float('-inf'), beta=float('inf')):
    terminal = game_state.is_terminal(
    )

    if depth == 0 or terminal:
        score = game_state.get_score(terminal)
        return score, None

    if maximizingPlayer:
        v = float('-inf')

        best_move = None
        for move in game_state.get_moves():
            state = game_state.get_new_state(move)
            new_v = min_value(state, alpha, beta)
            if new_v > v:
                v = new_v
                best_move = move
        return v, best_move
    else:
        v = float('inf')
        best_move = None
        for move in game_state.get_moves():
            state = game_state.get_new_state(move)
            new_v = max_value(state, alpha, beta)
            if new_v < v:
                v = new_v
                best_move = move
        return v, best_move


def minimax(game_state: GameStatus, depth: int, maximizingPlayer: bool, alpha=float('-inf'), beta=float('inf')):
    terminal = game_state.is_terminal()
    # print(game_state.is_terminal())
    if depth == 0 or terminal:
        # Assuming this returns a single score
        score, _ = game_state.get_score(terminal)
        return score, None  # No best move at leaf nodes or terminal states

    if maximizingPlayer:
        maxEval = float('-inf')
        best_move = None
        for move in game_state.get_moves():
            state = game_state.get_new_state(move)
            eval, _ = minimax(state, depth - 1, False, alpha, beta)
            if eval > maxEval:
                maxEval = eval
                best_move = move
            alpha = max(alpha, eval)
            if beta <= alpha:
                # print('pruning')
                break
        return maxEval, best_move
    else:
        minEval = float('inf')
        best_move = None
        for move in game_state.get_moves():
            state = game_state.get_new_state(move)
            eval, _ = minimax(state, depth - 1, True, alpha, beta)
            if eval < minEval:
                minEval = eval
                best_move = move
            beta = min(beta, eval)
            if beta <= alpha:
                # print('pruning')
                break
        return minEval, best_move


def negamax(game_status: GameStatus, depth: int, turn_multiplier: int, alpha=float('-inf'), beta=float('inf')):
    terminal = game_status.is_terminal()
    if (depth == 0) or (terminal):
        scores, _ = game_status.get_score(terminal)

        # Negate the score since negamax returns score from the perspective of the next player
        return scores * turn_multiplier, None

    """
    YOUR CODE HERE TO CALL NEGAMAX FUNCTION. REMEMBER THE RETURN OF THE NEGAMAX SHOULD BE THE OPPOSITE OF THE CALLING
    PLAYER WHICH CAN BE DONE USING -NEGAMAX(). THE REST OF YOUR CODE SHOULD BE THE SAME AS MINIMAX FUNCTION.
    YOU ALSO DO NOT NEED TO TRACK WHICH PLAYER HAS CALLED THE FUNCTION AND SHOULD NOT CHECK IF THE CURRENT MOVE
    IS FOR MINIMAX PLAYER OR NEGAMAX PLAYER
    RETURN THE FOLLOWING TWO ITEMS
    1. VALUE
    2. BEST_MOVE
    
    THE LINE TO RETURN THESE TWO IS COMMENTED BELOW WHICH YOU CAN USE
    
    """

    best_value = float('-inf')
    best_move = None

    for move in game_status.get_moves():

        # print('before\n', [print(row) for row in game_status.board_state])

        state = game_status.get_new_state(move)
        # print('after:\n', [print(row) for row in state.board_state])

        # print(f'Available Moves: {game_status.get_moves()}')

        # print('\n-------------------\n')

        # Negate the evaluated score and flip alpha and beta for the recursive call
        eval = -negamax(state, depth - 1, -
                        turn_multiplier, -beta, -alpha)[0]

        if eval > best_value:
            best_value = eval
            best_move = move

        alpha = max(alpha, best_value)
        if alpha >= beta:
            break
    # print(f'{best_value}, {best_move} yurrr')

    return best_value, best_move


# empty 5x5 board of just diagonals
board_state = [
    ["_", "_", "_", "_", "_"],
    ["_", "_", "_", "_", "_"],
    ["_", "_", "x", "_", "_"],
    ["_", "_", "_", "_", "_"],
    ["_", "_", "_", "_", "_"]
]

board_state = [
    ["x", "o", "x"],
    ["x", "o", "_"],
    ["_", "_", "o"]
]

state = GameStatus(board_state, False)


print(minimax(state, 9, True))
print(negamax(state, 9, 1))
# print(state.get_score(False))
