from classes import Card


def test_Card_init_and_properties():
    queen = Card('Queen', 'Spades', 11)
    assert queen.name == 'Queen'
    assert queen.points == 11
    assert queen.suit == 'Spades'
