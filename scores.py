import time


def get_scores(self, terminal):
    #    board_state = [["x", "x", "x"], ["_", "x", "_"], ["_", "_", "x"]]
    # 5x5 board
    board_state = [
        ["x", "x", "x", "x", "x"],
        ["o", "x", "_", "_", "x"],
        ["o", "_", "x", "_", "x"],
        ["o", "_", "_", "x", "_"],
        ["_", "_", "_", "_", "x"]]

    # 6x6 board
    board_state = [
        ["x", "x", "x", "x", "x", "x"],
        ["o", "_", "_", "_", "_", "_"],
        ["_", "_", "x", "_", "x", "x"],
        ["o", "_", "_", "x", "_", "_"],
        ["_", "_", "_", "_", "x", "x"],
        ["_", "_", "_", "_", "x", "x"]]

    # 7x7 board
    board_state = [
        ["x", "x", "x", "x", "x", "x", "x"],
        ["o", "_", "_", "_", "_", "_", "_"],
        ["_", "_", "x", "_", "x", "x", "x"],
        ["o", "_", "_", "x", "_", "_", "_"],
        ["_", "_", "_", "_", "x", "x", "x"],
        ["_", "_", "_", "_", "x", "x", "x"],
        ["_", "_", "_", "_", "x", "x", "x"]]
    # 14x14 board
    """
[
[],[],[],
[],[],[],
[],[],[],
]


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
        x_s = board_state[row].count("x")
        o_s = board_state[row].count("o")

        if x_s >= check_point:
            scores += x_s//check_point
        if o_s >= check_point:
            scores -= o_s//check_point

    for col in range(cols):
        x_s = [board_state[row][col] for row in range(rows)].count("x")
        o_s = [board_state[row][col] for row in range(rows)].count("o")

        if x_s >= check_point:
            scores += x_s//check_point

        if o_s >= check_point:
            scores -= o_s//check_point

    diag_x = [board_state[i][i] for i in range(3)].count("x")
    diag_o = [board_state[i][i] for i in range(3)].count("o")

    if diag_x >= check_point:
        scores += diag_x//check_point
    if diag_o >= check_point:
        scores -= diag_o//check_point

    return scores


start = time.time()
print(start)

print(get_scores(True, True))


end = time.time()

print("Time taken: ", end - start)
