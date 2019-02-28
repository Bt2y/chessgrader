import ctypes
import multiprocessing as mp
import time

import chess

import core.utils


class BasePlayer:
    def __init__(self, color):
        self.result = None

    def play(self, board: chess.Board, result, local_timeout, global_timeout):
        raise NotImplementedError()


class TimerControl:
    def __init__(self, local_timeout, global_time):
        self.local_timeout = local_timeout
        self.global_timeout = global_time

    def feed(self, delta):
        delta = max(delta - self.local_timeout, 0.)
        self.global_timeout = max(self.global_timeout - delta, 0.)

    def time(self):
        return self.local_timeout + self.global_timeout


def play(player0_cls, player1_cls, args):
    manager = mp.Manager()

    # Create instance of both players
    player0: BasePlayer = player0_cls(chess.WHITE)
    player1: BasePlayer = player1_cls(chess.BLACK)

    board = chess.Board()

    tc0 = TimerControl(args.local_timeout, args.global_timeout)
    tc1 = TimerControl(args.local_timeout, args.global_timeout)

    winner, error = 0, None
    steps = 0

    # Start game execution
    while not board.is_game_over():
        player = player0 if board.turn == chess.WHITE else player1
        tc = tc0 if board.turn == chess.WHITE else tc1

        result = manager.Value(ctypes.c_char_p, '')
        proc = mp.Process(target=player.play, args=(board.copy(), result, tc.local_timeout, tc.global_timeout))

        move, error = None, None

        try:
            start_time = time.time()
            proc.start()
            proc.join(tc.time())
            delta_time = time.time() - start_time
            tc.feed(delta_time)

            if proc.is_alive():
                proc.terminate()

                if result.value == '':
                    error = "Local Time Limit Exceeded"
                else:
                    move = result.value
                    move = chess.Move.from_uci(move)
            else:
                move = result.value
                move = chess.Move.from_uci(move)

        except Exception as e:
            if args.debug:
                raise e
            else:
                error = e.args[0]
                break

        if error is not None:
            break

        if not board.is_legal(move):
            error = "Illegal move, {}".format(move)
            break

        board.push(move)
        steps += 1

        if args.verbose >= 2:
            print("-------------------------------")
            print("Turn:", "BLACK" if board.turn == chess.WHITE else "WHITE")
            print("Move: {} Time remaining: {:.3}".format(move, tc.global_timeout))
            core.utils.print_pos(board)
        # input("esperando...")
        
    if error is None:
        result = board.result()

        if result == '1-0':
            winner = +1
        elif result == '0-1':
            winner = -1
        else:
            winner = 0
    else:
        winner = -1 if board.turn == chess.WHITE else +1

    if args.verbose >= 1:
        print("Winner:", "Black Draw White".split()[winner + 1])
        print("Error:", error)
        print("Steps:", steps)
        print()

    return winner, error
