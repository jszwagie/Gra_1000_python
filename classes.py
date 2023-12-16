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
        self._bid = 0

    def add_card(self, card):
        self._hand.append(card)

    def play_card(self, card):
        if card in self._hand:
            self._hand.remove(card)
            return card
        else:
            return None

    def add_from_musik(self, musik):
        for card in musik.cards_in_musik():
            self._hand.append(card)
        musik.clear()

    def show_hand(self):
        list_of_cards = []
        for card in self._hand:
            list_of_cards.append(f'{card.name} of {card.suit}')
        return list_of_cards

    def set_bid(self, bid):
        self._bid = bid

    def give_card(self, number, opponent):
        card = self._hand[number]
        self._hand.remove(card)
        opponent.add_card(card)

    @property
    def bid(self):
        return self._bid


class Musik:
    def __init__(self):
        self._cards = []

    def add_card(self, card):
        self._cards.append(card)

    def cards_in_musik(self):
        return self._cards

    def clear(self):
        self._cards.clear()


class Computer(Player):
    def __init__(self):
        super().__init__()

    def make_move(self):
        # This is a simple sketch, before apllying an algorithm for making
        # moves, i start by playing the first card
        if self._hand:
            card_to_play = self._hand[0]
            played_card = self.play_card(card_to_play)
            return played_card
        else:
            return None

    def decide_to_bid(self):
        # This is a sketch too, now computer always passes
        return False


class Game:
    def __init__(self, deck, player, computer, musiki):
        self._deck = deck
        self._player = player
        self._computer = computer
        self._musiki = musiki
        self._round = 'p'

    def deal_the_cards(self):
        deck = self._deck.deck
        player_cards = deck[0:10]
        computer_cards = deck[10:20]
        musik_1 = deck[20:22]
        musik_2 = deck[22:24]
        self._player._hand = player_cards
        self._computer._hand = computer_cards
        self._musiki[0]._cards = musik_1
        self._musiki[1]._cards = musik_2

    def player_won_bid(self):
        if self._player.bid > self._computer.bid:
            return True
        else:
            return False

    def play_round(self):
        if self._round == 'p':
            card_p = self._player.play_card(self._player._hand[0])
            # Choosing card will be implemented later
            card_c = self._computer.make_move()
        else:
            card_p = self._player.play_card(self._player._hand[0])
            # Choosing card will be implemented later
            card_c = self._computer.make_move()
        if card_p.points > card_c.points:
            self._round = 'p'
            self._player._points += card_c.points
        else:
            self._round = 'c'
            self._computer._points += card_p.points
