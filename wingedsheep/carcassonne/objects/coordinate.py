class Coordinate:

    def __init__(self, row: int, column: int):
        self.row = row
        self.column = column

    def __eq__(self, other: 'Coordinate'):
        return isinstance(other, Coordinate) and \
               self.row == other.row and \
               self.column == other.column

    def __hash__(self):
        return hash((self.row, self.column))

    def __str__(self):
        return f"({self.row:02}, {self.column:02})"
