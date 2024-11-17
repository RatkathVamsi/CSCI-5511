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

# def terminal_test(state,last_action,colour):
#     if check_win(state,last_action,colour):
#         return True
    
#     if not any(EMPTY in row for row in state.board_array):
#         return True
    
#     return False

# def check_win(state, move,color):
#     directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
#     for d in directions:
#         count = 1
#         for i in range(1, WIN_COUNT):
#             x = move[0] + i * d[0]
#             y = move[1] + i * d[1]
#             if 0 <= x < SIZE and 0 <= y < SIZE and state.board_array[x][y] == color:
#                 count += 1
#             else:
#                 break

#         for i in range(1, WIN_COUNT):
#             x = move[0] - i * d[0]
#             y = move[1] - i * d[1]
#             if 0 <= x < SIZE and 0 <= y < SIZE and state.board_array[x][y] == state.current.get_color():
#                 count += 1
#             else:
#                 break

#         if count >= WIN_COUNT:
#             return True
#     return False
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
        s = result(s, action)
        if terminal_test(s):
            print("Game over")
            display(s)
            display_final(s,1)
            break
        

        action = p2.make_move(s)
        print(action)
        if action not in actions(s):
            print("Illegal move made by Player 2")
            break
        s = result(s, action)
        if terminal_test(s):
            print("Game Over")
            display(s)
            display_final(s,-1)
            break
        

if __name__ == '__main__':
    play_game()

#the board i took is from (0,0) to (14,14) in (row,column) format