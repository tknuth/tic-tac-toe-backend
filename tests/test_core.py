from tictactoe import *

# 0 1 2
# 3 4 5
# 6 7 8


def test_free_slots():
    assert free_slots(range(7)) == [7, 8]


def test_lookahead():
    s = """
    X O X
    X _ X
    O _ O
    """
    bx, bo = parse(s)
    assert lookahead(bx, bo) == ("O", [(4, 0), (7, -1)])
    s = """
    X _ X
    O _ X
    O _ O
    """
    bx, bo = parse(s)
    assert lookahead(bx, bo) == ("X", [(1, 1), (4, -1), (7, 0)])


def test_minimax():
    s = """
    X O X
    X O X
    O _ O
    """
    bx, bo = parse(s)
    assert minimax(bx, bo) == 0
    s = """
    X O X
    X _ X
    O _ O
    """
    bx, bo = parse(s)
    assert minimax(bx, bo) == -1


def test_board_value():
    s = """
    X X X
    X _ O
    O _ O
    """
    bx, bo = parse(s)
    assert board_value(bx, bo) == 1
    s = """
    X _ X
    O O O
    X X O
    """
    bx, bo = parse(s)
    assert board_value(bx, bo) == -1
    s = """
    X O X
    X O O
    O X X
    """
    bx, bo = parse(s)
    assert board_value(bx, bo) == 0
    s = """
    X _ X
    _ _ O
    O _ X
    """
    bx, bo = parse(s)
    assert board_value(bx, bo) is None


def test_next_boards():
    s = """
    X X X
    X _ O
    O _ O
    """
    bx, bo = parse(s)
    assert next_boards(bx, bo) == [
        (set([0, 1, 2, 3]), set([5, 6, 8, 4])),
        (set([0, 1, 2, 3]), set([5, 6, 8, 7])),
    ]


def test_turn():
    s = """
    X X X
    X _ O
    O _ O
    """
    bx, bo = parse(s)
    assert turn(bx, bo) == "O"


def test_is_over():
    s = """
    X X X
    X O O
    O O X
    """
    bx, bo = parse(s)
    assert is_over(bx, bo) == True
    s = """
    X X X
    _ _ O
    O _ _
    """
    bx, bo = parse(s)
    assert is_over(bx, bo) == True
    s = """
    X O X
    X X O
    O X O
    """
    bx, bo = parse(s)
    assert is_over(bx, bo) == True


def test_parse():
    s = """
    X X X
    X O O
    O O X
    """
    bx, bo = parse(s)
    assert bx == set([0, 1, 2, 3, 8])
    assert bo == set([4, 5, 6, 7])


def test_get_winner():
    s = """
    X X X
    X O O
    O O X
    """
    bx, bo = parse(s)
    assert get_winner(bx, bo) == "X"
    s = """
    X X O
    _ O X
    O O X
    """
    bx, bo = parse(s)
    assert get_winner(bx, bo) == "O"
    s = """
    X O _
    X O X
    O _ X
    """
    bx, bo = parse(s)
    assert get_winner(bx, bo) is None


def test_count_leaves():
    assert count_leaves(set(), set()) == 255168
