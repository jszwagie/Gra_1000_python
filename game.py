from classes import Deck, Player, Musik, Computer, Game
from sys import exit


def is_exit(inputted_data):
    if inputted_data.lower() == 'exit':
        exit()


def input_cards_to_discard():
    bad_input = True
    while bad_input:
        try:
            cards = input(">")
            is_exit(cards)
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


def choose_card_input(game):
    bad_input = True
    while bad_input:
        try:
            cards_amount = game._player.cards_in_hand
            chosen_card = input(">")
            is_exit(chosen_card)
            chosen_card = int(chosen_card)
            if chosen_card in range(1, cards_amount+1):
                bad_input = False
            else:
                raise Exception
        except Exception:
            print("There is no card with this number. Try again.")
    return chosen_card - 1


def input_musik():
    bad_input = True
    while bad_input:
        try:
            chosen_musik = input(">")
            is_exit(chosen_musik)
            chosen_musik = int(chosen_musik) - 1
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
        is_exit(player_bid)
        if str(player_bid).lower() == "pass":
            print("You passed")
            player.set_bid(0)
            game._round = 'c'
            not_passed = False
            chosen_musik = computer.choose_musik()
            continue
        elif (player_bid not in list_of_bids or
              computer.bid >= int(player_bid)):
            print("You must bid points between 100 and 360, "
                  "tens, higher than opponent or pass")
            continue
        else:
            player.set_bid(int(player_bid))
        if computer.decide_to_bid(int(player_bid)):
            computer.set_bid(computer.make_a_bid(int(player_bid)))
            print(f"Opponent bidded: {computer.bid}")
            continue
        else:
            print('Opponent passed')
            game._round = 'p'
            computer.set_bid(0)
            not_passed = False
            print('Choose a musik to get(1,2): ')
            chosen_musik = input_musik()
    return chosen_musik


def points_battle(p_card, c_card):
    if p_card.points > c_card.points:
        return p_card
    else:
        return c_card


def cards_battle(first_card, second_card, game):
    if first_card.suit == game.active_trump:
        if second_card.suit == game.active_trump:
            winning_card = points_battle(first_card, second_card)
        else:
            winning_card = first_card
    else:
        if second_card.suit == game.active_trump:
            winning_card = second_card
        else:
            if first_card.suit == second_card.suit:
                winning_card = points_battle(first_card, second_card)
            else:
                winning_card = first_card
    return winning_card


def battle(player_card, computer_card, game):
    points_for_win = player_card.points + computer_card.points
    if game._round == 'p':
        winning_card = cards_battle(player_card, computer_card, game)
        if winning_card == player_card:
            game._player.add_points(points_for_win)
            next_round = 'p'
        else:
            game._computer.add_points(points_for_win)
            next_round = 'c'
    else:
        winning_card = cards_battle(computer_card, player_card, game)
        if winning_card == computer_card:
            game._computer.add_points(points_for_win)
            next_round = 'c'
        else:
            game._player.add_points(points_for_win)
            next_round = 'p'
    return next_round


def check_declaration(p_card, game, player):
    is_trump_card = (p_card.suit in player._trumps)
    if is_trump_card and p_card.name in ['Queen', 'King']:
        print(f"Newly declared trump: {p_card.suit}")
        game.set_trump(p_card.suit)
        player.trump_played(p_card.suit)
        player.add_points(game.trump_value(p_card.suit))


def check_played_card(p_card, c_card, game):
    base_suit = c_card.suit
    if p_card.suit == base_suit or p_card.suit == game.active_trump:
        return False
    else:
        if (game._player.suit_in_hand(c_card.suit) or
           game._player.suit_in_hand(game.active_trump)):
            print("Wrong card. Try card with simmilar suit or with trump")
            return True
        else:
            return False


def play_round(game):
    if game._round == 'p':
        print(game._player.cards_display())
        print(f'Choose a card to play(1-{game._player.cards_in_hand}): ')
        card_number = choose_card_input(game)
        played_p_card = game._player.play_card(card_number)
        print(f'You played: {played_p_card}.')
        check_declaration(played_p_card, game, game._player)
        played_c_card = game._computer.make_move(game, played_p_card)
        print(f'Opponent played: {played_c_card}.')
        next_round = battle(played_p_card, played_c_card, game)
        if next_round == 'p':
            print('You won!')
        else:
            print('Opponent won')
    else:
        played_c_card = game._computer.make_move(game)
        print(f'Opponent played: {played_c_card}.')
        check_declaration(played_c_card, game, game._computer)
        print(game._player.cards_display())
        print(f'Choose a card to play(1-{game._player.cards_in_hand}): ')
        invalid_card = True
        while invalid_card:
            card_number = choose_card_input(game)
            card = game._player._hand[card_number]
            invalid_card = check_played_card(card, played_c_card, game)
        played_p_card = game._player.play_card(card_number)
        print(f'You played: {played_p_card}.')
        next_round = battle(played_p_card, played_c_card, game)
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
        game._player.set_trumps()
        game._computer.set_trumps()
    else:
        musik = game._musiki[chosen_musik]
        print(f"Opponent chose {chosen_musik+1} Musik: {musik}")
        game._computer.add_from_musik(musik)
        card_1, card_2 = game._computer.remove_after_musik()
        game._player.set_trumps()
        game._computer.set_trumps()


def count_final_points(points, bid):
    if points < bid:
        final_points = 0 - points
    elif bid == 0:
        final_points = points
    else:
        final_points = bid
    return (round(final_points/10)*10)


def summary(game):
    p_points = game._player._points
    c_points = game._computer._points
    p_bid = game._player.bid
    c_bid = game._computer.bid
    print(f"You've got {p_points} points,"
          f' Opponent has got {c_points} points')
    if p_bid > 0:
        print(f'You bidded {p_bid}')
    else:
        print("You passed")
    if c_bid > 0:
        print(f'Opponent bidded {c_bid}')
    else:
        print("Opponent passed")
    final_p_points = count_final_points(p_points, p_bid)
    final_c_points = count_final_points(c_points, c_bid)
    print('Final points are going to be rounded')
    print('Final results after considering bids:')
    print(f'You: {final_p_points}, Opponent: {final_c_points}')
    if final_p_points < final_c_points:
        print("You lost")
    elif final_c_points == final_p_points:
        print("It's match")
    else:
        print("Congratulations, You won!")


def main():
    deck = Deck()
    player = Player()
    computer = Computer()
    musiki = (Musik(), Musik())
    deck.generate_deck()
    deck.shuffle_deck()
    game = Game(deck, player, computer, musiki)
    print('Welcome to the game "1000", cards are being dealt.')
    print('At any moment you can type exit to exit the game.')
    game.deal_the_cards()
    print(game._player.cards_display())
    chosen_musik = bidding(game)
    starting_player_clear_musik(chosen_musik, game)
    for i in range(10):
        play_round(game)
    summary(game)


if __name__ == "__main__":
    main()
