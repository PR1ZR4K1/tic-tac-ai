# -*- coding: utf-8 -*-
from typing import List, LiteralString
from copy import deepcopy


def evaluate_line(elements: List[LiteralString], check_point: int, empty_spaces: int):
    """
    Evaluates a line (row, column, or diagonal) and updates the score based on the elements,
    favoring sequences of 3 even when the check point is 2.
    """
    score = 0
    elements = "".join(elements)

    if check_point == 2:
        # print(empty_spaces, 'empty spaces')

        # x | x | x
        # o | x | o
        # x | o | o

        # Special handling for sequences of exactly 2 and favoring sequences of 3
        x_seq_2_begin = elements.count("_xx")
        x_seq_2_end = elements.count("xx_")
        o_seq_2_begin = elements.count("_oo")
        o_seq_2_end = elements.count("oo_")
        x_seq_3 = elements.count("x" * 3)
        o_seq_3 = elements.count("o" * 3)
        x_space = elements.count("x_x")
        o_space = elements.count("o_o")

        # print the score associated with x_space and o_space
        # print(f'x_space: {x_space * 3} o_space: {o_space * 3}')
        # print(f'x_seq_2: {x_seq_2 * 2} o_seq_2: {o_seq_2 * 2}')
        # print(f'x_seq_3: {x_seq_3 * 10} o_seq_3: {o_seq_3 * 10}')

        # Sequences of 2 are scored normally

        score += x_seq_2_begin * 2
        score += x_seq_2_end * 2

        score -= o_seq_2_begin * 2
        score -= o_seq_2_end * 2

        score += x_space * 2
        score -= o_space * 2
        # Sequences of 3 are scored higher to favor them
        # 10 can be adjusted based on how much you want to favor 3 sequences
        if x_seq_3 > 0:
            score += x_seq_3 * 10 + (empty_spaces + 1)
        # print(f'x_seq_3: {x_seq_3} o_seq_3: {o_seq_3 }')
        if o_seq_3 > 0:
            score -= o_seq_3 * 10 + (empty_spaces + 1)

    else:
        # For terminal check or any other check_point value, handle as before
        x_seq_3 = elements.count("x" * check_point)
        o_seq_3 = elements.count("o" * check_point)

        if x_seq_3 > 0:
            score += x_seq_3 * 10 + (empty_spaces + 1)
        if o_seq_3 > 0:
            score -= o_seq_3 * 10 + (empty_spaces + 1)

    return score, (x_seq_3, o_seq_3)


def get_diagonals(board):
    rows, cols = len(board), len(board[0])
    diagonals = []

    # Top-left to bottom-right diagonals
    # Only up to cols - 3 are considered starting points for at least 3 elements
    for col in range(cols - 2):
        diagonals.append([board[i][col + i]
                         for i in range(min(rows, cols - col)) if i < rows])

    # Start from the second row, ignore the last two as starting points
    for row in range(1, rows - 2):
        diagonals.append([board[row + i][i]
                         for i in range(min(rows - row, cols)) if i < cols])

    # Top-right to bottom-left diagonals
    for col in range(2, cols):  # Start from the third column to ensure at least 3 elements
        diagonals.append([board[i][col - i]
                         for i in range(min(rows, col + 1)) if i < rows])

    # Start from the second row, ignore the last two as starting points
    for row in range(1, rows - 2):
        diagonals.append([board[row + i][cols - i - 1]
                         for i in range(min(rows - row, cols)) if i < cols])

    return diagonals


class GameStatus:

    def __init__(self, board_state: List[List[LiteralString]] = None, turn_O: bool = False):

        if board_state is None:
            # Define a default empty board state
            board_state = [["_"] * 3 for _ in range(3)]

        self.board_state = board_state
        self.turn_O = turn_O
        self.oldScores = 0
        self.winner = ""

    def is_terminal(self):
        """
        YOUR CODE HERE TO CHECK IF ANY CELL IS EMPTY WITH THE VALUE 0. IF THERE IS NO EMPTY
        THEN YOU SHOULD ALSO RETURN THE WINNER OF THE GAME BY CHECKING THE SCORES FOR EACH PLAYER 
        """

        if len(self.board_state) == 3:
            score = self.get_score(True)[0]
            if score > 0:
                self.winner = "x"
                return True
            elif score < 0:
                self.winner = "o"
                return True
            else:
                for row in self.board_state:
                    if "_" in row:
                        # self.oldScores += self.get_score(False)
                        return False

                self.winner = "draw"
                return True
        else:
            for row in self.board_state:
                if "_" in row:
                    return False

            return True

        # self.oldScores = self.get_score(True)

    def get_score(self, terminal):
        """
        YOUR CODE HERE TO CALCULATE THE SCORES. MAKE SURE YOU ADD THE SCORE FOR EACH PLAYER BY CHECKING
        EACH TRIPLET IN THE BOARD IN EACH DIRECTION (HORIZONAL, VERTICAL, AND ANY DIAGONAL DIRECTION)

        YOU SHOULD THEN RETURN THE CALCULATED SCORE WHICH CAN BE POSITIVE (HUMAN PLAYER WINS),
        NEGATIVE (AI PLAYER WINS), OR 0 (DRAW)
        """
        rows = len(self.board_state)
        cols = len(self.board_state[0])
        empty_spaces = len(self.get_moves())
        # print(empty_spaces, 'empty spaces')
        total_score = 0
        x_score = 0
        o_score = 0
        scores = 0
        check_point = 3 if terminal else 2

        # this is how we evaluate all horizontal lines
        for row in range(rows):
            scores = evaluate_line(self.board_state[row],
                                   check_point, empty_spaces=empty_spaces)
            total_score += scores[0]

            if terminal:
                x_score += scores[1][0]
                o_score += scores[1][1]

            # print(
            #     f'Row: eval {evaluate_line(self.board_state[row], check_point, empty_spaces=empty_spaces)}')

        # this is how we evaluate all vertical lines
        for col in range(cols):
            scores = evaluate_line([self.board_state[row][col]
                                    for row in range(rows)], check_point, empty_spaces=empty_spaces)

            total_score += scores[0]

            if terminal:
                x_score += scores[1][0]
                o_score += scores[1][1]
            # print(
            # f'Col: eval {evaluate_line([self.board_state[row][col] for row in range(rows)], check_point, empty_spaces=empty_spaces)}')

        # this is how we evaluate all diagonal lines
        for diagonal in get_diagonals(self.board_state):
            scores = evaluate_line(diagonal, check_point,
                                   empty_spaces=empty_spaces)

            total_score += scores[0]

            if terminal:
                x_score += scores[1][0]
                o_score += scores[1][1]
            # print(
            # f'Diagonal: eval {evaluate_line(diagonal, check_point, empty_spaces=empty_spaces)}')

        return total_score, (x_score, o_score)

    def get_negamax_score(self, terminal):
        rows = len(self.board_state)
        cols = len(self.board_state[0])
        empty_spaces = len(self.get_moves())
        total_score = 0
        check_point = 3 if terminal else 2

        for row in range(rows):
            total_score += evaluate_line(
                self.board_state[row], check_point, empty_spaces=empty_spaces)[0]

        for col in range(cols):
            total_score += evaluate_line([self.board_state[row][col] for row in range(
                rows)], check_point, empty_spaces=empty_spaces)[0]
            # print('This thing /n', [self.board_state[row][col] for row in range(
            #     rows)])

        for diagonal in get_diagonals(self.board_state):
            total_score += evaluate_line(diagonal,
                                         check_point, empty_spaces=empty_spaces)[0]

        return total_score

    def get_moves(self):
        return [(x, y) for x, row in enumerate(self.board_state) for y, col in enumerate(row) if col == "_"]

    def get_new_state(self, move):
        new_board_state = deepcopy(self.board_state)
        x, y = move
        new_board_state[x][y] = "o" if self.turn_O else "x"
        return GameStatus(new_board_state, not self.turn_O)
