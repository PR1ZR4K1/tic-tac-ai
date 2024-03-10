# -*- coding: utf-8 -*-
from typing import List, LiteralString


def evaluate_line(elements: List[LiteralString], check_point: int):
    """
    Evaluates a line (row, column, or diagonal) and updates the score based on the elements.
    """
    score = 0
    x_count = elements.count("x")
    o_count = elements.count("o")

    if x_count > check_point:
        score += (x_count // check_point) * check_point
    elif x_count == check_point:
        score += x_count//check_point
    if o_count > check_point:
        score -= (o_count // check_point) * check_point
    elif o_count == check_point:
        score -= o_count//check_point

    return score


class GameStatus:

    def __init__(self, board_state: List[List[LiteralString]], turn_O: bool):

        self.board_state = board_state
        self.turn_O = turn_O
        self.oldScores = 0
        self.winner = ""

    def is_terminal(self):
        """
        YOUR CODE HERE TO CHECK IF ANY CELL IS EMPTY WITH THE VALUE 0. IF THERE IS NO EMPTY
        THEN YOU SHOULD ALSO RETURN THE WINNER OF THE GAME BY CHECKING THE SCORES FOR EACH PLAYER 
        """
        for row in self.board_state:
            if "_" in row:
                self.oldScores = self.get_score(False)
                return False

        self.oldScores = self.get_score(True)

        if self.oldScores > 0:
            self.winner = "x"
            return True
        elif self.oldScores < 0:
            self.winner = "o"
            return True
        else:
            self.winner = "draw"
            return True

    def get_score(self, terminal):
        """
        YOUR CODE HERE TO CALCULATE THE SCORES. MAKE SURE YOU ADD THE SCORE FOR EACH PLAYER BY CHECKING
        EACH TRIPLET IN THE BOARD IN EACH DIRECTION (HORIZONAL, VERTICAL, AND ANY DIAGONAL DIRECTION)

        YOU SHOULD THEN RETURN THE CALCULATED SCORE WHICH CAN BE POSITIVE (HUMAN PLAYER WINS),
        NEGATIVE (AI PLAYER WINS), OR 0 (DRAW)
        """
        rows = len(self.board_state)
        cols = len(self.board_state[0])
        scores = 0
        check_point = 3 if terminal else 2

        for row in range(rows):
            scores += evaluate_line(self.board_state[row], check_point)

        for col in range(cols):
            scores += evaluate_line([self.board_state[row][col]
                                    for row in range(rows)], check_point)

        scores += evaluate_line([self.board_state[i][i]
                                for i in range(rows)], check_point)

        scores += evaluate_line([self.board_state[i][rows-i-1]
                                for i in range(rows)], check_point)

        return scores

    def get_negamax_scores(self, terminal):
        """
YOUR CODE HERE TO CALCULATE NEGAMAX SCORES. THIS FUNCTION SHOULD EXACTLY BE THE SAME OF GET_SCORES UNLESS
YOU SET THE SCORE FOR NEGAMX TO A VALUE THAT IS NOT AN INCREMENT OF 1 (E.G., YOU CAN DO SCORES = SCORES + 100 
                                                                                                                                   FOR HUMAN PLAYER INSTEAD OF 
                                                                                                                                   SCORES = SCORES + 1)
"""
        rows = len(self.board_state)
        cols = len(self.board_state[0])
        scores = 0
        check_point = 3 if terminal else 2

    def get_moves(self):
        return [(x, y) for x, row in enumerate(self.board_state) for y, col in enumerate(row) if col == "_"]

    def get_new_state(self, move):
        if self.is_terminal():
            return self
        new_board_state = self.board_state.copy()
        x, y = move
        new_board_state[x][y] = "o" if self.turn_O else "x"
        return GameStatus(new_board_state, not self.turn_O)
