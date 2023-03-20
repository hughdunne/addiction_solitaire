import pytest

from card import Card
from board import Board
from node import Node
from test_strings import *
import addiction


def test_card():
    c1 = Card('CA')
    assert c1.suit == 0
    assert c1.value == 0

    c2 = Card('C1')
    assert c2.suit == 0
    assert c2.value == 0


@pytest.mark.parametrize("cardstr, errmsg", [
    ('E', "Invalid card"),
    ('E4', "Invalid suit"),
    ('C8', "Invalid face value"),
    ('CD',  "Invalid face value")
])
def test_card_invalid(cardstr, errmsg):
    with pytest.raises(ValueError) as e:
        Card(cardstr)  # noqa
    assert str(e.value) == errmsg


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


@pytest.mark.parametrize("initstr, errmsg", [
    (TESTSTR_INVALID, "Missing cards - check the initialization string"),
    (TESTSTR_INVALID1, "Check the initialization string"),
    (TESTSTR_INVALID2, "Check the initialization string"),
    (TESTSTR_INVALID3, "Invalid card D8, check the initialization string"),
    (TESTSTR_INVALID4, "Invalid card A3, check the initialization string")
])
def test_board_invalid(initstr, errmsg):
    with pytest.raises(ValueError) as e:
        Board(initstr)  # noqa
    assert str(e.value) == errmsg


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


@pytest.mark.parametrize("initstr, move, errmsg", [
    (TESTSTR1, ((1, 4), (1, 4)), "Must move card to a different slot"),
    (TESTSTR1, ((1, 4), (0, 1)), "Card can only be moved to an empty slot"),
    (TESTSTR1, ((1, 3), (0, 5)), "Card must be one higher than its left neighbor"),
    (TESTSTR3, ((1, 6), (0, 6)), "Trying to move from an empty slot"),
    (TESTSTR5, ((3, 0), (1, 0)), "Ace cannot move after being locked in"),
    (TESTSTR10, ((2, 5), (0, 0)), "Only an ace can go in the first slot")
])
def test_move_card_invalid(initstr, move, errmsg):
    b = Board(initstr)
    with pytest.raises(ValueError) as e:
        b.move_card(*move)  # noqa
    assert str(e.value) == errmsg


def test_find_card():
    b = Board(TESTSTR1)
    assert b.find_card(Card('C5')) == (3, 2)
    assert b.find_card(Card('S6')) == (3, 6)


def test_solved():
    b = Board(TESTSTR1)
    assert not b.solved()
    b = Board(TESTSTR3)
    assert b.solved()


@pytest.mark.parametrize("initstr, score", [
    (TESTSTR1, 4),
    (TESTSTR3, 24),
    (TESTSTR4, 23),
    (TESTSTR10, 0)
])
def test_score(initstr, score):
    b = Board(initstr)
    assert b.score() == score


@pytest.mark.parametrize("initstr, validmoves", [
    (TESTSTR3, []),
    (TESTSTR4, [((3, 6), (3, 5))]),
    (TESTSTR5, [((1, 3), (0, 2)), ((1, 2), (1, 0)), ((0, 3), (1, 0)),
                ((0, 5), (1, 0)), ((2, 2), (2, 6)), ((1, 4), (3, 6))]),
    (TESTSTR6, [((2, 6), (1, 1)), ((2, 1), (3, 5))]),
    (TESTSTR7, [((0, 1), (0, 3)), ((1, 1), (2, 1))]),
    (TESTSTR12, [((0, 6), (0, 0)), ((1, 0), (0, 0)), ((3, 0), (0, 0)), ((3, 6), (3, 5))]),
    (TESTSTR13, [((0, 1), (1, 0)), ((3, 0), (1, 0)), ((2, 0), (1, 0)),
                 ((0, 0), (1, 0)), ((2, 2), (2, 1)), ((3, 2), (3, 1))])
])
def test_valid_moves(initstr, validmoves):
    b = Board(initstr)  # noqa
    assert b.valid_moves() == validmoves


def test_node():
    b = Board(TESTSTR3)
    n = Node(b)
    assert n.solution() == []
    assert len(n.children) == 0

    b = Board(TESTSTR4)
    n = Node(b)
    assert n.solution() == [((3, 6), (3, 5))]
    assert len(n.children) == 1
    bd = n.children[0].board
    assert bd.solved()
    assert str(bd) == TESTSTR3

    b = Board(TESTSTR1)
    n = Node(b)
    solution = n.solution()
    assert len(Node.boards_seen) == 2000
    assert Node.best_score == 24
    assert len(solution) == 30


@pytest.mark.slow
def test_hard_mode():
    # This board has an obvious solution but a large move tree.
    b = Board(TEST_HARD_MODE)
    n = Node(b)
    assert len(n.solution()) == 24
    assert Node.best_score == 24


def test_find_optimum():
    b = Board(TEST_BLOCKED)
    n = Node(b)
    assert n.solution() is None
    assert n.find_optimum() == [((1, 3), (0, 2)), ((1, 4), (0, 3)), ((3, 2), (2, 3)),
                                ((0, 4), (3, 2)), ((1, 5), (0, 4))]


def test_solution():
    b = Board(TESTSTR11)
    n = Node(b)
    moves = n.solution()
    for move in moves:
        b = b.move_card(*move)
    assert b.solved()
    assert len(moves) == 24


def test_path_from_root():
    b = Board(TESTSTR4)
    n = Node(b)
    solution = n.solution()
    assert n.path_from_root == []
    assert n.children[0].path_from_root == solution
    assert solution == [((3, 6), (3, 5))]


class TestMain:

    @pytest.fixture()
    def expected_prompts(self):
        return ["Row 1: ", "Row 2: ", "Row 3: ", "Row 4: "]

    @pytest.fixture()
    def input_mocker(self):
        def wrapper(prompts, input_values):
            def mock_input(s):
                prompts.append(s)
                return input_values.pop(0)
            return mock_input
        return wrapper

    @pytest.mark.parametrize("inputs, expout", [
        ([
             'SA,D5,S6,H3,C2,H5,C4',
             'DA,S5,S3,,,,C6',
             'CA,D4,D6,H4,C5,C3,S4',
             'HA,H2,H6,D2,S2,,D3'
         ], "Solved in 26 moves\n"),
        ([
             'SA,S2,,,H3,H4,',
             'DA,D5,D6,S3,S4,S5,S6',
             'CA,C2,C3,,D4,D2,D3',
             'HA,H2,C4,C5,C6,H5,H6'
         ], "Move S5 from Row 2, Col 6 to Row 1, Col 5\n")
    ])
    def test_addiction(self, capsys, expected_prompts, input_mocker, inputs, expout):
        prompts = []
        addiction.input = input_mocker(prompts, inputs)
        addiction.main()
        out, err = capsys.readouterr()
        assert prompts == expected_prompts
        assert out.endswith(expout)
        assert err == ''
