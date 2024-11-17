'''
randothellogame module

sets up a RandOthello game closely following the book's framework for games

RandOthelloState is a class that will handle our state representation, then we've 
got stand-alone functions for player, actions, result and terminal_test

Differing from the book's framework, is that utility is *not* a stand-alone 
function, as each player might have their own separate way of calculating utility


'''
import random
import copy

WHITE = 1
BLACK = -1
EMPTY = 0
BLOCKED = -2
SIZE = 8
SKIP = "SKIP"

class OthelloPlayerTemplate:
    '''Template class for an Othello Player

    An othello player *must* implement the following methods:

    get_color(self) - correctly returns the agent's color

    make_move(self, state) - given the state, returns an action that is the agent's move
    '''
    def __init__(self, mycolor):
        self.color = mycolor

    def get_color(self):
        return self.color

    def make_move(self, state):
        '''Given the state, returns a legal action for the agent to take in the state
        '''
        return None
    
class RandomPlayer(OthelloPlayerTemplate):
    def __init__(self, mycolor):
        self.color = mycolor

    def get_color(self):
        return self.color
    
    def make_move(self,state):
        move=None
        legal=actions(state)
        move=random.choice(legal)
        return move

class MiniMaxPlayer(OthelloPlayerTemplate):
    def __init__(self, mycolor,d):
        self.color=mycolor
        self.depth=d

    def get_color(self):
        return self.color
    
    def minimax(self,state,depth): 
        value,move=self.maxvalue(state,depth)
        return move


    def maxvalue(self,state, depth):
        if depth == 0 or terminal_test(state):
            return self.utility_function(state), None
        best_value = -float('inf')
        
        for move in actions(state):
            v2, a2 = self.minvalue(result(state, move), depth - 1)
            if v2 > best_value:
                best_value = v2
                best_move = move
        return best_value, best_move

    def minvalue(self,state, depth):
        if depth == 0 or terminal_test(state):
            return self.utility_function(state), None
        best_value = float('inf')
        
        for move in actions(state):
            v2,a2 = self.maxvalue(result(state, move), depth - 1)
            if v2< best_value:
                best_value = v2
                best_move = move
        return best_value, best_move
    
    def utility_function(self,state):
        wc=0
        bc=0
        value=0
        color=self.color
        for i in range(SIZE):
            for j in range(SIZE):
                if state.board_array[i][j] == WHITE:
                    wc += 1
                elif state.board_array[i][j] == BLACK:
                    bc += 1
    
        if color==1:
            if terminal_test(state) is True:
                if wc>bc:
                    value=100
                
                else:
                    value=-150
                return value
        
            else:
                value= wc-bc
                return value
    
        else:
            if terminal_test(state) is True:
                if bc>wc:
                    value=100
                else:
                    value=-150
                return value
        
            else:
                value=bc-wc
                return value
        
    def make_move(self, state):
        curr_move = None
        legals = actions(state)
        curr_move=self.minimax(state,4)
        return curr_move


class HumanPlayer(OthelloPlayerTemplate):
    def __init__(self, mycolor):
        self.color = mycolor

    def get_color(self):
        return self.color

    def make_move(self, state):
        curr_move = None
        legals = actions(state)
        while curr_move == None:
            display(state)
            if self.color == 1:
                print("White ", end='')
            else:
                print("Black ", end='')
            print(" to play.")
            print("Legal moves are " + str(legals))
            move = input("Enter your move as a r,c pair:")
            if move == "":
                return legals[0]

            if move == SKIP and SKIP in legals:
                return move

            try:
                movetup = int(move.split(',')[0]), int(move.split(',')[1])
            except:
                movetup = None
            if movetup in legals:
                curr_move = movetup
            else:
                print("That doesn't look like a legal action to me")
        return curr_move
    
class AlphaBetaPlayer(OthelloPlayerTemplate):
    def __init__(self, mycolor,d):
        self.color=mycolor
        self.depth=d

    def get_color(self):
        return self.color
    
    def alphabeta(self,state,depth): 
        value,move=self.maxvalue(state,depth,float("inf"),float("inf"))
        return move


    def maxvalue(self,state, depth,alpha,beta):
        if depth == 0 or terminal_test(state):
            return self.utility_function(state), None
        best_value = -float('inf')
        
        for move in actions(state):
            v2, a2 = self.minvalue(result(state, move), depth - 1,alpha,beta)
            if v2 > best_value:
                best_value = v2
                best_move = move
                alpha=max(alpha,best_value)
            if best_value>=beta:
                return best_value,move
        return best_value, best_move

    def minvalue(self,state, depth,alpha,beta):
        if depth == 0 or terminal_test(state):
            return self.utility_function(state), None
        best_value = float('inf')
        
        for move in actions(state):
            v2,a2 = self.maxvalue(result(state, move), depth - 1,alpha,beta)
            if v2< best_value:
                best_value = v2
                best_move = move
                beta=min(beta,best_value)
            if alpha>=best_value:
                return best_value,best_move

        return best_value, best_move
    
    def utility_function(self,state):
        wc=0
        bc=0
        value=0
        color=self.color
        for i in range(SIZE):
            for j in range(SIZE):
                if state.board_array[i][j] == WHITE:
                    wc += 1
                elif state.board_array[i][j] == BLACK:
                    bc += 1
    
        if color==1:
            if terminal_test(state) is True:
                if wc>bc:
                    value=100
                
                else:
                    value=-150
                return value
        
            else:
                value= wc-bc
                return value
    
        else:
            if terminal_test(state) is True:
                if bc>wc:
                    value=100
                else:
                    value=-150
                return value
        
            else:
                value=bc-wc
                return value
        
    def make_move(self, state):
        curr_move = None
        legals = actions(state)
        curr_move=self.alphabeta(state,8)
        return curr_move




class RandOthelloState:
    '''A class to represent an othello game state'''

    def __init__(self, currentplayer, otherplayer, board_array = None, num_skips = 0):
        if board_array != None:
            self.board_array = board_array
        else:
            self.board_array = [[EMPTY] * SIZE for i in range(SIZE)]
            self.board_array[3][3] = WHITE
            self.board_array[4][4] = WHITE
            self.board_array[3][4] = BLACK
            self.board_array[4][3] = BLACK
            x1 = random.randrange(8)
            x2 = random.randrange(8)
            self.board_array[x1][0] = BLOCKED
            self.board_array[x2][7] = BLOCKED
        self.num_skips = num_skips
        self.current = currentplayer
        self.other = otherplayer


def player(state):
    return state.current

def actions(state):
    '''Return a list of possible actions given the current state
    '''
    legal_actions = []
    for i in range(SIZE):
        for j in range(SIZE):
            if result(state, (i,j)) != None:
                legal_actions.append((i,j))
    if len(legal_actions) == 0:
        legal_actions.append(SKIP)
    return legal_actions

def result(state, action):
    '''Returns the resulting state after taking the given action

    (This is the workhorse function for checking legal moves as well as making moves)

    If the given action is not legal, returns None

    '''
    # first, special case! an action of SKIP is allowed if the current agent has no legal moves
    # in this case, we just skip to the other player's turn but keep the same board
    if action == SKIP:
        newstate = RandOthelloState(state.other, state.current, copy.deepcopy(state.board_array), state.num_skips + 1)
        return newstate

    if state.board_array[action[0]][action[1]] != EMPTY:
        return None

    color = state.current.get_color()
    # create new state with players swapped and a copy of the current board
    newstate = RandOthelloState(state.other, state.current, copy.deepcopy(state.board_array))

    newstate.board_array[action[0]][action[1]] = color
    
    flipped = False
    directions = [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]
    for d in directions:
        i = 1
        count = 0
        while i <= SIZE:
            x = action[0] + i * d[0]
            y = action[1] + i * d[1]
            if x < 0 or x >= SIZE or y < 0 or y >= SIZE:
                count = 0
                break
            elif newstate.board_array[x][y] == -1 * color:
                count += 1
            elif newstate.board_array[x][y] == color:
                break
            else:
                count = 0
                break
            i += 1

        if count > 0:
            flipped = True

        for i in range(count):
            x = action[0] + (i+1) * d[0]
            y = action[1] + (i+1) * d[1]
            newstate.board_array[x][y] = color

    if flipped:
        return newstate
    else:  
        # if no pieces are flipped, it's not a legal move
        return None

def terminal_test(state):
    '''Simple terminal test
    '''
    # if both players have skipped
    if state.num_skips == 2:
        return True

    # if there are no empty spaces
    empty_count = 0
    for i in range(SIZE):
        for j in range(SIZE):
            if state.board_array[i][j] == EMPTY:
                empty_count += 1
    if empty_count == 0:
        return True
    return False


# To start the minimax search with a given depth, you can call minimax like this:
"""depth = 3  # Set the desired depth
best_move = minimax(state, depth, MiniMaxPlayer.get_color())"""

def display(state):
    '''Displays the current state in the terminal window
    '''
    print('  ', end='')
    for i in range(SIZE):
        print(i,end='')
    print()
    for i in range(SIZE):
        print(i, '', end='')
        for j in range(SIZE):
            if state.board_array[j][i] == WHITE:
                print('W', end='')
            elif state.board_array[j][i] == BLACK:
                print('B', end='')
            elif state.board_array[j][i] == BLOCKED:
                print('X', end='')
            else:
                print('-', end='')
        print()

def display_final(state):
    '''Displays the score and declares a winner (or tie)
    '''
    wcount = 0
    bcount = 0
    for i in range(SIZE):
        for j in range(SIZE):
            if state.board_array[i][j] == WHITE:
                wcount += 1
            elif state.board_array[i][j] == BLACK:
                bcount += 1

    print("Black: " + str(bcount))
    print("White: " + str(wcount))
    if wcount > bcount:
        print("White wins")
    elif wcount < bcount:
        print("Black wins")
    else:
        print("Tie")
           

def play_game(p1 = None, p2 = None):
    '''Plays a game with two players. By default, uses two humans
    '''
    if p1 == None:
        #p1 = HumanPlayer(BLACK)
        p1=RandomPlayer(BLACK)
        #p1=MiniMaxPlayer(BLACK,4)
    if p2 == None:
        #p2 = HumanPlayer(WHITE)
        p2=RandomPlayer(WHITE)

    s = RandOthelloState(p1, p2)
    while True:
        action = p1.make_move(s)
        print(action)
        if action not in actions(s):
            print("Illegal move made by Black")
            print("White wins!")
            return
        s = result(s, action)
        if terminal_test(s):
            print("Game Over")
            display(s)
            display_final(s)
            return
        action = p2.make_move(s)
        if action not in actions(s):
            print("Illegal move made by White")
            print("Black wins!")
            return
        s = result(s, action)
        if terminal_test(s):
            print("Game Over")
            display(s)
            display_final(s)
            return

def main():
    play_game(p1=AlphaBetaPlayer(BLACK,4))
    print("After swapping colors:")
    play_game(p2=AlphaBetaPlayer(WHITE,5))

if __name__ == '__main__':
    main()

"""Sample Output:

(4, 5)
(2, 3)
(3, 6)
(4, 1)
(6, 3)
(1, 7)
(6, 5)
(1, 1)
(6, 1)
SKIP
(7, 1)
(4, 0)
(7, 5)
(1, 5)
(0, 3)
(5, 6)
(2, 5)
(4, 7)
(2, 7)
(3, 1)
(7, 4)
(2, 4)
(5, 4)
(7, 0)
(0, 7)
(6, 6)
(0, 1)
(1, 2)
(1, 0)
(7, 6)
Game Over
  01234567
0 WBWWWWXB
1 BBBWWWBB
2 BBWBWBBB
3 BBWWBWBB
4 BBWBWBBB
5 BBBWBWBB
6 BBBBBBBB
7 BBBBBWXW
Black: 43
White: 19
Black wins
After swapping colors:
(2, 3)
(2, 1)
(5, 4)
(5, 3)
(4, 5)
(1, 2)
(4, 1)
(5, 6)
(2, 7)
(1, 6)
(1, 4)
(5, 1)
(0, 3)
(1, 5)
(1, 1)
(6, 3)
(4, 7)
(3, 1)
(6, 1)
(1, 7)
(6, 6)
(6, 5)
(3, 2)
(5, 0)
(7, 4)
(7, 2)
(0, 1)
(7, 6)
(7, 5)
Game Over
  01234567
0 WWWWWBWX
1 BWBBBWWW
2 BWWBBWWW
3 BWBWBBWW
4 WWWWWBBW
5 WWWWWWWW
6 WBBBBBWW
7 XBBWWWWW
Black: 21
White: 41
White wins
"""