from dataclasses import dataclass
from random import shuffle


@dataclass
class Card:
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


class Deck:
    def __init__(self):
        self._deck = []

    def generate_deck(self):
        deck = []
        cards = {'Ace': 11, '10': 10, 'King': 4, 'Queen': 3, 'Jack': 2, '9': 0}
        suits = ['Spades', 'Hearts', 'Clubs', 'Diamonds']
        for suit in suits:
            for figure, points in cards.items():
                card = Card(figure, suit, points)
                deck.append(card)
        self._deck = deck

    def shuffle_deck(self):
        shuffle(self._deck)

    @property
    def deck(self):
        return self._deck
