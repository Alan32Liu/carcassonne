import json

from wingedsheep.carcassonne.objects.farmer_side import FarmerSide
from wingedsheep.carcassonne.objects.side import Side


class FarmerConnection:
    def __init__(self, farmer_positions: [Side], tile_connections: [FarmerSide] = (), city_sides: [Side] = ()):
        self.farmer_positions: [Side] = farmer_positions
        self.tile_connections: [FarmerSide] = tile_connections
        self.city_sides: [Side] = city_sides

    def to_json(self):
        return {
            "farmer_position": [farmer_position.to_json() for farmer_position in self.farmer_positions],
            "tile_connections": [tile_connection.to_json() for tile_connection in self.tile_connections],
            "city_sides": [city_side.to_json() for city_side in self.city_sides]
        }

    def __str__(self):
        return json.dumps(self.to_json(), indent=2)

    def __eq__(self, other: 'FarmerConnection'):
        return isinstance(other, FarmerConnection) and \
               self.farmer_positions == other.farmer_positions and \
               self.tile_connections == other.tile_connections and \
               self.city_sides == other.city_sides

    def __hash__(self):
        return hash((tuple(self.farmer_positions), tuple(self.tile_connections), tuple(self.city_sides)))
