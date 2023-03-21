MAX_CARD = 6  # Face value 6
SUITS = 'CDHS'


class Card:
    def __init__(self, value: str):
        # Suits: 0, 1, 2, 3 => club, diamond, heart, spade
        # Value: 1 - 6 => Ace - 6
        if len(value) != 2:
            raise ValueError("Invalid card")
        str_suit, str_value = value
        if str_suit not in SUITS:
            raise ValueError("Invalid suit")
        self.suit = SUITS.index(str_suit)
        if str_value == 'A':
            self.value = 1
        elif str_value.isdigit():
            self.value = int(str_value)
        else:
            raise ValueError("Invalid face value")
        if self.value not in range(1, MAX_CARD + 1):
            raise ValueError("Invalid face value")

    def __str__(self):
        face_value: str
        if self.value == 1:
            face_value = 'A'
        else:
            face_value = str(self.value)
        return SUITS[self.suit] + face_value

    def __eq__(self, other):
        return isinstance(other, Card) and self.suit == other.suit and self.value == other.value

    def successor(self):
        if self.value == MAX_CARD:
            return None
        c = self.__new__(self.__class__)
        c.suit = self.suit
        c.value = self.value + 1
        return c
