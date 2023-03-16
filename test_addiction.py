import pytest

from card import Card, card_from_tuple
from board import Board
from node import Node
from test_strings import *
import addiction


def test_card_from_tuple():
    assert card_from_tuple((0, 0)) == Card('CA')
    assert card_from_tuple((3, 5)) == Card('S6')
    assert card_from_tuple((3, 0)) == Card('S1')


def test_card():
    c1 = Card('CA')
    assert c1.suit == 0
    assert c1.value == 0

    c2 = Card('C1')
    assert c2.suit == 0
    assert c2.value == 0

    with pytest.raises(ValueError) as e:
        Card('E')  # noqa
    assert str(e.value) == "Invalid card"

    with pytest.raises(ValueError) as e:
        Card('E4')  # noqa
    assert str(e.value) == "Invalid suit"

    with pytest.raises(ValueError) as e:
        Card('C8')  # noqa
    assert str(e.value) == "Invalid face value"


def test_to_tuple():
    c1 = Card('C1')
    assert c1.to_tuple() == (0, 0)
    c2 = Card('S6')
    assert c2.to_tuple() == (3, 5)


def test_card_str():
    assert str(Card('C5')) == 'C5'
    assert str(Card('D1')) == 'DA'


def test_successor():
    c1 = Card('C5')
    c2 = c1.successor()
    assert c2.suit == 0
    assert c2.value == 5
    assert c2.successor() is None


def test_board():
    b = Board(TESTSTR1)
    assert b.grid[0][0].suit == 0
    assert b.grid[0][0].value == 0
    assert b.grid[0][1].suit == 3
    assert b.grid[0][1].value == 4
    assert b.grid[0][2].suit == 2
    assert b.grid[0][2].value == 4
    assert b.grid[0][3].suit == 1
    assert b.grid[0][3].value == 1
    assert b.grid[0][4].suit == 1
    assert b.grid[0][4].value == 2
    assert b.grid[0][5] is None
    assert b.grid[0][6].suit == 1
    assert b.grid[0][6].value == 5

    assert b.grid[1][0].suit == 3
    assert b.grid[1][0].value == 0
    assert b.grid[1][1].suit == 0
    assert b.grid[1][1].value == 3
    assert b.grid[1][2].suit == 0
    assert b.grid[1][2].value == 2
    assert b.grid[1][3].suit == 1
    assert b.grid[1][3].value == 4
    assert b.grid[1][4].suit == 1
    assert b.grid[1][4].value == 3
    assert b.grid[1][5] is None
    assert b.grid[1][6].suit == 2
    assert b.grid[1][6].value == 3

    assert b.grid[2][0].suit == 2
    assert b.grid[2][0].value == 0
    assert b.grid[2][1] is None
    assert b.grid[2][2].suit == 3
    assert b.grid[2][2].value == 3
    assert b.grid[2][3].suit == 3
    assert b.grid[2][3].value == 1
    assert b.grid[2][4].suit == 2
    assert b.grid[2][4].value == 2
    assert b.grid[2][5].suit == 0
    assert b.grid[2][5].value == 5
    assert b.grid[2][6] is None

    assert b.grid[3][0].suit == 1
    assert b.grid[3][0].value == 0
    assert b.grid[3][1].suit == 0
    assert b.grid[3][1].value == 1
    assert b.grid[3][2].suit == 0
    assert b.grid[3][2].value == 4
    assert b.grid[3][3].suit == 2
    assert b.grid[3][3].value == 1
    assert b.grid[3][4].suit == 2
    assert b.grid[3][4].value == 5
    assert b.grid[3][5].suit == 3
    assert b.grid[3][5].value == 2
    assert b.grid[3][6].suit == 3
    assert b.grid[3][6].value == 5


def test_board_invalid():
    with pytest.raises(ValueError) as e:
        Board(TESTSTR_INVALID)  # noqa
    assert str(e.value) == "Missing cards - check the initialization string"
    with pytest.raises(ValueError) as e:
        Board(TESTSTR_INVALID1)  # noqa
    assert str(e.value) == "Check the initialization string"
    with pytest.raises(ValueError) as e:
        Board(TESTSTR_INVALID2)  # noqa
    assert str(e.value) == "Check the initialization string"
    with pytest.raises(ValueError) as e:
        Board(TESTSTR_INVALID3)  # noqa
    assert str(e.value) == "Invalid card D8, check the initialization string"
    with pytest.raises(ValueError) as e:
        Board(TESTSTR_INVALID4)  # noqa
    assert str(e.value) == "Invalid card A3, check the initialization string"


def test_board_str():
    b = Board(TESTSTR1)
    assert str(b) == TESTSTR1


def test_move_card():
    b = Board(TESTSTR1)
    b1 = b.move_card((1, 4), (0, 5))
    assert str(b1) == TESTSTR2
    b2 = Board(TESTSTR4)
    b3 = b2.move_card((3, 6), (3, 5))
    assert str(b3) == TESTSTR3


def test_move_card_invalid():
    b = Board(TESTSTR1)
    with pytest.raises(ValueError) as e:
        b.move_card((1, 4), (1, 4))  # noqa
    assert str(e.value) == "Must move card to a different slot"
    with pytest.raises(ValueError) as e:
        b.move_card((1, 4), (0, 1))  # noqa
    assert str(e.value) == "Card can only be moved to an empty slot"
    with pytest.raises(ValueError) as e:
        b.move_card((1, 3), (0, 5))  # noqa
    assert str(e.value) == "Card must be one higher than its left neighbor"

    b3 = Board(TESTSTR3)
    with pytest.raises(ValueError) as e:
        b3.move_card((1, 6), (0, 6))  # noqa
    assert str(e.value) == "Trying to move from an empty slot"
    with pytest.raises(ValueError) as e:
        b4 = Board(TESTSTR5)
        b4.move_card((3, 0), (1, 0))  # noqa
    assert str(e.value) == "Cannot move an ace out of the first slot"
    with pytest.raises(ValueError) as e:
        b5 = Board(TESTSTR10)
        b5.move_card((2, 5), (0, 0))  # noqa
    assert str(e.value) == "Only an ace can go in the first slot"


def test_find_card():
    b = Board(TESTSTR1)
    assert b.find_card(Card('C5')) == (3, 2)
    assert b.find_card(Card('S6')) == (3, 6)

    b1 = Board(TESTSTR1)
    b1.grid[3][6] = None
    with pytest.raises(ValueError) as e:
        b1.find_card(Card('S6'))  # noqa
    assert str(e.value) == "Could not find card"


def test_solved():
    b = Board(TESTSTR1)
    assert not b.solved()
    b = Board(TESTSTR3)
    assert b.solved()


def test_score():
    b = Board(TESTSTR3)
    assert b.score() == 24
    b1 = Board(TESTSTR1)
    assert b1.score() == 4
    b2 = Board(TESTSTR1)
    assert b2.score() == 4
    b3 = Board(TESTSTR4)
    assert b3.score() == 23
    b4 = Board(TESTSTR10)
    assert b4.score() == 0


def test_valid_moves():
    b = Board(TESTSTR3)
    assert b.valid_moves() == set()

    b1 = Board(TESTSTR4)
    expected1 = set()
    expected1.add(((3, 6), (3, 5)))
    assert b1.valid_moves() == expected1

    b2 = Board(TESTSTR5)
    expected2 = set()
    expected2.add(((1, 3), (0, 2)))
    expected2.add(((1, 2), (1, 0)))
    expected2.add(((0, 3), (1, 0)))
    expected2.add(((0, 5), (1, 0)))
    expected2.add(((2, 2), (2, 6)))
    expected2.add(((1, 4), (3, 6)))
    assert b2.valid_moves() == expected2

    b3 = Board(TESTSTR6)
    expected3 = set()
    expected3.add(((2, 6), (1, 1)))
    expected3.add(((2, 1), (3, 5)))
    assert b3.valid_moves() == expected3

    b4 = Board(TESTSTR7)
    expected4 = set()
    expected4.add(((0, 1), (0, 3)))
    expected4.add(((1, 1), (2, 1)))
    assert b4.valid_moves() == expected4


def test_node():
    b = Board(TESTSTR3)
    n = Node(b)
    n.get_subtree()
    assert len(n.children) == 0

    b = Board(TESTSTR4)
    n = Node(b)
    n.get_subtree()
    assert len(n.children) == 1
    bd = n.children[0].board
    assert n.children[0].parent == n
    assert bd.solved()
    assert str(bd) == TESTSTR3

    b = Board(TESTSTR1)
    n = Node(b)
    n.get_subtree()
    assert len(Node.boards_seen) == 2001
    assert Node.best_score == 24


def test_find_optimum():
    b = Board(TESTSTR3)
    n = Node(b)
    n.get_subtree()
    assert n.find_optimum() == []

    b = Board(TESTSTR4)
    n = Node(b)
    n.get_subtree()
    assert n.find_optimum() == [((3, 6), (3, 5))]

    b = Board(TESTSTR8)
    n = Node(b)
    n.get_subtree()
    assert n.find_optimum() == [((1, 6), (1, 5)), ((3, 6), (3, 5)), ((2, 6), (2, 5)), ((0, 6), (0, 5))]

    b = Board(TESTSTR3131)
    n = Node(b)
    n.get_subtree()
    moves = n.find_optimum()
    for move in moves:
        b = b.move_card(*move)
    assert b.solved()


def test_path_from_root():
    b = Board(TESTSTR4)
    n = Node(b)
    n.get_subtree()
    assert n.path_from_root() == []
    assert n.children[0].path_from_root() == [((3, 6), (3, 5))]


def test_addiction(capsys):
    input_values = [
        'SA,D5,S6,H3,C2,H5,C4',
        'DA,S5,S3,,,,C6',
        'CA,D4,D6,H4,C5,C3,S4',
        'HA,H2,H6,D2,S2,,D3'
    ]

    def mock_input(s):
        print(s, end='')
        return input_values.pop(0)
    addiction.input = mock_input
    addiction.main()
    out, err = capsys.readouterr()
    assert out.endswith("Solved in 29 moves\n")
    assert err == ''
