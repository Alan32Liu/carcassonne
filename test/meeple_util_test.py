import copy
import unittest

from main.carcassonne_game_state import CarcassonneGameState
from main.tile_sets.base_deck import base_tiles
from main.objects.city import City
from main.objects.coordinate import Coordinate
from main.objects.coordinate_with_side import CoordinateWithSide
from main.objects.meeple_position import MeeplePosition
from main.objects.meeple_type import MeepleType
from main.objects.side import Side
from main.utils.city_util import CityUtil
from main.utils.meeple_util import MeepleUtil


class TestMeepleUtil(unittest.TestCase):

    def test_find_meeples_in_donut_city(self):
        """
        Find meeple positions for a donut shaped city
        """

        # Given
        meeple_util: MeepleUtil = MeepleUtil()
        game_state: CarcassonneGameState = self.create_donut_city_board()
        game_state.placed_meeples = [[], []]

        meeple_0_1 = MeeplePosition(meeple_type=MeepleType.NORMAL, coordinate_with_side=CoordinateWithSide(Coordinate(2, 1), Side.RIGHT))
        meeple_0_2 = MeeplePosition(meeple_type=MeepleType.NORMAL, coordinate_with_side=CoordinateWithSide(Coordinate(0, 1), Side.LEFT))
        meeple_1_1 = MeeplePosition(meeple_type=MeepleType.BIG, coordinate_with_side=CoordinateWithSide(Coordinate(1, 2), Side.TOP))

        game_state.placed_meeples[0].append(meeple_0_1)
        game_state.placed_meeples[0].append(meeple_0_2)
        game_state.placed_meeples[1].append(meeple_1_1)
        game_state.players = 2

        meeples_to_remove = [[], []]
        meeples_to_remove[0].append(copy.deepcopy(meeple_0_1))
        meeples_to_remove[1].append(copy.deepcopy(meeple_1_1))

        # When
        meeple_util.remove_meeples(game_state=game_state, meeples=meeples_to_remove)

        # Then
        self.assertEqual(1, len(game_state.placed_meeples[0]))
        self.assertEqual(0, len(game_state.placed_meeples[1]))
        self.assertIn(copy.deepcopy(meeple_0_2), game_state.placed_meeples[0])

    def create_donut_city_board(self) -> CarcassonneGameState:
        game_state = CarcassonneGameState()
        city_narrow_left_right = base_tiles["city_narrow"]
        city_narrow_top_bottom = base_tiles["city_narrow"].turn(1)
        city_diagonal_top_right = base_tiles["city_diagonal_top_right"]
        city_diagonal_bottom_right = base_tiles["city_diagonal_top_right"].turn(1)
        city_diagonal_bottom_left = base_tiles["city_diagonal_top_right"].turn(2)
        city_diagonal_top_left = base_tiles["city_diagonal_top_right"].turn(3)

        game_state.board = [[None for column in range(3)] for row in range(3)]

        game_state.board[0][0] = city_diagonal_bottom_right
        game_state.board[0][1] = city_narrow_left_right
        game_state.board[0][2] = city_diagonal_bottom_left
        game_state.board[1][0] = city_narrow_top_bottom
        game_state.board[1][2] = city_narrow_top_bottom
        game_state.board[2][0] = city_diagonal_top_right
        game_state.board[2][1] = city_narrow_left_right
        game_state.board[2][2] = city_diagonal_top_left
        return game_state
