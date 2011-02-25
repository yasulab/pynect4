#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
import copy
height = -1
width = -1
connect_n = -1
play_style = ""
#board = []
#possible_moves = []
SPACE = " "
P1 = "x"
P2 = "o"
NONE = ""
turn = P1
#winner = NONE
DEBUG = False
EMPTY = []
HUMAN = "human"
CPU = "cpu"

class State:
    def __init__(self, board, turn):
        self.board = board
        #self.possible_moves = possible_moves
        self.turn = turn
        #self.winner = winner
        
def create_board(height, width, connect_n):
    board = []
    for y in range(height):
        line = []
        #print "y="+str(y)
        for x in range(width):
            #print "x="+str(x)
            line.append(SPACE)
        board.append(line)
    return board

def show_board(board):
    for i,line in enumerate(board):
        print str(i) + " |",
        for j,elem in enumerate(line):
            print elem,
        print
    print "   ",
    for x in range(width):
        print "-",
    print
    print "   ",
    for x in range(width):
        print str(x)[0],
    print

def is_board_full(board):
    for line in board:
        for elem in line:
            if elem == P1 or elem == P2:
                continue
            return False
    return True

def show_whos_turn(state):
    turn = state.turn
    if turn == P1:
        print "Player 1's turn: "
    else:
        print "Player 2's turn: "

def get_possible_moves(state):
    board = state.board
    possible_moves = []
    for x in range(width):
        if is_row_filled(board, x) == False:
            possible_moves.append(x)
    return possible_moves

def get_current_player(state):
    board = state.board
    p1 = p2 = 0
    for line in board:
        for elem in line:
            if elem == P1:
                p1 += 1
            elif elem == P2:
                p2 += 1
            else:
                continue
    if p1 == p2:
        return P1
    else:
        return P2        
    
def get_input():
    possible_moves = get_possible_moves(state)
    show_whos_turn(state)
    while True:
        print "\tPossible Moves"+str(possible_moves)+": ",
        given = raw_input()
        try:
            given_row = int(given)
        except:
            #print "Please input integer number."
            continue

        if given_row in possible_moves:
            return given_row

def get_winner(state):
    board = state.board
    if is_player_win(board, P1) == True:
        return P1
    elif is_player_win(board, P2) == True:
        return P2
    else:
        return NONE

def is_player_win(board, turn):
    global width, height, connect_n
    #turn = state.turn
    #winner = state.winner
    #board = state.board
    max_connect = -1
    current_state = SPACE
    state_list = []

    if DEBUG: print turn+"'s X state check."
    for line in board:
        max_connect = calc_max_connect(turn, line)
        if max_connect >= connect_n:
            return True

    if DEBUG: print turn+"'s Y state check."
    for x in range(width):
        state_list = []
        for y in range(height):
            state_list.append(board[y][x])
        max_connect = calc_max_connect(turn, state_list)
        if max_connect >= connect_n:
            return True

    if DEBUG: print turn+"'s diagonal state check."
    state_list = []
    for x in range(width):
        state_list = get_right_diagonal_state(board, x, 0)
        max_connect = calc_max_connect(turn, state_list)
        if max_connect >= connect_n:
            return True
        state_list = get_left_diagonal_state(board, x, 0)
        max_connect = calc_max_connect(turn, state_list)
        if max_connect >= connect_n:
            return True
        
    for y in range(height):
        state_list = get_right_diagonal_state(board, 0, y)
        max_connect = calc_max_connect(turn, state_list)
        if max_connect >= connect_n:
            return True

    for y in range(height):
        state_list = get_left_diagonal_state(board, width-1, y)
        max_connect = calc_max_connect(turn, state_list)
        if max_connect >= connect_n:
            return True
    return False
            
def get_right_diagonal_state(board, x, y):
    state_list = []
    while x < width and y < height:
        state_list.append(board[y][x])
        x += 1
        y += 1
    return state_list           

def get_left_diagonal_state(board, x, y):
    state_list = []
    while 0 <= x and y < height:
        state_list.append(board[y][x])
        x -= 1
        y += 1
    return state_list           
    
def calc_max_connect(turn, state_list):
    max_connect = 0
    max_connects = []
    for state in state_list:
        if state == turn:
            max_connect += 1
        else:
            max_connects.append(max_connect)
            max_connect = 0
    max_connects.append(max_connect)
    if DEBUG: print max_connects
    return max(max_connects)
        

def is_elem_filled(board, x, y):
    if board[y][x] == SPACE:
        return False
    else:
        return True

def is_row_filled(board, row):
    for y in range(height):
        if board[y][row] == SPACE:
            return False
        else:
            continue
    return True

def set_elem(state, x, y):
    state.board[y][x] = state.turn
    return state

def get_next_state(original_state, row):
    global height
    state = copy.deepcopy(original_state)
    board = state.board
    turn = state.turn
    y = height - 1
    while 0 <= y:
        if is_elem_filled(board, row, y) == True:
            y -= 1
            continue
        else:
            state = set_elem(state, row, y)
            state.turn = get_current_player(state)
            return state
    return NONE

def show_whos_win(state):
    winner = get_winner(state)
    if winner == NONE:
        print "Drawn Game!"
    elif winner == P1:
        print "Player 1 wins!"
    elif winner == P2:
        print "Player 2 wins!"
    else:
        print "Error: unknown winner..."
    return

def get_state_score(state, alpha, beta):
    return _get_state_score(state, state.turn, alpha, beta)
    
def _get_state_score(original_state, turn, alpha, beta):
    state = copy.deepcopy(original_state)
    score = 0
    child_scores = []
    possible_moves = get_possible_moves(state)
    if possible_moves == EMPTY: # Board is Full
        #show_board(state.board)
        winner = get_winner(state)
        if winner == NONE:
            #print "Drawn!"
            return 0
        elif winner == P2:
            #print "P2 win!"
            return 1
        else:
            #print "P1 win!"
            return -1
    else:
        for move in possible_moves:
            winner = get_winner(state)
            if winner == NONE:
                next_state = get_next_state(state, move)
                #show_board(next_state.board)
                score = _get_state_score(next_state, turn, alpha, beta)
                child_scores.append(score)
            elif winner == P2:
                return 1
            else:
                return -1
    # Already have all scores from children
    if state.turn == P2:
        return max(child_scores)
    else:
        return min(child_scores)

def ai_input(original_state):
    state = copy.deepcopy(original_state)
    possible_moves = get_possible_moves(state)
    max_move = -1
    max_score = -100
    
    alpha = -100
    beta = 100
    print
    print "move\t->\tscore"
    for move in possible_moves:
        next_state = get_next_state(state, move)
        alpha = score = get_state_score(next_state, alpha, beta)
        print str(move)+"\t->\t"+ str(score)
        if max_score <= score:
            max_score = score
            max_move = move
    print "max_score="+str(max_score)+", so next move is "+str(move) +"."
    print 
    return max_move

def show_state_score(original_state):
    state = copy.deepcopy(original_state)
    possible_moves = get_possible_moves(state)
    #print
    print possible_moves
    for move in possible_moves:
        print "move=" + str(move) + " -> " + str(get_state_score(get_next_state(state, move)))
    #print
    
def game_play(state):
    while is_board_full(state.board) == False and get_winner(state) == NONE:
        #show_state_score(state)
        show_board(state.board)
        if state.turn == P1:
            given_row = get_input()
        elif play_style == CPU and state.turn == P2:
            given_row = ai_input(state)
        else:
            print "Unknown Player..."
        state = get_next_state(state, given_row)
        #state.winner = get_winner(state)
        #state.turn = get_current_player(state)

    show_board(state.board)
    show_whos_win(state)
    print
    print "Game Is Over!"
    
if __name__ == "__main__":
    argvs = sys.argv 
    argc = len(argvs)
    if (argc != 5):
        print 'Usage: $ python %s WIDTH HEIGHT CONNECT_N PLAY_STYLE' % argvs[0]
        quit()

    height = int(argvs[1])
    width = int(argvs[2])
    connect_n = int(argvs[3])
    play_style = str(argvs[4])
    if play_style != "human" and play_style != "cpu":
        print "PLAY_STYLE should be either 'human' or 'cpu'."
        quit()

    print "height = " + str(height)
    print "width = " + str(width)
    print "connect_n = " + str(connect_n)

    
    board = create_board(height, width, connect_n)
    state = State(board, P1)
    game_play(state)
    
