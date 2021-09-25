from typing import Optional
from wingedsheep.carcassonne.carcassonne_game_state import CarcassonneGameState
from wingedsheep.carcassonne.carcassonne_visualiser import CarcassonneVisualiser
from wingedsheep.carcassonne.objects.actions.action import Action
from wingedsheep.carcassonne.tile_sets.supplementary_rules import SupplementaryRule
from wingedsheep.carcassonne.tile_sets.tile_sets import TileSet
from wingedsheep.carcassonne.utils.action_util import ActionUtil
from wingedsheep.carcassonne.utils.state_updater import StateUpdater


class CarcassonneGame:

    def __init__(self,
                 players: int = 2,
                 board_size: (int, int) = (17, 31),  # (35, 35),
                 starting_position: (int, int) = (8, 15),
                 tile_sets: [TileSet] = (TileSet.BASE, TileSet.THE_RIVER, TileSet.INNS_AND_CATHEDRALS),
                 supplementary_rules: [SupplementaryRule] = (SupplementaryRule.FARMERS, SupplementaryRule.ABBOTS),
                 visualise_screen: Optional[int] = None):
        self.players = players
        self.tile_sets = tile_sets
        self.supplementary_rules = supplementary_rules
        self.state: CarcassonneGameState = CarcassonneGameState(
            players=players,
            board_size=board_size,
            starting_position=starting_position,
            tile_sets=tile_sets,
            supplementary_rules=supplementary_rules
        )
        self.visualise_screen = visualise_screen
        if visualise_screen is not None:
            self.visualiser = CarcassonneVisualiser(screen=visualise_screen)

    def reset(self):
        self.state = CarcassonneGameState(tile_sets=self.tile_sets,
                                          supplementary_rules=self.supplementary_rules,
                                          players=self.players)
        if self.visualise_screen is not None:
            self.visualiser.cleanup()

    def step(self, player: int, action: Action):
        self.state = StateUpdater.apply_action(game_state=self.state, action=action)

    def render(self):
        self.visualiser.draw_game_state(self.state)

    def is_finished(self) -> bool:
        return self.state.is_terminated()

    def get_current_player(self) -> int:
        return self.state.current_player

    def get_possible_actions(self) -> [Action]:
        return ActionUtil.get_possible_actions(self.state)
