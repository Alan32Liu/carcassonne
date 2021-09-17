from wingedsheep.carcassonne.objects.coordinate_with_side import CoordinateWithSide


class City:
    def __init__(self, city_positions: [CoordinateWithSide], finished: bool):
        self.city_positions = city_positions
        self.finished = finished

    def __eq__(self, other: 'City'):
        return isinstance(other, City) and \
               self.city_positions == other.city_positions and \
               self.finished == other.finished

    def __hash__(self):
        return hash(self.__dict__.values())
