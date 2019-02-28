import importlib
import os


def is_player(mod):
    try:
        assert hasattr(mod, 'AUTHOR')
        assert hasattr(mod, 'NAME')
        assert hasattr(mod, 'Player')
        assert hasattr(mod.Player, 'play')
        return True

    except AssertionError as e:
        return False


def name2std(name):
    return name.lower().replace("-", "_").replace(" ", "_")


def discover_players():
    names = {}

    for folder in os.scandir('players'):
        try:
            mod = importlib.import_module('players.{}.player'.format(folder.name))
            if is_player(mod):
                name = name2std(mod.NAME)

                if name in names:
                    print("Colliding name {0}, between {1} and {2}".format(name, mod.AUTHOR, names[name].AUTHOR))
                else:
                    names[name] = mod
        except ModuleNotFoundError:
            pass

    return names


def print_pos(pos):
    print()
    # uni_pieces = {'R': '♜', 'N': '♞', 'B': '♝', 'Q': '♛', 'K': '♚', 'P': '♟',
    #               'r': '♖', 'n': '♘', 'b': '♗', 'q': '♕', 'k': '♔', 'p': '♙', '.': '·'}

    uni_pieces = {'R': 'R', 'N': 'N', 'B': 'B', 'Q': 'Q', 'K': 'K', 'P': 'P',
                  'r': 'r', 'n': 'n', 'b': 'b', 'q': 'q', 'k': 'k', 'p': 'p', '.': '·'}
    for i, row in enumerate(str(pos).strip().split('\n')):
        print(8 - i, ' '.join(uni_pieces[i] for i in row.split(' ')))
    print('  a b c d e f g h \n\n')
