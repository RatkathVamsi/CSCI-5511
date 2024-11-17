import random
import math

# Define the list of players
players = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M']

# Initialize the league
def initialize():
    league = []
   
    # Generate the league schedule
    for i in range(0, 13):
        bye_player = players[i]
        week_players = [player for player in players if player != bye_player]
        random.shuffle(week_players)
        group_size = 4
        temp = [week_players[i:i + group_size] for i in range(0, len(week_players), group_size)]
        league.append(bye_player)
        league.append(temp)
    abc=calculate_player_counts(league)
    if check_validity(abc) is not True:   
        return initialize()
    else :
        return league
# Calculate the score of the league schedule
def scorecalculate(league):
    unique_game = set()
    score = -1500

    # Condition 3 (no repetition of games if possible)
    for i in range(0, len(league), 2):
        for j in range(0, 3):
            unique_game.add(frozenset(league[i + 1][j]))

    """if len(unique_game) != 39:
        score = score - 2000"""
    score+= 1000*(len(unique_game))
    
    #condition2
    metric = {
    1: +300,
    2: +500,
    3: +2500,
    4: +1500,
    5: +600,
    6: -40000,
    7: -50000,
    8: -60000,
    9: -80000,
    10: -100000,
    11: -120000,
    }

    player_counts=calculate_player_counts(league)
    for player1_index,player1 in enumerate(players):
        for player2_index,player2 in enumerate(players):
            if player1!=player2:
                count=player_counts[player1_index][player2_index]
                score+=metric.get(count,0)
    #print(score)
    #condition 1(everyone plays atleast once against each other)
    all_players_played=all(0 not in row for row in player_matchups)
    if not all_players_played:
        score=score-499999

    return score

def scorecalculate2(league):
    unique_game = []
    score = -1500

    # Condition 3 (no repetition of games if possible)
    for i in range(0, len(league), 2):
        for j in range(0, 3):
            game = sorted(league[i + 1][j])
            if game not in unique_game:
                unique_game.append(game)

    """if len(unique_game) != 39:
        score = score - 2000"""
    score+= 1000*(len(unique_game))
    
    #condition2
    metric = {
    1: +300,
    2: +500,
    3: +2500,
    4: +1500,
    5: +600,
    6: -40000,
    7: -50000,
    8: -60000,
    9: -80000,
    10: -100000,
    11: -120000,
    }

    player_counts=calculate_player_counts(league)
    for player1_index,player1 in enumerate(players):
        for player2_index,player2 in enumerate(players):
            if player1!=player2:
                count=player_counts[player1_index][player2_index]
                score+=metric.get(count,0)
    #print(score)
    #condition 1(everyone plays atleast once against each other)
    all_players_played=all(0 not in row for row in player_matchups)
    if not all_players_played:
        score=score-499999

    return score 


player_matchups = [[0 for _ in players] for _ in players]
def calculate_player_counts(league):
    for i in range(len(players)):
        for j in range(len(players)):
            player_matchups[i][j]=0

    for i in range(0, len(league), 2):
        bye_player = league[i]
        for game in league[i + 1]:
            for player1 in game:
                for player2 in game:
                    if player1 != player2:
                        player1_index = players.index(player1)
                        player2_index = players.index(player2)
                        player_matchups[player1_index][player2_index] += 1

                    elif player1==player2:
                        player1_index = players.index(player1)
                        player_matchups[player1_index][player1_index]=-1
    #print(player_matchups)
    return player_matchups

def check_validity(player_matchups):
    for row in player_matchups:
        for count in row:
            if count==0:
                return False
    return True
#generating neighbors
class GenerateNeighbors:
    def __init__(self, current_state):
        self.current_state = current_state

    def get_neighbors(self):
        neighbors = []
        valid_neighbors = []

        for bye, games in enumerate(self.current_state):
            for i in range(0, len(games)):
                for j in range(i + 1, len(games)):
                    game1, game2 = games[i].copy(), games[j].copy()
                    for k in range(len(game1)):
                        for l in range(len(game2)):
                            newgame_1,newgame_2 = game1.copy(),game2.copy()
                            newgame_1[k], newgame_2[l] = newgame_2[l], newgame_1[k]
                            newgames = games.copy()
                            newgames[i],newgames[j] = newgame_1,newgame_2
                            neighbor = self.current_state.copy()
                            neighbor[bye] = newgames
                            neighbors.append(neighbor)
        for neighbor in neighbors:
            pairs = calculate_player_counts(neighbor)
            if check_validity(pairs):
                valid_neighbors.append(GenerateNeighbors(neighbor))
        return valid_neighbors

def generate(league):
    neighbors = []

    # Convert the league to a GenerateNeighbors object
    league_obj = GenerateNeighbors(league)

    # Get valid neighboring schedules using the get_neighbors method
    valid_neighbors = league_obj.get_neighbors()

    for valid_neighbor in valid_neighbors:
        neighbors.append(valid_neighbor.current_state)
    
    """if len(valid_neighbors)==0:
        hillclimbing(initialize())"""

    return neighbors


# Hill Climbing Algorithm

def hillclimbing(league):
    current = league
    current_score = scorecalculate(current)
    limit = 0

    neighbors = generate(current)

    best_solution = current
    best_score = current_score

    for neighbor in neighbors:
        new_score = scorecalculate(neighbor)

        if new_score > best_score:
            best_score = new_score
            best_solution = neighbor
            print(best_score)

        if new_score > current_score:
            current_score = new_score
            current = neighbor

    # If a better solution was found, continue hill climbing with the best solution
    if best_score > scorecalculate(league):
        return hillclimbing(best_solution)
    print(best_score)
    return current

def temp_sched(t):
    y=math.exp(-t)

    return y
# Simulated Annealing Algorithm
def simannealing(league):
    current=league
    print(current)
    current_score=scorecalculate2(league)

    for t in range(0,1000):
        temperature=temp_sched(t)

        if temperature==0:
            return current

        next=generate(current)
        for neighbor in next:
            temp_score=scorecalculate2(neighbor)


            """x=random.choice(next)
            temp=scorecalculate(x)"""
            de=temp_score-current_score

            if de>0:
                current=neighbor
                current_score=scorecalculate2(current)

            else:
                prob=math.exp(de/temperature)
                if random.random()<prob:
                    current=neighbor
                    current_score=scorecalculate2(current)
    
    return current


    # Implement your simulated annealing logic here
    # You'll need to define the acceptance probability and temperature schedule
    # Return the best solution and its score

if __name__ == "__main__":
    # Initialize the league
    league = initialize()

    # Calculate player counts
    player_counts = calculate_player_counts(league)

    hc_schedule = hillclimbing(league)
    for i in range(0,len(hc_schedule),2):
        if i+1<len(hc_schedule):
            print(f"Bye player {hc_schedule[i]},{hc_schedule[i+1]}")

    print("** Replay Summary **")
    for player1_index, player1 in enumerate(players):
        print(player1 + ":", end=" ")
        for player2_index, player2 in enumerate(players):
            if player1 != player2:
                matchup_count = player_matchups[player1_index][player2_index]
                print(f"{player2}:{matchup_count},", end=" ")
        print()

 
    # Run Hill Climbing algorithm

    league2=initialize()
    # Run Simulated Annealing algorithm
    simulated_annealing = simannealing(league2)
    print("For Simulated Annealing:")
    for i in range(0,len(simulated_annealing),2):
        if i+1<len(simulated_annealing):
            print(f"Bye player {simulated_annealing[i]}: {simulated_annealing[i+1]}")
    #print("Best Score (Simulated Annealing):", best_score_simulated_annealing)

    print("** Replay Summary **")
    for player1_index, player1 in enumerate(players):
        print(player1 + ":", end=" ")
        for player2_index, player2 in enumerate(players):
            if player1 != player2:
                matchup_count = player_matchups[player1_index][player2_index]
                print(f"{player2}:{matchup_count},", end=" ")
        print()
