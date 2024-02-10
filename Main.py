from MultiplayerGame import MultiplayerGame
from Player import Player

if __name__ == "__main__":
    game = MultiplayerGame(100, 50, 95, 90, 10, 1.50)

    # Adding players
    game.add_player(Player("x1", 50))

    # Playing a round
    game.play_round()
    df_players = game.get_player_details()
    print(df_players)

