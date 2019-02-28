""" Plantilla para crear un nuevo jugador.
"""
from tools import minimax,heuristics
from random import choice
import chess

AUTHOR = ['Beatriz Perez Vera',"Roman Antonio Pozas"]
NAME = 'Normy'

oo = 10e100

class Player:
	def __init__(self, color):
		self.color = color

	def play(self, board: chess.Board, result, local_timeout, global_timeout):
		legal_moves = list(board.legal_moves)
		move = choice(legal_moves)
		result.value = str(move)
		depth=3

		result.value = str(minimax.Alpha_Beta(board,None, self.color, depth, heuristics.Control_tablero, -oo,oo,False)[0])


