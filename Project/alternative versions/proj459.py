import random
import copy
import math

EMPTY = 0
SIZE = 15
WIN_COUNT = 5
SKIP = "SKIP"

class Connect5PlayerTemplate:
    def __init__(self, mycolor):
        self.color = mycolor

    def get_color(self):
        return self.color

    def make_move(self, state):
        return None

class RandomConnect5Player(Connect5PlayerTemplate):
    def __init__(self, mycolor):
        super().__init__(mycolor)

    def make_move(self, state):
        move = None
        legal = actions(state)
        move = random.choice(legal)
        return move

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
    if len(legal_actions) == 0:
        legal_actions.append(SKIP)
    return legal_actions

def result(state, action):
    if action == SKIP:
        newstate = Connect5State(state.other, state.current, copy.deepcopy(state.board_array))
        return newstate

    if state.board_array[action[0]][action[1]] != EMPTY:
        return None

    color = state.current.get_color()
    newstate = Connect5State(state.other, state.current, copy.deepcopy(state.board_array))
    newstate.board_array[action[0]][action[1]] = color

    return newstate

def terminal_test(state):
    for i in range(SIZE):
        for j in range(SIZE):
            if state.board_array[i][j] == EMPTY:
                if check_win(state, (i, j)):
                    return True
    return False

def check_win(state, move):
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    for d in directions:
        count = 1
        for i in range(1, WIN_COUNT):
            x = move[0] + i * d[0]
            y = move[1] + i * d[1]
            if 0 <= x < SIZE and 0 <= y < SIZE and state.board_array[x][y] == state.current.get_color():
                count += 1
            else:
                break

        for i in range(1, WIN_COUNT):
            x = move[0] - i * d[0]
            y = move[1] - i * d[1]
            if 0 <= x < SIZE and 0 <= y < SIZE and state.board_array[x][y] == state.current.get_color():
                count += 1
            else:
                break

        if count >= WIN_COUNT:
            return True
    return False

class MiniMaxConnect5Player(Connect5PlayerTemplate):
    def __init__(self, mycolor, d):
        super().__init__(mycolor)
        self.depth = d

    def make_move(self, state):
        _, best_move = self.minimax(state, self.depth, -math.inf, math.inf)
        return best_move

    def minimax(self, state, depth, alpha, beta):
        if depth == 0 or terminal_test(state):
            return utility_function(state, self.color), None

        best_value = -math.inf if state.current.get_color() == self.color else math.inf
        best_move = None

        for move in actions(state):
            new_state = result(state, move)
            v, _ = self.minimax(new_state, depth - 1, alpha, beta)

            if state.current.get_color() == self.color:
                if v > best_value:
                    best_value = v
                    best_move = move
                alpha = max(alpha, best_value)
            else:
                if v < best_value:
                    best_value = v
                    best_move = move
                beta = min(beta, best_value)

            if beta <= alpha:
                break

        return best_value, best_move

def utility_function(state, player_color):
    score = 0
    for i in range(SIZE):
        for j in range(SIZE):
            if state.board_array[i][j] != EMPTY:
                # Check for active rows of length 4 and 3 and score them accordingly
                score += score_active_rows(state, (i, j), player_color)
    return score

def score_active_rows(state, move, player_color):
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    row_length_4 = 0
    row_length_3 = 0

    for d in directions:
        count = 1
        for i in range(1, WIN_COUNT):
            x = move[0] + i * d[0]
            y = move[1] + i * d[1]
            if 0 <= x < SIZE and 0 <= y < SIZE and state.board_array[x][y] == player_color:
                count += 1
            else:
                break

        for i in range(1, WIN_COUNT):
            x = move[0] - i * d[0]
            y = move[1] - i * d[1]
            if 0 <= x < SIZE and 0 <= y < SIZE and state.board_array[x][y] == player_color:
                count += 1
            else:
                break

        if count == 4:
            row_length_4 += 1
        elif count == 3:
            row_length_3 += 1

    # Assign scores based on the lengths of active rows
    return row_length_4 * 100 + row_length_3 * 10


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

def display_final(state):
    if check_win(state, (0, 0)):
        print("X wins!")
    elif check_win(state, (0, SIZE - 1)):
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
        s = result(s, action)
        if terminal_test(s):
            print("Game Over")
            display(s)
            display_final(s)
            return
        action = p2.make_move(s)
        print(action)
        if action not in actions(s):
            print("Illegal move made by Player 2")
            return
        s = result(s, action)
        if terminal_test(s):
            print("Game Over")
            display(s)
            display_final(s)
            return

if __name__ == '__main__':
    play_game(p1=MiniMaxConnect5Player(1, 3), p2=RandomConnect5Player(-1))
