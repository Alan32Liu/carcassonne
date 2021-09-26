from typing import Dict, Optional, Set

from wingedsheep.carcassonne.carcassonne_game_state import CarcassonneGameState
from wingedsheep.carcassonne.objects.coordinate import Coordinate
from wingedsheep.carcassonne.objects.playing_position import PlayingPosition
from wingedsheep.carcassonne.objects.tile import Tile
from wingedsheep.carcassonne.utils.map_util import MapUtil
from wingedsheep.carcassonne.utils.tile_fitter import TileFitter


class TilePositionFinder:

    @staticmethod
    def get_neighbours(game_state: CarcassonneGameState, center: Coordinate) \
            -> Dict[Coordinate, Optional[Tile]]:
        row, col = center.row, center.column

        return {
            Coordinate(row=neighbour_row, column=neighbour_col):
                game_state.get_tile(row=neighbour_row, column=neighbour_col)
            for neighbour_row, neighbour_col in [(row, col-1), (row, col+1), (row+1, col), (row-1, col)]
            if MapUtil.within_board(c=Coordinate(row=neighbour_row, column=neighbour_col), game_state=game_state)
        }

    @staticmethod
    def get_open_neighbours(game_state: CarcassonneGameState, center: Coordinate) -> Set[Coordinate]:
        return {neighbour_coordinate for neighbour_coordinate, neighbour_tile in
                TilePositionFinder.get_neighbours(game_state=game_state, center=center).items()
                if neighbour_tile is None}

    @staticmethod
    def possible_playing_positions(game_state: CarcassonneGameState, tile_to_play: Tile) -> [PlayingPosition]:

        def tile_fits(tile_turns: int, coordinate: Coordinate):
            row, col = coordinate.row, coordinate.column
            return TileFitter.fits(
                center=tile_to_play.turn(tile_turns),
                top=game_state.get_tile(row - 1, col),
                bottom=game_state.get_tile(row + 1, col),
                left=game_state.get_tile(row, col - 1),
                right=game_state.get_tile(row, col + 1),
                game_state=game_state)

        if game_state.empty_board():
            return [PlayingPosition(coordinate=game_state.starting_position, turns=i) for i in range(0, 4)]

        playing_positions = [
            PlayingPosition(coordinate=tile_coordinate, turns=tile_turns)
            for tile_turns in range(0, 4)
            for tile_coordinate in game_state.open_coordinates
            if tile_fits(tile_turns=tile_turns, coordinate=tile_coordinate)
        ]
        # print("[possible_playing_positions] Open Coordinates")
        # print([f"{coordinate}" for coordinate in game_state.open_coordinates])
        # print("[possible_playing_positions] possible_playing_positions:")
        # print([f"{coordinate.coordinate}, {coordinate.turns}" for coordinate in playing_positions])

        return playing_positions
