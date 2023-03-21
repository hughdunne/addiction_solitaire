from card import Card, MAX_CARD, SUITS

SEPARATOR: str = ','
ROWS: int = 4
ROW_LENGTH: int = 7


class Board:
    def __init__(self, initstr: str):
        cells = initstr.strip().upper().split(SEPARATOR)
        if len(cells) != ROWS * ROW_LENGTH:
            raise ValueError("Wrong number of cards. Check the initialization string")
        self.grid = [[] for _ in range(ROWS)]
        self.lookup = dict()
        for i, cell in enumerate(cells):
            row: int = i // ROW_LENGTH
            col: int = i % ROW_LENGTH
            if cell == '':
                c = None
            else:
                if cell in self.lookup:
                    msg = "Duplicate card {0} in Row {1}, Col {2} and Row {3}, Col {4}. Check the initialization string"
                    raise ValueError(msg.format(cell, row + 1, col + 1,
                                                self.lookup[cell][0] + 1, self.lookup[cell][1] + 1))
                try:
                    c = Card(cell)
                    self.lookup[cell] = (row, col)
                except ValueError:
                    raise ValueError("Invalid card {0}, check the initialization string".format(cell))
            self.grid[row].append(c)

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
        # noinspection PyUnresolvedReferences
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
            # noinspection PyUnresolvedReferences
            if left_neighbor.successor() != src_card:
                raise ValueError("Card must be one higher than its left neighbor")

        # Clone the board.
        board = self.__new__(self.__class__)
        board.grid = [list(row) for row in self.grid]
        board.grid[src_row][src_slot], board.grid[target_row][target_slot] = \
            board.grid[target_row][target_slot], board.grid[src_row][src_slot]
        board.lookup = dict(self.lookup)
        board.lookup[str(src_card)] = target
        return board

    def find_card(self, card):
        return self.lookup[str(card)]

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
