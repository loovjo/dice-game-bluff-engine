from functools import total_ordering
import unittest

class Interjection:
    def __init__(self, data):
        self.data = data

    def is_statement(self):
        return self.data is not None

    def is_call(self):
        return self.data is None

    def __str__(self):
        if self.is_call():
            return "Call"
        return "State(" + str(self.data) + ")"

    def __repr__(self):
        if self.is_call():
            return "Call"
        return "State(" + repr(self.data) + ")"


@total_ordering
class Statement:
    def __init__(self, count, suit):
        self.count = count
        self.suit = suit

    def get_effective_count(self):
        return self.count * (1 + (self.suit == 1))

    def __gt__(self, other):
        if self.get_effective_count() > other.get_effective_count():
            return True

        if self.get_effective_count() < other.get_effective_count():
            return False

        return self.suit > other.suit

    def __lt__(self, other):
        if self.get_effective_count() < other.get_effective_count():
            return True

        if self.get_effective_count() > other.get_effective_count():
            return False

        return self.suit < other.suit

    def __eq__(self, other):
        if isinstance(other, Statement):
            return self.suit == other.suit and self.count == other.count
        return False

    def __repr__(self):
        return "Statement(" + str(self.count) + "x" + str(self.suit) + ")"

    __str__ = __repr__

