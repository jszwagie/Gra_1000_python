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


class Player:
    def __init__(self):
        self._hand = []
        self._points = 0

    def add_card(self, card):
        self._hand.append(card)

    def play_card(self, card):
        if card in self._hand:
            self._hand.remove(card)
            return card
        else:
            return None

    def add_from_musik(self, musik):
        for card in musik:
            self._hand.append(card)

    def show_hand(self):
        list_of_cards = []
        for card in self._hand:
            list_of_cards.append(f'{card.name} of {card.suit}')
        return list_of_cards


class Musik:
    def __init__(self):
        self._cards = []

    def add_card(self, card):
        self._cards.append(card)

    def cards_in_musik(self):
        return self._cards
