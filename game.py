from classes import Deck, Player, Musik, Computer, Game
from sys import exit
import os
from time import sleep
from rich.console import Console
from rich.markdown import Markdown
from rich.progress import track
from rich.text import Text
from rich.table import Table


def clear():
    os.system('clear')
    markdown = Markdown("""# Welcome to the game "1000"!""")
    Console().print(markdown)


def clear_in_game(game):
    clear()
    suits = game.suits_dict()
    if game.active_trump:
        trump = game.active_trump
        disp = Text(f"Active trump: {trump}{suits[trump][0]}",
                    style=suits[trump][1]+" bold underline")
        disp.align('center', os.get_terminal_size()[0])
        Console().print(disp)
        Console().print("\n")


def is_exit(inputted_data):
    if inputted_data.lower() == 'exit':
        os.system('clear')
        exit()


def input_cards_to_discard(game):
    bad_input = True
    while bad_input:
        try:
            Console().print(cards_with_emoji(game.player))
            Console().print("")
            info = "Choose two cards to discard (number, number)(1-12):"
            Console().print(info, style="magenta b")
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
            Console().print('I do not know what you mean.'
                            'Try again with "number, number".', style="b red")
            sleep(2)
            clear()
    return cards_numbers


def choose_card_input(game):
    bad_input = True
    while bad_input:
        try:
            Console().print("")
            Console().print(cards_with_emoji(game.player))
            Console().print("")
            info = f'Choose a card to play(1-{game.player.cards_in_hand}): '
            Console().print(info, style="magenta b")
            cards_amount = game._player.cards_in_hand
            chosen_card = input(">")
            is_exit(chosen_card)
            chosen_card = int(chosen_card)
            if chosen_card in range(1, cards_amount+1):
                bad_input = False
            else:
                raise Exception
        except Exception:
            Console().print("There is no card with this number. Try again.",
                            style="b red")
            sleep(2)
            clear_in_game(game)
    return chosen_card - 1


def choose_card_for_card_input(game, played_c_card, cplayed):
    clear_in_game(game)
    invalid_card = True
    bad_input = True
    while bad_input or invalid_card:
        try:
            Console().print("")
            Console().print(cplayed)
            Console().print("")
            Console().print(cards_with_emoji(game.player))
            info = f'Choose a card to play(1-{game.player.cards_in_hand}): '
            Console().print(info, style="magenta b")
            cards_amount = game._player.cards_in_hand
            card_number = input(">")
            is_exit(card_number)
            card_number = int(card_number)
            if card_number in range(1, cards_amount+1):
                bad_input = False
            else:
                bad_input = True
                raise Exception
            card_number -= 1
            card = game.player.hand[card_number]
            invalid_card = game.check_played_card(card, played_c_card)
            if invalid_card:
                info = "Wrong card. Try card with simmilar suit or with trump"
                Console().print(info, style="b red")
                sleep(2)
                clear_in_game(game)
        except Exception:
            Console().print("There is no card with this number. Try again.",
                            style="b red")
            sleep(2)
            clear_in_game(game)
    return card_number


def next_round_text(next_round, game):
    sleep(1)
    if next_round == 'p':
        Console().print('You won!', style="b bright_green underline")
    else:
        Console().print('Opponent won', style="b red underline")
    sleep(2.5)
    clear_in_game(game)


def input_musik():
    bad_input = True
    while bad_input:
        try:
            Console().print('Choose a musik to get(1,2): ', style="magenta b")
            chosen_musik = str(input(">").strip())
            is_exit(chosen_musik)
            chosen_musik = int(chosen_musik) - 1
            if chosen_musik in [0, 1]:
                bad_input = False
            else:
                raise Exception
        except Exception:
            Console().print("There is no musik with this number. Try again.",
                            style="b red")
            sleep(2)
            clear()
    return chosen_musik


def card_colored(card):
    suits = Game(0, 0, 0, 0).suits_dict()
    card_c = Text(f'{card.name}{suits[card.suit][0]}',
                  style=suits[card.suit][1])
    return card_c


def cards_with_emoji(player):
    list_of_cards = player.hand
    number = 1
    joined = Text()
    joined.append("Your cards: ", style="blue bold")
    for card in list_of_cards:
        joined.append(f"{number}.", style="white")
        joined.append(card_colored(card))
        if number != len(list_of_cards):
            joined.append(", ", style="white")
        else:
            joined.append(".", style="white")
        number += 1
    return joined


def waiting_for_opponent():
    Console().print("Waiting for opponent", end="", style="b white")
    sleep(0.5)
    for i in range(3):
        Console().print(".", end="")
        sleep(0.5)
    Console().print(".")
    sleep(0.5)


def text_c_played(played_c_card):
    cplayed = Text()
    cplayed.append('Opponent played: ', style="blue b")
    cplayed.append(card_colored(played_c_card))
    cplayed.append('.', style="white")
    return cplayed


def text_p_played(played_p_card):
    played = Text()
    played.append('You played: ', style="blue b")
    played.append(card_colored(played_p_card))
    played.append('.', style="white")
    return played


def bidding(game):
    list_of_bids = [str(element) for element in list(range(100, 361))]
    list_of_bids = list_of_bids[::10]
    list_of_bids.append("pass")
    player = game.player
    computer = game.computer
    not_passed = True
    computer_bid = 0
    while not_passed:
        clear()
        Console().print(cards_with_emoji(game.player))
        if computer_bid != 0:
            bid = Text(f"Opponent bidded: {computer_bid}", style="chartreuse3")
            bid.align('right', os.get_terminal_size()[0])
            Console().print(bid)
        else:
            Console().print("")
        quest = Text("How much are you bidding?:",
                     style="bold underline wheat1")
        Console().print(quest)
        player_bid = input(">")
        is_exit(player_bid)
        if str(player_bid).lower() == "pass":
            Console().print("You passed", style="b orange_red1")
            sleep(1)
            clear()
            player.set_bid(0)
            game.set_round('c')
            not_passed = False
            chosen_musik = computer.choose_musik()
            continue
        elif (player_bid not in list_of_bids or
              computer.bid >= int(player_bid)):
            info = ("You must bid points between 100 and 360 tens,"
                    " higher than opponent or pass!")
            Console().print(info, style="b red")
            sleep(3)
            clear()
            continue
        else:
            player.set_bid(int(player_bid))
        computer_bid = computer.make_a_bid(int(player_bid))
        if computer_bid != 0:
            computer.set_bid(computer_bid)
            Console().print(f"Opponent bidded: {computer.bid}",
                            style="chartreuse3")
            sleep(1)
            continue
        else:
            Console().print('Opponent passed', style="b bright_green")
            game.set_round('p')
            computer.set_bid(0)
            not_passed = False
            sleep(1)
            clear()
            chosen_musik = input_musik()
            sleep(1)
            clear()
    return chosen_musik


def play_round(game):
    if game.round == 'p':
        card_number = choose_card_input(game)
        played_p_card = game.player.play_card(card_number)
        sleep(0.5)
        clear_in_game(game)
        Console().print("")
        played = text_p_played(played_p_card)
        Console().print(played)
        new_trump = game.check_declaration(played_p_card, game.player)
        sleep(0.5)
        if new_trump:
            clear_in_game(game)
            Console().print("")
            Console().print(played)
            sleep(0.5)
        waiting_for_opponent()
        clear_in_game(game)
        played_c_card = game.computer.make_move(game, played_p_card)
        Console().print("")
        Console().print(played)
        cplayed = text_c_played(played_c_card)
        Console().print(cplayed)
        next_round = game.battle(played_p_card, played_c_card)
        next_round_text(next_round, game)
    else:
        clear_in_game(game)
        played_c_card = game.computer.make_move(game)
        Console().print("")
        cplayed = text_c_played(played_c_card)
        Console().print(cplayed)
        new_trump = game.check_declaration(played_c_card, game.computer)
        sleep(0.5)
        if new_trump:
            clear_in_game(game)
            Console().print("")
            Console().print(cplayed)
            sleep(0.5)
        sleep(0.5)
        card_number = choose_card_for_card_input(game, played_c_card, cplayed)
        played_p_card = game.player.play_card(card_number)
        clear_in_game(game)
        Console().print("")
        Console().print(cplayed)
        played = text_p_played(played_p_card)
        Console().print(played)
        next_round = game.battle(played_p_card, played_c_card)
        next_round_text(next_round, game)
    game._round = next_round


def starting_player_clear_musik(chosen_musik, game):
    if game.round == 'p':
        game.player.add_from_musik(game.musiki[chosen_musik])
        cards = input_cards_to_discard(game)
        card_1, card_2 = game.player.remove_after_musik(cards)
        cards_discarded = Text()
        cards_discarded.append("You discarded: ", style="blue b")
        cards_discarded.append(card_colored(card_1))
        cards_discarded.append(", ", style="white")
        cards_discarded.append(card_colored(card_2))
        cards_discarded.append(".", style="white")
        Console().print("")
        Console().print(cards_discarded)
        sleep(2)
        clear()
    else:
        musik = game.musiki[chosen_musik]
        numbers = {
            1: "first",
            2: "second"
        }
        cards_colored = (card_colored(musik.cards_in_musik()[0]),
                         card_colored(musik.cards_in_musik()[1]))
        chosen = Text()
        chosen.append(f"Opponent chosen {numbers[chosen_musik+1]} Musik: ",
                      style="b blue")
        chosen.append(cards_colored[0])
        chosen.append(", ", style="white")
        chosen.append(cards_colored[1])
        chosen.append(".", style="white")
        Console().print(chosen)
        game.computer.add_from_musik(musik)
        card_1, card_2 = game.computer.remove_after_musik()
        sleep(2)
        clear()
    game.set_trumps_for_players()


def summary(game):
    clear()
    p_points = game.player.points
    c_points = game.computer.points
    p_bid = game.player.bid if game.player.bid > 0 else "Passed"
    c_bid = game.computer.bid if game.computer.bid > 0 else "Passed"
    table = Table(title="Summary")
    table.add_column("", style="cyan b")
    table.add_column("Player", style="magenta")
    table.add_column("Opponent", style="green")
    table.add_row(f"Bare points{''*10}", str(p_points), str(c_points))
    Console().print(table)
    sleep(1)
    clear()
    table.add_row("Bids", str(p_bid), str(c_bid))
    Console().print(table)
    sleep(1)
    clear()
    final_p_points, final_c_points, result = game.count_final_points()
    table.add_row("Final points(rounded)",
                  str(final_p_points), str(final_c_points))
    Console().print(table)
    sleep(1)
    if result == 'c':
        markdown = Markdown("""# You lost!""", style="red")
    elif result == 'm':
        markdown = Markdown("""# It's a match!""", style="orange_red1")
    elif result == 'p':
        markdown = Markdown("""# You won!""", style="green")
    Console().print(markdown)
    sleep(1)
    Console().print("Type enything to exit:", style="magenta")
    input(">")
    is_exit("exit")


def intro(game):
    clear()
    sleep(1)
    info = Text('At any moment you can type exit to quit the game!',
                style="bold red frame")
    info.align('center', os.get_terminal_size()[0])
    Console().print(info)
    sleep(2)
    clear()
    for i in track(range(25), description="Dealing cards..."):
        sleep(0.1)
    clear()


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
