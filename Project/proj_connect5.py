#Project
import random
import copy
import math

EMPTY = 0
SIZE = 15
WIN_COUNT = 5

class Connect5PlayerTemplate:
    def __init__(self, mycolor):
        self.color = mycolor

    def get_color(self):
        return self.color

    def make_move(self, state):
        return None
    
    def utility(self,state):
        return None


class RandomConnect5Player(Connect5PlayerTemplate):
    def __init__(self, mycolor):
        super().__init__(mycolor)

    def make_move(self, state):
        move = None
        legal = actions(state)
        move = random.choice(legal)
        return move
    
class MinimaxConnect5Player(Connect5PlayerTemplate):
    def __init__(self,mycolor,depth):
        self.color=mycolor
        self.depth=depth

    def get_color(self):
        return self.color
    
    def make_move(self,state):
        curr_move=None
        curr_move=self.minimax(state,3)

        return curr_move
    
    def minimax(self,state,depth):
        count=0
        for i in range(SIZE):
            for j in range(SIZE):
                if state.board_array[i][j]==EMPTY:
                    count+=1
            
        if count>215:
            move=random.choice(actions(state))
            
        else:

            _, move = self.max_value(state,depth)
        return move
    

           
    def max_value(self,state,depth):
        if terminal_test(state) or depth==0:
            return self.evalmove(state),None
            #return self.evalmove1(state),None
            
        v = float('-inf')
        move = None
        for a in actions(state):
            v2, _ = self.min_value(result(state, a), depth - 1)
            if v2 > v:
                v, move = v2, a
        return v, move
        
    def min_value(self,state, depth):
        if terminal_test(state) or depth == 0:
            return self.evalmove(state), None
        v = float('inf')
        move = None
        for a in actions(state):
            v2, _ = self.max_value(result(state, a), depth - 1)
            if v2 < v:
                v, move = v2, a
        return v, move
    
    def evalmove1(self, state):
        score = 0

        if check_win(state):
        # If the current player wins, return a high utility value
            if state.current.get_color() == 1:
                return 1000

        # If the other player wins, return a low utility value
            if state.other.get_color() == 1:
                return -1000
            
        total_cells = sum(row.count(1) + row.count(-1) for row in state.board_array)
        exploration_threshold = 10  # Adjust the threshold as needed

        if total_cells < exploration_threshold:
        # Prioritize center and corners
            score += self.prioritize_center_and_corners(state)


        else:
            for i in range(0, SIZE):
                for j in range(0, SIZE):
                    for d in [(0, 1), (1, 0), (1, 1), (-1, -1)]:
                        score += self.evaluate_direction(state, i, j, d)

        return score
    
    def prioritize_center_and_corners(self, state):
        center_row, center_col = SIZE // 2, SIZE // 2
        center_score = -abs(center_row - SIZE // 2) - abs(center_col - SIZE // 2)

        corner_scores = [
            (-1, -1), (-1, SIZE - 1), (SIZE - 1, -1), (SIZE - 1, SIZE - 1)
        ]
        corner_score = sum(state.board_array[row][col] for row, col in corner_scores)

        return center_score + corner_score 
    
    def evaluate_direction(self, state, row, col, direction):
        player_color = self.color
        opponent_color = -1 if player_color == 1 else 1
        score = 0

    # Define a helper function to count consecutive stones in a direction
        def count_consecutive(x, y, dx, dy, color):
            count = 0
            while 0 <= x < SIZE and 0 <= y < SIZE and state.board_array[x][y] == color:
                count += 1
                x += dx
                y += dy
            return count

        def is_open(x, y, dx, dy, color):
            x_open = x + dx
            y_open = y + dy
            x_next = x + 5 * dx
            y_next = y + 5 * dy
            return (
                (0 <= x_open < SIZE and 0 <= y_open < SIZE and state.board_array[x_open][y_open] == EMPTY) or
                (0 <= x_next < SIZE and 0 <= y_next < SIZE and state.board_array[x_next][y_next] == EMPTY)
            )

        for k in range(1, 5):
        # Check forward direction
            x_forward = row + k * direction[0]
            y_forward = col + k * direction[1]
            count_forward = count_consecutive(x_forward, y_forward, direction[0], direction[1], player_color)

            # Check backward direction
            x_backward = row - k * direction[0]
            y_backward = col - k * direction[1]
            count_backward = count_consecutive(x_backward, y_backward, -direction[0], -direction[1], player_color)

            # Check for open and semi-open patterns
            open_forward = is_open(row, col, direction[0], direction[1], player_color)
            open_backward = is_open(row, col, -direction[0], -direction[1], player_color)

        # Evaluate patterns
            if count_forward + count_backward >= 4 and (open_forward or open_backward):
             # Live Four or more
                score += 1000
            elif count_forward + count_backward == 3 and (open_forward or open_backward):
            # Live Three
                score += 100
            elif count_forward + count_backward == 2 and (open_forward or open_backward):
            # Live Two
                score += 10
            elif count_forward+count_backward == 1 and (open_forward or open_backward):
                score+=1

        #print(score)
        return score

    def evalmove(self, state):
        # Check for a win
        if check_win(state):
            if state.current.get_color() == 1:
                return 1000
            else:
                return -1000

        # Evaluate based on potential winning patterns
        score = self.evaluate_potential_wins(state)

        return score

    def evaluate_potential_wins(self, state):
        score = 0
        directions = [(0, 1), (1, 0), (1, 1), (-1, -1)]

        for i in range(SIZE):
            for j in range(SIZE):
                for d in directions:
                    score += self.evaluate_directions(state, i, j, d)

        return score

    def evaluate_directions(self, state, row, col, direction):
        player_color = self.color
        opponent_color = -1 if player_color == 1 else 1
        score = 0

        # Define a helper function to count consecutive stones in a direction
        def count_consecutive(x, y, dx, dy, color):
            count = 0
            while 0 <= x < SIZE and 0 <= y < SIZE and state.board_array[x][y] == color:
                count += 1
                x += dx
                y += dy
            return count

        for k in range(1, 5):
            # Check forward direction
            x_forward = row + k * direction[0]
            y_forward = col + k * direction[1]
            count_forward = count_consecutive(x_forward, y_forward, direction[0], direction[1], player_color)

            # Check backward direction
            x_backward = row - k * direction[0]
            y_backward = col - k * direction[1]
            count_backward = count_consecutive(x_backward, y_backward, -direction[0], -direction[1], player_color)

            # Check for open and semi-open patterns
            open_forward = self.is_open(state,row, col, direction[0], direction[1], player_color)
            open_backward = self.is_open(state,row, col, -direction[0], -direction[1], player_color)

            # Evaluate patterns
            if count_forward + count_backward >= 4 and (open_forward or open_backward):
                # Live Four or more
                score += 1000
            elif count_forward + count_backward == 3 and (open_forward or open_backward):
                # Live Three
                score += 100
            elif count_forward + count_backward == 2 and (open_forward or open_backward):
                # Live Two
                score += 10
            elif count_forward + count_backward == 1 and (open_forward or open_backward):
                score += 1
        return score

    def is_open(self,state, x, y, dx, dy, color):
        x_open = x + dx
        y_open = y + dy
        x_next = x + 5 * dx
        y_next = y + 5 * dy
        return (
            (0 <= x_open < SIZE and 0 <= y_open < SIZE and state.board_array[x_open][y_open] == EMPTY) or
            (0 <= x_next < SIZE and 0 <= y_next < SIZE and state.board_array[x_next][y_next] == EMPTY)
        )    


class AlphaBetaConnect5Player(Connect5PlayerTemplate):
    def __init__(self,mycolor,depth):
        self.color=mycolor
        self.depth=depth

    def get_color(self):
        return self.color
    
    def make_move(self,state):
        
        def max_value(state, alpha, beta, depth):
            if terminal_test(state) or depth == 0:
                return self.evalmove(state), None
                #return evalmove1(state),None
            v = float('-inf')
            move = None
            for a in actions(state):
                v2, _ = min_value(result(state, a), alpha, beta, depth - 1)
                if v2 > v:
                    v, move = v2, a
                alpha = max(alpha, v)
                if v >= beta:
                    return v, move
            return v, move

        def min_value(state, alpha, beta, depth):
            if terminal_test(state) or depth == 0:
                return self.evalmove(state), None
                #return evalmove1(state),None
            v = float('inf')
            move = None
            for a in actions(state):
                v2, _ = max_value(result(state, a), alpha, beta, depth - 1)
                if v2 < v:
                    v, move = v2, a
                beta = min(beta, v)
                if v <= alpha:
                    return v, move
            return v, move

        _, move = max_value(state, float('-inf'), float('inf'), self.depth)
        return move
    
    def evalmove1(self, state):
        score = 0

        if check_win(state):
        # If the current player wins, return a high utility value
            if state.current.get_color() == 1:
                return 1000

        # If the other player wins, return a low utility value
            if state.other.get_color() == 1:
                return -1000
            
        total_cells = sum(row.count(1) + row.count(-1) for row in state.board_array)
        exploration_threshold = 10  # Adjust the threshold as needed

        if total_cells < exploration_threshold:
        # Prioritize center and corners
            score += self.prioritize_center_and_corners(state)


        else:
            for i in range(0, SIZE):
                for j in range(0, SIZE):
                    for d in [(0, 1), (1, 0), (1, 1), (-1, -1)]:
                        score += self.evaluate_direction(state, i, j, d)

        return score
    
    def prioritize_center_and_corners(self, state):
        center_row, center_col = SIZE // 2, SIZE // 2
        center_score = -abs(center_row - SIZE // 2) - abs(center_col - SIZE // 2)

        corner_scores = [
            (-1, -1), (-1, SIZE - 1), (SIZE - 1, -1), (SIZE - 1, SIZE - 1)
        ]
        corner_score = sum(state.board_array[row][col] for row, col in corner_scores)

        return center_score + corner_score 
    
    def evaluate_direction(self, state, row, col, direction):
        player_color = self.color
        opponent_color = -1 if player_color == 1 else 1
        score = 0

    # Define a helper function to count consecutive stones in a direction
        def count_consecutive(x, y, dx, dy, color):
            count = 0
            while 0 <= x < SIZE and 0 <= y < SIZE and state.board_array[x][y] == color:
                count += 1
                x += dx
                y += dy
            return count

        def is_open(x, y, dx, dy, color):
            x_open = x + dx
            y_open = y + dy
            x_next = x + 5 * dx
            y_next = y + 5 * dy
            return (
                (0 <= x_open < SIZE and 0 <= y_open < SIZE and state.board_array[x_open][y_open] == EMPTY) or
                (0 <= x_next < SIZE and 0 <= y_next < SIZE and state.board_array[x_next][y_next] == EMPTY)
            )

        for k in range(1, 5):
        # Check forward direction
            x_forward = row + k * direction[0]
            y_forward = col + k * direction[1]
            count_forward = count_consecutive(x_forward, y_forward, direction[0], direction[1], player_color)

            # Check backward direction
            x_backward = row - k * direction[0]
            y_backward = col - k * direction[1]
            count_backward = count_consecutive(x_backward, y_backward, -direction[0], -direction[1], player_color)

            # Check for open and semi-open patterns
            open_forward = is_open(row, col, direction[0], direction[1], player_color)
            open_backward = is_open(row, col, -direction[0], -direction[1], player_color)

        # Evaluate patterns
            if count_forward + count_backward >= 4 and (open_forward or open_backward):
             # Live Four or more
                score += 1000
            elif count_forward + count_backward == 3 and (open_forward or open_backward):
            # Live Three
                score += 100
            elif count_forward + count_backward == 2 and (open_forward or open_backward):
            # Live Two
                score += 10
            elif count_forward+count_backward == 1 and (open_forward or open_backward):
                score+=1

        #print(score)
        return score

    def evalmove(self, state):
        # Check for a win
        if check_win(state):
            if state.current.get_color() == 1:
                return 1000
            else:
                return -1000

        # Evaluate based on potential winning patterns
        score = self.evaluate_potential_wins(state)

        return score

    def evaluate_potential_wins(self, state):
        score = 0
        directions = [(0, 1), (1, 0), (1, 1), (-1, -1)]

        for i in range(SIZE):
            for j in range(SIZE):
                for d in directions:
                    score += self.evaluate_directions(state, i, j, d)

        return score

    def evaluate_directions(self, state, row, col, direction):
        player_color = self.color
        opponent_color = -1 if player_color == 1 else 1
        score = 0

        # Define a helper function to count consecutive stones in a direction
        def count_consecutive(x, y, dx, dy, color):
            count = 0
            while 0 <= x < SIZE and 0 <= y < SIZE and state.board_array[x][y] == color:
                count += 1
                x += dx
                y += dy
            return count

        for k in range(1, 5):
            # Check forward direction
            x_forward = row + k * direction[0]
            y_forward = col + k * direction[1]
            count_forward = count_consecutive(x_forward, y_forward, direction[0], direction[1], player_color)

            # Check backward direction
            x_backward = row - k * direction[0]
            y_backward = col - k * direction[1]
            count_backward = count_consecutive(x_backward, y_backward, -direction[0], -direction[1], player_color)

            # Check for open and semi-open patterns
            open_forward = self.is_open(state,row, col, direction[0], direction[1], player_color)
            open_backward = self.is_open(state,row, col, -direction[0], -direction[1], player_color)

            # Evaluate patterns
            if count_forward + count_backward >= 4 and (open_forward or open_backward):
                # Live Four or more
                score += 1000
            elif count_forward + count_backward == 3 and (open_forward or open_backward):
                # Live Three
                score += 100
            elif count_forward + count_backward == 2 and (open_forward or open_backward):
                # Live Two
                score += 10
            elif count_forward + count_backward == 1 and (open_forward or open_backward):
                score += 1
        return score

    def is_open(self,state, x, y, dx, dy, color):
        x_open = x + dx
        y_open = y + dy
        x_next = x + 5 * dx
        y_next = y + 5 * dy
        return (
            (0 <= x_open < SIZE and 0 <= y_open < SIZE and state.board_array[x_open][y_open] == EMPTY) or
            (0 <= x_next < SIZE and 0 <= y_next < SIZE and state.board_array[x_next][y_next] == EMPTY)
        )      

class Connect5State:
    def __init__(self, currentplayer, otherplayer, board_array=None):
        if board_array is not None:
            self.board_array = board_array
        else:
            self.board_array = [[EMPTY] * SIZE for _ in range(SIZE)]
        self.current = currentplayer
        self.other = otherplayer

def player(state):
    return state.current

def actions(state):
    legal_actions = []
    for i in range(SIZE):
        for j in range(SIZE):
            if state.board_array[i][j] == EMPTY:
                legal_actions.append((i, j))
    return legal_actions

def result(state, action):
    if state.board_array[action[0]][action[1]] != EMPTY:
        return None

    color = state.current.get_color()
    newstate = Connect5State(state.other, state.current, copy.deepcopy(state.board_array))
    newstate.board_array[action[0]][action[1]] = color

    return newstate

def terminal_test(state):
    if check_win(state):
        return True
    
    if not any(EMPTY in row for row in state.board_array):
        return True
    
    return False

def check_win(state):
    for i in range(SIZE):
        for j in range(SIZE):
            if state.board_array[i][j] != EMPTY:
                if check_win_from_position(state, (i, j)):
                    return True
    return False

def check_win_from_position(state, move):
    color = state.board_array[move[0]][move[1]]
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    for d in directions:
        count = 1
        for i in range(1, WIN_COUNT):
            x = move[0] + i * d[0]
            y = move[1] + i * d[1]
            if 0 <= x < SIZE and 0 <= y < SIZE and state.board_array[x][y] == color:
                count += 1
            else:
                break

        for i in range(1, WIN_COUNT):
            x = move[0] - i * d[0]
            y = move[1] - i * d[1]
            if 0 <= x < SIZE and 0 <= y < SIZE and state.board_array[x][y] == color:
                count += 1
            else:
                break

        if count >= WIN_COUNT:
            return True
    return False

def display(state):
    for i in range(SIZE):
        for j in range(SIZE):
            if state.board_array[i][j] == EMPTY:
                print('-', end=' ')
            elif state.board_array[i][j] == 1:
                print('X', end=' ')
            elif state.board_array[i][j] == -1:
                print('O', end=' ')
        print()

def display_final(state,color):
    if check_win(state):
        if color == 1:
            print("X wins!")
        else:
            print("O wins!")
    else:
        print("It's a tie!")

def play_game(p1=None, p2=None):
    if p1 is None:
        p1 = RandomConnect5Player(1)
    if p2 is None:
        p2 = RandomConnect5Player(-1)

    s = Connect5State(p1, p2)

    while True:
        action = p1.make_move(s)
        print(action)
        if action not in actions(s):
            print("Illegal move made by Player 1")
            return
        
        s=result(s,action)
        if terminal_test(s):
            print("Game over")
            display(s)
            display_final(s,1)
            return

        action = p2.make_move(s)
        print(action)
        if action not in actions(s):
            print("Illegal move made by Player 2")
            return
        
        s=result(s,action)
        if terminal_test(s):
            print("Game Over")
            display(s)
            display_final(s,-1)
            return

if __name__ == '__main__':
    play_game()
    #can execute by passing p1=AlphaBetaConnect5Player(1,3)

#the board i took is from (0,0) to (14,14) in (row,column) format