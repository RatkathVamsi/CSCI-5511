import itertools
import random

def initialize():
    players= ['A','B','C','D','E','F','G','H','I','J','K','L','M']

#league generation
    league=[]
    
    for i in range(0,13):
        byeplayer=players[i]
        weekplayers=[]
        for item in players:
            if item!=byeplayer:
                weekplayers.append(item)
    
        random.shuffle(weekplayers)

        groupsize=4
        temp=[weekplayers[i:i+groupsize] for i in range(0,len(weekplayers),groupsize)]
        league.append(byeplayer)
        league.append(temp)
    return league

def scorecalculate(league): #
    t=league
    uniquegame=set()
    score=0
    #condition3(no repetetion of games if possible)
    for i in range(0,len(t),2):
        for j in range(0,3):
            uniquegame.add(frozenset(t[i+1][j]))

    if len(uniquegame)!=39:
        score=score-100
    return score

def calculate_player_counts(league):
    player_counts = {player: 0 for player in players}

    for i in range(0, len(league), 2):
        bye_player = league[i]
        for game in league[i + 1]:
            for player in game:
                player_counts[player] += 1

    return player_counts

# Initialize the league
league = initialize()

# Calculate the player counts
player_counts = calculate_player_counts(league)

# Print the player counts
for player, count in player_counts.items():
    print(f"{player} has played against {count} other players.")


def generate(league): #swaps to get neighbors
    t=league
    

    return t

def hillclimbing(league,max,restartnum): #randomrestart should check if its implemented right
    bestsoln=None
    bestscore=0

    for _ in range(restartnum):
        current=league
        currentscore=scorecalculate(current)
        limit=0
        while current is True & limit<max:
            neighbor=generate(current)
            newscore=scorecalculate(neighbor)

            if newscore>currentscore:
                currentscore=newscore
                current=neighbor
                limit+=1
    
        if currentscore>bestscore:
            bestsoln=current
            bestscore=currentscore
        
       # else

    
    return bestscore, bestsoln


def simannealing(league):
    





"""if __name__ =="__main__":
    after intialize function to print the league
        for i in range(0,len(league),2):
        if i+1<len(league):
            print(league[i],league[i+1])"""

"""
# Generate a neighboring solution by swapping games
def generate(league):
    # Create a list to store all possible neighboring schedules
    neighbors = []
    for i in range(0, len(league), 2):
        games = league[i + 1]

        # Randomly choose two different games
        game_indices = random.sample(range(3), 2)
        game1_index, game2_index = game_indices

        # Randomly choose two players, one from each game
        game1 = games[game1_index]
        game2 = games[game2_index]

        player1 = random.choice(game1)
        player2 = random.choice(game2)

        # Create a copy of the current league to make modifications
        new_league = league.copy()

        # Swap the two players
        game1[game1.index(player1)] = player2
        game2[game2.index(player2)] = player1

        # Update the league schedule with the modified games
        new_league[i + 1][game1_index] = game1
        new_league[i + 1][game2_index] = game2
        week_indices = random.sample(range(13), 2)
    week1, week2 = schedule[week_indices[0]], schedule[week_indices[1]]
    
    group_indices = random.sample(range(3), 2)
    group1, group2 = week1[group_indices[0]], week2[group_indices[1]]
    
    player_indices = random.sample(range(4), 2)
    player1, player2 = group1[player_indices[0]], group2[player_indices[1]]
    
    # Swap the players
    group1[player_indices[0]], group2[player_indices[1]] = player2, player1
    return schedule
        # Append the modified league to the list of neighbors
        neighbors.append(new_league)

    return neighbors

"""
"""
def generate(league):
    # Create a list to store all possible neighboring schedules
    neighbors = []
    
    for i in range(0, len(league), 2):
        games = league[i + 1]

        # Randomly choose two different weeks
        week_indices = random.sample(range(len(games)), 2)
        week1, week2 = games[week_indices[0]], games[week_indices[1]]

        # Randomly choose two different groups within the chosen weeks
        group_indices = random.sample(range(3), 2)
        group1, group2 = week1[group_indices[0]], week2[group_indices[1]]

        # Randomly choose two players from the selected groups
        player_indices = random.sample(range(4), 2)
        player1_index, player2_index = player_indices

        player1 = group1[player1_index]
        player2 = group2[player2_index]

        # Create a copy of the current league to make modifications
        new_league = league.copy()

        # Swap the two players
        group1[player1_index] = player2
        group2[player2_index] = player1

        # Update the league schedule with the modified games
        week1[group_indices[0]] = group1
        week2[group_indices[1]] = group2

        # Append the modified league to the list of neighbors
        neighbors.append(new_league)

    return neighbors
"""
"""def generate(league):
    # Create a list to store all possible neighboring schedules
    neighbors = []

    # Get all possible combinations of weeks and games
    week_combinations = list(combinations(range(13), 2))
    game_combinations = list(combinations(range(3), 2))

    # Iterate through each combination of weeks
    for week1_index, week2_index in week_combinations:
        week1, week2 = league[week1_index * 2 + 1], league[week2_index * 2 + 1]

        # Iterate through each combination of games
        for game1_index, game2_index in game_combinations:
            group1, group2 = week1[game1_index], week2[game2_index]

            # Iterate through each combination of players
            for player1_index, player2_index in combinations(range(4), 2):
                player1, player2 = group1[player1_index], group2[player2_index]

                # Create a copy of the current league to make modifications
                new_league = league.copy()
                new_week1 = week1.copy()
                new_week2 = week2.copy()
                new_group1 = group1.copy()
                new_group2 = group2.copy()

                # Swap the players
                new_group1[player1_index], new_group2[player2_index] = player2, player1
                new_week1[game1_index] = new_group1
                new_week2[game2_index] = new_group2
                new_league[week1_index * 2 + 1] = new_week1
                new_league[week2_index * 2 + 1] = new_week2

                # Append the modified league to the list of neighbors
                neighbors.append(new_league)

    return neighbors
"""


"""
def hillclimbing(league, max_iterations, restart_num):
    best_solution = league
    best_score = scorecalculate(league)

    for _ in range(restart_num):
        current = league
        current_score = scorecalculate(current)
        limit = 0

        while limit < max_iterations:
            neighbors = generate(current)
            #print(neighbors[1],neighbors[38])
            for neighbor in neighbors:
                new_score = scorecalculate(neighbor)
                #print(new_score)
                if new_score > current_score:
                    current_score = new_score
                    current = neighbor
                    break
                    #limit =0

            if current_score > best_score:
                best_solution = current
                best_score = current_score
            
            current=initialize()
            limit+=1
            #print(best_score,current_score)
    """"""while best_solution:
        for i in range(0,len(best_solution),2):
            if i+1<len(best_solution):
                print(best_solution[i],best_solution[i+1])
                
    return best_score, best_solution
"""

"""def generate(league):
    # Create a list to store all possible neighboring schedules
    neighbors = []

    # Iterate through the league schedule
    for i in range(0, len(league), 2):
        bye_player = league[i]
        games = league[i + 1]

        # Iterate through each game in the current week
        for game_index, game in enumerate(games):
            # Create a copy of the current league to make modifications
            new_league = league.copy()
            new_games = [game.copy() for game in games]

            # Randomly choose two players, one from the current game and one from another game
            player1 = random.choice(game)
            game2_index = (game_index + 1) % 3  # Choose a different game
            player2 = random.choice(games[game2_index])

            # Swap the players
            new_games[game_index][game.index(player1)] = player2
            new_games[game2_index][games[game2_index].index(player2)] = player1

            # Update the league schedule with the modified games
            new_league[i + 1] = new_games

            # Append the modified league to the list of neighbors
            neighbors.append(new_league)

    return neighbors
"""
"""
class ScheduleState:
    def _init_(self, current_state):
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
                            updated_game1 = game1.copy()
                            updated_game2 = game2.copy()
                            updated_game1[k], updated_game2[l] = updated_game2[l], updated_game1[k]
                            updated_games = games.copy()
                            updated_games[i] = updated_game1
                            updated_games[j] = updated_game2
                            neighbor = self.current_state.copy()
                            neighbor[bye] = updated_games
                            neighbors.append(neighbor)

        for neighbor in neighbors:
            player_pairs = evaluate_schedule(neighbor)
            if validate_cond_1(player_pairs):
                valid_neighbors.append(ScheduleState(neighbor))

        return valid_neighbors

"""

class GenerateNeighbors:
    def __init__(self, current_state):
        self.current_state = current_state

    def get_neighbors(self):
        neighbors = []
        valid_neighbors = []

        for bye, games in enumerate(self.current_state):
            for i in range(len(games)):
                for j in range(i + 1, len(games)):
                    neighbor = self.swap_players(games, i, j, bye)
                    if neighbor:
                        neighbors.append(neighbor)

        for neighbor in neighbors:
            pairs = calculate_player_counts(neighbor)
            if check_validity(pairs):
                valid_neighbors.append(GenerateNeighbors(neighbor))

        return valid_neighbors

    def swap_players(self, games, i, j, bye):
        game1, game2 = games[i].copy(), games[j].copy()
        for k in range(len(game1)):
            for l in range(len(game2)):
                newgame_1, newgame_2 = game1.copy(), game2.copy()
                newgame_1[k], newgame_2[l] = newgame_2[l], newgame_1[k]
                newgames = games.copy()
                newgames[i], newgames[j] = newgame_1, newgame_2
                neighbor = self.current_state.copy()
                neighbor[bye] = newgames
                if is_valid_neighbor(neighbor):
                    return neighbor
        return None