from card import Card
from deck import Deck
from player import Player
from musik import Musik
from computer import Computer
from game import Game


class TestGame():
    def __init__(self):
        self.trump = ''

    @property
    def active_trump(self):
        return self.trump


# testy klasy Card:
def test_card_properties():
    card = Card("Ace", "Hearts", 11)
    assert card.name == "Ace"
    assert card.suit == "Hearts"
    assert card.points == 11


def test_card_equality():
    card_1 = Card("Ace", "Hearts", 11)
    card_2 = Card("Ace", "Hearts", 11)
    assert card_1 == card_2


def test_card_inequality():
    card_1 = Card("Ace", "Hearts", 11)
    card_2 = Card("King", "Spades", 4)
    assert card_1 != card_2


# testy klasy Deck:
def test_deck_init():
    deck = Deck()
    assert len(deck.deck) == 0


def test_deck_generate_deck():
    deck = Deck()
    deck.generate_deck()
    assert len(deck.deck) == 24


def test_deck_shuffle_deck():
    deck = Deck()
    deck.generate_deck()
    original = list(deck.deck)
    deck.shuffle_deck()
    assert deck.deck != original


# testy klasy Player
def test_player_init():
    player = Player()
    assert player.cards_in_hand == 0
    assert player.bid == 0
    assert player.points == 0


def test_player_play_card():
    player = Player()
    card = Card("Ace", "Hearts", 11)
    player._hand = [card]
    played_card = player.play_card(0)
    assert played_card == card
    assert player.cards_in_hand == 0


def test_player_add_from_musik():
    player = Player()
    musik = Musik()
    musik._cards = [Card("Ace", "Hearts", 11), Card("10", "Diamonds", 10)]
    player.add_from_musik(musik)
    assert player.cards_in_hand == 2
    assert not musik.cards_in_musik()


def test_player_set_bid():
    player = Player()
    player.set_bid(100)
    assert player.bid == 100


def test_player_remove_after_musik():
    player = Player()
    player._hand = [Card("Ace", "Hearts", 11),
                    Card("10", "Diamonds", 10),
                    Card("King", "Spades", 4)]
    cards_to_remove = [0, 2]
    removed = player.remove_after_musik(cards_to_remove)
    assert len(removed) == 2
    assert player.cards_in_hand == 1


def test_player_add_points():
    player = Player()
    player._add_points(15)
    assert player.points == 15


def test_player_have_trump():
    player = Player()
    player._hand = [Card("Queen", "Hearts", 3),
                    Card("King", "Hearts", 4)]
    trumps = player._have_trump()
    assert trumps == ["Hearts"]


def test_player_set_trumps():
    player = Player()
    player._hand = [Card("Queen", "Hearts", 3),
                    Card("King", "Hearts", 4)]
    player._set_trumps()
    assert player._trumps == ["Hearts"]


def test_player_trump_played():
    player = Player()
    player._trumps = ["Hearts", "Spades", "Diamonds"]
    player._trump_played("Hearts")
    assert player._trumps == ["Spades", "Diamonds"]


def test_player_suit_in_hand_true():
    player = Player()
    player._hand = [Card("Ace", "Hearts", 11),
                    Card("10", "Diamonds", 10)]
    assert player._suit_in_hand("Hearts") is True


def test_player_suit_in_hand_false():
    player = Player()
    player._hand = [Card("Ace", "Hearts", 11),
                    Card("10", "Diamonds", 10)]
    assert player._suit_in_hand("Spades") is False


def test_player_final_points_below_bid():
    player = Player()
    player._points = 14
    player._bid = 120
    final_points = player._final_points()
    assert final_points == -10


def test_player_final_points_bid_zero():
    player = Player()
    player._points = 97
    player._bid = 0
    final_points = player._final_points()
    assert final_points == 100


def test_player_final_points_equal_bid():
    player = Player()
    player._points = 120
    player._bid = 120
    final_points = player._final_points()
    assert final_points == 120


def test_player_final_points_above_bid():
    player = Player()
    player._points = 145
    player._bid = 120
    final_points = player._final_points()
    assert final_points == 120


# Testy klasy Musik
def test_musik_init():
    musik = Musik()
    assert len(musik.cards_in_musik()) == 0


def test_musik_cards_in_musik():
    musik = Musik()
    cards = [Card("Ace", "Spades", 11), Card("10", "Diamonds", 10)]
    musik._cards = cards
    assert len(musik.cards_in_musik()) == 2
    assert musik.cards_in_musik() == cards


def test_musik_clear():
    musik = Musik()
    cards = [Card("Ace", "Spades", 11), Card("10", "Diamonds", 10)]
    musik._cards = cards
    musik._clear()
    assert len(musik.cards_in_musik()) == 0


# Testy klasy Computer
def test_computer_init():
    computer = Computer()
    assert computer.cards_in_hand == 0
    assert computer.bid == 0
    assert computer.points == 0


def test_computer_pri_first_ace():
    computer = Computer()
    card = Card("Ace", "Hearts", 11)
    priority = computer._pri_first(card)
    assert priority == -1


def test_computer_pri_first_trump_queen():
    computer = Computer()
    computer._trumps = ["Hearts"]
    card = Card("Queen", "Hearts", 3)
    priority = computer._pri_first(card)
    assert priority == 12


def test_computer_pri_suit_same_suit():
    computer = Computer()
    card = Card("10", "Diamonds", 10)
    base_suit = "Diamonds"
    game = TestGame()
    priority = computer._pri_suit(card, base_suit, game)
    assert priority == 110


def test_computer_pri_suit_trump_suit():
    computer = Computer()
    card = Card("10", "Diamonds", 10)
    base_suit = "Spades"
    game = TestGame()
    game.trump = "Diamonds"
    priority = computer._pri_suit(card, base_suit, game)
    assert priority == 60


def test_computer_pri_suit_unmatching_suit():
    computer = Computer()
    card = Card("10", "Diamonds", 10)
    base_suit = "Clubs"
    game = TestGame()
    priority = computer._pri_suit(card, base_suit, game)
    assert priority == 10


def test_computer_make_move_first():
    computer = Computer()
    game = TestGame()
    card_1 = Card("Ace", "Hearts", 11)
    card_2 = Card("10", "Diamonds", 10)
    computer._hand = [card_1, card_2]
    played_card = computer.make_move(game)
    assert played_card not in computer.hand
    assert played_card == card_1


def test_computer_make_move_trump_declared_first():
    computer = Computer()
    game = TestGame()
    card_1 = Card("Queen", "Hearts", 3)
    card_2 = Card("King", "Hearts", 4)
    card_3 = Card("Ace", "Spades", 11)
    computer._hand = [card_1, card_2, card_3]
    computer._temporary_trump = "Hearts"
    computer._trump_declared = False
    played_card = computer.make_move(game)
    assert played_card not in computer.hand
    assert played_card == card_3


def test_computer_make_move_trump_declared_second():
    computer = Computer()
    game = TestGame()
    game.trump = "Hearts"
    card_1 = Card("Queen", "Hearts", 3)
    card_2 = Card("King", "Hearts", 4)
    card_3 = Card("Ace", "Spades", 11)
    computer._hand = [card_1, card_2, card_3]
    computer._temporary_trump = "Hearts"
    computer._trump_declared = True
    opponent_card = Card("Ace", "Diamonds", 11)
    played_card = computer.make_move(game, opponent_card)
    assert played_card not in computer.hand
    assert played_card == card_2


def test_computer_make_move_no_trump_declared_second():
    computer = Computer()
    game = TestGame()
    card_1 = Card("Queen", "Hearts", 3)
    card_2 = Card("King", "Hearts", 4)
    card_3 = Card("10", "Diamonds", 10)
    computer._hand = [card_1, card_2, card_3]
    computer._temporary_trump = ""
    computer._trump_declared = False
    opponent_card = Card("Ace", "Diamonds", 11)
    played_card = computer.make_move(game, opponent_card)
    assert played_card not in computer.hand
    assert played_card == card_3


def test_computer_points_from_trumps_no_trumps():
    computer = Computer()
    trumps_points = computer._points_from_trumps()
    assert trumps_points == 0


def test_computer_points_from_trumps_with_trumps():
    computer = Computer()
    computer._hand = [Card("Queen", "Hearts", 3), Card("King", "Hearts", 4)]
    trumps_points = computer._points_from_trumps()
    assert trumps_points == 100


def test_computer_possible_points_min_bid():
    computer = Computer()
    computer._hand = [Card("Queen", "Spades", 3),
                      Card("King", "Hearts", 4),
                      Card("10", "Diamonds", 10)]
    opponent_bid = 0
    possible_points = computer._possible_points(opponent_bid)
    assert possible_points == 100


def test_computer_possible_points_with_trumps():
    computer = Computer()
    computer._hand = [Card("Queen", "Hearts", 3),
                      Card("King", "Hearts", 4),
                      Card("10", "Diamonds", 10)]
    opponent_bid = 0
    possible_points = computer._possible_points(opponent_bid)
    assert possible_points == 120


def test_computer_make_bid_zero_points():
    computer = Computer()
    opponent_bid = 100
    bid = computer.make_a_bid(opponent_bid)
    assert bid == 0


def test_computer_make_bid_possible_points(monkeypatch):
    computer = Computer()
    computer._hand = [Card("Queen", "Hearts", 3),
                      Card("King", "Hearts", 4),
                      Card("10", "Diamonds", 10),
                      Card("10", "Spades", 10)]
    opponent_bid = 100
    monkeypatch.setattr("classes.choice", lambda x: 10)
    bid = computer.make_a_bid(opponent_bid)
    assert bid == 110


def test_computer_make_bid_higher_player_bid():
    computer = Computer()
    computer._hand = [Card("Queen", "Hearts", 3),
                      Card("King", "Hearts", 4),
                      Card("10", "Diamonds", 10),
                      Card("10", "Spades", 10)]
    opponent_bid = 200
    bid = computer.make_a_bid(opponent_bid)
    assert bid == 0


def test_computer_choose_musik(monkeypatch):
    computer = Computer()
    monkeypatch.setattr("classes.randint", lambda a, b: 0)
    musik_choice = computer.choose_musik()
    assert musik_choice == 0


def test_computer_choose_to_remove(monkeypatch):
    computer = Computer()

    def new_choice():
        return computer._hand[0]
    card_1 = Card("Queen", "Hearts", 3)
    card_2 = Card("King", "Hearts", 4)
    card_3 = Card("10", "Diamonds", 10)
    card_4 = Card("9", "Clubs", 0)
    computer._hand = [card_1, card_2, card_3, card_4]
    monkeypatch.setattr("classes.choice", new_choice())
    cards_to_remove = computer._choose_to_remove()
    assert len(cards_to_remove) == 2
    assert card_3 in cards_to_remove
    assert card_4 in cards_to_remove


def test_computer_remove_after_musik(monkeypatch):
    computer = Computer()

    def new_choice():
        return computer._hand[0]
    card_1 = Card("Queen", "Hearts", 3)
    card_2 = Card("King", "Hearts", 4)
    card_3 = Card("10", "Diamonds", 10)
    card_4 = Card("9", "Clubs", 0)
    computer._hand = [card_1, card_2, card_3, card_4]
    monkeypatch.setattr("classes.choice", new_choice())
    removed_cards = computer.remove_after_musik()
    assert len(removed_cards) == 2
    assert card_3 in removed_cards
    assert card_4 in removed_cards


# Testy dla klasy Game
def test_game_initialization():
    deck = Deck()
    player = Player()
    computer = Computer()
    musiki = [Musik(), Musik()]
    game = Game(deck, player, computer, musiki)
    assert game.active_trump == ''
    assert game.player == player
    assert game.computer == computer
    assert game.round == 'p'
    assert game.musiki == musiki


def test_deal_the_cards():
    deck = Deck()
    deck.generate_deck()
    player = Player()
    computer = Computer()
    musiki = [Musik(), Musik()]
    game = Game(deck, player, computer, musiki)
    game.deal_the_cards()
    assert len(player._hand) == 10
    assert len(computer._hand) == 10
    assert len(musiki[0]._cards) == 2
    assert len(musiki[1]._cards) == 2


def test_trump_value():
    game = Game(Deck(), Player(), Computer(), [Musik(), Musik()])
    assert game._trump_value('Spades') == 40
    assert game._trump_value('Hearts') == 100
    assert game._trump_value('Clubs') == 60
    assert game._trump_value('Diamonds') == 80
    assert game._trump_value('Invalid_Suit') is None


def test_count_final_points():
    deck = Deck()
    player = Player()
    computer = Computer()
    musiki = [Musik(), Musik()]
    game = Game(deck, player, computer, musiki)
    player._add_points(30)
    computer._add_points(40)
    final_p_points, final_c_points, result = game.count_final_points()
    assert final_p_points == 30
    assert final_c_points == 40
    assert result == 'c'


def test_set_trump():
    deck = Deck()
    player = Player()
    computer = Computer()
    musiki = [Musik(), Musik()]
    game = Game(deck, player, computer, musiki)
    game._set_trump('Hearts')
    assert game.active_trump == 'Hearts'


def test_set_round():
    deck = Deck()
    player = Player()
    computer = Computer()
    musiki = [Musik(), Musik()]
    game = Game(deck, player, computer, musiki)
    game.set_round('c')
    assert game.round == 'c'


def test_set_trumps_for_players():
    deck = Deck()
    player = Player()
    computer = Computer()
    musiki = [Musik(), Musik()]
    game = Game(deck, player, computer, musiki)
    game.set_trumps_for_players()
    assert player._trumps == []
    assert computer._trumps == []
    player._hand = [Card('Queen', 'Hearts', 3), Card('King', 'Hearts', 4)]
    computer._hand = [Card('Queen', 'Diamonds', 3),
                      Card('King', 'Diamonds', 4)]
    game.set_trumps_for_players()
    assert player._trumps == ['Hearts']
    assert computer._trumps == ['Diamonds']


def test_check_played_card():
    deck = Deck()
    player = Player()
    computer = Computer()
    musiki = [Musik(), Musik()]
    game = Game(deck, player, computer, musiki)
    player._hand = [Card('9', 'Hearts', 0), Card('King', 'Diamonds', 4),
                    Card('10', 'Spades', 10), Card('Queen', 'Diamonds', 3)]
    p_card = Card('10', 'Spades', 10)
    c_card = Card('9', 'Clubs', 0)
    assert game.check_played_card(p_card, c_card) is False
    p_card = Card('Queen', 'Diamonds', 3)
    c_card = Card('9', 'Clubs', 0)
    assert game.check_played_card(p_card, c_card) is False
    p_card = Card('9', 'Hearts', 0)
    c_card = Card('9', 'Spades', 0)
    assert game.check_played_card(p_card, c_card) is True


def test_check_declaration():
    deck = Deck()
    player = Player()
    computer = Computer()
    musiki = [Musik(), Musik()]
    game = Game(deck, player, computer, musiki)
    p_card = Card('Queen', 'Diamonds', 3)
    player._trumps = ['Diamonds']
    trump_suit = game.check_declaration(p_card, player)
    assert trump_suit == 'Diamonds'
    assert game.active_trump == 'Diamonds'
    assert player._trumps == []
    game._trump = ''
    p_card_2 = Card('Queen', 'Diamonds', 3)
    player._trumps = ['Hearts']
    trump_suit = game.check_declaration(p_card_2, player)
    assert trump_suit is None
    assert game.active_trump == ''


def test_points_battle():
    deck = Deck()
    player = Player()
    computer = Computer()
    musiki = [Musik(), Musik()]
    game = Game(deck, player, computer, musiki)
    p_card = Card('King', 'Hearts', 4)
    c_card = Card('Queen', 'Hearts', 3)
    winner_card = game._points_battle(p_card, c_card)
    assert winner_card == p_card
    p_card = Card('10', 'Spades', 10)
    c_card = Card('King', 'Diamonds', 4)
    winner_card = game._points_battle(p_card, c_card)
    assert winner_card == p_card
    p_card = Card('9', 'Clubs', 0)
    c_card = Card('9', 'Diamonds', 0)
    winner_card = game._points_battle(p_card, c_card)
    assert winner_card == c_card


def test_cards_battle():
    deck = Deck()
    player = Player()
    computer = Computer()
    musiki = [Musik(), Musik()]
    game = Game(deck, player, computer, musiki)
    p_card = Card('King', 'Hearts', 4)
    c_card = Card('Queen', 'Hearts', 3)
    winner_card = game._cards_battle(p_card, c_card)
    assert winner_card == p_card
    p_card = Card('10', 'Spades', 10)
    c_card = Card('King', 'Diamonds', 4)
    winner_card = game._cards_battle(p_card, c_card)
    assert winner_card == p_card
    p_card = Card('9', 'Clubs', 0)
    c_card = Card('9', 'Diamonds', 0)
    winner_card = game._cards_battle(p_card, c_card)
    assert winner_card == p_card
    game._trump = 'Clubs'
    p_card = Card('Queen', 'Diamonds', 3)
    c_card = Card('9', 'Clubs', 0)
    winner_card = game._cards_battle(p_card, c_card)
    assert winner_card == c_card
    p_card = Card('King', 'Spades', 4)
    c_card = Card('10', 'Spades', 10)
    winner_card = game._cards_battle(p_card, c_card)
    assert winner_card == c_card


def test_battle():
    deck = Deck()
    player = Player()
    computer = Computer()
    musiki = [Musik(), Musik()]
    game = Game(deck, player, computer, musiki)
    p_card = Card('King', 'Hearts', 4)
    c_card = Card('Queen', 'Hearts', 3)
    game.set_round('p')
    next_round = game.battle(p_card, c_card)
    assert player.points == 7
    assert computer.points == 0
    assert next_round == 'p'
    p_card = Card('10', 'Spades', 10)
    c_card = Card('King', 'Diamonds', 4)
    game.set_round('c')
    next_round = game.battle(p_card, c_card)
    assert player.points == 7
    assert computer.points == 14
    assert next_round == 'c'
    game._trump = 'Clubs'
    p_card = Card('9', 'Clubs', 0)
    c_card = Card('9', 'Diamonds', 0)
    game.set_round('p')
    next_round = game.battle(p_card, c_card)
    assert player.points == 7
    assert computer.points == 14
    assert next_round == 'p'


def test_suits_dict():
    deck = Deck()
    player = Player()
    computer = Computer()
    musiki = [Musik(), Musik()]
    game = Game(deck, player, computer, musiki)
    suits = game.suits_dict()
    assert suits['Clubs'] == (' \u2663', "black b")
    assert suits['Diamonds'] == (' \u2666', "red b")
    assert suits['Hearts'] == (' \u2665', "red b")
    assert suits['Spades'] == (' \u2660', "black b")
