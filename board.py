from copy import deepcopy
from card import Card, MAX_CARD, SUITS

SEPARATOR: str = ','
ROWS: int = 4
ROW_LENGTH: int = 7


class Board:
    def __init__(self, initstr: str):
        cells = initstr.strip().upper().split(SEPARATOR)
        if len(cells) != ROWS * ROW_LENGTH:
            raise ValueError("Check the initialization string")
        self.grid = [[] for _ in range(ROWS)]
        cards_found = set()
        for i, cell in enumerate(cells):
            row: int = i // ROW_LENGTH
            if cell == '':
                c = None
            else:
                try:
                    c = Card(cell)
                    cards_found.add(cell)
                except ValueError:
                    raise ValueError("Invalid card {0}, check the initialization string".format(cell))
            self.grid[row].append(c)
        if len(cards_found) != ROWS * (MAX_CARD + 1):
            raise ValueError("Missing cards - check the initialization string")

    def __str__(self):
        cells = []
        for row in self.grid:
            for cell in row:
                if cell is None:
                    cells.append('')
                else:
                    cells.append(str(cell))
        return SEPARATOR.join(cells)

    def move_card(self, src, target):
        if src == target:
            raise ValueError("Must move card to a different slot")
        src_row, src_slot = src
        target_row, target_slot = target
        src_card = self.grid[src_row][src_slot]
        if src_card is None:
            raise ValueError("Trying to move from an empty slot")
        elif target_slot == 0 and src_card.value != 0:
            raise ValueError("Only an ace can go in the first slot")
        elif self.grid[target_row][target_slot] is not None:
            raise ValueError("Card can only be moved to an empty slot")
        elif src_slot == 0 and src_card.value == 0 and src_card.successor() == self.grid[src_row][src_slot + 1]:
            raise ValueError("Ace cannot move after being locked in")
        elif target_slot != 0:
            left_neighbor = self.grid[target_row][target_slot - 1]
            if left_neighbor.successor() != src_card:
                raise ValueError("Card must be one higher than its left neighbor")
        board = deepcopy(self)
        board.grid[src_row][src_slot], board.grid[target_row][target_slot] = \
            board.grid[target_row][target_slot], board.grid[src_row][src_slot]
        return board

    def find_card(self, card):
        for i, row in enumerate(self.grid):
            for j, cell in enumerate(row):
                if cell == card:
                    return i, j
        else:
            # Should never get here
            raise ValueError("Could not find card")

    def score(self):
        # Returns the number of cards locked in
        retval: int = 0
        for row in self.grid:
            card = row[0]
            if card is None:
                break
            suit = card.suit
            for idx, card1 in enumerate(row):
                if card1 is None or card1.suit != suit or card1.value != idx:
                    break
                retval += 1
        return retval

    def solved(self):
        return self.score() == ROWS * (MAX_CARD + 1)

    def valid_moves(self):
        retval = []
        for i, row in enumerate(self.grid):
            prev_card = None
            for j, card in enumerate(row):
                if card is None:
                    target = (i, j)
                    if j == 0:
                        # Can only arise in hard mode.
                        # Any ace can be moved to this cell if it is not already locked in.
                        aces = []
                        for suit in SUITS:
                            src = self.find_card(Card(suit + 'A'))
                            deuce = self.find_card(Card(suit + '2'))
                            if src[1] != 0 or not(deuce[0] == src[0] and deuce[1] == 1):
                                aces.append((src, target))
                        # If the card to the right of the target slot is a 2, give preference to
                        # moving the ace of the same suit here.
                        neighbor = self.grid[i][1]
                        if neighbor is not None and neighbor.value == 1:
                            aces[0], aces[neighbor.suit] = aces[neighbor.suit], aces[0]
                        retval.extend(aces)
                    elif prev_card is not None:
                        src_card = prev_card.successor()
                        if src_card is not None:
                            src = self.find_card(src_card)
                            retval.append((src, target))
                prev_card = card
        return retval
