from tictactoe import *
from pathlib import Path
import json

# 0 1 2
# 3 4 5
# 6 7 8


def test_free_slots():
    assert free_slots(range(7)) == [7, 8]
    assert free_slots(range(9)) == []


def test_is_ancestor():
    assert is_ancestor("X124-O378", "X0124-O378") == True
    assert is_ancestor("X01-O37", "X0124-O378") == True
    assert is_ancestor("X01-O56", "X0124-O378") == False
    assert is_ancestor("X124-O358", "X0124-O378") == False


def test_game_over():
    assert get_winner(*parse_key("X578-O036")) == "O"
    assert is_over(*parse_key("X578-O036"))
    assert next_boards(*parse_key("X578-O036")) == []


def test_parse_key():
    assert parse_key("X124-O035") == ([1, 2, 4], [0, 3, 5])


def test_lookahead():
    s = """
    X O X
    X _ X
    O _ O
    """
    bx, bo = parse_textboard(s)
    assert lookahead(bx, bo) == ("O", [(4, 0), (7, -1)])
    s = """
    X _ X
    O _ X
    O _ O
    """
    bx, bo = parse_textboard(s)
    assert lookahead(bx, bo) == ("X", [(1, 1), (4, -1), (7, 0)])


def test_minimax():
    s = """
    X O X
    X O X
    O _ O
    """
    bx, bo = parse_textboard(s)
    assert minimax(bx, bo) == 0
    s = """
    X O X
    X _ X
    O _ O
    """
    bx, bo = parse_textboard(s)
    assert minimax(bx, bo) == -1


def test_board_value():
    s = """
    X X X
    X _ O
    O _ O
    """
    bx, bo = parse_textboard(s)
    assert board_value(bx, bo) == 1
    s = """
    X _ X
    O O O
    X X O
    """
    bx, bo = parse_textboard(s)
    assert board_value(bx, bo) == -1
    s = """
    X O X
    X O O
    O X X
    """
    bx, bo = parse_textboard(s)
    assert board_value(bx, bo) == 0
    s = """
    X _ X
    _ _ O
    O _ X
    """
    bx, bo = parse_textboard(s)
    assert board_value(bx, bo) is None


def test_next_boards():
    s = """
    X O X
    X _ X
    O _ O
    """
    bx, bo = parse_textboard(s)
    assert next_boards(bx, bo) == [
        (set([0, 2, 3, 5]), set([1, 6, 8, 4])),
        (set([0, 2, 3, 5]), set([1, 6, 8, 7])),
    ]


def test_turn():
    s = """
    X X X
    X _ O
    O _ O
    """
    bx, bo = parse_textboard(s)
    assert turn(bx, bo) == "O"


def test_is_over():
    s = """
    X X X
    X O O
    O O X
    """
    bx, bo = parse_textboard(s)
    assert is_over(bx, bo) == True
    s = """
    X X X
    _ _ O
    O _ _
    """
    bx, bo = parse_textboard(s)
    assert is_over(bx, bo) == True
    s = """
    X O X
    X X O
    O X O
    """
    bx, bo = parse_textboard(s)
    assert is_over(bx, bo) == True


def test_parse():
    s = """
    X X X
    X O O
    O O X
    """
    bx, bo = parse_textboard(s)
    assert bx == set([0, 1, 2, 3, 8])
    assert bo == set([4, 5, 6, 7])


def test_get_winner():
    s = """
    X X X
    X O O
    O O X
    """
    bx, bo = parse_textboard(s)
    assert get_winner(bx, bo) == "X"
    s = """
    X X O
    _ O X
    O O X
    """
    bx, bo = parse_textboard(s)
    assert get_winner(bx, bo) == "O"
    s = """
    X O _
    X O X
    O _ X
    """
    bx, bo = parse_textboard(s)
    assert get_winner(bx, bo) is None


# https://math.stackexchange.com/questions/2592077
def test_tree():
    tree = json.load(Path("./data.json").open())
    assert tree["X-O"][1]["1"] == 626
    assert tree["X-O"][1]["0"] == 16
    assert tree["X-O"][1]["-1"] == 316


# http://www.se16.info/hgb/tictactoe.htm
def test_count_leaves():
    assert count_leaves(set(), set()) == 255168
