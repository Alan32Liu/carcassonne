from wingedsheep.carcassonne.objects.actions.action import Action
from wingedsheep.carcassonne.objects.coordinate import Coordinate
from wingedsheep.carcassonne.objects.tile import Tile


class TileAction(Action):
    def __init__(self, tile: Tile, coordinate: Coordinate, tile_rotations: int):
        self.tile = tile
        self.coordinate = coordinate
        self.tile_rotations = tile_rotations

    def __eq__(self, other: 'TileAction'):
        return isinstance(other, TileAction) and \
               self.tile == other.tile and\
               self.coordinate == other.coordinate and \
               self.tile_rotations == other.tile_rotations
