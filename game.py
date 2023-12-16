from classes import Deck, Player, Musik, Computer, Game


def starting_player_clear_musik(chosen_musik, game):
    chosen_musik -= 1
    game._player.add_from_musik(game._musiki[chosen_musik])
    if game._round == 'p':
        print(game._player.show_hand())
        print("choose a card for your opponent (1 - 10):")
        card = int(input(">")) - 1
        game._player.give_card(card, game._computer)
    else:
        game._computer.give_card(0, game._player)


def main():
    deck = Deck()
    player = Player()
    computer = Computer()
    musiki = (Musik(), Musik())
    deck.generate_deck()
    deck.shuffle_deck()
    game = Game(deck, player, computer, musiki)
    print('Welcome to the game "1000", cards are being dealt')
    game.deal_the_cards()
    print([game._player.show_hand(), game._computer.show_hand(),
           game._musiki[0].cards_in_musik(), game._musiki[1].cards_in_musik()])
    print("Insert your bid:")
    not_passed = True
    chosen_musik = 1
    while not_passed:
        player_bid = input(">")
        if player_bid == "pass":
            player.set_bid(-1)
            game._round = 'c'
            not_passed = False
        elif computer.decide_to_bid() is False:
            game._round = 'p'
            computer.set_bid(-1)
            not_passed = False
            chosen_musik = int(input('Choose a musik to get: '))
    starting_player_clear_musik(chosen_musik, game)
    print([game._player.show_hand(), game._computer.show_hand(),
           game._musiki[0].cards_in_musik(), game._musiki[1].cards_in_musik()])


if __name__ == "__main__":
    main()
