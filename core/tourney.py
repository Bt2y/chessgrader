from core import game


class Tourney:
    def __init__(self, players, args):
        self.players = players
        self.args = args
        self.points = [0.] * self.total

    @property
    def total(self):
        return len(self.players)

    def presentation(self):
        print("Total players:", len(self.players))
        print("{:25}| {}".format("Name", "Author"))
        for player in self.players:
            print("{:25}| {}".format(player.NAME, ', '.join(player.AUTHOR)))
        print()

    def run(self):
        raise NotImplementedError()

    def results(self):
        players = [(pnt, mod) for mod, pnt in zip(self.players, self.points)]
        players.sort(key=lambda x: -x[0])

        print("{0:5}| {1:25}| {2}".format("Score", "Name", "Author"))

        for pnt, player in players:
            print("{0:5}| {1:25}| {2}".format(pnt, player.NAME, ', '.join(player.AUTHOR)))


class RoundRobin(Tourney):
    def run(self):
        self.points = [0] * self.total

        for i in range(self.total):
            for j in range(self.total):
                if i == j:
                    continue

                print("-- {0}(W) VS {1}(B) --".format(self.players[i].NAME, self.players[j].NAME))
                winner, error = game.play(self.players[i].Player, self.players[j].Player, self.args)

                if winner == +1:
                    self.points[i] += 1.
                if winner == -1:
                    self.points[j] += 1.
                else:
                    self.points[i] += .5
                    self.points[j] += .5


class SwissSystem(Tourney):
    def run(self):
        import random

        order = random.sample(range(self.total), self.total)  # Initial random order
        rounds = self.rounds

        print("Rounds:", rounds)
        print("Matches:", rounds * self.total // 2)

        for i_round in range(rounds):
            for i in range(0, self.total, 2):
                p0 = self.players[order[i]]
                p1 = self.players[order[i + 1]]

                print("-- {0}(W) VS {1}(B) --".format(p0.NAME, p1.NAME))
                winner, error = game.play(p0.Player, p1.Player, self.args)

                if winner == +1:
                    self.points[order[i]] += 1.
                elif winner == -1:
                    self.points[order[i + 1]] += 1.
                else:
                    self.points[order[i]] += .5
                    self.points[order[i + 1]] += .5

            order.sort(key=lambda x: -self.points[x])

            if self.args.verbose >= 1:
                print("Round:", i_round)
                print(order)
                print([self.points[order[i]] for i in range(self.total)])

        return order

    def set_rounds(self, rounds):
        self._rounds = rounds

    @property
    def rounds(self):
        if not hasattr(self, '_rounds'):
            r = 1
            while 2 ** r < self.total:
                r += 1
            return 2 * r
        else:
            return self._rounds
