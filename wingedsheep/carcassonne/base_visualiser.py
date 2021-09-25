import os
from PIL import ImageTk
from tkinter import Toplevel, Canvas
from typing import Tuple, List, Dict
from screeninfo import get_monitors, Enumerator, Monitor

import wingedsheep
from wingedsheep.carcassonne.objects.meeple_type import MeepleType
from wingedsheep.carcassonne.objects.side import Side


class BaseVisualiser:

    meeple_icons = {
        MeepleType.NORMAL: ["blue_meeple.png", "red_meeple.png", "black_meeple.png", "yellow_meeple.png",
                            "green_meeple.png", "pink_meeple.png"],
        MeepleType.ABBOT: ["blue_abbot.png", "red_abbot.png", "black_abbot.png", "yellow_abbot.png",
                           "green_abbot.png", "pink_abbot.png"]
    }
    player_colour = ["blue", "red", "black", "yellow", "green", "pink"]
    tile_size = 60
    meeple_size = 15
    big_meeple_size = 25

    meeple_position_offsets = {
        Side.TOP: (tile_size / 2, (meeple_size / 2) + 3),
        Side.RIGHT: (tile_size - (meeple_size / 2) - 3, tile_size / 2),
        Side.BOTTOM: (tile_size / 2, tile_size - (meeple_size / 2) - 3),
        Side.LEFT: ((meeple_size / 2) + 3, tile_size / 2),
        Side.CENTER: (tile_size / 2, tile_size / 2),
        Side.TOP_LEFT: (tile_size / 4, (meeple_size / 2) + 3),
        Side.TOP_RIGHT: ((tile_size / 4) * 3, (meeple_size / 2) + 3),
        Side.BOTTOM_LEFT: (tile_size / 4, tile_size - (meeple_size / 2) - 3),
        Side.BOTTOM_RIGHT: ((tile_size / 4) * 3, tile_size - (meeple_size / 2) - 3)
    }

    big_meeple_position_offsets = {
        Side.TOP: (tile_size / 2, (big_meeple_size / 2) + 3),
        Side.RIGHT: (tile_size - (big_meeple_size / 2) - 3, tile_size / 2),
        Side.BOTTOM: (tile_size / 2, tile_size - (big_meeple_size / 2) - 3),
        Side.LEFT: ((big_meeple_size / 2) + 3, tile_size / 2),
        Side.CENTER: (tile_size / 2, tile_size / 2),
        Side.TOP_LEFT: (tile_size / 4, (big_meeple_size / 2) + 3),
        Side.TOP_RIGHT: ((tile_size / 4) * 3, (big_meeple_size / 2) + 3),
        Side.BOTTOM_LEFT: (tile_size / 4, tile_size - (big_meeple_size / 2) - 3),
        Side.BOTTOM_RIGHT: ((tile_size / 4) * 3, tile_size - (big_meeple_size / 2) - 3)
    }

    def __init__(self, screen: int):
        self.images_path: str = os.path.join(wingedsheep.__path__[0], 'carcassonne', 'resources', 'images')
        self.tile_xy: Tuple[int, int] = (self.tile_size, self.tile_size)

        self.monitors: List[Monitor] = get_monitors(Enumerator.OSX)
        monitor: Monitor = self.monitors[screen]
        self.board: Toplevel = Toplevel()
        self.board.wm_geometry(f"{monitor.width}x{monitor.height}+{monitor.x}+{monitor.y}")

        self.canvas: Canvas = Canvas(self.board, width=1920, height=1080, bg='black')
        self.canvas.pack(fill='both', expand=True)
        self.meeple_image_refs: Dict[str, ImageTk] = {}
        self.tile_image_refs: Dict[str, ImageTk] = {}

    def cleanup(self):
        self.canvas.destroy()
        self.canvas: Canvas = Canvas(self.board, width=1920, height=1080, bg='black')
        self.canvas.pack(fill='both', expand=True)
        self.meeple_image_refs: Dict[str, ImageTk] = {}
        self.tile_image_refs: Dict[str, ImageTk] = {}

    # def draw_boarder(self, board_size: Tuple[int, int]):
    #     def draw_boarder_cell(r: int, c: int):
    #         self.canvas.create_image(
    #             c * self.tile_size,
    #             r * self.tile_size,
    #             anchor=NW,
    #             image=ImageTk.PhotoImage(Image.new("RGBA", (60, 60), color="black")))
    #
    #     row_max, column_max = board_size
    #     for row_index in range(row_max):
    #         # pdb.set_trace()
    #         draw_boarder_cell(r=row_index, c=0)
    #         draw_boarder_cell(r=row_index, c=column_max)
    #     for col_index in range(column_max):
    #         draw_boarder_cell(r=0, c=col_index)
    #         draw_boarder_cell(r=row_max, c=col_index)
