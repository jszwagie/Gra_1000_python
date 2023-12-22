from game import initialize_game, summary, play_game
from colorama import init as colorama_init


def main():
    colorama_init()
    game = initialize_game()
    play_game(game)
    summary(game)


if __name__ == "__main__":
    main()
