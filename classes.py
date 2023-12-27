from dataclasses import dataclass
from random import shuffle, randint, choice


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


class Player:
    """
    :param name: _hand - List of cards in the player's hand.
    :param type: list
    :param name: _points - Points accumulated by the player.
    :param type: int
    :param name: _bid - Bid made by the player.
    :param type: int
    :param name: _trumps - List of trumps in the player's hand.
    :param type: list

    Represents a player in the game.

    Properties:
    - cards_in_hand - returns number of cards in hand
    - bid - returns player bid
    - points - returns player points
    - hand - returns list of cards in player's hand

    Methods:
    - play_card: Plays a card from the player's hand.
    - add_from_musik: Adds cards from Musik to the player's hand.
    - set_bid: Sets the bid made by the player.
    - remove_after_musik: Removes cards from the player's hand after Musik.
    - _add_points: Adds points to the player's total points.
    - _have_trump: Checks trumps in player's hand.
    - _set_trumps: Sets the trumps for the player.
    - _trump_played: Updates the trumps after a trump card is played.
    - _suit_in_hand: Checks if a specific suit is in the player's hand.
    - _final_points: Calculates the final points based on the bid.
    """
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

    def play_card(self, card_number):
        card = self._hand[card_number]
        self._hand.remove(card)
        return card

    def add_from_musik(self, musik):
        for card in musik.cards_in_musik():
            self._hand.append(card)
        musik._clear()

    def set_bid(self, bid):
        self._bid = bid

    def remove_after_musik(self, cards):
        cards_discard = []
        for number in cards:
            cards_discard.append(self._hand[number])
        for card in cards_discard:
            self._hand.remove(card)
        return cards_discard

    def _add_points(self, points):
        self._points += points

    def _have_trump(self):
        trumps = []
        suits = ['Spades', 'Hearts', 'Clubs', 'Diamonds']
        for suit in suits:
            queen_card = Card('Queen', suit, 3)
            king_card = Card('King', suit, 4)
            if queen_card in self._hand and king_card in self._hand:
                trumps.append(suit)
        return trumps

    def _set_trumps(self):
        trumps = self._have_trump()
        self._trumps = trumps

    def _trump_played(self, trump):
        self._trumps.remove(trump)

    def _suit_in_hand(self, suit):
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


class Computer(Player):
    """
    Represents an opponent in the game, inheriting from Player.

    Additional params:
    :param name: _temporary_trump - Helping param for making moves.
    :param type: str
    :param name: _trump_declared - Helping param saving info if
                                   opponent declared a trump
    :param type: bool

    Additional methods:
    - _pri_first: Function for sorting cards while choosing the best move
                  if opponent plays first.
    - _pri_suit: Function for sorting cards while choosing the best move
                  if opponent plays second.
    - make_move: Chosess a card to play by the opponent.
    - _points_from_trumps: Calculates points from trumps
                           in the computer's hand.
    - _possible_points: Calculates the possible points for a bid.
    - make_a_bid: Makes a bid for the opponent.
    - choose_musik: Chooses musik to get.
    - _choose_to_remove: Chooses cards to remove from the computer's hand
                         after clearing musik.
    - remove_after_musik: Removes cards from the computer's hand
                          after clearing musik.
    """
    def __init__(self):
        super().__init__()
        self._temporary_trump = ''
        self._trump_declared = False

    def _pri_first(self, card):
        if card.name == 'Ace':
            return -1
        elif card.suit in self._trumps and card.name in ["Queen", "King"]:
            return 12
        else:
            return card.points

    def _pri_suit(self, card, suit, game):
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
        if not self._suit_in_hand(self._temporary_trump):
            if len(trumps) > 1:
                trumps = sorted(trumps, key=lambda x: game._trump_value(x),
                                reverse=True)
            if trumps:
                self._temporary_trump = trumps[0]
        if opponent_card:
            base_suit = opponent_card.suit
            pri_cards = sorted(hand, key=lambda x:
                               self._pri_suit(x, base_suit, game),
                               reverse=True)
            card_to_play_index = hand.index(pri_cards[0])
        else:
            if self._temporary_trump and not self._trump_declared:
                card = Card("Queen", self._temporary_trump, 3)
                card_to_play_index = hand.index(card)
                self._trump_declared = True
            else:
                pri_cards = sorted(hand, key=lambda x: self._pri_first(x))
                card_to_play_index = hand.index(pri_cards[0])
        played_card = self.play_card(card_to_play_index)
        return played_card

    def _points_from_trumps(self):
        trumps = self._have_trump()
        points = 0
        suits = {'Spades': 40, 'Hearts': 100, 'Clubs': 60, 'Diamonds': 80}
        for element in trumps:
            points += suits[element]
        return points

    def _possible_points(self, opponent_bid):
        possible_points = 0
        trump_points = self._points_from_trumps()
        trumps = self._have_trump()
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
        if points_to_bid != 100:
            points_to_bid += 10
        if points_to_bid > opponent_bid:
            return points_to_bid
        else:
            return 0

    def make_a_bid(self, opponent_bid):
        max_points = self._possible_points(opponent_bid)
        if max_points != 0:
            bid = opponent_bid + choice([10, 20])
            points = min(bid, max_points)
        else:
            points = 0
        return points

    def choose_musik(self):
        return randint(0, 1)

    def _choose_to_remove(self):
        trumps = self._have_trump()
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

    def remove_after_musik(self):
        cards = self._choose_to_remove()
        for card in cards:
            self._hand.remove(card)
        return cards


class Game:
    """
    :param name: _deck - Deck used in the game
    :param type: object of class Deck
    :param name: _player - Player in the game
    :param type: object of class Player
    :param name: _computer - Opponent in the game
    :param type: object of class Computer
    :param name: _musiki - Two musiks (piles of cards to choose after bidding)
    :param type: list of objects of class Musik
    :param name: _round - Round of the game
    :param type: str
    :param name: _trump - Declared trump in the game
    :param type: str

    Represents the overall game.

    Properties:
    - active_trump - the active declared trump suit in the game.
    - player - player in the game.
    - computer - opponent in the game.
    - musiki -  two musiks
    - round - current round of the game ('p' for player, 'c' for computer).

    Methods:
    - deal_the_cards: Deals cards to the players and musiks.
    - _trump_value: Returns the point value of a trump suit.
    - count_final_points: Counts the final points for both players
                          and determines the result.
    - _set_trump: Sets the active trump suit.
    - set_round: Sets the current round of the game.
    - set_trumps_for_players: Sets the trumps for both players.
    - check_played_card: Checks if a played card is valid.
    - check_declaration: Checks if a player made a declaration of trump.
    - _points_battle: Determines the winning card by points.
    - _cards_battle: Determines the winning card taking into account trumps
                     and suits.
    - battle: Gives a result of a round and determines next round.
    - suits_dict: Returns a dictionary of suits with their symbols
                  and color/styles codes.
    """
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

    def _trump_value(self, trump):
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

    def _set_trump(self, trump):
        self._trump = trump

    def set_round(self, new_round):
        self._round = new_round

    def set_trumps_for_players(self):
        self._player._set_trumps()
        self._computer._set_trumps()

    def check_played_card(self, p_card, c_card):
        base_suit = c_card.suit
        if p_card.suit == base_suit or p_card.suit == self.active_trump:
            return False
        else:
            if (self._player._suit_in_hand(c_card.suit) or
               self._player._suit_in_hand(self.active_trump)):
                return True
            else:
                return False

    def check_declaration(self, p_card, player):
        is_trump_card = (p_card.suit in player._trumps)
        if is_trump_card and p_card.name in ['Queen', 'King']:
            self._set_trump(p_card.suit)
            player._trump_played(p_card.suit)
            player._add_points(self._trump_value(p_card.suit))
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
                self._player._add_points(points_for_win)
                next_round = 'p'
            else:
                self._computer._add_points(points_for_win)
                next_round = 'c'
        else:
            winning_card = self._cards_battle(computer_card, player_card)
            if winning_card == computer_card:
                self._computer._add_points(points_for_win)
                next_round = 'c'
            else:
                self._player._add_points(points_for_win)
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
