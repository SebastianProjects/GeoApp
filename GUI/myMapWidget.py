from GUI.canvasDraw import Rectangle, DrawableObject
from tkintermapview import TkinterMapView
from geopy.geocoders import Nominatim
import customtkinter
from tkinter import messagebox
from geopy.exc import GeocoderUnavailable
from tkintermapview.canvas_button import CanvasButton
from typing_extensions import override


class MyMapWidget(TkinterMapView):
    def __init__(self, master, command, **kwargs):
        self.__canvas_object_list: list[DrawableObject] = []

        super().__init__(master, **kwargs)
        # self.set_address("https://a.tile.openstreetmap.org/{z}/{x}/{y}.png", max_zoom=22)
        self.set_address("Slovakia")

        self.__geolocator: Nominatim = Nominatim(user_agent="Location app for school")
        self.__mouse_coordinates: tuple[float, float] = 0, 0
        self.__option_button = CanvasButton(self, (20, 100), text="O", command=command)
        self.canvas.bind("<Motion>", self.__update_mouse_coordinates)
        self.bind("<Configure>", self.update_dimensions)

    @override
    def draw_initial_array(self):
        super().draw_initial_array()
        for object in self.__canvas_object_list:
            object.draw()

        self.pre_cache_position = (
            round((self.upper_left_tile_pos[0] + self.lower_right_tile_pos[0]) / 2),
            round((self.upper_left_tile_pos[1] + self.lower_right_tile_pos[1]) / 2),
        )

    @override
    def draw_move(self, called_after_zoom: bool = False):
        super().draw_move(called_after_zoom)
        for object in self.__canvas_object_list:
            object.draw(move=not called_after_zoom)

        self.pre_cache_position = (
            round((self.upper_left_tile_pos[0] + self.lower_right_tile_pos[0]) / 2),
            round((self.upper_left_tile_pos[1] + self.lower_right_tile_pos[1]) / 2),
        )

    @override
    def manage_z_order(self):
        super().manage_z_order()
        self.canvas.lift("circle")
        self.canvas.lift("rectangle")
        self.canvas.lift("monitoring_device")
        self.canvas.lift("image")
        self.canvas.lift("square_corner")
        self.canvas.lift("move_circle")

    def __update_mouse_coordinates(self, event):
        self.__mouse_coordinates = self.convert_canvas_coords_to_decimal_coords(
            event.x, event.y
        )

    def set_rectangle(
        self, coordinates_upper_left, coordinates_lower_right, **kwargs
    ) -> Rectangle:
        coordinates_upper_left = tuple(map(float, coordinates_upper_left.split()))
        coordinates_lower_right = tuple(map(float, coordinates_lower_right.split()))
        rectangle = Rectangle(
            self, coordinates_upper_left, coordinates_lower_right, **kwargs
        )
        rectangle.draw()
        self.__canvas_object_list.append(rectangle)
        return rectangle
    
    def append_canvas_object_list(self, shape):
        self.__canvas_object_list.append(shape)

    def delete_all_objects(self):
        for object in self.__canvas_object_list:
            object.delete()
        self.__canvas_object_list.clear()

    def get_mouse_coordinates(self) -> tuple[float, float]:
        return self.__mouse_coordinates

    def __update_coordinates_for_textBox(self, event, textBox: customtkinter.CTkEntry):
        latitude, longitude = self.convert_canvas_coords_to_decimal_coords(
            event.x, event.y
        )
        current_coordinates_as_string = f"{latitude:.7f} {longitude:.7}"
        textBox.delete(0, customtkinter.END)
        textBox.insert(0, current_coordinates_as_string)

    def bind_coordinates_function(self, textBox: customtkinter.CTkEntry):
        self.canvas.bind(
            "<Button-1>",
            lambda event: self.__update_coordinates_for_textBox(event, textBox),
            add=True,
        )

    def unbind_coordinates_function(self):
        self.canvas.unbind("<Button-1>")
        self.canvas.bind("<Button-1>", self.mouse_click)

    def unbind_moving_functions(self):
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<Button-1>")
        self.canvas.unbind("<ButtonRelease-1>")

    def bind_moving_functions_back(self):
        self.canvas.bind("<B1-Motion>", self.mouse_move)
        self.canvas.bind("<Button-1>", self.mouse_click)
        self.canvas.bind("<ButtonRelease-1>", self.mouse_release)

    def search_all_locations(self, location_name: str):
        location_info = None

        try:
            location_info = self.__geolocator.geocode(location_name, exactly_one=False)
        except GeocoderUnavailable:
            messagebox.showwarning("Warning", "There is no internet connection!")

        if location_info:
            locations_with_same_name = [loc for loc in location_info]
            options = []
            for loc in locations_with_same_name:
                address = f"{loc.raw['display_name']}"
                options.append(address)
            return options
        else:
            messagebox.showwarning("Warning", "The location doesn't exist!")

    def go_to_location_address(self, name: str):
        self.set_address(name)

    def change_type_of_map(self, map: str):
        if map == "OpenStreetMap Standard":
            self.set_tile_server("https://tile.openstreetmap.org/{z}/{x}/{y}.png")
        elif map == "OpenStreetMap Humanitarian":
            self.set_tile_server("https://a.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png")

    def get_canvas(self):
        return self.canvas

    def default_zoom_in(self):
        self.set_zoom(self.zoom + 1, relative_pointer_x=0.5, relative_pointer_y=0.5)

    def default_zoom_out(self):
        self.set_zoom(self.zoom - 1, relative_pointer_x=0.5, relative_pointer_y=0.5)

    def get_marker_names(self):
        return [marker.text for marker in self.canvas_marker_list]

    pass
