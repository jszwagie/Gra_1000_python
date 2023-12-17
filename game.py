from classes import Deck, Player, Musik, Computer, Game


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
            chosen_musik = int(input('>')) - 1
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
        print("Choose a card for your opponent (1 - 12):")
        card = int(input(">")) - 1
        game._player.give_card(card, game._computer)
    else:
        game._computer.add_from_musik(game._musiki[chosen_musik])
        card = game._computer.give_card(0, game._player)
        print(f'Opponent gave you card: {card}')


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
    for _ in range(11):
        play_round(game)
    print(f'You have {game._player._points} points,'
          f' Opponent have {game._computer._points} points')


if __name__ == "__main__":
    main()
