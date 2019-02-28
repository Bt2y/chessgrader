from tools import values
import chess

# Heuristics = [
# 	#Movilidad del tablero
# 	"goloso_heuristic(board,color)",
# 	"conection_heuristic(board,color)",
# 	"ControlCenter(board,color)",
# 	# "par_de_alfiles(board,color)",
# 	# "alfiles_en_la_primera_fila(board,color)",
# 	# "torre_septima_fila(board,color)",
# 	"posision_piezas(board,color)",
# 	## "casillas_controladas(board,color)",
# 	# "RookFreeColumn(board,color)",
# 	# "RookFreeSemiColumn(board,color)",
# 	# "VerticalRookConetion(board,color)",
# 	# "HorizontalRookConetion(board,color)",
# 	# #Seguridad del rey
# 	# "Castle(board,color)",
# 	# "KingThreats(board,color)"

# ]
# heuristic_mask = [1 for _ in range(len(Heuristics))]

def Control_tablero(board:chess.Board, color,in_time):
	# result = 0
	# for h in range(len(Heuristics)):
	# 	# print(Heuristics[h],eval(Heuristics[h]))
	# 	# print(board)
	# 	result += heuristic_mask[h]*eval(Heuristics[h])
	# return result

	h1 =goloso_heuristic(board,color)
	h2 =conection_heuristic(board,color)
	h3 =posision_piezas(board,color)
	if(in_time):
		h4 =ControlCenter(board,color)
		return h1+h2+h3+h4
		# h4 =casillas_controladas(board,color)
	return h1+h2+h3

#############################################################################################
######################MOVILIDAD DEL TABLERO##################################################
#############################################################################################
def goloso_heuristic(board:chess.Board, color):
	"""Trata de comer la mayor cantidad de piezas enemigas posibles"""
	result = 0
	for pos in str(board):
		if pos in values.value_piece:
			result += values.value_piece[pos]
	return result if color == chess.WHITE else -result

def conection_heuristic(board:chess.Board, player):
	pieces = board.piece_map()
	value = 0

	for p in pieces:
		if pieces[p].color == player:
			attack = board.attackers(player,p)
			if len(attack)!=0:
				value+=values.value_protect_piece
		else:
			attack = board.attackers(pieces[p].color, p)
			if len(attack) != 0:
				value -= values.value_protect_piece
	return value if player == chess.WHITE else -value

# YA
def ControlCenter(board:chess.Board, color):

	result = 0
	for i in [27,28,35,36]:
		p=board.piece_at(i)
		if p!=None:
			result+=values.value_center[p.symbol()]
	return result if color == chess.WHITE else -result

# YA
def par_de_alfiles(board:chess.Board,player):
	return _par_de_alfiles(board,player)-_par_de_alfiles(board,not player)

def _par_de_alfiles(board:chess.Board,player):
	piece = board.pieces(chess.BISHOP, player)
	if len(piece) == 2:
		return 25
	return 0
# YA
def alfiles_en_la_primera_fila(board:chess.Board, player):
	return _alfiles_en_la_primera_fila(board,player)-_alfiles_en_la_primera_fila(board,not player)


def _alfiles_en_la_primera_fila(board:chess.Board, player):
	result = 0
	if player == chess.WHITE:
		for i in range(0,8):
			if board.piece_at(i) == chess.BISHOP and  board.piece_at(i).color == player:
				result+=-15
	else:
		for i in range(56,64):
			if board.piece_at(i) == chess.BISHOP and board.piece_at(i).color == player:
				result+=-15
	return result

# YA
def torre_septima_fila(board:chess.Board,player):
	return _torre_septima_fila(board,player) - _torre_septima_fila(board,not player)

def _torre_septima_fila(board:chess.Board,player):
	result = 0
	if player == chess.WHITE:
		for i in range(48, 56):
			if board.piece_at(i) == chess.ROOK and board.piece_at(i).color == player:
				result += 20
		# for i in range(8, 16):
		# 	if board.piece_at(i) == chess.ROOK and board.piece_at(i).color != player:
		# 		result -= 20
	else:
		for i in range(8, 16):
			if board.piece_at(i) == chess.ROOK and board.piece_at(i).color == player:
				result += 20
		# for i in range(48,56):
		# 	if board.piece_at(i) == chess.ROOK and board.piece_at(i).color != player:
		# 		result -= 20
	return result

# YA
def posision_piezas(board:chess.Board, player):
	result = 0
	pieces = board.piece_map()
	for pos in pieces:
		if pieces[pos].color == player:
			# print("MIO", pos)
			# print("MIOPieza", pieces[pos])
			if str(pieces[pos]) == chess.KING:
				result += (values.values_position_pieces[str(pieces[pos])])[pos][0]
			else:
				result += (values.values_position_pieces[str(pieces[pos])])[pos]
		else:
			# print("MIO", pos)
			# print("MIOPieza", pieces[pos])
			if str(pieces[pos]) == chess.KING:
				result -= (values.values_position_pieces[str(pieces[pos])])[pos][0]
			else:
				result -= (values.values_position_pieces[str(pieces[pos])])[pos]
	return result

# YA
def casillas_controladas(board:chess.Board, player):
	return _casillas_controladas(board,player) - _casillas_controladas(board,not player)

def _casillas_controladas(board:chess.Board, player):
	result = 0
	for i in range(0,64):
		if board.piece_at(i) !=None:
			if board.piece_at(i).color != player and len(board.attackers(player,i))!=0:
				result += 5
		elif len(board.attackers(player,i))!=0:
			result += 5
	return result

def RookFreeColumn(board: chess.Board, Player):
	valueW = _RookFreeColumn(board, chess.WHITE)
	valueB = _RookFreeColumn(board, chess.BLACK)

	value = valueW - valueB
	return value if Player == chess.WHITE else -value

def _RookFreeColumn(board: chess.Board, Player):
	Rooks = board.pieces(chess.ROOK, Player)
	value = len(Rooks)

	if value==0:
		return 0

	for r in Rooks:
		pos = r
		for i in range(0, 7):
			pos = (pos + 8) % 64
			if (board.piece_type_at(pos) == chess.PAWN):
				if (board.piece_at(r).color == Player):
					value -= 1
				break
	return value * 15

def RookFreeSemiColumn(board: chess.Board, Player):
	valueW = _RookFreeSemiColumn(board, chess.WHITE)
	valueB = _RookFreeSemiColumn(board, chess.BLACK)

	value = valueW - valueB
	return value if Player == chess.WHITE else -value

def _RookFreeSemiColumn(board: chess.Board, Player):
	Rooks = board.pieces(chess.ROOK, Player)

	value = -1
	for r in Rooks:
		pos = r
		for i in range(0, 7):
			pos = (pos + 8) % 64
			piece = board.piece_at(pos)
			if (piece != None and piece.piece_type == chess.PAWN and piece.color != Player):
				#               solo puede haber un peon del contrario
				value = 1 if value == -1 else 0

	value = 1 if value == 1 else 0
	return value * 17

def VerticalRookConetion(board: chess.Board, Player):
	valueW = _VerticalRookConetion(board, chess.WHITE)
	valueB = _VerticalRookConetion(board, chess.BLACK)

	value = valueW - valueB
	return value if Player == chess.WHITE else -value

def _VerticalRookConetion(board: chess.Board, Player):
	Rooks = board.pieces(chess.ROOK, Player)
	value = len(Rooks)

	if value < 2:
		return 0
	pos = Rooks.pop()

	for i in range(0, 7):
		pos = (pos + 8) % 64
		piece = board.piece_at(pos)

		if (piece != None and piece.piece_type != chess.ROOK):
			return 0
	return 40

def HorizontalRookConetion(board: chess.Board, Player):
	valueW = _HorizontalRookConetion(board, chess.WHITE)
	valueB = _HorizontalRookConetion(board, chess.BLACK)

	value = valueW - valueB
	return value if Player == chess.WHITE else -value

def _HorizontalRookConetion(board: chess.Board, Player):
	Rooks = board.pieces(chess.ROOK, Player)
	value = len(Rooks)

	if value < 2:
		return 0
	pos = Rooks.pop()

	for i in range(0, 7):
		pos = (pos + 1) % 8
		piece = board.piece_at(pos)

		if (piece != None and piece.piece_type != chess.ROOK):
			return 0
	return 40

#############################################################################################
##########################SEGURIDAD DEL REY##################################################
#############################################################################################

def Castle(board:chess.Board, player):
	if(board.has_kingside_castling_rights(player)):
		return 50
	if(board.has_queenside_castling_rights(player)):
		return 40
	return -60

def KingThreats(board: chess.Board, Player):
	result = 0
	pieces = board.piece_map()
	for pos in pieces:
		if board.is_pinned(pieces[pos].color,pos):
			result +=-8

	result += -8*len(board.attackers(not Player, board.king(Player)))
	return result

#############################################################################################
##########################POSICION DE LOS PEONES#############################################
#############################################################################################

def PassPawn(board,Player):
    Pawns=board.pieces(Player,chess.PAWN)
    value=len(Pawns)
    for p in Pawns:
        pos=p
        for i in range(0,7):
            if Player==chess.WHITE:
                pos=(pos+8)
                if pos>63:
                    break
                piece=board.piece_at(pos)
                if piece!=None and piece.color!=chess.WHITE and pieces.piece_type == chess.PAWN:
                    value-=1
                    break
            else:
                pos=(pos-8)
                if pos<0:
                    break
                piece=board.piece_at(pos)
                if piece!=None and piece.color!=chess.BLACK and pieces.piece_type == chess.PAWN:
                    value-=1
                    break
    return value*20

    
