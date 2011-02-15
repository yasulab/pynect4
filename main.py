#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys 
height = -1
width = -1
connect_n = -1
board = []
possible_moves = []
SPACE = " "
P1 = "x"
P2 = "o"
NONE = ""
turn = P1
winner = NONE
DEBUG = False

def create_board(height, width, connect_n):
    global board
    for y in range(height):
        line = []
        #print "y="+str(y)
        for x in range(width):
            #print "x="+str(x)
            line.append(SPACE)
        board.append(line)

def show_board():
    global board
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

def is_board_full():
    global board
    for line in board:
        for elem in line:
            if elem == P1 or elem == P2:
                continue
            return False
    return True

def switch_turn():
    global turn
    if turn == P1:
        turn = P2
    else:
        turn = P1

def show_whos_turn():
    global turn
    if turn == P1:
        print "Player 1's turn: "
    else:
        print "Player 2's turn: "

def calc_possible_moves():
    global board, possible_moves
    possible_moves = []
    for x in range(width):
        if is_row_filled(x) == False:
            possible_moves.append(x)

def get_current_player():
    global board
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
    global possible_moves
    #flg = True
    calc_possible_moves()
    show_whos_turn()
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

def check_win_state():
    global board, width, height, turn, connect_n, winner
    max_connect = -1
    current_state = SPACE
    state_list = []

    if DEBUG: print turn+"'s X state check."
    for line in board:
        max_connect = calc_max_connect(turn, line)
        if max_connect >= connect_n:
            winner = turn
            return

    if DEBUG: print turn+"'s Y state check."
    for x in range(width):
        state_list = []
        for y in range(height):
            state_list.append(board[y][x])
        max_connect = calc_max_connect(turn, state_list)
        if max_connect >= connect_n:
            winner = turn
            return

    if DEBUG: print turn+"'s diagonal state check."
    state_list = []
    for x in range(width):
        state_list = get_right_diagonal_state(x,0)
        max_connect = calc_max_connect(turn, state_list)
        if max_connect >= connect_n:
            winner = turn
            return
        state_list = get_left_diagonal_state(x,0)
        max_connect = calc_max_connect(turn, state_list)
        if max_connect >= connect_n:
            winner = turn
            return
        
    for y in range(height):
        state_list = get_right_diagonal_state(0,y)
        max_connect = calc_max_connect(turn, state_list)
        if max_connect >= connect_n:
            winner = turn
            return
        state_list = get_left_diagonal_state(0,y)
        max_connect = calc_max_connect(turn, state_list)
        if max_connect >= connect_n:
            winner = turn
            return
            
def get_right_diagonal_state(x, y):
    global board
    state_list = []
    while x < width and y < height:
        state_list.append(board[y][x])
        x += 1
        y += 1
    return state_list           

def get_left_diagonal_state(x, y):
    global board
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
        

def is_elem_filled(x, y):
    global board
    if board[y][x] == SPACE:
        return False
    else:
        return True

def is_row_filled(row):
    global board
    for y in range(height):
        if board[y][row] == SPACE:
            return False
        else:
            continue
    return True

def set_elem(x, y, turn):
    global board
    board[y][x] = turn

def insert_coin(turn, row):
    global board, height
    y = height - 1
    while 0 <= y:
        if is_elem_filled(row, y) == True:
            y -= 1
            continue
        else:
            set_elem(row, y, turn)
            return

def show_whos_win():
    global winner
    if winner == NONE:
        print "Game is over!"
    elif winner == P1:
        print "Player 1 wins!"
    elif winner == P2:
        print "Player 2 wins!"
    else:
        print "Error: unknown winner..."
    return

def game_play():
    global turn, winner
    turn = P1
    while is_board_full() == False and winner == NONE:
        show_board()
        given_row = get_input()
        insert_coin(turn, given_row)
        check_win_state()
        turn = get_current_player()
    show_board()
    show_whos_win()
    print
    print "Game Is Over!"
    
if __name__ == "__main__":
    argvs = sys.argv 
    argc = len(argvs)
    if (argc != 4):  
        print 'Usage: $ python %s WIDTH HEIGHT CONNECT_N' % argvs[0]
        quit()

    #print 'The content of %s ...n' % argvs[1]
    height = int(argvs[1])
    width = int(argvs[2])
    connect_n = int(argvs[3])
    print "height = " + str(height)
    print "width = " + str(width)
    print "connect_n = " + str(connect_n)

    create_board(height, width, connect_n)
    game_play()
    
