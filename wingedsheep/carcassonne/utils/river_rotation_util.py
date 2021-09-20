from wingedsheep.carcassonne.carcassonne_game_state import CarcassonneGameState
from wingedsheep.carcassonne.objects.actions.tile_action import TileAction
from wingedsheep.carcassonne.objects.rotation import Rotation
from wingedsheep.carcassonne.objects.side import Side
from wingedsheep.carcassonne.utils.side_modification_util import SideModificationUtil
from wingedsheep.carcassonne.utils.map_util import MapUtil


class RiverRotationUtil:

    @classmethod
    def get_river_rotation(cls, game_state: CarcassonneGameState, this_tile_action: TileAction) -> Rotation:
        if this_tile_action.tile.has_river() and game_state.last_tile_action is not None:
            river_rotation: Rotation = cls.get_river_rotation_tile(
                state=game_state,
                this_tile_action=this_tile_action)
            if river_rotation != Rotation.NONE:
                return river_rotation
            else:
                return game_state.last_river_rotation
        return Rotation.NONE

    @classmethod
    def get_river_rotation_tile(cls, state: CarcassonneGameState, this_tile_action: TileAction) -> Rotation:
        def get_non_connecting_side() -> Side:
            for side in this_tile_action.tile.get_river_ends():
                if side == prev_relative_to_this:
                    continue
                return side

        prev_relative_to_this: Side \
            = MapUtil.c1_relative_to_c2(c1=state.last_tile_action.coordinate,
                                        c2=this_tile_action.coordinate)
        assert prev_relative_to_this in this_tile_action.tile.get_river_ends()

        return cls.get_river_rotation_ends(connecting_side=prev_relative_to_this,
                                           non_connecting_side=get_non_connecting_side())

    @classmethod
    def get_river_rotation_ends(cls, connecting_side: Side, non_connecting_side: Side) -> Rotation:
        if SideModificationUtil.turn_side(non_connecting_side, 1) == connecting_side:
            return Rotation.CLOCKWISE
        elif SideModificationUtil.turn_side(non_connecting_side, 3) == connecting_side:
            return Rotation.COUNTER_CLOCKWISE
        else:
            return Rotation.NONE
