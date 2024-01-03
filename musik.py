from deck import Deck


class Musik(Deck):
    """
    Represents Musik - a pile of cards that is selected after bidding.
    Inheriting from Deck.

    Additional methods:
    - _clear: Clears the cards in Musik.
    - cards_in_musik: List of cards in Musik.
    """
    def __init__(self):
        super().__init__()

    def cards_in_musik(self):
        return self._cards

    def _clear(self):
        self._cards.clear()
