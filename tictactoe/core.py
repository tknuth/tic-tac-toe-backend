import math


WINNING_LOCATIONS = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6],
]


def free_slots(*args):
    board = set().union(*args)
    if len(board) > 8:
        return []
    return [i for i in range(9) if i not in board]


def turn(bx, bo):
    return "X" if not len([*bx, *bo]) % 2 else "O"


def parse(s: str):
    bx = set()
    bo = set()
    for i, v in enumerate([l for l in s if l in ["X", "O", "_"]]):
        if v == "X":
            bx.add(i)
        if v == "O":
            bo.add(i)
    return bx, bo


def next_boards(bx, bo):
    slots = free_slots(bx, bo)
    if turn(bx, bo) == "X":
        return [(set().union([*bx, slot]), bo) for slot in slots]
    if turn(bx, bo) == "O":
        return [(bx, set().union([*bo, slot])) for slot in slots]


def get_winner(bx, bo):
    # assumes that only one winner is possible
    # returns None on tie
    for stoplist in WINNING_LOCATIONS:
        for k, v in {"X": bx, "O": bo}.items():
            if len(v & set(stoplist)) == 3:
                return k


def is_over(bx, bo):
    return get_winner(bx, bo) is not None or len(set([*bx, *bo])) == 9


def count_leaves(bx, bo, i=0):
    if is_over(bx, bo):
        return 1
    return sum([count_leaves(bx, bo) for bx, bo in next_boards(bx, bo)])


def board_value(bx, bo):
    if is_over(bx, bo):
        return {"X": 1, "O": -1, None: 0}[get_winner(bx, bo)]


def minimax(bx, bo):
    if is_over(bx, bo):
        return board_value(bx, bo)
    if turn(bx, bo) == "X":
        v = -math.inf
        for cx, co in next_boards(bx, bo):
            v = max(v, minimax(cx, co))
        return v
    if turn(bx, bo) == "O":
        v = math.inf
        for cx, co in next_boards(bx, bo):
            v = min(v, minimax(cx, co))
        return v


def lookahead(bx, bo):
    # new set is only one element larger
    predictions = []
    for cx, co in next_boards(bx, bo):
        if turn(bx, bo) == "X":
            diff = cx - bx
        if turn(bx, bo) == "O":
            diff = co - bo
        predictions.append((list(diff)[0], minimax(cx, co)))
    return (turn(bx, bo), predictions)


def grow_tree(bx=set(), bo=set()):
    game_tree = {}

    def s(board):
        return "".join(map(str, sorted(board)))

    def f(bx, bo):
        key = f"X{s(bx)}-O{s(bo)}"
        if key not in game_tree:
            game_tree[key] = lookahead(bx, bo)
        if is_over(bx, bo):
            return
        for cx, co in next_boards(bx, bo):
            f(cx, co)

    f(bx, bo)
    return game_tree
