from collections import defaultdict, Counter
import math
from typing import List


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
    return "O" if len([*bx, *bo]) % 2 else "X"


def parse_textboard(s: str):
    bx = set()
    bo = set()
    for i, v in enumerate([l for l in s if l in ["X", "O", "_"]]):
        if v == "X":
            bx.add(i)
        if v == "O":
            bo.add(i)
    return bx, bo


def next_boards(bx, bo):
    if is_over(bx, bo):
        return []
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
            if len(set(v) & set(stoplist)) == 3:
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
    predictions = []
    for cx, co in next_boards(bx, bo):
        if turn(bx, bo) == "X":
            diff = cx - bx
        if turn(bx, bo) == "O":
            diff = co - bo
        # new set is only one element larger
        predictions.append((list(diff)[0], minimax(cx, co)))
    return (turn(bx, bo), predictions)


def parse_key(key):
    bx = [int(slot) for slot in key[1 : key.index("-")]]
    bo = [int(slot) for slot in key[key.index("O") + 1 :]]
    return bx, bo


def is_ancestor(a, b):
    # if game over is not checked, ancestors would be
    # registered for games that had already ended
    if is_over(*parse_key(a)):
        return False
    i = 0
    j = 0
    while i < len(a) and j < len(b):
        if a[i] == b[j]:
            i += 1
            j += 1
        else:
            j += 1
    return i == len(a)


def analyze_tree(tree):
    r = defaultdict(list)
    leaves = [
        (key, board_value(*parse_key(key)))
        for key in tree.keys()
        if is_over(*parse_key(key))
    ]
    for key in tree:
        for leaf_key, leaf_value in leaves:
            if is_ancestor(key, leaf_key):
                n = r[key].append(leaf_value)
    for key, v in tree.items():
        player, choices = v
        tree[key] = [player, Counter(r[key]), dict(choices)]
    return tree


def create_key(bx, bo):
    def s(board):
        return "".join(map(str, sorted(board)))

    return f"X{s(bx)}-O{s(bo)}"


def grow_tree(bx=None, bo=None):
    if bx is None:
        bx = set()
    if bo is None:
        bo = set()
    game_tree = {}

    def f(bx, bo):
        if (key := create_key(bx, bo)) not in game_tree:
            game_tree[key] = lookahead(bx, bo)
        if is_over(bx, bo):
            return
        for cx, co in next_boards(bx, bo):
            f(cx, co)

    f(bx, bo)

    return game_tree
