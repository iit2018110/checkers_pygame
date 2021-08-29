from copy import deepcopy
import pygame
from .constants import *

def minimax(board,depth,color,game):
	if depth==0 or board.winner()!=None:
		return board.heuristic(),board

	if color == WHITE:
		maxvalue=float('-10000')
		best_move=None
		for move in all_moves(board,WHITE,game):
			maxvalue=max(minimax(move,depth-1,WHITE,game)[0],maxvalue)
			if maxvalue == minimax(move,depth-1,WHITE,game)[0]:
				best_move=move

		return maxvalue,best_move
	else:
		minvalue=float('10000')
		best_move=None
		for move in all_moves(board,RED,game):
			minvalue=min(minimax(move,depth-1,RED,game)[0],maxvalue)
			if minvalue == minimax(move,depth-1,RED,game)[0]:
				best_move=move

		return minvalue,best_move



def all_moves(board,color,game):
	moves=[]
	for piece in board.get_all_pieces(color):
		valid_moves=board.get_valid_moves(piece)
		for i ,j in valid_moves.items():
#			draw_moves(game, board, piece)
			temp=deepcopy(board)
			temp.move(temp.get_piece(piece.row,piece.col),i[0],i[1])
			if j:
				temp.remove(j)
			moves.append(temp)
	return moves

def draw_moves(game, board, piece):
    valid_moves = board.get_valid_moves(piece)
    board.draw(game.win)
    pygame.draw.circle(game.win, (0,255,0), (piece.x, piece.y), 50, 5)
    game.draw_valid_moves(valid_moves.keys())
    pygame.display.update()

