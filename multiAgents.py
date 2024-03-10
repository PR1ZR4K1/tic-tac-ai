from GameStatus_5120 import GameStatus

# 3x3 tic-tac-toe board


def minimax(game_state, depth, maximizingPlayer, alpha=float('-inf'), beta=float('inf')):
    best_move = None
    terminal = game_state.is_terminal()
    if depth == 0 or terminal:
        return game_state.get_score(terminal), None

    if maximizingPlayer:
        value = float('-inf')
        for move in game_state.get_moves():
            state = game_state.get_new_state(move)
            eval, n = minimax(state, depth - 1, False, alpha, beta)
            print(eval, n)

            if eval > value:
                value = eval
                best_move = move
            alpha = max(alpha, value)
            if beta <= alpha:
                break
    else:
        value = float('inf')
        for move in game_state.get_moves():
            state = game_state.get_new_state(move)
            eval, n = minimax(state, depth - 1, True, alpha, beta)
            if eval < value:
                value = eval
                best_move = move
            beta = min(beta, value)
            if beta <= alpha:
                print("Pruning")
                break

    print(value, best_move)

    return value, best_move

    """
    YOUR CODE HERE TO FIRST CHECK WHICH PLAYER HAS CALLED THIS FUNCTION (MAXIMIZING OR MINIMIZING PLAYER)
    YOU SHOULD THEN IMPLEMENT MINIMAX WITH ALPHA-BETA PRUNING AND RETURN THE FOLLOWING TWO ITEMS
    1. VALUE
    2. BEST_MOVE
    
    THE LINE TO RETURN THESE TWO IS COMMENTED BELOW WHICH YOU CAN USE
    """


def negamax(game_status: GameStatus, depth: int, turn_multiplier: int, alpha=float('-inf'), beta=float('inf')):
    terminal = game_status.is_terminal()
    if (depth == 0) or (terminal):
        scores = game_status.get_negamax_scores(terminal)
        return scores, None

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

    child_nodes = game_status.get_moves()

    best_move = float('-inf')

    for child in child_nodes:
        state = game_status.get_new_state()

        value = -negamax(game_status=game_status, depth=depth-1,
                         alpha=-alpha, beta=-beta, turn_multiplier=-turn_multiplier)
        best_move = max(best_move, value)
        alpha = max(alpha, value)
        if alpha >= beta:
            break

    return value, best_move


board_state = [
    ["x", "_", "o"],
    ["_", "_", "_"],
    ["o", "_", "x"]
]

state = GameStatus(board_state, False)

print(minimax(state, 999993939, True))
