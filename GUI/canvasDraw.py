import sys
from typing import TYPE_CHECKING, Callable, List, Tuple, Dict
from abc import abstractmethod
from geopy.distance import distance
from PIL import Image, ImageTk
import math
from typing_extensions import override

from tkintermapview.utility_functions import decimal_to_osm
from tkintermapview.canvas_position_marker import CanvasPositionMarker

from shapely.geometry import Point
from shapely.geometry.polygon import Polygon as ShapelyPolygon

if TYPE_CHECKING:
    from myMapWidget import MyMapWidget


class DrawableObject:
    def __init__(
        self,
        mmw: "MyMapWidget",
        outline_color: str = "blue",
        border_width: int = 2,
        fill_color: str = None,
        command: Callable = None,
        name: str = None,
    ):

        self._mmw: "MyMapWidget" = mmw
        self._outline_color: str = outline_color
        self._border_width: int = border_width
        self._fill_color: str = fill_color
        self._command: Callable = command
        self._name: str = name
        self._position_list: List[Tuple[float, float]] = []
        self._drawable_object_canvas_positions: List[Tuple[float, float]] = []
        self._drawable_object: any = None
        self._deleted: bool = False

        self._last_upper_left_tile_pos = None
        self._last_position_list_length = len(self._position_list)

    @abstractmethod
    def draw(move: bool):
        pass

    def delete(self):
        self._mmw.get_canvas().delete(self._drawable_object)

        self._drawable_object = None
        self._deleted = True

    def get_name(self):
        return self._name

    def get_position_list(self):
        return self._position_list

    def _mouse_enter(self, event=None):
        if sys.platform == "darwin":
            self._mmw.get_canvas().config(cursor="pointinghand")
        elif sys.platform.startswith("win"):
            self._mmw.get_canvas().config(cursor="hand2")
        else:
            self._mmw.get_canvas().config(
                cursor="hand2"
            )  # not tested what it looks like on Linux!

    def _mouse_leave(self, event=None):
        self._mmw.get_canvas().config(cursor="arrow")

    def _click(self, event=None):
        if self._command is not None:
            self._command(self)

    def _get_canvas_pos(self, position, widget_tile_width, widget_tile_height):
        tile_position = decimal_to_osm(*position, round(self._mmw.zoom))

        canvas_pos_x = (
            (tile_position[0] - self._mmw.upper_left_tile_pos[0]) / widget_tile_width
        ) * self._mmw.width
        canvas_pos_y = (
            (tile_position[1] - self._mmw.upper_left_tile_pos[1]) / widget_tile_height
        ) * self._mmw.height

        return canvas_pos_x, canvas_pos_y

    def mark_object(self):
        self._mmw.get_canvas().itemconfig(self._drawable_object, outline="red")

    def unmark_object(self):
        self._mmw.get_canvas().itemconfig(
            self._drawable_object, outline=self._outline_color
        )

    @override
    def _click(self, event=None):
        if self._command is not None:
            self._command(self.get_name())

class Rectangle(DrawableObject):
    def __init__(
        self,
        mmw: "MyMapWidget",
        coordinates_upper_left: Tuple[float, float],
        coordinates_lower_right: Tuple[float, float],
        **kwargs
    ):

        super().__init__(mmw=mmw, **kwargs)

        if coordinates_upper_left[0] < coordinates_lower_right[0]:
            c = coordinates_upper_left[0]
            coordinates_upper_left = (
                coordinates_lower_right[0],
                coordinates_upper_left[1],
            )
            coordinates_lower_right = c, coordinates_lower_right[1]

        if coordinates_upper_left[1] > coordinates_lower_right[1]:
            c = coordinates_upper_left[1]
            coordinates_upper_left = (
                coordinates_upper_left[0],
                coordinates_lower_right[1],
            )
            coordinates_lower_right = coordinates_lower_right[0], c

        self._position_list.extend([coordinates_upper_left, coordinates_lower_right])

    def draw(self, move=False):
        # get current tile size of map widget
        widget_tile_width = (
            self._mmw.lower_right_tile_pos[0] - self._mmw.upper_left_tile_pos[0]
        )
        widget_tile_height = (
            self._mmw.lower_right_tile_pos[1] - self._mmw.upper_left_tile_pos[1]
        )

        # if only moving happened and len(self.position_list) did not change, shift current positions, else calculate new position_list
        if move is True and self._last_upper_left_tile_pos is not None:
            x_move = (
                (self._last_upper_left_tile_pos[0] - self._mmw.upper_left_tile_pos[0])
                / widget_tile_width
            ) * self._mmw.width
            y_move = (
                (self._last_upper_left_tile_pos[1] - self._mmw.upper_left_tile_pos[1])
                / widget_tile_height
            ) * self._mmw.height

            for i in range(0, len(self._position_list) * 2, 2):
                self._drawable_object_canvas_positions[i] += x_move
                self._drawable_object_canvas_positions[i + 1] += y_move
        else:
            self._drawable_object_canvas_positions = []
            for position in self._position_list:
                canvas_position = self._get_canvas_pos(
                    position, widget_tile_width, widget_tile_height
                )
                self._drawable_object_canvas_positions.append(canvas_position[0])
                self._drawable_object_canvas_positions.append(canvas_position[1])

        if self._drawable_object is None:
            self._mmw.get_canvas().delete(self._drawable_object)
            self._drawable_object = self._mmw.get_canvas().create_rectangle(
                self._drawable_object_canvas_positions[0],
                self._drawable_object_canvas_positions[1],
                self._drawable_object_canvas_positions[2],
                self._drawable_object_canvas_positions[3],
                width=self._border_width,
                outline=self._outline_color,
                tag="rectangle",
            )

            if self._command is not None:
                self._mmw.get_canvas().tag_bind(
                    self._drawable_object, "<Enter>", self._mouse_enter
                )
                self._mmw.get_canvas().tag_bind(
                    self._drawable_object, "<Leave>", self._mouse_leave
                )
                self._mmw.get_canvas().tag_bind(
                    self._drawable_object, "<Button-1>", self._click
                )
        else:
            self._mmw.get_canvas().coords(
                self._drawable_object, self._drawable_object_canvas_positions
            )
