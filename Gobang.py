import sys
import string
import argparse
import re
import Board as board
import Evaluation as e
from time import time

global alphabet_dict
alphabet_dict = {"a": 1, "b": 2, "c": 3, "d": 4, "e": 5, "f":6, "g":7, "h": 8, "i": 9, "j":10, "k":11, "l":12, "m":13, "n":14, "o":15, "p":16, "q":17, "r":18, "s":19, "t":20, "u":21, "v":22, "w":23, "x":24, "y":25, "z":26}

def move_played(current_board, move_made):
	print("Move played: " + move_made) #need to convert coordinates to <letter><value>

def evaluate_user_input(current_board, user_input, size):
	user_input = user_input.replace("-", "!!5") #dont accept negative numbers 

	split_input = re.findall(r'[A-Za-z]+|\d+', user_input); #["a", [20]]
	if(len(split_input) != 2):
		print("Error: Invalid input size")
		return evaluate_user_input(current_board, raw_input(""), size) #CHANGE BACK TO INPUT FOR 3.0
	elif(split_input[0].isdigit() or len(split_input[0]) != 1):
		print("Error: First value cannot be a number or is invalid character")
		return evaluate_user_input(current_board, raw_input(""), size)
	elif(not(split_input[1].isdigit())): # we want the second value to be a number
		print("Error: Second value cannot be a character")
		return evaluate_user_input(current_board, raw_input(""), size)
	elif(int(split_input[1]) > size or alphabet_dict[split_input[0].lower()] > size): #assume here the corrrect two values were given..now check if the number hasn't exceeded size
		print("Error: Tried to move outside the table")
		return evaluate_user_input(current_board, raw_input(""), size)
	elif(not(current_board.is_unoccupied(((int(split_input[1])-1), (alphabet_dict[split_input[0].lower()]-1))))): #ck if move is in taken spot
		print("Error: This space is already taken")
		return evaluate_user_input(current_board, raw_input(""), size)
	else: #assume now that input could be done
		valid_move_as_coord = (int(split_input[1])-1, (alphabet_dict[split_input[0].lower()]-1))
		return (valid_move_as_coord, user_input)

def evaluate_AI_move(coordinates):
	(x, y) = coordinates 
	#return chr(y + 97) + str(x+1)
	return unichr(y+97) + str(x+1) # UNCOMMENT FOR PYTHON 2.7

def main():
	parser = argparse.ArgumentParser()

	args = parser.add_argument('-n', nargs='?', type=int, default=11)
	args = parser.add_argument('-l', action="store_true", default=False)

	args = vars(parser.parse_args())

	size = 0
	my_player = 0

	if(args["l"] == False): #l is unspecified
		my_player = board.Board.white_player
	else:
		my_player = board.Board.black_player

	if(args["n"] == 11):
		size = 11
	elif(args["n"] > 26 or args["n"] < 5):
		print("Error: Not a valid board size")
		return
	else:
		size = args["n"]


	current_board = e.Initial_State(size, my_player)

	e.print_board(current_board)

	move_played(current_board, "--")

	while(not(current_board.won) and not(current_board.is_board_full())): #stop looping if you win/if its a tie
		current_color = "Dark" if(current_board.player == 2) else "Light"
		if(current_board.my_player == current_board.player): #this means it is my turn to make a move
			print(current_color + " player (COM) plays now")
			start_time = time()
			move = e.iterative_deepening(current_board, start_time)
			current_board = e.Result(current_board, move)
			e.print_board(current_board) #printboard
			move_played(current_board, evaluate_AI_move(move))

		else:
			#need to wait for the user's input

			print(current_color + " player (human) plays now")
			user_input = raw_input("") #NEED TO CHANGE TO RAW_INPUT() FOR PYTHON 3..input() if python 2.7

			human_move = evaluate_user_input(current_board, user_input, size)

			current_board = e.Result(current_board, human_move[0])

			e.print_board(current_board) #print the board
			move_played(current_board, human_move[1]) #display the move made

	if(current_board.goal_test()):
		print(current_board.interpret_player(current_board.player) + " won!")
	else: 
		print("Tie")

if __name__ == '__main__':
	main()


#FINAL OUTPUT
#print board
#print last played move
#print whose turn it is now.