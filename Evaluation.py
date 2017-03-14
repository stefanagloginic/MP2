import Board as b
import sys
import random
import string
import math
import numpy as np
from time import time
from collections import Counter
from operator import itemgetter

INF = sys.maxint #CHANGE THIS TO MAXINT SO IT WORKS FOR PYTHON2.7 maxsize for python 3
NEG_INF = -1*INF

def Initial_State(size, my_player): #from AI book
	return(b.Board(size, b.Board.black_player, my_player)) #black player always goes first

def Player(board): #from AI book
	return(board.player)

def Actions(board): #from AI book
	return (board.get_actions())

def Result(board, action): #from AI book
	return(board.move(action)) #the acting depending on the coordinate that we choose

def print_board(brd): #from referee.py
	sys.stdout.write("  ")
	i = 0
	for c in string.ascii_lowercase:
		i += 1
		if i > brd.size:
			break
		sys.stdout.write("   %s" % c)
	sys.stdout.write("\n   +")
	for i in range(0, brd.size):
		sys.stdout.write("---+")
	sys.stdout.write("\n")

	for i in range(0, brd.size):
		sys.stdout.write("%2d |" % (i + 1))
		for j in range(0, brd.size):
			if brd.board[i][j] == b.Board.white_player:	
				sys.stdout.write(" L |")
			elif brd.board[i][j] == b.Board.black_player:
				sys.stdout.write(" D |")
			else:
				sys.stdout.write("   |")
		sys.stdout.write("\n   +")
		for j in range(0, brd.size):
			sys.stdout.write("---+")
		sys.stdout.write("\n")

def get_my_player(board):
	return board.my_player


def evaluation(board):
	"""This is my evaluation function"""

	directions = [(1,0), (0,1), (1,1), (1,-1)]

	sum_white = 0
	sum_black = 0
	
	for white_pieces in board.white:
		"""for each piece calculate all possible in a row connections and apply value"""
		for pair in directions:
			first_direction = board.check_connection(white_pieces, pair, b.Board.white_player)
			(row_move, col_move) = pair
			new_pair = (-row_move, -col_move)
			second_direction = board.check_connection(white_pieces, new_pair, b.Board.white_player)

			total_size = first_direction + second_direction

			if(total_size == 1):
				sum_white += 10
			if(total_size == 2):
				sum_white += 100
			if(total_size == 3):
				sum_white += 1000 #if(COLOR != s.State.white) else 500
			if(total_size == 4):
				sum_white += 10000 #if(COLOR != s.State.white) else 5000
			if(total_size + 1 == 5):
				sum_white += 100000 #if(COLOR != s.State.white) else 150000

	for black_pieces in board.black:
		"""for each piece calculate all possible in a row connections and apply value"""
		for pair in directions:
			first_direction = board.check_connection(black_pieces, pair, b.Board.black_player)
			(row_move, col_move) = pair
			new_pair = (-row_move, -col_move)
			second_direction = board.check_connection(black_pieces, new_pair, b.Board.black_player)

			total_size = first_direction + second_direction

			if(total_size == 1):
				sum_black += 10
			if(total_size == 2):
				sum_black += 100
			if(total_size == 3):
				sum_black += 1000 
			if(total_size == 4):
				sum_black += 10000 #if(COLOR != s.State.black) else 5000
			if(total_size + 1 == 5):
				sum_black += 100000 #if(COLOR != s.State.black) else 150000

	state_eval = (sum_white - sum_black) if(board.player == b.Board.white_player) else (sum_black - sum_white)

	return state_eval


"""def evaluation(board):
	return random.randint(0, 1000)
"""

'''def evaluation(board):
	directions = [(1,0), (0,1), (1,1), (1,-1)]

	total_sum_white = 0
	total_sum_black = 0

	for coordinates in board.black: #this for loop takes care of moving in both directions
		black_connect = 0
		for pair in directions:
			black_connect += 1 + board.check_connection(coordinates, pair, b.Board.black_player)
			(row, col) = pair
			black_connect += board.check_connection(coordinates, (-row,-col), b.Board.black_player)

		total_sum_black += pow(4, black_connect) #connect will always be at least 1. 

		if(black_connect == 5):
			total_sum_black += (pow(4, black_connect))

	for coordinates in board.white: #this for loop takes care of moving in both directions
		white_connect = 0
		for pair in directions:
			white_connect += 1 + board.check_connection(coordinates, pair, b.Board.white_player)
			(row, col) = pair
			white_connect += board.check_connection(coordinates, (-row,-col), b.Board.white_player)


		total_sum_white += pow(4, white_connect) 
		if(white_connect == 5):
			total_sum_white += (pow(4, white_connect))

	if(board.player == board.white_player):
		return(total_sum_white-total_sum_black)

	#I will take the max of the return value, thus prioritizing if my opponent has a better connection
	return(total_sum_black-total_sum_white)
'''

def is_time_exceeded(start_time):
	return((time()-start_time) >= b.Board.time_limit)		

def iterative_deepening(board, start_time):
	global evaluated 
	evaluated = "complete"

	depth = 0
	act = Actions(board)
	array_of_0 = [0 for val in range(len(act))]
	actions = zip(act, array_of_0) #want a tuple of action & value
	final_ordered_actions = []

	while(not(is_time_exceeded(start_time))):
		
		actions = alpha_beta_search(board, depth, actions, start_time) #will return when it sees it exceeded time limit
		if(evaluated == "incomplete"):
			if(len(final_ordered_actions) == 0):
				return actions[0][0]	
			return final_ordered_actions[0][0] #return the action with maximum value 
		
		final_ordered_actions = actions
		depth+=1

	return final_ordered_actions[0][0] #final selected action

def alpha_beta_search(board, depth_lim, actions_list, start_time): #from AI book, uses minimax with alpha beta pruning through iterative deepening.

	#will return sorted array consisting of tuple with coordinate, and corresponding value

	def max_value(curr_board, alpha, beta, depth, start_time): #from AI book
		if(is_time_exceeded(start_time) or depth > depth_lim or curr_board.goal_test()): #consider time limit & the depth according to the limit
			return evaluation(curr_board) #NEED TO IMPLEMENT

		v = NEG_INF
		for act in Actions(curr_board):
			v = max(v, min_value(Result(curr_board, act), alpha, beta, depth+1, start_time))
			if(v >= beta):
				return v 
			alpha = max(alpha, v) #want to pass the bigger of the two values
		return v

	def min_value(curr_board, alpha, beta, depth, start_time): #from AI book
		if(is_time_exceeded(start_time) or depth > depth_lim or curr_board.goal_test()): #consider time limit & the depth according to the limit
			return evaluation(curr_board)

		v = INF
		for act in Actions(curr_board):
			v = min(v, max_value(Result(curr_board, act), alpha, beta, depth+1, start_time))
			if(v <= alpha): #where the pruning comes in
				return v 
			beta = min(beta, v)
		return v


	sorted_actions = []			
	for act in actions_list: #alpha_beta_search's code
		
		if(is_time_exceeded(start_time)):
			evaluated = "incomplete"
			sorted_actions.sort(key=itemgetter(1), reverse=True) #return the list of actions sorted according to the highest value
			return sorted_actions

		(coordinates, value) = act
		val = min_value(Result(board, coordinates), NEG_INF, INF, 0, start_time)

		sorted_actions.append((coordinates, val)) #change action

	sorted_actions.sort(key=itemgetter(1), reverse=True) #return the list of actions sorted according to the highest value

	return sorted_actions