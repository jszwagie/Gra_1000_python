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
