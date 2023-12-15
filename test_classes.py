from classes import Card, Deck


def test_Card_init_and_properties():
    queen = Card('Queen', 'Spades', 11)
    assert queen.name == 'Queen'
    assert queen.points == 11
    assert queen.suit == 'Spades'


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
