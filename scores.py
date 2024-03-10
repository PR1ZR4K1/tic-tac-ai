import time
from typing import List, LiteralString
from GameStatus_5120 import GameStatus


def evaluate_line(elements: List[LiteralString], check_point: int):
    """
    Evaluates a line (row, column, or diagonal) and updates the score based on the elements.
    """
    score = 0
    x_count = elements.count("x")
    o_count = elements.count("o")

    if x_count >= check_point:
        score += x_count // check_point
    if o_count >= check_point:
        score -= o_count // check_point

    return score


def get_scores(self, terminal):
    board_state = [["x", "x", "x"], ["x", "x", "_"], ["x", "_", "x"]]
    """
    YOUR CODE HERE TO CALCULATE THE SCORES. MAKE SURE YOU ADD THE SCORE FOR EACH PLAYER BY CHECKING
    EACH TRIPLET IN THE BOARD IN EACH DIRECTION (HORIZONAL, VERTICAL, AND ANY DIAGONAL DIRECTION)

    YOU SHOULD THEN RETURN THE CALCULATED SCORE WHICH CAN BE POSITIVE (HUMAN PLAYER WINS),
    NEGATIVE (AI PLAYER WINS), OR 0 (DRAW)
    """
    rows = len(board_state)
    cols = len(board_state[0])
    scores = 0
    check_point = 3 if terminal else 2

    for row in range(rows):
        scores += evaluate_line(board_state[row], check_point)

    for col in range(cols):
        scores += evaluate_line([board_state[row][col]
                                for row in range(rows)], check_point)

    scores += evaluate_line([board_state[i][i]
                            for i in range(rows)], check_point)

    scores += evaluate_line([board_state[i][rows-i-1]
                            for i in range(rows)], check_point)

    return scores


def get_moves(self):
    """
    YOUR CODE HERE TO ADD ALL THE NON EMPTY CELLS TO MOVES VARIABLES AND RETURN IT TO BE USE BY YOUR
    MINIMAX OR NEGAMAX FUNCTIONS
    """

    return [(x, y) for x, row in enumerate(self.board_state) for y, col in enumerate(row) if col == "_"]


def get_negamax_score(terminal, board_state):
    rows = len(board_state)
    cols = len(board_state[0])
    total_score = 0
    check_point = 3 if terminal else 2

    # Adjusting score increments for demonstration purposes
    # A significant positive score for human player's win scenarios
    score_increment_for_human = 100
    # A significant negative score for AI player's win scenarios
    score_decrement_for_ai = -100

    for row in range(rows):
        total_score += evaluate_negamax_line(
            board_state[row], check_point, score_increment_for_human, score_decrement_for_ai)

    for col in range(cols):
        total_score += evaluate_negamax_line([board_state[row][col] for row in range(
            rows)], check_point, score_increment_for_human, score_decrement_for_ai)

    total_score += evaluate_negamax_line([board_state[i][i] for i in range(
        rows)], check_point, score_increment_for_human, score_decrement_for_ai)
    total_score += evaluate_negamax_line([board_state[i][rows-i-1] for i in range(
        rows)], check_point, score_increment_for_human, score_decrement_for_ai)

    return total_score


def evaluate_negamax_line(elements, check_point, score_increment_for_human, score_decrement_for_ai):

    score = 0
    x_count = elements.count("x")
    o_count = elements.count("o")
    empty_count = elements.count("_")

    # Adjust scoring to account for potential wins or blocks
    if x_count > 0 and o_count == 0:  # Potential for "x" to win
        score += (x_count / check_point) * score_increment_for_human
    if o_count > 0 and x_count == 0:  # Potential for "o" to win
        score += (o_count / check_point) * score_decrement_for_ai
    if x_count == check_point and empty_count == 1:  # Immediate win opportunity for "x"
        score += 2 * score_increment_for_human
    if o_count == check_point and empty_count == 1:  # Immediate block/win opportunity for "o"
        score += 2 * score_decrement_for_ai

    return score


# print(get_scores(None, True))


def negamax(game_status: GameStatus, depth: int, turn_multiplier: int, alpha=float('-inf'), beta=float('inf')):
    terminal = game_status.is_terminal()
    if (depth == 0) or (terminal):
        scores = get_negamax_score(
            terminal, game_status.board_state)
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
        state = game_status.get_new_state(move)
        print(state.board_state)

        # Negate the evaluated score and flip alpha and beta for the recursive call
        eval, _ = negamax(state, depth - 1, -turn_multiplier, -beta, -alpha)
        eval = -eval  # Negate the score since negamax returns score from the perspective of the next player

        if eval > best_value:
            best_value = eval
            best_move = move

        alpha = max(alpha, eval)
        if alpha >= beta:
            print('Pruning')
            break
    print(f'{best_value}, {best_move} yurrr')

    return best_value, best_move


board_state = [
    ["x", "_", "o"],
    ["_", "_", "_"],
    ["o", "_", "x"]
]

state = GameStatus(board_state, False)
print(get_negamax_score(False, state.board_state))
# print(negamax(state, depth=100, turn_multiplier=-1))

# print(negamax(state, 999, True))
