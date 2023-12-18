from dataclasses import dataclass
from random import shuffle, randint, choice


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

    def __str__(self):
        desc = f'{self.name} of {self.suit}'
        return desc

    def __eq__(self, other):
        if (self.name == other._name and self.suit == other.suit and
           self.points == other.points):
            return True
        else:
            return False


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
        self._trumps = []

    def add_card(self, card):
        self._hand.append(card)

    def play_card(self, card_number):
        card = self._hand[card_number]
        self._hand.remove(card)
        return card

    def add_from_musik(self, musik):
        for card in musik.cards_in_musik():
            self._hand.append(card)
        musik.clear()

    def show_hand(self):
        list_of_cards = []
        for card in self._hand:
            list_of_cards.append(str(card))
        return list_of_cards

    def cards_display(self):
        list_of_cards = self.show_hand()
        result = "Yours cards: " + ', '.join(list_of_cards) + '.'
        return result

    def set_bid(self, bid):
        self._bid = bid

    def remove_card(self, number):
        card = self._hand[number]
        self._hand.remove(card)
        return card

    def remove_after_musik(self, cards):
        cards_discard = []
        for number in cards:
            cards_discard.append(self._hand[number])
        for card in cards_discard:
            self._hand.remove(card)
        return cards_discard

    def add_points(self, points):
        self._points += points

    def have_trump(self):
        # suits = {'Spades': 40, 'Hearts': 100, 'Clubs': 60, 'Diamonds': 80}
        trumps = []
        suits = ['Spades', 'Hearts', 'Clubs', 'Diamonds']
        for suit in suits:
            queen_card = Card('Queen', suit, 3)
            king_card = Card('King', suit, 4)
            if queen_card in self._hand and king_card in self._hand:
                trumps.append(suit)
        return trumps

    def set_trumps(self):
        trumps = self.have_trump()
        self._trumps = trumps

    def trump_played(self, trump):
        self._trumps.remove(trump)

    def suit_in_hand(self, suit):
        for card in self._hand:
            if card.suit == suit:
                return True
        return False

    @property
    def cards_in_hand(self):
        return len(self._hand)

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

    def __str__(self):
        result = f'{self._cards[0]}, {self._cards[1]}'
        return result

    def clear(self):
        self._cards.clear()


class Computer(Player):
    def __init__(self):
        super().__init__()

    def make_move(self, game, opponent_card=None):
        # This is a simple sketch, before apllying an algorithm for making
        # moves, i start by playing the first card
        if self._hand:
            played_card = self.play_card(0)
            return played_card
        else:
            return None

    def points_from_trumps(self):
        trumps = self.have_trump()
        points = 0
        suits = {'Spades': 40, 'Hearts': 100, 'Clubs': 60, 'Diamonds': 80}
        for element in trumps:
            points += suits[element]
        return points

    def possible_points(self, opponent_bid):
        possible_points = 0
        trump_points = self.points_from_trumps()
        trumps = self.have_trump()
        winning_cards = []
        for card in self._hand:
            if card.suit in trumps:
                winning_cards.append(card)
            elif card.points >= 10:
                winning_cards.append(card)
        for card in winning_cards:
            possible_points += card.points
        possible_points += trump_points
        points_to_bid = min(max(100, possible_points), 360)
        points_to_bid -= points_to_bid % 10
        points_to_bid += 10
        if points_to_bid > opponent_bid:
            return points_to_bid
        else:
            return 0

    def decide_to_bid(self, opponent_bid):
        points = self.possible_points(opponent_bid)
        if points == 0:
            return False
        else:
            return True

    def make_a_bid(self, opponent_bid):
        max_points = self.possible_points(opponent_bid)
        bid = opponent_bid + choice([10, 20])
        points = min(bid, max_points)
        return points

    def choose_musik(self):
        return randint(0, 1)

    def give_card(self, number, opponent):
        card = self._hand[number]
        self._hand.remove(card)
        opponent.add_card(card)
        return card

    def remove_after_musik(self):
        cards = self.choose_to_remove()
        for card in cards:
            self._hand.remove(card)
        return cards

    def choose_to_remove(self):
        trumps = self.have_trump()
        points = [0, 2, 3, 4, 10, 11]
        cards_to_remove = []
        names = ["Queen", "King"]
        for point in points:
            for card in self._hand:
                if len(cards_to_remove) == 2:
                    return cards_to_remove
                else:
                    if card.name not in names and card.suit not in trumps:
                        if card.points == point:
                            cards_to_remove.append(card)
        copy = self._hand.copy()
        while len(cards_to_remove) != 2:
            card = choice(copy)
            cards_to_remove.append(card)
            copy = copy.remove(card)
        return cards_to_remove


class Game:
    def __init__(self, deck, player, computer, musiki):
        self._deck = deck
        self._player = player
        self._computer = computer
        self._musiki = musiki
        self._round = 'p'
        self._trump = ''

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

    def trump_value(self, trump):
        suits = {'Spades': 40, 'Hearts': 100, 'Clubs': 60, 'Diamonds': 80}
        return suits.get(trump)

    @property
    def active_trump(self):
        return self._trump

    def set_trump(self, trump):
        self._trump = trump
