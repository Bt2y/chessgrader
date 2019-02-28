import chess


oo = 10e100


def Alpha_Beta(board, play, player, depth, h, alpha, beta,in_time):
	best = None
	if (board.is_game_over()):
		if (board.is_checkmate()):
			return play, -oo
		return play, h(board, board.turn,in_time)
	if (depth == 0):
		return play, h(board, board.turn,in_time)
	movimientos = board.generate_legal_moves()

	moves = Order_moves(board, movimientos)
	best = moves[0] if len(moves) > 0 else None
	for mov in moves:
		board.push(mov)

		b, valor = Alpha_Beta(board, mov, board.turn, depth - 1, h, -1 * beta, -1 * alpha,in_time)

		board.pop()
		valor *= -1

		if (valor >= beta):
			return mov, beta
		if (valor > alpha):
			best = mov
			alpha = valor

	return best, alpha


def Order_moves(board, moves):
	a = []
	b = []
	for i in moves:
		a.append(i)
	for i in a:

		if board.is_capture(i) == True:
			b.append(i)
	for i in a:
		if board.is_capture(i) == False:
			b.append(i)
	return b
