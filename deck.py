from random import shuffle
from card import Card


class Deck:
    """
    :param name: _cards - Lisy of cards in deck.
    :param type: list

    Represents a deck of cards.

    Properties:
    - deck - returns list of cards in deck

    Methods:
    - generate_deck: Generates a standard deck of cards for "1000" game.
    - shuffle_deck: Shuffles the deck of cards.
    """
    def __init__(self):
        self._cards = []

    @property
    def deck(self):
        return self._cards

    def generate_deck(self):
        deck = []
        cards = {'Ace': 11, '10': 10, 'King': 4, 'Queen': 3, 'Jack': 2, '9': 0}
        suits = ['Spades', 'Hearts', 'Clubs', 'Diamonds']
        for suit in suits:
            for figure, points in cards.items():
                card = Card(figure, suit, points)
                deck.append(card)
        self._cards = deck

    def shuffle_deck(self):
        shuffle(self._cards)
