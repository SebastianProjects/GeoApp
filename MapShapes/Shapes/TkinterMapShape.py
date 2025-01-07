from MapShapes.Shapes.Shape import Rectangle, Circle
from tkintermapview.utility_functions import decimal_to_osm

class TkinterMapRectangle(Rectangle):
    def __init__(self, 
                 map_widget, 
                 left_upper_position, 
                 right_bottom_position
                 ):
        super().__init__(left_upper_position, right_bottom_position)
        
        self._mmw = map_widget
        self._position_list: list[tuple[float, float]] = [] 
        self._command = None
        self._outline_color = 'red'
        self._border_width = 2
        self._position_list = [left_upper_position, right_bottom_position]
        self._drawable_object_canvas_positions: list[tuple[float, float]] = []
       
        self._deleted: bool = False
        self._rectangle : any = None
        
        self._last_upper_left_tile_pos = None
        self._last_position_list_length = len(self._position_list)

    def draw(self, move=False):
        widget_tile_width = (
            self._mmw.lower_right_tile_pos[0] - self._mmw.upper_left_tile_pos[0]
        )
        widget_tile_height = (
            self._mmw.lower_right_tile_pos[1] - self._mmw.upper_left_tile_pos[1]
        )

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

        if self._rectangle is None:
            self._mmw.get_canvas().delete(self._rectangle)
            self._rectangle = self._mmw.get_canvas().create_rectangle(
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
                    self._rectangle, "<Enter>", self._mouse_enter
                )
                self._mmw.get_canvas().tag_bind(
                    self._rectangle, "<Leave>", self._mouse_leave
                )
                self._mmw.get_canvas().tag_bind(
                    self._rectangle, "<Button-1>", self._click
                )
        else:
            self._mmw.get_canvas().coords(
                self._rectangle, self._drawable_object_canvas_positions
            )
            
    def _get_canvas_pos(self, position, widget_tile_width, widget_tile_height):
        tile_position = decimal_to_osm(*position, round(self._mmw.zoom))

        canvas_pos_x = (
            (tile_position[0] - self._mmw.upper_left_tile_pos[0]) / widget_tile_width
        ) * self._mmw.width
        canvas_pos_y = (
            (tile_position[1] - self._mmw.upper_left_tile_pos[1]) / widget_tile_height
        ) * self._mmw.height

        return canvas_pos_x, canvas_pos_y
            

class TkinterMapCircle(Circle):
    def __init__(self, canvas, x, y, radius):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.radius = radius

    def draw(self):
        self.canvas.create_oval(self.x - self.radius, self.y - self.radius,
                                self.x + self.radius, self.y + self.radius, fill="red")