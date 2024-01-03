from player import Player
from card import Card
from random import choice, randint


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
