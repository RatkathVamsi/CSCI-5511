import random
import math

players = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M']

def initialize():
    league = []
   
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

def scorecalculate(league):
    unique_game = []
    score = -1500

    for i in range(0, len(league), 2):
        for j in range(0, 3):
            game = sorted(league[i + 1][j])
            if game not in unique_game:
                unique_game.append(game)

    score+= 1000*(len(unique_game))
    
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
    return player_matchups

def check_validity(player_matchups):
    for row in player_matchups:
        for count in row:
            if count==0:
                return False
    return True

class GenerateNeighbors:
    def __init__(self, current_state):
        self.current_state = current_state

    def get_neighbors(self):
        neighbors = []
        valid_neighbors = []

        for bye, games in enumerate(self.current_state):
            for i in range(len(games)):
                for j in range(i + 1, len(games)):
                    neighbor = self.swap(games, i, j, bye)
                    if neighbor:
                        neighbors.append(neighbor)

        for neighbor in neighbors:
            pairs = calculate_player_counts(neighbor)
            if check_validity(pairs):
                valid_neighbors.append(GenerateNeighbors(neighbor))

        return valid_neighbors

    def swap(self, games, i, j, bye):
        game1, game2 = games[i].copy(), games[j].copy()
        for a in range(len(game1)):
            for b in range(len(game2)):
                newgame_1, newgame_2 = game1.copy(), game2.copy()
                newgame_1[a], newgame_2[b] = newgame_2[b], newgame_1[a]

                newgames = games.copy()
                newgames[i], newgames[j] = newgame_1, newgame_2

                neighbor = self.current_state.copy()
                neighbor[bye] = newgames
                if check_validity(neighbor):
                    return neighbor
        return None


def generate(league):
    neighbors = []

    league_obj = GenerateNeighbors(league)

    valid_neighbors = league_obj.get_neighbors()

    for valid_neighbor in valid_neighbors:
        neighbors.append(valid_neighbor.current_state)
    
    return neighbors


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

        if new_score > current_score:
            current_score = new_score
            current = neighbor

    if best_score > scorecalculate(league):
        return hillclimbing(best_solution)
    
    return current

def temp_sched(t):
    y=math.exp(-t) 
    return y


def simannealing(league):
    current=league
    current_score=scorecalculate(league)

    for t in range(0,2000):
        temperature=temp_sched(t)

        if temperature==0:
            return current

        next=generate(current)
        for neighbor in next:
            temp_score=scorecalculate(neighbor)
            de=temp_score-current_score

            if de>0:
                current=neighbor
                current_score=scorecalculate(current)

            else:
                prob=math.exp(de/temperature)
                if random.random()<prob:
                    current=neighbor
                    current_score=scorecalculate(current)
    
    return current


if __name__ == "__main__":

    league = initialize()
    player_counts = calculate_player_counts(league)

    print("For Hill Climbing:")
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
  
    league2=initialize()
    simulated_annealing = simannealing(league2)
    print("For Simulated Annealing:")
    for i in range(0,len(simulated_annealing),2):
        if i+1<len(simulated_annealing):
            print(f"Bye player {simulated_annealing[i]}: {simulated_annealing[i+1]}")

    print("** Replay Summary **")
    for player1_index, player1 in enumerate(players):
        print(player1 + ":", end=" ")
        for player2_index, player2 in enumerate(players):
            if player1 != player2:
                matchup_count = player_matchups[player1_index][player2_index]
                print(f"{player2}:{matchup_count},", end=" ")
        print()

"""Sample Output:

    For Hill Climbing:
Bye player A,[['H', 'K', 'C', 'E'], ['J', 'G', 'F', 'L'], ['M', 'I', 'D', 'B']]
Bye player B,[['D', 'C', 'M', 'A'], ['E', 'L', 'J', 'I'], ['G', 'H', 'F', 'K']]
Bye player C,[['F', 'L', 'J', 'H'], ['B', 'M', 'I', 'G'], ['E', 'K', 'A', 'D']]
Bye player D,[['J', 'M', 'L', 'E'], ['I', 'K', 'F', 'A'], ['H', 'C', 'G', 'B']]
Bye player E,[['K', 'G', 'L', 'B'], ['A', 'I', 'M', 'H'], ['J', 'D', 'F', 'C']]
Bye player F,[['M', 'A', 'K', 'G'], ['J', 'D', 'E', 'H'], ['B', 'C', 'L', 'I']]
Bye player G,[['I', 'J', 'C', 'B'], ['F', 'A', 'D', 'H'], ['L', 'M', 'K', 'E']]
Bye player H,[['F', 'E', 'M', 'G'], ['A', 'L', 'D', 'B'], ['I', 'C', 'K', 'J']]
Bye player I,[['K', 'M', 'F', 'D'], ['B', 'H', 'J', 'E'], ['L', 'C', 'G', 'A']]
Bye player J,[['E', 'I', 'G', 'F'], ['C', 'K', 'D', 'B'], ['H', 'M', 'A', 'L']]
Bye player K,[['C', 'F', 'L', 'H'], ['D', 'A', 'M', 'I'], ['G', 'J', 'E', 'B']]
Bye player L,[['E', 'H', 'K', 'A'], ['M', 'B', 'F', 'C'], ['I', 'D', 'G', 'J']]
Bye player M,[['A', 'L', 'C', 'J'], ['E', 'H', 'D', 'G'], ['F', 'I', 'K', 'B']]
** Replay Summary **
A: B:1, C:3, D:5, E:2, F:2, G:2, H:4, I:3, J:1, K:4, L:4, M:5, 
B: A:1, C:5, D:3, E:2, F:2, G:4, H:2, I:5, J:3, K:3, L:3, M:3, 
C: A:3, B:5, D:3, E:1, F:3, G:2, H:3, I:3, J:4, K:3, L:4, M:2,
D: A:5, B:3, C:3, E:3, F:3, G:2, H:3, I:3, J:3, K:3, L:1, M:4,
E: A:2, B:2, C:1, D:3, F:2, G:4, H:5, I:2, J:5, K:4, L:3, M:3,
F: A:2, B:2, C:3, D:3, E:2, G:4, H:4, I:3, J:3, K:4, L:3, M:3,
G: A:2, B:4, C:2, D:2, E:4, F:4, H:3, I:3, J:3, K:3, L:3, M:3,
H: A:4, B:2, C:3, D:3, E:5, F:4, G:3, I:1, J:3, K:3, L:3, M:2,
I: A:3, B:5, C:3, D:3, E:2, F:3, G:3, H:1, J:4, K:3, L:2, M:4,
J: A:1, B:3, C:4, D:3, E:5, F:3, G:3, H:3, I:4, K:1, L:5, M:1,
K: A:4, B:3, C:3, D:3, E:4, F:4, G:3, H:3, I:3, J:1, L:2, M:3,
L: A:4, B:3, C:4, D:1, E:3, F:3, G:3, H:3, I:2, J:5, K:2, M:3,
M: A:5, B:3, C:2, D:4, E:3, F:3, G:3, H:2, I:4, J:1, K:3, L:3,
For Simulated Annealing:
Bye player A: [['J', 'C', 'L', 'K'], ['G', 'H', 'F', 'I'], ['B', 'D', 'M', 'E']]
Bye player B: [['J', 'C', 'A', 'H'], ['I', 'M', 'G', 'E'], ['F', 'D', 'K', 'L']]
Bye player C: [['F', 'L', 'G', 'M'], ['D', 'A', 'J', 'E'], ['K', 'B', 'I', 'H']]
Bye player D: [['K', 'H', 'F', 'J'], ['G', 'E', 'B', 'L'], ['I', 'M', 'C', 'A']]
Bye player E: [['I', 'A', 'J', 'C'], ['H', 'F', 'D', 'L'], ['K', 'B', 'G', 'M']]
Bye player F: [['D', 'A', 'H', 'M'], ['B', 'K', 'G', 'E'], ['I', 'C', 'L', 'J']]
Bye player G: [['C', 'E', 'J', 'F'], ['B', 'H', 'A', 'L'], ['M', 'D', 'K', 'I']]
Bye player H: [['E', 'C', 'L', 'I'], ['D', 'J', 'M', 'G'], ['K', 'B', 'A', 'F']]
Bye player I: [['H', 'D', 'E', 'J'], ['G', 'K', 'M', 'C'], ['A', 'B', 'L', 'F']]
Bye player J: [['D', 'K', 'I', 'L'], ['F', 'M', 'B', 'H'], ['G', 'C', 'A', 'E']]
Bye player K: [['H', 'I', 'M', 'A'], ['G', 'E', 'J', 'F'], ['C', 'B', 'D', 'L']]
Bye player L: [['E', 'C', 'M', 'A'], ['K', 'G', 'H', 'J'], ['F', 'D', 'I', 'B']]
Bye player M: [['G', 'J', 'B', 'I'], ['H', 'A', 'F', 'L'], ['C', 'D', 'E', 'K']]
** Replay Summary **
A: B:3, C:6, D:2, E:3, F:3, G:1, H:4, I:3, J:3, K:1, L:3, M:4,
B: A:3, C:1, D:3, E:3, F:4, G:4, H:3, I:3, J:1, K:4, L:4, M:3,
C: A:6, B:1, D:1, E:4, F:2, G:2, H:1, I:4, J:5, K:2, L:5, M:3,
D: A:2, B:3, C:1, E:4, F:3, G:1, H:4, I:3, J:3, K:4, L:4, M:4,
E: A:3, B:3, C:4, D:4, F:2, G:5, H:2, I:2, J:4, K:2, L:2, M:3,
F: A:3, B:4, C:2, D:3, E:2, G:3, H:4, I:2, J:3, K:3, L:5, M:2,
G: A:1, B:4, C:2, D:1, E:5, F:3, H:2, I:3, J:4, K:4, L:2, M:5,
H: A:4, B:3, C:1, D:4, E:2, F:4, G:2, I:3, J:4, K:4, L:2, M:3,
I: A:3, B:3, C:4, D:3, E:2, F:2, G:3, H:3, J:3, K:3, L:3, M:4,
J: A:3, B:1, C:5, D:3, E:4, F:3, G:4, H:4, I:3, K:3, L:2, M:1,
K: A:1, B:4, C:2, D:4, E:2, F:3, G:4, H:4, I:3, J:3, L:3, M:3,
L: A:3, B:4, C:5, D:4, E:2, F:5, G:2, H:2, I:3, J:2, K:3, M:1,
M: A:4, B:3, C:3, D:4, E:3, F:2, G:5, H:3, I:4, J:1, K:3, L:1,
"""