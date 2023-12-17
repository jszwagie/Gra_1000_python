from classes import Deck, Player, Musik, Computer, Game


def input_cards_to_discard():
    bad_input = True
    while bad_input:
        try:
            cards = input(">")
            cards = cards.split(", ")
            card_1 = int(cards[0])
            card_2 = int(cards[1])
            if (card_1 in range(1, 13) and card_2 in range(1, 13) and
               card_1 != card_2):
                cards_numbers = [card_1 - 1, card_2 - 1]
                bad_input = False
            else:
                raise Exception
        except Exception:
            print('I do not know what you mean.'
                  'Try again with "number, number".')
    return cards_numbers


def input_musik():
    bad_input = True
    while bad_input:
        try:
            chosen_musik = int(input(">")) - 1
            if chosen_musik in [0, 1]:
                bad_input = False
            else:
                raise Exception
        except Exception:
            print("There is no musik with this number. Try again.")
    return chosen_musik


def bidding(game):
    list_of_bids = [str(element) for element in list(range(100, 361))]
    list_of_bids = list_of_bids[::10]
    list_of_bids.append("pass")
    player = game._player
    computer = game._computer
    not_passed = True
    while not_passed:
        print("How much are you bidding?:")
        player_bid = input(">")
        if str(player_bid).lower() == "pass":
            print("You passed")
            player.set_bid(-1)
            game._round = 'c'
            not_passed = False
            chosen_musik = computer.choose_musik()
            continue
        elif (player_bid not in list_of_bids or
              computer.bid > int(player_bid)):
            print("You must bid points between 100 and 360, "
                  "tens, higher than opponent or pass")
            continue
        else:
            player.set_bid(player_bid)
        if computer.decide_to_bid(int(player_bid)):
            computer.set_bid(computer.make_a_bid(int(player_bid)))
            print(f"Opponent bidded: {computer.bid}")
            continue
        else:
            print('Opponent passed')
            game._round = 'p'
            computer.set_bid(-1)
            not_passed = False
            print('Choose a musik to get(1,2): ')
            chosen_musik = input_musik()
    return chosen_musik


def cards_battle(p_card, c_card, game):
    if p_card.points > c_card.points:
        game._player.add_points(p_card.points + c_card.points)
        next_round = 'p'
    else:
        game._computer.add_points(p_card.points + c_card.points)
        next_round = 'c'
    return next_round


def play_round(game):
    if game._round == 'p':
        print(game._player.cards_display())
        print(f'Choose a card to play(1-{game._player.cards_in_hand}): ')
        card_number = int(input('>')) - 1
        played_p_card = game._player.play_card(card_number)
        print(f'You played: {played_p_card}.')
        played_c_card = game._computer.make_move(played_p_card)
        print(f'Opponent played: {played_c_card}.')
        next_round = cards_battle(played_p_card, played_c_card, game)
        if next_round == 'p':
            print('You won!')
        else:
            print('Computer won')
    else:
        played_c_card = game._computer.make_move()
        print(f'Opponent played: {played_c_card}.')
        print(game._player.cards_display())
        print(f'Choose a card to play(1-{game._player.cards_in_hand}): ')
        card_number = int(input('>')) - 1
        played_p_card = game._player.play_card(card_number)
        print(f'You played: {played_p_card}.')
        next_round = cards_battle(played_p_card, played_c_card, game)
        if next_round == 'p':
            print('You won!')
        else:
            print('Opponent won')
    game._round = next_round


def starting_player_clear_musik(chosen_musik, game):
    if game._round == 'p':
        game._player.add_from_musik(game._musiki[chosen_musik])
        print(game._player.cards_display())
        print("Choose two cards to discard (number, number)(1-12):")
        cards = input_cards_to_discard()
        card_1, card_2 = game._player.remove_after_musik(cards)
        print(f"You discarded: {card_1}, {card_2}.")
    else:
        musik = game._musiki[chosen_musik]
        print(f"Opponent chose {chosen_musik+1} Musik: {musik}")
        game._computer.add_from_musik(musik)
        print(game._computer.cards_display())
        card_1, card_2 = game._computer.remove_after_musik()
        print(game._computer.cards_display())


def main():
    deck = Deck()
    player = Player()
    computer = Computer()
    musiki = (Musik(), Musik())
    deck.generate_deck()
    deck.shuffle_deck()
    game = Game(deck, player, computer, musiki)
    print('Welcome to the game "1000", cards are being dealt.')
    game.deal_the_cards()
    chosen_musik = bidding(game)
    starting_player_clear_musik(chosen_musik, game)
    for _ in range(10):
        play_round(game)
    print(f'You have {game._player._points} points,'
          f' Opponent have {game._computer._points} points')


if __name__ == "__main__":
    main()
