from classes import Deck, Player, Musik, Computer, Game
from sys import exit
import os
from time import sleep
from colorama import Fore
from colorama import Style


def clear():
    os.system('clear')


def is_exit(inputted_data):
    if inputted_data.lower() == 'exit':
        clear()
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
            sleep(1)
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
            sleep(1)
    return chosen_card - 1


def input_musik():
    bad_input = True
    while bad_input:
        try:
            chosen_musik = str(input(">").strip())
            is_exit(chosen_musik)
            chosen_musik = int(chosen_musik) - 1
            if chosen_musik in [0, 1]:
                bad_input = False
            else:
                raise Exception
        except Exception:
            print("There is no musik with this number. Try again.")
    return chosen_musik


def card_colored(card):
    suits = {
        'Clubs': (' \u2663', Fore.BLACK),
        'Diamonds': (' \u2666', Fore.RED),
        'Hearts': (' \u2665', Fore.RED),
        'Spades': (' \u2660', Fore.BLACK)
    }
    return (f'{suits[card.suit][1]}{card.name} '
            f'{suits[card.suit][0]}{Style.RESET_ALL}')


def cards_with_emoji(player):
    list_of_cards = player.hand
    new_list = []
    suits = {
        'Clubs': (' \u2663', Fore.BLACK),
        'Diamonds': (' \u2666', Fore.RED),
        'Hearts': (' \u2665', Fore.RED),
        'Spades': (' \u2660', Fore.BLACK)
    }
    number = 1
    for card in list_of_cards:
        suit = card.suit
        emoji = suits[suit][0]
        des = f"{number}.{suits[suit][1]}{card.name}{emoji}{Style.RESET_ALL}"
        new_list.append(des)
        number += 1
    joined_cards = ', '.join(new_list) + '.'
    result = f"{Fore.BLUE}Yours cards{Style.RESET_ALL}: " + joined_cards
    return result


def waiting_for_opponent():
    print("Waiting for opponent")
    sleep(0.5)
    print("Waiting for opponent.")
    sleep(0.5)
    print("Waiting for opponent..")
    sleep(0.5)
    print("Waiting for opponent...")
    sleep(0.5)


def bidding(game):
    list_of_bids = [str(element) for element in list(range(100, 361))]
    list_of_bids = list_of_bids[::10]
    list_of_bids.append("pass")
    player = game.player
    computer = game.computer
    not_passed = True
    while not_passed:
        print("How much are you bidding?:")
        player_bid = input(">")
        is_exit(player_bid)
        if str(player_bid).lower() == "pass":
            print("You passed")
            sleep(1)
            player.set_bid(0)
            game.set_round('c')
            not_passed = False
            chosen_musik = computer.choose_musik()
            continue
        elif (player_bid not in list_of_bids or
              computer.bid >= int(player_bid)):
            print("You must bid points between 100 and 360, "
                  "tens, higher than opponent or pass")
            sleep(1)
            continue
        else:
            player.set_bid(int(player_bid))
        computer_bid = computer.make_a_bid(int(player_bid))
        if computer_bid != 0:
            computer.set_bid(computer_bid)
            print(f"Opponent bidded: {computer.bid}")
            sleep(1)
            continue
        else:
            print('Opponent passed')
            game.set_round('p')
            computer.set_bid(0)
            not_passed = False
            sleep(1)
            print('Choose a musik to get(1,2): ')
            chosen_musik = input_musik()
            sleep(1)
    return chosen_musik


def play_round(game):
    if game.round == 'p':
        print(cards_with_emoji(game.player))
        print(f'Choose a card to play(1-{game.player.cards_in_hand}): ')
        card_number = choose_card_input(game)
        played_p_card = game.player.play_card(card_number)
        sleep(0.5)

        print(f'You played: {card_colored(played_p_card)}.')
        new_trump = game.check_declaration(played_p_card, game.player)
        if new_trump:
            print(f"Newly declared trump: {new_trump}")
        sleep(0.5)
        waiting_for_opponent()
        played_c_card = game.computer.make_move(game, played_p_card)
        print(f'Opponent played: {card_colored(played_c_card)}.')
        next_round = game.battle(played_p_card, played_c_card)
        sleep(1)
        if next_round == 'p':
            print('You won!')
        else:
            print('Opponent won')
        sleep(1)

    else:
        played_c_card = game.computer.make_move(game)
        print(f'Opponent played: {card_colored(played_c_card)}.')
        new_trump = game.check_declaration(played_c_card, game.computer)
        if new_trump:
            print(f"Newly declared trump: {new_trump}")
        sleep(1)
        print(cards_with_emoji(game.player))
        print(f'Choose a card to play(1-{game.player.cards_in_hand}): ')
        invalid_card = True
        while invalid_card:
            card_number = choose_card_input(game)
            card = game.player.hand[card_number]
            invalid_card = game.check_played_card(card, played_c_card)
            if invalid_card:
                print("Wrong card. Try card with simmilar suit or with trump")
                sleep(1)
        played_p_card = game.player.play_card(card_number)

        print(f'Opponent played: {card_colored(played_c_card)}.')
        print(f'You played: {card_colored(played_p_card)}.')
        sleep(1)
        next_round = game.battle(played_p_card, played_c_card)
        if next_round == 'p':
            print('You won!')
        else:
            print('Opponent won')
        sleep(1)

    game._round = next_round


def starting_player_clear_musik(chosen_musik, game):
    if game.round == 'p':
        game.player.add_from_musik(game.musiki[chosen_musik])
        print(cards_with_emoji(game.player))
        print("Choose two cards to discard (number, number)(1-12):")
        cards = input_cards_to_discard()
        card_1, card_2 = game.player.remove_after_musik(cards)
        cards_discarded = f"{card_colored(card_1)}, {card_colored(card_2)}"
        print(f"You discarded: {cards_discarded}.")
        sleep(1)

    else:
        musik = game.musiki[chosen_musik]
        cards_colored = (f"{card_colored(musik.cards_in_musik()[0])},"
                         f" {card_colored(musik.cards_in_musik()[1])}")
        print(f"Opponent chose {chosen_musik+1} Musik: {cards_colored}")
        game.computer.add_from_musik(musik)
        card_1, card_2 = game.computer.remove_after_musik()
    game.set_trumps_for_players()


def summary(game):
    p_points = game.player.points
    c_points = game.computer.points
    p_bid = game.player.bid
    c_bid = game.computer.bid
    print(f"You've got {p_points} points,"
          f' Opponent has got {c_points} points')
    sleep(1.5)

    print(f'You bidded {p_bid}' if p_bid > 0 else "You passed")
    sleep(0.5)
    print(f'Opponent bidded {c_bid}' if c_bid > 0 else "Opponent passed")
    final_p_points, final_c_points, result = game.count_final_points()
    sleep(1)

    print('Final points are going to be rounded')
    sleep(1)

    print('Final results after considering bids:')
    sleep(1)
    print(f'You: {final_p_points}, Opponent: {final_c_points}')
    sleep(0.5)
    if result == 'c':
        print("You lost")
    elif result == 'm':
        print("It's match")
    elif result == 'p':
        print("Congratulations, You won!")


def intro(game):

    print('Welcome to the game "1000", cards are being dealt.')
    sleep(1)
    print('At any moment you can type exit to exit the game.')
    sleep(1)

    print(cards_with_emoji(game.player))


def initialize_game():
    deck = Deck()
    player = Player()
    computer = Computer()
    musiki = (Musik(), Musik())
    deck.generate_deck()
    deck.shuffle_deck()
    game = Game(deck, player, computer, musiki)
    return game


def play_game(game):
    game.deal_the_cards()
    intro(game)
    chosen_musik = bidding(game)
    starting_player_clear_musik(chosen_musik, game)
    for i in range(10):
        play_round(game)


# main do innego pliku, funkcje zamienić na metody game: oddzielić
    # całkowicie interfejs od logiki
# przeczyścic po clearowniu musiku przez kompa, zeczy w musiku display
