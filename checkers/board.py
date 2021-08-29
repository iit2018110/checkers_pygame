import pygame
from .constants import *
from .piece import Piece

class Board:
    def __init__(self):
        self.board = []
        self.yellow_left = self.white_left = 12
        self.yellow_kings = self.white_kings = 0
        self.create_board()
    
    def draw_squares(self, win):
        win.fill(BLACK)
        for row in range(ROWS):
            for col in range(row % 2, COLS, 2):
                pygame.draw.rect(win, RED, (row*SQUARE_SIZE, col *SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def move(self, piece, row, col):
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        piece.move(row, col)

        if row == ROWS - 1 or row == 0:
            piece.make_king()
            if piece.color == WHITE:
                self.white_kings += 1
            else:
                self.yellow_kings += 1 

    def get_piece(self, row, col):
        return self.board[row][col]

    def get_all_pieces(self,color):
    	piece=[]
    	for row in self.board:
    		for i in row:
    			if i!=0 and i.color==color:
    				piece.append(i)
    	return piece



    def create_board(self):
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                if col % 2 == ((row +  1) % 2):
                    if row < 3:
                        self.board[row].append(Piece(row, col, WHITE))
                    elif row > 4:
                        self.board[row].append(Piece(row, col, YELLOW))
                    else:
                        self.board[row].append(0)
                else:
                    self.board[row].append(0)
        
    def draw(self, win):
        self.draw_squares(win)
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(win)

    def remove(self, pieces):
        for piece in pieces:
            self.board[piece.row][piece.col] = 0
            if piece != 0:
                if piece.color == YELLOW:
                    self.yellow_left -= 1
                else:
                    self.white_left -= 1
    
    def heuristic(self):
    	return self.white_left*1+self.white_kings*0.9-self.yellow_left*1-self.yellow_kings*0.9

    
    def winner(self):
        if self.yellow_left <= 0:
            return WHITE
        elif self.white_left <= 0:
            return YELLOW
        
        return None


    def get_valid_moves(self, piece):
        moves = {}
        if piece.color == YELLOW or piece.king:
	       	moves.update(self.transverse(piece.row,piece.col,piece.color,-1))
        if piece.color == WHITE or piece.king:
        	moves.update(self.transverse(piece.row,piece.col,piece.color,+1))
    
        return moves

    def transverse(self,row,col,color,dir):
    	moves={}
    	queue=[]
    	if dir==1:
    		if(col-1>=0 and row+1<8):
    			queue.append((row+1,col-1,-1))
    		if(col+1<8 and row+1<8):
    			queue.append((row+1,col+1,1))
    	else:
    		if(col-1>=0 and row-1>=0):
    			queue.append((row-1,col-1,-1))
    		if(col+1<8 and row-1>=0):
    			queue.append((row-1,col+1,1))


    	while(len(queue) > 0):
    		item=queue.pop(0)
    		current=self.board[item[0]][item[1]]
    		if current == 0:
    			if (item[0],item[1]) not in moves:
    				moves[(item[0],item[1])]=[]
    		elif current.color == color:
    			pass
    		else:
    			if(dir==1):
    				if (item[0]+1<8 and item[1]+1<8 and self.board[item[0]+1][item[1]+1] == 0 and item[2] ==1):
    					queue.append((item[0]+1,item[1]+1))
    					moves[(item[0]+1,item[1]+1)]=[self.board[item[0]][item[1]]]
    				if (item[0]+1<8 and item[1]-1>=0 and self.board[item[0]+1][item[1]-1] == 0 and item[2] ==-1):
    					queue.append((item[0]+1,item[1]-1))
    					moves[(item[0]+1,item[1]-1)]=[self.board[item[0]][item[1]]]
    			else:
    				if (item[0]-1>=0 and item[1]+1<8 and self.board[item[0]-1][item[1]+1] == 0 and item[2]==1):
    					queue.append((item[0]-1,item[1]+1))
    					moves[(item[0]-1,item[1]+1)]=[self.board[item[0]][item[1]]]
    				if (item[0]-1>=0 and item[1]-1>=0 and self.board[item[0]-1][item[1]-1] == 0 and item[2]==-1):
    					queue.append((item[0]-1,item[1]-1))
    					moves[(item[0]-1,item[1]-1)]=[self.board[item[0]][item[1]]]   					

    	return moves


