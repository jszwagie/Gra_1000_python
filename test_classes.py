from classes import Card, Deck, Player, Musik, Computer


# Testy dla klasy Card
def test_Card_init_and_properties():
    queen = Card('Queen', 'Spades', 11)
    assert queen.name == 'Queen'
    assert queen.points == 11
    assert queen.suit == 'Spades'


# Testy dla klasy Deck
def test_generate_deck():
    deck_1 = Deck()
    deck_1.generate_deck()
    assert len(deck_1.deck) == 24


def test_schuffle_deck():
    deck_1 = Deck()
    deck_1.generate_deck()
    original = deck_1.deck.copy()
    deck_1.shuffle_deck()
    assert original != deck_1.deck
    assert len(original) == len(deck_1.deck)


# Testy dla klasy Player
def test_Player_add_card():
    player = Player()
    card = Card("Ace", "Spades", 11)
    player.add_card(card)
    assert len(player._hand) == 1
    assert player._hand[0] == card


def test_Player_play_card():
    player = Player()
    card_1 = Card("Ace", "Spades", 11)
    card_2 = Card("King", "Hearts", 4)
    player.add_card(card_1)
    player.add_card(card_2)
    played_card = player.play_card(0)
    assert played_card == card_1
    assert len(player._hand) == 1


def test_add_from_musik():
    player = Player()
    musik = Musik()
    musik._cards = [Card("Ace", "Spades", 11), Card("10", "Hearts", 10)]
    player.add_from_musik(musik)
    assert len(player._hand) == 2


def test_show_hand():
    player = Player()
    card_1 = Card("Ace", "Spades", 11)
    card_2 = Card("10", "Hearts", 10)
    player.add_card(card_1)
    player.add_card(card_2)
    hand = player.show_hand()
    assert len(hand) == 2
    assert 'Ace of Spades' in hand
    assert '10 of Hearts' in hand


# Testy dla klasy Musik
def test_add_card_to_musik():
    musik = Musik()
    card = Card("Ace", "Spades", 11)
    musik.add_card(card)
    assert len(musik.cards_in_musik()) == 1
    assert musik.cards_in_musik()[0] == card


def test_cards_in_musik():
    musik = Musik()
    card_1 = Card("Ace", "Spades", 11)
    card_2 = Card("10", "Hearts", 10)
    musik.add_card(card_1)
    musik.add_card(card_2)
    cards_in_musik = musik.cards_in_musik()
    assert len(cards_in_musik) == 2
    assert card_1 in cards_in_musik
    assert card_2 in cards_in_musik


# Wstępne testy dla wersji testowej klasy Computer
def test_Computer_make_move():
    computer = Computer()
    card_1 = Card("Ace", "Spades", 11)
    card_2 = Card("10", "Hearts", 10)
    computer.add_card(card_1)
    computer.add_card(card_2)
    played_card = computer.make_move()
    assert played_card == card_1
    assert len(computer._hand) == 1


def test_Computer_decide_to_bid():
    computer = Computer()
    decision = computer.decide_to_bid()
    assert not decision
