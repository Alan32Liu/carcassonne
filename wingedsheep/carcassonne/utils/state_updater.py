import copy
import pdb

from typing import Optional

from wingedsheep.carcassonne.carcassonne_game_state import CarcassonneGameState
from wingedsheep.carcassonne.objects.actions.action import Action
from wingedsheep.carcassonne.objects.actions.meeple_action import MeepleAction
from wingedsheep.carcassonne.objects.actions.pass_action import PassAction
from wingedsheep.carcassonne.objects.actions.tile_action import TileAction
from wingedsheep.carcassonne.objects.coordinate import Coordinate
from wingedsheep.carcassonne.objects.game_phase import GamePhase
from wingedsheep.carcassonne.objects.meeple_position import MeeplePosition
from wingedsheep.carcassonne.objects.meeple_type import MeepleType
from wingedsheep.carcassonne.objects.player import Player
from wingedsheep.carcassonne.utils.points_collector import PointsCollector
from wingedsheep.carcassonne.utils.river_rotation_util import RiverRotationUtil
from wingedsheep.carcassonne.utils.tile_position_finder import TilePositionFinder


class StateUpdater:

    @staticmethod
    def next_player(game_state: CarcassonneGameState) -> CarcassonneGameState:
        game_state.phase = GamePhase.TILES
        game_state.current_player = game_state.current_player + 1
        if game_state.current_player >= game_state.players:
            game_state.current_player = 0
        return game_state

    @staticmethod
    def play_tile(game_state: CarcassonneGameState, tile_action: TileAction) -> CarcassonneGameState:
        game_state.board[tile_action.coordinate.row][tile_action.coordinate.column] = tile_action.tile
        game_state.phase = GamePhase.MEEPLES
        game_state.last_river_rotation = RiverRotationUtil.get_river_rotation(game_state=game_state,
                                                                              this_tile_action=tile_action)
        game_state.last_tile_action = tile_action
        return game_state

    @staticmethod
    def play_meeple(game_state: CarcassonneGameState, meeple_action: MeepleAction) -> CarcassonneGameState:
        if not meeple_action.remove:
            game_state.placed_meeples[game_state.current_player].append(
                MeeplePosition(meeple_type=meeple_action.meeple_type,
                               coordinate_with_side=meeple_action.coordinate_with_side))
        else:
            game_state.placed_meeples[game_state.current_player].remove(
                MeeplePosition(meeple_type=meeple_action.meeple_type,
                               coordinate_with_side=meeple_action.coordinate_with_side))

        if meeple_action.meeple_type == MeepleType.NORMAL or meeple_action.meeple_type == MeepleType.FARMER:
            game_state.meeples[game_state.current_player] += 1 if meeple_action.remove else -1
        elif meeple_action.meeple_type == MeepleType.ABBOT:
            if meeple_action.remove:
                points = PointsCollector.chapel_or_flowers_points(game_state=game_state,
                                                                  coordinate=meeple_action.coordinate_with_side.coordinate)
                game_state.scores[game_state.current_player] += points
            game_state.abbots[game_state.current_player] += 1 if meeple_action.remove else -1
        elif meeple_action.meeple_type == MeepleType.BIG or meeple_action.meeple_type == MeepleType.BIG_FARMER:
            game_state.big_meeples[game_state.current_player] += 1 if meeple_action.remove else -1

        return game_state

    @staticmethod
    def draw_tile(game_state: CarcassonneGameState) -> CarcassonneGameState:
        if len(game_state.deck) == 0:
            game_state.next_tile = None
        else:
            game_state.next_tile = game_state.deck.pop(0)
        return game_state

    @staticmethod
    def remove_meeples_and_update_score(game_state: CarcassonneGameState) -> CarcassonneGameState:
        if game_state.last_tile_action is not None and game_state.last_tile_action.tile is not None:
            PointsCollector.remove_meeples_and_collect_points(game_state=game_state,
                                                              coordinate=game_state.last_tile_action.coordinate)
        return game_state

    @classmethod
    def apply_action(cls, game_state: CarcassonneGameState, action: Action) -> CarcassonneGameState:
        def update_board_player(row: int, col: int):
            new_game_state.board_player[row][col] = Player(game_state.current_player)

        def is_valid_meeple_placement(meeple_coordinate: Coordinate):
            if new_game_state.board_player[meeple_coordinate.row][meeple_coordinate.column] is None:
                pdb.set_trace()
                return False
            player_owns_tile: Optional[int] = \
                new_game_state.board_player[meeple_coordinate.row][meeple_coordinate.column].id()
            return player_owns_tile == game_state.current_player

        def update_open_coordinates(state: CarcassonneGameState, tile_coordinate: Coordinate):
            # print([f"{coordinate}" for coordinate in state.open_coordinates])
            state.open_coordinates.remove(tile_coordinate)
            # print([f"{coordinate}" for coordinate in state.open_coordinates])
            state.open_coordinates.update(
                TilePositionFinder.get_open_neighbours(game_state=state, center=tile_coordinate)
            )
            # print([f"{coordinate}" for coordinate in state.open_coordinates])

        new_game_state: CarcassonneGameState = copy.deepcopy(game_state)

        if isinstance(action, TileAction):
            cls.play_tile(game_state=new_game_state, tile_action=action)
            update_board_player(action.coordinate.row, action.coordinate.column)
            update_open_coordinates(state=new_game_state, tile_coordinate=action.coordinate)
            new_game_state.phase = GamePhase.MEEPLES
        elif isinstance(action, MeepleAction):
            if not is_valid_meeple_placement(meeple_coordinate=action.coordinate_with_side.coordinate):
                print("ERROR: Invalid Meeple placement")
                pdb.set_trace()
            assert is_valid_meeple_placement(meeple_coordinate=action.coordinate_with_side.coordinate)
            cls.play_meeple(game_state=new_game_state, meeple_action=action)
        elif isinstance(action, PassAction):
            if game_state.phase == GamePhase.TILES:
                assert game_state.is_terminated()
                # A very rare case
                print("WARN: The last tile cannot be placed on the board")
                pdb.set_trace()
            elif game_state.phase == GamePhase.MEEPLES:
                pass

        if game_state.phase == GamePhase.MEEPLES:
            cls.remove_meeples_and_update_score(game_state=new_game_state)
            cls.draw_tile(game_state=new_game_state)
            cls.next_player(game_state=new_game_state)

        if new_game_state.is_terminated():
            PointsCollector.count_final_scores(game_state=new_game_state)

        return new_game_state
