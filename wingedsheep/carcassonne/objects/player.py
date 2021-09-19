from enum import Enum


class Player(Enum):
    PLAYER1 = 0
    PLAYER2 = 1
    PLAYER3 = 2
    PLAYER4 = 3
    PLAYER5 = 4
    PLAYER6 = 5

    @staticmethod
    def all_colours():
        return ["BLUE", "RED", "BLACK", "YELLOW", "GREEN", "PINK"]

    def id(self):
        return self.value

    def colour(self):
        return self.all_colours()[self.id()]

    def __str__(self):
        return f"({self.value}, {self.colour()})"
