from wingedsheep.carcassonne.objects.coordinate_with_side import CoordinateWithSide


class Road:
    def __init__(self, road_positions: [CoordinateWithSide], finished: bool):
        self.road_positions = road_positions
        self.finished = finished

    def __eq__(self, other: 'Road'):
        return isinstance(other, Road) and \
               self.road_positions == other.road_positions and \
               self.finished == other.finished

    def __hash__(self):
        return hash(self.__dict__.values())
