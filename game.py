from classes import Deck, Player, Musik, Computer, Game
from sys import exit
import os
from time import sleep
from rich.console import Console
from rich.markdown import Markdown
from rich.progress import track
from rich.text import Text
from rich.table import Table


def _clear():
    """
    Clears terminal and prints the markdown of the game.
    """
    os.system('clear')
    markdown = Markdown("""# Welcome to the game "1000"!""")
    Console().print(markdown)


def _clear_in_game(game):
    """
    Special form of clearing terminal, this one take into account active trump.
    """
    _clear()
    suits = game.suits_dict()
    if game.active_trump:
        trump = game.active_trump
        disp = Text(f"Active trump: {trump}{suits[trump][0]}",
                    style=suits[trump][1]+" bold underline")
        disp.align('center', os.get_terminal_size()[0])
        Console().print(disp)
        Console().print("\n")


def _is_exit(inputted_data):
    """
    Checks if inputted data is exit. If it is - closes the program.
    """
    if inputted_data.lower() == 'exit':
        os.system('clear')
        exit()


def _input_cards_to_discard(game):
    """
    Function responsible for getting valid input
    for cards to discard from players hand.
    """
    bad_input = True
    while bad_input:
        try:
            Console().print(_cards_with_emoji(game.player))
            Console().print("")
            info = "Choose two cards to discard (number, number)(1-12):"
            Console().print(info, style="magenta b")
            cards = input(">")
            _is_exit(cards)
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
            _clear()
    return cards_numbers


def _choose_card_input(game):
    """
    Function responsible for getting valid input for cards to play,
    when player starts a round.
    """
    bad_input = True
    while bad_input:
        try:
            Console().print("")
            Console().print(_cards_with_emoji(game.player))
            Console().print("")
            info = f'Choose a card to play(1-{game.player.cards_in_hand}): '
            Console().print(info, style="magenta b")
            cards_amount = game._player.cards_in_hand
            chosen_card = input(">")
            _is_exit(chosen_card)
            chosen_card = int(chosen_card)
            if chosen_card in range(1, cards_amount+1):
                bad_input = False
            else:
                raise Exception
        except Exception:
            Console().print("There is no card with this number. Try again.",
                            style="b red")
            sleep(2)
            _clear_in_game(game)
    return chosen_card - 1


def _choose_card_for_card_input(game, played_c_card, cplayed):
    """
    Function responsible for getting valid input for cards to play,
    when opponent started a round.
    """
    _clear_in_game(game)
    invalid_card = True
    bad_input = True
    while bad_input or invalid_card:
        try:
            Console().print("")
            Console().print(cplayed)
            Console().print("")
            Console().print(_cards_with_emoji(game.player))
            info = f'Choose a card to play(1-{game.player.cards_in_hand}): '
            Console().print(info, style="magenta b")
            cards_amount = game._player.cards_in_hand
            card_number = input(">")
            _is_exit(card_number)
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
                _clear_in_game(game)
        except Exception:
            Console().print("There is no card with this number. Try again.",
                            style="b red")
            sleep(2)
            _clear_in_game(game)
    return card_number


def _next_round_text(next_round, game):
    """
    Prints who won the round
    """
    sleep(1)
    if next_round == 'p':
        Console().print('You won!', style="b bright_green underline")
    else:
        Console().print('Opponent won', style="b red underline")
    sleep(2.5)
    _clear_in_game(game)


def _input_musik():
    """
    Function responsible for getting valid input for choosing musik.
    """
    bad_input = True
    while bad_input:
        try:
            Console().print('Choose a musik to get(1,2): ', style="magenta b")
            chosen_musik = str(input(">").strip())
            _is_exit(chosen_musik)
            chosen_musik = int(chosen_musik) - 1
            if chosen_musik in [0, 1]:
                bad_input = False
            else:
                raise Exception
        except Exception:
            Console().print("There is no musik with this number. Try again.",
                            style="b red")
            sleep(2)
            _clear()
    return chosen_musik


def suits_dict():
    """
    Function which stores emojis and colors/styles for cards.
    """
    suits = {
        'Clubs': (' \u2663', "black b"),
        'Diamonds': (' \u2666', "red b"),
        'Hearts': (' \u2665', "red b"),
        'Spades': (' \u2660', "black b")
    }
    return suits


def _card_colored(card):
    """
    Function responsible for making graphical representation of a card.
    """
    suits = suits_dict()
    card_c = Text(f'{card.name}{suits[card.suit][0]}',
                  style=suits[card.suit][1])
    return card_c


def _cards_with_emoji(player):
    """
    Function responsible for making graphical representation of cards
    in players's hand.
    """
    list_of_cards = player.hand
    number = 1
    joined = Text()
    joined.append("Your cards: ", style="blue bold")
    for card in list_of_cards:
        joined.append(f"{number}.", style="white")
        joined.append(_card_colored(card))
        if number != len(list_of_cards):
            joined.append(", ", style="white")
        else:
            joined.append(".", style="white")
        number += 1
    return joined


def _waiting_for_opponent():
    """
    Prints waiting for opponent in stylish way.
    """
    Console().print("Waiting for opponent", end="", style="b white")
    sleep(0.5)
    for i in range(2):
        Console().print(".", end="")
        sleep(0.5)
    Console().print(".")
    sleep(0.5)


def _text_c_played(played_c_card):
    """
    Function responsible for printing card played by opponent.
    """
    cplayed = Text()
    cplayed.append('Opponent played: ', style="blue b")
    cplayed.append(_card_colored(played_c_card))
    cplayed.append('.', style="white")
    return cplayed


def _text_p_played(played_p_card):
    """
    Function responsible for printing card played by player.
    """
    played = Text()
    played.append('You played: ', style="blue b")
    played.append(_card_colored(played_p_card))
    played.append('.', style="white")
    return played


def _bidding(game):
    """
    Function responsible for handling the bidding phase of the game.
    """
    list_of_bids = [str(element) for element in list(range(100, 361))]
    list_of_bids = list_of_bids[::10]
    list_of_bids.append("pass")
    player = game.player
    computer = game.computer
    not_passed = True
    computer_bid = 0
    while not_passed:
        _clear()
        Console().print(_cards_with_emoji(game.player))
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
        _is_exit(player_bid)
        if str(player_bid).lower() == "pass":
            Console().print("You passed", style="b orange_red1")
            sleep(1)
            _clear()
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
            _clear()
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
            _clear()
            chosen_musik = _input_musik()
            sleep(1)
            _clear()
    return chosen_musik


def _play_round(game):
    """
    Function responsible for handling the single round of the game.
    """
    if game.round == 'p':
        card_number = _choose_card_input(game)
        played_p_card = game.player.play_card(card_number)
        sleep(0.5)
        _clear_in_game(game)
        Console().print("")
        played = _text_p_played(played_p_card)
        Console().print(played)
        new_trump = game.check_declaration(played_p_card, game.player)
        sleep(0.5)
        if new_trump:
            _clear_in_game(game)
            Console().print("")
            Console().print(played)
            sleep(0.5)
        _waiting_for_opponent()
        _clear_in_game(game)
        played_c_card = game.computer.make_move(game, played_p_card)
        Console().print("")
        Console().print(played)
        cplayed = _text_c_played(played_c_card)
        Console().print(cplayed)
        next_round = game.battle(played_p_card, played_c_card)
        _next_round_text(next_round, game)
    else:
        _clear_in_game(game)
        played_c_card = game.computer.make_move(game)
        Console().print("")
        cplayed = _text_c_played(played_c_card)
        Console().print(cplayed)
        new_trump = game.check_declaration(played_c_card, game.computer)
        sleep(0.5)
        if new_trump:
            _clear_in_game(game)
            Console().print("")
            Console().print(cplayed)
            sleep(0.5)
        sleep(0.5)
        card_number = _choose_card_for_card_input(game, played_c_card, cplayed)
        played_p_card = game.player.play_card(card_number)
        _clear_in_game(game)
        Console().print("")
        Console().print(cplayed)
        played = _text_p_played(played_p_card)
        Console().print(played)
        next_round = game.battle(played_p_card, played_c_card)
        _next_round_text(next_round, game)
    game._round = next_round


def _starting_player_clear_musik(chosen_musik, game):
    """
    Function responsible for handling the phase of cleaning musiks
    after bidding.
    """
    if game.round == 'p':
        game.player.add_from_musik(game.musiki[chosen_musik])
        cards = _input_cards_to_discard(game)
        card_1, card_2 = game.player.remove_after_musik(cards)
        cards_discarded = Text()
        cards_discarded.append("You discarded: ", style="blue b")
        cards_discarded.append(_card_colored(card_1))
        cards_discarded.append(", ", style="white")
        cards_discarded.append(_card_colored(card_2))
        cards_discarded.append(".", style="white")
        Console().print("")
        Console().print(cards_discarded)
        sleep(2)
        _clear()
    else:
        musik = game.musiki[chosen_musik]
        numbers = {
            1: "first",
            2: "second"
        }
        cards_colored = (_card_colored(musik.cards_in_musik()[0]),
                         _card_colored(musik.cards_in_musik()[1]))
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
        _clear()
    game.set_trumps_for_players()


def _intro():
    """
    Prints intro for the game.
    """
    _clear()
    sleep(1)
    info = Text('At any moment you can type exit to quit the game!',
                style="bold red frame")
    info.align('center', os.get_terminal_size()[0])
    Console().print(info)
    sleep(2)
    _clear()
    for i in track(range(25), description="Dealing cards..."):
        sleep(0.1)
    _clear()


def summary(game):
    """
    Prints summary.
    """
    _clear()
    p_points = game.player.points
    c_points = game.computer.points
    p_bid = game.player.bid if game.player.bid > 0 else "Passed"
    c_bid = game.computer.bid if game.computer.bid > 0 else "Passed"
    table = Table(title="Summary")
    table.add_column("", style="cyan b")
    table.add_column("Player", style="magenta")
    table.add_column("Opponent", style="green")
    table.add_row("Bare points", str(p_points), str(c_points))
    Console().print(table)
    sleep(1)
    _clear()
    table.add_row("Bids", str(p_bid), str(c_bid))
    Console().print(table)
    sleep(1)
    _clear()
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
    Console().print("Click enter to quit:", style="magenta")
    input()
    _is_exit("exit")


def initialize_game():
    """
    Function responsible for initializing the game.
    """
    deck = Deck()
    player = Player()
    computer = Computer()
    musiki = (Musik(), Musik())
    deck.generate_deck()
    deck.shuffle_deck()
    game = Game(deck, player, computer, musiki)
    return game


def play_game(game):
    """
    Function responsible for starting the game and watching over the rounds.
    """
    game.deal_the_cards()
    _intro()
    chosen_musik = _bidding(game)
    _starting_player_clear_musik(chosen_musik, game)
    for i in range(10):
        _play_round(game)
