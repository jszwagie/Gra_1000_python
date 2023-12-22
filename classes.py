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
        desc = f'{self._name} {self._suit}'
        return desc

    def __eq__(self, other):
        if (self._name == other._name and self._suit == other._suit and
           self._points == other._points):
            return True
        else:
            return False


class Deck:
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


class Player:
    def __init__(self):
        self._hand = []
        self._points = 0
        self._bid = 0
        self._trumps = []

    @property
    def cards_in_hand(self):
        return len(self._hand)

    @property
    def bid(self):
        return self._bid

    @property
    def points(self):
        return self._points

    @property
    def hand(self):
        return self._hand

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

    def _final_points(self):
        if self._points < self._bid:
            final_points = 0 - self._points
        elif self._bid == 0:
            final_points = self._points
        else:
            final_points = self._bid
        return (round(final_points/10)*10)


class Musik(Deck):
    def __init__(self):
        super().__init__()

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
        self._temporary_trump = ''
        self._trump_declared = False

    def pri_first(self, card):
        if card.name == 'Ace':
            return -1
        elif card.suit in self._trumps and card.name in ["Queen", "King"]:
            return 12
        else:
            return card.points

    def pri_suit(self, card, suit, game):
        priority = 0
        if card.suit == suit:
            priority += 100
        elif card.suit == game.active_trump:
            priority += 50
        priority += card.points
        return priority

    def make_move(self, game, opponent_card=None):
        hand = self._hand
        trumps = self._trumps
        if game.active_trump != self._temporary_trump:
            self._temporary_trump = ''
        if not self.suit_in_hand(self._temporary_trump):
            if len(trumps) > 1:
                trumps = sorted(trumps, key=lambda x: game.trump_value(x),
                                reverse=True)
            if trumps:
                self._temporary_trump = trumps[0]
        if opponent_card:
            base_suit = opponent_card.suit
            pri_cards = sorted(hand, key=lambda x:
                               self.pri_suit(x, base_suit, game),
                               reverse=True)
            card_to_play_index = hand.index(pri_cards[0])
        else:
            if self._temporary_trump and not self._trump_declared:
                card = Card("Queen", self._temporary_trump, 3)
                card_to_play_index = hand.index(card)
                self._trump_declared = True
            else:
                pri_cards = sorted(hand, key=lambda x: self.pri_first(x))
                card_to_play_index = hand.index(pri_cards[0])
        played_card = self.play_card(card_to_play_index)
        return played_card

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

    def make_a_bid(self, opponent_bid):
        max_points = self.possible_points(opponent_bid)
        if max_points != 0:
            bid = opponent_bid + choice([10, 20])
            points = min(bid, max_points)
        else:
            points = 0
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

    @property
    def active_trump(self):
        return self._trump

    @property
    def player(self):
        return self._player

    @property
    def computer(self):
        return self._computer

    @property
    def round(self):
        return self._round

    @property
    def musiki(self):
        return self._musiki

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

    def count_final_points(self):
        final_p_points = self._player._final_points()
        final_c_points = self._computer._final_points()
        if final_p_points < final_c_points:
            result = 'c'
        elif final_c_points == final_p_points:
            result = 'm'
        else:
            result = 'p'
        return final_p_points, final_c_points, result

    def set_trump(self, trump):
        self._trump = trump

    def set_round(self, new_round):
        self._round = new_round

    def set_trumps_for_players(self):
        self._player.set_trumps()
        self._computer.set_trumps()

    def check_played_card(self, p_card, c_card):
        base_suit = c_card.suit
        if p_card.suit == base_suit or p_card.suit == self.active_trump:
            return False
        else:
            if (self._player.suit_in_hand(c_card.suit) or
               self._player.suit_in_hand(self.active_trump)):
                return True
            else:
                return False

    def check_declaration(self, p_card, player):
        is_trump_card = (p_card.suit in player._trumps)
        if is_trump_card and p_card.name in ['Queen', 'King']:
            self.set_trump(p_card.suit)
            player.trump_played(p_card.suit)
            player.add_points(self.trump_value(p_card.suit))
            return p_card.suit
        else:
            return None

    def _points_battle(self, p_card, c_card):
        if p_card.points > c_card.points:
            return p_card
        else:
            return c_card

    def _cards_battle(self, first_card, second_card):
        if first_card.suit == self.active_trump:
            if second_card.suit == self.active_trump:
                winning_card = self._points_battle(first_card, second_card)
            else:
                winning_card = first_card
        else:
            if second_card.suit == self.active_trump:
                winning_card = second_card
            else:
                if first_card.suit == second_card.suit:
                    winning_card = self._points_battle(first_card, second_card)
                else:
                    winning_card = first_card
        return winning_card

    def battle(self, player_card, computer_card):
        points_for_win = player_card.points + computer_card.points
        if self._round == 'p':
            winning_card = self._cards_battle(player_card, computer_card)
            if winning_card == player_card:
                self._player.add_points(points_for_win)
                next_round = 'p'
            else:
                self._computer.add_points(points_for_win)
                next_round = 'c'
        else:
            winning_card = self._cards_battle(computer_card, player_card)
            if winning_card == computer_card:
                self._computer.add_points(points_for_win)
                next_round = 'c'
            else:
                self._player.add_points(points_for_win)
                next_round = 'p'
        return next_round

    def suits_dict(self):
        suits = {
            'Clubs': (' \u2663', "black b"),
            'Diamonds': (' \u2666', "red b"),
            'Hearts': (' \u2665', "red b"),
            'Spades': (' \u2660', "black b")
        }
        return suits
