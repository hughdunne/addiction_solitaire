from copy import deepcopy

MAX_CARD = 5  # Face value 6
SUITS = 'CDHS'


class Card:
    def __init__(self, value: str):
        # Suits: 0, 1, 2, 3 => club, diamond, heart, spade
        # Value: 0 - 5 => Ace - 6
        if len(value) != 2:
            raise ValueError("Invalid card")
        str_suit, str_value = value
        if str_suit not in SUITS:
            raise ValueError("Invalid suit")
        self.suit = SUITS.index(str_suit)
        if str_value == 'A':
            self.value = 0
        elif str_value.isdigit():
            self.value = int(str_value) - 1
        else:
            raise ValueError("Invalid face value")
        if self.value not in range(MAX_CARD + 1):
            raise ValueError("Invalid face value")

    def __str__(self):
        face_value: str
        if self.value == 0:
            face_value = 'A'
        else:
            face_value = str(1 + self.value)
        return SUITS[self.suit] + face_value

    def __eq__(self, other):
        return isinstance(other, Card) and self.suit == other.suit and self.value == other.value

    def successor(self):
        if self.value == MAX_CARD:
            return None
        c = deepcopy(self)
        c.value += 1
        return c
