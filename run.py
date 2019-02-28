import argparse


def build_parser():
    parser = argparse.ArgumentParser("Chess Grader")

    parser.add_argument("-v", "--verbose", type=int, default=1)
    parser.add_argument("-d", "--debug", action="store_true", default=False)
    parser.add_argument("-l", "--local_timeout", type=float, default=1.)
    parser.add_argument("-g", "--global_timeout", type=float, default=60.)

    subparsers = parser.add_subparsers()

    tourney = subparsers.add_parser("tourney")
    tourney.set_defaults(mode="tourney")
    tourney_mode = tourney.add_mutually_exclusive_group()
    tourney_mode.add_argument("--swiss", action="store_true")

    match = subparsers.add_parser("match")
    match.set_defaults(mode="match")
    match.add_argument("player0")
    match.add_argument("player1")

    listp = subparsers.add_parser("list")
    listp.set_defaults(mode="list")

    return parser


if __name__ == '__main__':
    parser = build_parser()

    args = parser.parse_args()

    if not hasattr(args, 'mode'):
        parser.print_help()
        exit(10)

    if args.mode == 'tourney':
        from core import tourney, utils

        mods = utils.discover_players()
        players = [mod for name, mod in mods.items()]

        if args.swiss:
            if len(players) % 2 == 1:
                players.remove(mods['plantilla'])

            t = tourney.SwissSystem(players, args)
        else:  # Default tourney: Round robin
            t = tourney.RoundRobin(players, args)

        t.presentation()
        t.run()
        t.results()

    elif args.mode == 'match':
        from core import utils, game

        mods = utils.discover_players()

        name0 = utils.name2std(args.player0)
        name1 = utils.name2std(args.player1)

        mod0 = mods[name0]
        mod1 = mods[name1]

        game.play(mod0.Player, mod1.Player, args)

    elif args.mode == "list":
        from core import utils

        mods = utils.discover_players()

        for _, mod in mods.items():
            print("{0}: {1}".format(mod.NAME, ", ".join(mod.AUTHOR)))
