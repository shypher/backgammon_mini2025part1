import random
from random import randint
from src.colour import Colour
from src.game import Game
from src.strategies import HumanStrategy

def print_tournament_placement(player_names):
    print("Tournament Placement:")
    random.shuffle(player_names)
    for i in range(0, len(player_names), 2):
        if i + 1 < len(player_names):
            print(f"{player_names[i]} vs {player_names[i + 1]}")
        else:
            print(f"{player_names[i]} gets a bye")

def print_tournament_branch(tournament_branch):
    print("\nTournament Branch:")
    for round_num, matchups in enumerate(tournament_branch, start=1):
        print(f"Round {round_num}:")
        for matchup in matchups:
            print(f"  {matchup}")

def run_tournament(player_names):
    players = {name: HumanStrategy(name) for name in player_names}
    print_tournament_placement(player_names)
    
    time_limit = input("Enter time limit in seconds (or 'inf' for no limit): ")
    if time_limit.lower() == 'inf':
        time_limit = -1
    else:
        time_limit = int(time_limit)
    
    best_of = int(input("Enter the number of games for best of series (must be an odd number): "))
    if best_of % 2 == 0:
        raise ValueError("The number of games must be an odd number.")
    
    game_results = []
    tournament_branch = []
    while len(players) > 1:
        next_round_players = {}
        player_names = list(players.keys())
        random.shuffle(player_names)
        round_matchups = []
        for i in range(0, len(player_names), 2):
            if i + 1 >= len(player_names):
                next_round_players[player_names[i]] = players[player_names[i]]
                continue
            player1 = player_names[i]
            player2 = player_names[i + 1]
            round_matchups.append(f"{player1} vs {player2}")
            print(f"Starting game: {player1} vs {player2}")  
            colour1 = Colour(randint(0, 1))
            colour2 = colour1.other()
            first_player = colour1

            wins = {player1: 0, player2: 0}
            for game_number in range(1, best_of + 1):
                current_first_player = first_player if game_number % 2 != 0 else first_player.other()
                game = Game(
                    white_strategy=players[player1] if colour1 == Colour.WHITE else players[player2],
                    black_strategy=players[player1] if colour1 == Colour.BLACK else players[player2],
                    first_player=current_first_player,
                    time_limit=time_limit
                )
                game.run_game(verbose=False)
                winner = game.who_won()
                winner_name = player1 if winner == colour1 else player2
                wins[winner_name] += 1
                if wins[winner_name] > best_of // 2:
                    break

            series_winner = player1 if wins[player1] > wins[player2] else player2
            next_round_players[series_winner] = players[series_winner]
            game_results.append(f"{player1} vs {player2}: {series_winner} won the series")
            print(f"{series_winner} won the series!")
        tournament_branch.append(round_matchups)
        players = next_round_players
    final_winner = list(players.keys())[0]
    print(f"{final_winner} is the tournament champion!")
    print("\nTournament Results:")
    for result in game_results:
        print(result)
    print_tournament_branch(tournament_branch)

if __name__ == '__main__':
    while True:
        try:
            num_players = int(input("Enter the number of players: "))
            if num_players > 0:
                break
            else:
                print("The number of players must be greater than 0.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")
    
    player_names = [input(f"Name of player {i + 1}: ") for i in range(num_players)]
    run_tournament(player_names)
