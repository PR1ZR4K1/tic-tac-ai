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


def find_winning_lines(board, win_length=3):
    n = len(board)  # Assume square board for simplicity
    winning_lines = []

    # Check rows and columns
    for i in range(n):
        for j in range(n - win_length + 1):
            # Check row [i] from column [j]
            if all(board[i][j] == board[i][k] != "_" for k in range(j, j + win_length)):
                winning_lines.append(((i, j), (i, j + win_length - 1)))
            # Check column [j] from row [i]
            if all(board[j][i] == board[k][i] != "_" for k in range(j, j + win_length)):
                winning_lines.append(((j, i), (j + win_length - 1, i)))

    # Function to extract diagonals
    def get_diagonals(board):
        rows, cols = len(board), len(board[0])
        diagonals = []

        # Top-left to bottom-right diagonals
        for col in range(cols - 2):
            diagonals.append([(i, col + i)
                             for i in range(min(rows, cols - col)) if i < rows])

        for row in range(1, rows - 2):
            diagonals.append([(row + i, i)
                             for i in range(min(rows - row, cols)) if i < cols])

        # Top-right to bottom-left diagonals
        for col in range(2, cols):
            diagonals.append([(i, col - i)
                             for i in range(min(rows, col + 1)) if i < rows])

        for row in range(1, rows - 2):
            diagonals.append([(row + i, cols - i - 1)
                             for i in range(min(rows - row, cols)) if i < cols])

        return diagonals

    # Check diagonals using the adjusted get_diagonals function
    for diagonal in get_diagonals(board):
        if len(diagonal) >= win_length:  # Ensure diagonal is long enough
            symbols = [board[x][y] for x, y in diagonal]
            for i in range(len(symbols) - win_length + 1):
                if all(s == symbols[i] != "_" for s in symbols[i:i+win_length]):
                    winning_lines.append(
                        (diagonal[i], diagonal[i+win_length-1]))

    # tuple of tuples which represent the start and end of each winning line
    # using the format ((row_start, col_start), (row_end, col_end))
    return winning_lines


# Example usage
board_state = [
    ["x", "o", "x", "x"],
    ["x", "o", "x", "x"],
    ["o", "x", "o", "o"],
    ["x", "o", "o", "o"],
]
win_length = 3  # For a Tic-Tac-Toe game
winning_lines = find_winning_lines(board_state, win_length)
print(winning_lines)

# board_state = [
#     ["x", "_", "o"],
#     ["_", "_", "_"],
#     ["o", "_", "x"]
# ]

# state = GameStatus(board_state, False)
# # print(get_negamax_score(False, state.board_state))
# print(negamax(state, depth=9, turn_multiplier=1))

# print(state.get_score(True))
# print(negamax(state, 999, True))
