from GameStatus_5120 import GameStatus


def minimax(game_state: GameStatus, depth: int, maximizingPlayer: bool, alpha=float('-inf'), beta=float('inf')):
    best_move = None

    terminal = game_state.is_terminal()
    if (depth == 0) or (terminal):
        newScores = game_state.get_scores(terminal)
        return newScores, best_move

    if maximizingPlayer:
        bestVal = float('-inf')
        for move in game_state.get_moves():
            value, foundMove = minimax(game_state, depth+1, False, alpha, beta)
            best_move = foundMove

            bestVal = max(bestVal, value)
            alpha = max(alpha, bestVal)

            if beta <= alpha:
                best_move = move
                break
        return bestVal, best_move
    else:
        bestVal = float('inf')
        for move in game_state.get_moves():
            value, foundMove = minimax(game_state, depth+1, False, alpha, beta)
            best_move = foundMove

            bestVal = max(bestVal, value)
            alpha = max(alpha, bestVal)

            if beta <= alpha:
                best_move = move
                break
        return bestVal, best_move

    """
    YOUR CODE HERE TO FIRST CHECK WHICH PLAYER HAS CALLED THIS FUNCTION (MAXIMIZING OR MINIMIZING PLAYER)
    YOU SHOULD THEN IMPLEMENT MINIMAX WITH ALPHA-BETA PRUNING AND RETURN THE FOLLOWING TWO ITEMS
    1. VALUE
    2. BEST_MOVE
    
    THE LINE TO RETURN THESE TWO IS COMMENTED BELOW WHICH YOU CAN USE
    """

    # return value, best_move


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
        value = -negamax(game_status=game_status, depth=depth-1,
                         alpha=-alpha, beta=-beta, turn_multiplier=-turn_multiplier)
        best_move = max(best_move, value)
        alpha = max(alpha, value)
        if alpha >= beta:
            break

    return value, best_move
