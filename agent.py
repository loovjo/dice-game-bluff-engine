from say import Interjection, Statement
from collections import Counter
import random

def dice():
    l = list(range(1, 7))
    random.shuffle(l)
    return l

def get_count(counter, val):
    if val == 1:
        return counter[val]
    return counter[val] + counter[1]

class Agent:
    def __init__(self, nr_dice_per_player, dice):
        self.nr_dice_per_player = nr_dice_per_player
        self.dice = dice

    # Gives an Interjection
    def play(self):
        raise NotImplementedError()

    # rel_player_id is number of players left before self
    # The person before self is 1, self is 0, next is nr_players-1 etc.
    def observe(self, rel_player_id, interj):
        raise NotImplementedError()

    def __str__(self):
        return self.__class__.__name__ + "(dice=" + str(self.dice) + ")"

    __repr__ = __str__


class SafeAgent(Agent):
    def __init__(self, nr_dice_per_player, dice):
        super().__init__(nr_dice_per_player, dice)
        self.last_statement = Interjection(None)

        self.count = Counter(dice)

    def play(self):
        for i in dice():
            for c in range(1, self.count[i] + 1):
                st = Statement(c, i)
                if self.last_statement.is_call() or st > self.last_statement.data:
                    return Interjection(st)
        return Interjection(None)

    def observe(self, rel_player_id, interj):
        self.last_statement = interj

class StatsAgent(Agent):
    def __init__(self, nr_dice_per_player, dice):
        super().__init__(nr_dice_per_player, dice)
        self.last_statement = Interjection(None)

        self.avg_dice = int(sum(nr_dice_per_player[1:]) / 6)

        self.count = Counter(dice)

    def play(self):
        for i in dice():
            count = get_count(self.count, i)
            count += self.avg_dice
            if i != 1:
                count += self.avg_dice
            for c in range(1, count + 1):
                st = Statement(c, i)
                if self.last_statement.is_call() or st > self.last_statement.data:
                    return Interjection(st)
        return Interjection(None)

    def observe(self, rel_player_id, interj):
        self.last_statement = interj

class ObserverAgent(Agent):
    def __init__(self, nr_dice_per_player, dice):
        super().__init__(nr_dice_per_player, dice)
        self.last_statement = Interjection(None)

        self.other_dices = Counter()

        self.count = Counter(dice)

    def play(self):
        for i in dice():
            count = get_count(self.count, i) + get_count(self.other_dices, i)
            for c in range(1, count + 1):
                st = Statement(c, i)
                if self.last_statement.is_call() or st > self.last_statement.data:
                    return Interjection(st)
        return Interjection(None)

    def observe(self, rel_player_id, interj):
        self.last_statement = interj

        if interj.is_statement() and rel_player_id != 0:
            self.other_dices[interj.data.suit] = \
                max(self.other_dices[interj.data.suit], interj.data.count-1)

class StupidAgent(Agent):
    def __init__(self, nr_dice_per_player, dice):
        super().__init__(nr_dice_per_player, dice)
        self.last_statement = Interjection(None)

    def play(self):
        for i in dice() * 2:
            count = random.randint(1, 7)
            st = Statement(count, i)
            if self.last_statement.is_call() or st > self.last_statement.data:
                return Interjection(st)
        return Interjection(None)

    def observe(self, rel_player_id, interj):
        self.last_statement = interj

class InputAgent(Agent):
    def __init__(self, nr_dice_per_player, dice):
        super().__init__(nr_dice_per_player, dice)

    # Gives an Interjection
    def play(self):
        print("Your dice are:", self.dice)
        print("\n")
        while True:
            ans = input("\033[2A\033[100DPlay (nr x suit) / call (c): ")
            ans = ans.replace(" ", "")
            if ans == "c":
                print("\033[2A\033[100D\033[15C<REDACTED>" + " " * 50 + "\033[1B")
                return Interjection(None)
            if "x" in ans:
                nr, suit = ans.split("x")
                try:
                    nr = int(nr)
                    suit = int(suit)
                    print("\033[2A\033[100D\033[15C<REDACTED>" + " " * 50 + "\033[1B")
                    return Interjection(Statement(nr, suit))
                except:
                    pass
            print("Invalid!")

    # rel_player_id is number of players left before self
    # The person before self is 1, self is 0, next is nr_players-1 etc.
    def observe(self, rel_player_id, interj):
        print("Player +" + str(rel_player_id), "played", interj)
