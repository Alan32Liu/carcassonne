from typing import Optional
from wingedsheep.carcassonne.objects.side import Side
from wingedsheep.carcassonne.objects.coordinate import Coordinate


class MapUtil:

    @staticmethod
    def c1_relative_to_c2(c1: Coordinate, c2: Coordinate) -> Optional[Side]:
        if c1.row == (c2.row - 1):
            return Side.TOP
        if c1.row == (c2.row + 1):
            return Side.BOTTOM
        if c1.column == (c2.column - 1):
            return Side.LEFT
        if c1.column == (c2.column + 1):
            return Side.RIGHT
        return None
