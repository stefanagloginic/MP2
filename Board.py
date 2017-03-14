import copy 
import sys
from time import time

class Board:

	black_player = 2
	white_player = 1
	empty = 0
	time_limit = 28 #CHANGE TO 28 SECONDS WHEN TURNING IN

	def __init__(self, size, player, my_player):
		#1 = white 2 = black
		self.white = [] # white pieces in play
		self.black = []
		self.board = [[0 for x in range(size)] for x in range(size)]
		self.size = size
		self.won = False
		self.player = player
		self.max_cells = size*size
		self.cells_occupied = 0 #used to check if board is full resulting in a tie
		self.my_player = my_player

	def goal_test(self): return self.won

	def is_my_opponent(self, player):
		return not(player != self.my_player)

	def is_board_full(self): return (self.max_cells == self.cells_occupied)

	def move_valid(self, coordinates): #ret bool...check if move is in scope of board & if unoccupied
		return(self.in_scope(coordinates) and self.is_unoccupied(coordinates))

	def in_scope(self, coordinates):
		(x,y) = coordinates
		return(x >= 0 and x < self.size and y >= 0 and y < self.size)
	
	def is_unoccupied(self, coordinates): #ret boolean if spot in board is taken/not
		(x,y) = coordinates
		occupied = self.board[x][y] == 0 
		return occupied

	def interpret_player(self, curr_player):
		if(curr_player == Board.black_player):
			return "Dark"
		return "Light"

	def __eq__(self, other_board):
		return(
			type(self) == type(other_board) and
			self.white == other_board.white and
			self.black == other_board.black and
			self.size == other_board.size
			)
	def __ne__(self, other_board):
		return (not(self == other_board))

	def move(self, coordinates): #will return same board if move isnt valid, otherwise returns new modified board
		(x,y) = coordinates 

		if(not(self.move_valid(coordinates))):
			return self #don't make a change to the board if move is out of scope/occupied/full

		new_board = copy.deepcopy(self)

		new_board.board[x][y] = self.player

		new_board.is_win(new_board.player, coordinates, 1)
	#	print(self.white)
	#	print(self.black)
		if(self.player == Board.white_player):
			new_board.white.append(coordinates) #add the new coordinate white is taking up
			new_board.player = Board.black_player 
		else:
			new_board.black.append(coordinates)  #add the new coordinate black is taking up
			new_board.player = Board.white_player #change to next player

		new_board.cells_occupied += 1 

		return new_board

	def is_win(self, curr_player, coordinates, connect):
		directions = [(1,0), (0,1), (1,1), (1,-1)]

		for pair in directions: #this for loop takes care of moving in both directions
			new_connect = connect + self.check_connection(coordinates, pair, curr_player)
			(row, col) = pair
			new_connect += self.check_connection(coordinates, (-row,-col), curr_player) 

			if(new_connect >= 5): #5 is all we need to win. 
				self.won = True
		
	def check_connection(self, coordinates, pair, curr_player): #recursive function to return connection
		(old_row, old_col) = coordinates
		(row_dir, col_dir) = pair
		new_coordinates = (old_row+row_dir, old_col+col_dir)
		if(not(self.in_scope(new_coordinates)) or not(curr_player == self.board[old_row+row_dir][old_col+col_dir])):
			return 0

		return self.check_connection(new_coordinates, pair, curr_player) + 1

	def get_actions(self): #returns a list of coordinates to the empty spots in board
		actions = []
		for row in range(0, self.size):
			for col in range(0, self.size):
				if(self.board[row][col] == Board.empty):
					actions.append((row, col))
		return actions
