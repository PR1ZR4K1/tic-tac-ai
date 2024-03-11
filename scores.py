import time
from typing import List, LiteralString
from GameStatus import GameStatus


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

    for row in range(rows):
        total_score += evaluate_negamax_line(board_state[row], check_point)

    for col in range(cols):
        total_score += evaluate_negamax_line([board_state[row][col] for row in range(
            rows)], check_point)
        # print('This thing /n', [board_state[row][col] for row in range(
        #     rows)])

    total_score += evaluate_negamax_line([board_state[i][i] for i in range(
        rows)], check_point)
    total_score += evaluate_negamax_line([board_state[i][rows-i-1] for i in range(
        rows)], check_point)

    return total_score


def evaluate_negamax_line(elements, check_point):

    score = 0
    x_count = elements.count("x")
    o_count = elements.count("o")
    # empty_count = elements.count("_")

    # Adjust scoring to account for potential wins or blocks

    if x_count > check_point:
        score += (x_count // check_point) * check_point
    elif x_count == check_point:
        score += x_count//check_point
    if o_count > check_point:
        score -= (o_count // check_point) * check_point
    elif o_count == check_point:
        score -= o_count//check_point

    # print(score)
    return score


# print(get_scores(None, True))


def negamax(game_status: GameStatus, depth: int, turn_multiplier: int, alpha=float('-inf'), beta=float('inf')):
    terminal = game_status.is_terminal()
    if (depth == 0) or (terminal):
        scores = get_negamax_score(
            terminal, game_status.board_state)

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


board_state = [
    ["x", "_", "o"],
    ["_", "_", "_"],
    ["o", "_", "x"]
]

state = GameStatus(board_state, False)
# print(get_negamax_score(False, state.board_state))
print(negamax(state, depth=9, turn_multiplier=1))

print(state.get_score(True))
# print(negamax(state, 999, True))
