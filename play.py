from agent import *
import random


def gen_dice(nr):
    return [random.randint(1, 6) for _ in range(nr)]

class GameManager:
    def __init__(self, player_inits, nr_dice_per_player):
        self.player_inits = player_inits
        self.nr_dice_per_player = nr_dice_per_player

        self.turn = 0
        self.start()

    def start(self):
        print("\n=== Start ===\n")
        bads = [i for i, x in enumerate(self.nr_dice_per_player) if x <= 0]

        for i in bads[::-1]:
            del self.player_inits[i]
            del self.nr_dice_per_player[i]

        self.players = []
        for i, pl_init in enumerate(self.player_inits):
            if self.nr_dice_per_player[i] <= 0:
                continue
            print("Player", i, ":", pl_init.__name__, "with", self.nr_dice_per_player[i], "dice")
            dice = gen_dice(self.nr_dice_per_player[i])

            nr = self.nr_dice_per_player[i:] + self.nr_dice_per_player[:i]
            self.players.append(pl_init(nr, dice))

        self.last_statement = Interjection(None)

    def __str__(self):
        return "GM(players=" + str(self.players) + ")"

    def step(self):
        self.turn = self.turn % len(self.players)

        curr_interj = self.players[self.turn].play()
        print("\tPlayer", self.turn, "played", curr_interj)

        if self.last_statement.is_statement() and curr_interj.is_statement():
            if curr_interj.data < self.last_statement.data:
                print("Invalid!")
                return

        for i, pl in enumerate(self.players):
            pl.observe((i - self.turn) % len(self.players), curr_interj)

        if curr_interj.is_call():
            self.check_last_call()
            return

        self.turn += 1

        self.last_statement = curr_interj

    def check_last_call(self):
        print("Players:", self.players)
        all_dice = [dice for pl in self.players for dice in pl.dice]
        count = Counter(all_dice)
        print("Dice:", all_dice, "count", count)

        statement = self.last_statement.data

        actual_count = count[statement.suit]
        if statement.suit != 1:
            total_count = actual_count + count[1]
        else:
            total_count = actual_count

        print("Was:", total_count, "(", actual_count, "+", total_count - actual_count, ")")

        if total_count == statement.count:
            if len(gm.nr_dice_per_player) > 2:
                self.nr_dice_per_player[self.turn - 1] += 1
            self.nr_dice_per_player[self.turn] -= 1
            print("Player", self.turn-1, "(stater) won exactly!")

        elif total_count < statement.count:
            dice_loss = statement.count - total_count
            self.nr_dice_per_player[self.turn - 1] -= dice_loss

            print("Player", self.turn-1, "(stater) lost", dice_loss, "dice")
        else:
            self.nr_dice_per_player[self.turn] -= 1
            print("Player", self.turn-1, "(stater) won")

        self.start()


if __name__ == "__main__":
    gm = GameManager([StatsAgent, ObserverAgent, StupidAgent, InputAgent], [4] * 4)

    while len(gm.nr_dice_per_player) > 1:
        gm.step()
