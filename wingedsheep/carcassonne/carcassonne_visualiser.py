import os

from PIL import ImageTk, Image, ImageDraw
from tkinter import PhotoImage, NW, CENTER
from wingedsheep.carcassonne.base_visualiser import BaseVisualiser
from wingedsheep.carcassonne.carcassonne_game_state import CarcassonneGameState
from wingedsheep.carcassonne.objects.meeple_position import MeeplePosition
from wingedsheep.carcassonne.objects.meeple_type import MeepleType
from wingedsheep.carcassonne.objects.tile import Tile


class CarcassonneVisualiser(BaseVisualiser):

    def draw_game_state(self, game_state: CarcassonneGameState):
        self.canvas.delete('all')
        self.draw_tiles(game_state=game_state)
        self.draw_meeples(game_state=game_state)
        self.canvas.update()

    def draw_tiles(self, game_state: CarcassonneGameState):
        for row_index, row in enumerate(game_state.board):
            for column_index, tile in enumerate(row):
                tile: Tile
                if tile is not None:
                    self.__draw_tile(
                        column_index, row_index, tile, game_state.board_player[row_index][column_index].id())

    def draw_meeples(self, game_state: CarcassonneGameState):
        for player, placed_meeples in enumerate(game_state.placed_meeples):
            meeple_position: MeeplePosition
            for meeple_position in placed_meeples:
                self.__draw_meeple(player, meeple_position)

    def __draw_meeple(self, player_index: int, meeple_position: MeeplePosition):
        image = self.__get_meeple_image(player=player_index, meeple_type=meeple_position.meeple_type)

        if meeple_position.meeple_type == MeepleType.BIG:
            x = meeple_position.coordinate_with_side.coordinate.column * self.tile_size \
                + self.big_meeple_position_offsets[meeple_position.coordinate_with_side.side][0]
            y = meeple_position.coordinate_with_side.coordinate.row * self.tile_size \
                + self.big_meeple_position_offsets[meeple_position.coordinate_with_side.side][1]
        else:
            x = meeple_position.coordinate_with_side.coordinate.column * self.tile_size \
                + self.meeple_position_offsets[meeple_position.coordinate_with_side.side][0]
            y = meeple_position.coordinate_with_side.coordinate.row * self.tile_size \
                + self.meeple_position_offsets[meeple_position.coordinate_with_side.side][1]

        self.canvas.create_image(
            x,
            y,
            anchor=CENTER,
            image=image
        )

    def __draw_tile(self, column_index: int, row_index: int, tile: Tile, player_index: int):
        image_filename = tile.image
        reference = f"{image_filename}_{str(tile.turns)}_{row_index}_{column_index}"
        photo_image: PhotoImage
        if reference in self.tile_image_refs:
            photo_image = self.tile_image_refs[reference]
        else:
            abs_file_path = os.path.join(self.images_path, image_filename)
            image = Image.open(abs_file_path).resize((self.tile_size, self.tile_size), Image.ANTIALIAS).rotate(
                -90 * tile.turns)
            height = image.height
            width = image.width
            crop_width = max(0, width - height) / 2
            crop_height = max(0, height - width) / 2
            image.crop((crop_width, crop_height, crop_width, crop_height))
            ImageDraw.Draw(image).text(
                xy=(10, 10),
                text=str((row_index, column_index,)),
                fill=(255, 255, 255, 255),
            )

            player_colour: Image = Image.new(
                mode="RGBA",
                size=self.tile_xy,
                color=self.player_colour[player_index]
            )

            photo_image = ImageTk.PhotoImage(
                image=Image.blend(im1=image, im2=player_colour, alpha=0.25)
            )
            self.tile_image_refs[reference] = photo_image

        self.canvas.create_image(
            column_index * self.tile_size,
            row_index * self.tile_size,
            anchor=NW,
            image=photo_image)

    def __get_meeple_image(self, player: int, meeple_type: MeepleType):
        reference = f"{str(player)}_{str(meeple_type)}"

        if reference in self.meeple_image_refs:
            return self.meeple_image_refs[reference]

        icon_type = MeepleType.NORMAL
        if meeple_type == MeepleType.ABBOT:
            icon_type = meeple_type

        image_filename = self.meeple_icons[icon_type][player]
        abs_file_path = os.path.join(self.images_path, image_filename)

        image: Image = Image.open(abs_file_path)
        photo_image: ImageTk = None
        if meeple_type == MeepleType.NORMAL or meeple_type == MeepleType.ABBOT:
            image_resize: Image = image.resize((self.meeple_size, self.meeple_size), Image.ANTIALIAS)
            photo_image = ImageTk.PhotoImage(image_resize)
        elif meeple_type == MeepleType.BIG:
            image_resize: Image = image.resize((self.big_meeple_size, self.big_meeple_size), Image.ANTIALIAS)
            photo_image = ImageTk.PhotoImage(image_resize)
        elif meeple_type == MeepleType.FARMER:
            image_resize: Image = image.resize((self.meeple_size, self.meeple_size), Image.ANTIALIAS)
            photo_image = ImageTk.PhotoImage(image_resize.rotate(-90))
        elif meeple_type == MeepleType.BIG_FARMER:
            image_resize: Image = image.resize((self.big_meeple_size, self.big_meeple_size), Image.ANTIALIAS)
            photo_image = ImageTk.PhotoImage(image_resize.rotate(-90))
        else:
            print(f"ERROR LOADING IMAGE {abs_file_path}!")
            exit(1)

        self.meeple_image_refs[f"{str(player)}_{str(meeple_type)}"] = photo_image
        return photo_image
