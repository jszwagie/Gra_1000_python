from dataclasses import dataclass


@dataclass
class Card:
    """
    :param name: _name - Name of the card.
    :param type: str
    :param name: _suit - Suit of the card.
    :param type: str
    :param name: _points - Points assigned to the card.
    :param type: int

    Represents a playing card with a name, suit, and points.

    Properties:
    - name - returns name
    - suit - returns suit
    - points - returns points

    Methods:
    - __eq__: shows how two objects can be compared
    """
    _name: str
    _suit: str
    _points: int

    @property
    def name(self):
        return self._name

    @property
    def suit(self):
        return self._suit

    @property
    def points(self):
        return self._points

    def __eq__(self, other):
        if (self._name == other._name and self._suit == other._suit and
           self._points == other._points):
            return True
        else:
            return False
