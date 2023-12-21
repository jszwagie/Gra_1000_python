from game import initialize_game, summary, play_game


def main():
    game = initialize_game()
    play_game(game)
    summary(game)


if __name__ == "__main__":
    main()
