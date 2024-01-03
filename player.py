from card import Card


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
    - _points_from_trumps: Calculates points from trumps
                           in player's hand.
    - _max_bid: Calculates max bid the player can make.
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

    def _points_from_trumps(self):
        trumps = self._have_trump()
        points = 0
        suits = {'Spades': 40, 'Hearts': 100, 'Clubs': 60, 'Diamonds': 80}
        for element in trumps:
            points += suits[element]
        return points

    def _max_bid(self):
        max_points = self._points_from_trumps()
        for card in self._hand:
            max_points += card.points
        max_points = max_points - (max_points % 10) + 10
        max_points = max(110, max_points)
        return max_points

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
