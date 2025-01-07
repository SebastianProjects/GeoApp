from global_values import float_compare_tolerance


class GPS_position:
    def __init__(
        self,
        lat_position: float = 0,
        lat_direction: str = "N",
        lon_position: float = 0,
        lon_direction: str = "E",
    ):
        self.__lat_position: float = lat_position
        self.__lat_direction: str = lat_direction
        self.__lon_position: float = lon_position
        self.__lon_direction: str = lon_direction

    def __eq__(self, other: "GPS_position") -> bool:
        return (
            abs(self.__lat_position - other.__lat_position) < float_compare_tolerance
            and self.__lat_direction == other.__lat_direction
            and abs(self.__lon_position - other.__lon_position)
            < float_compare_tolerance
            and self.__lon_direction == other.__lon_direction
        )

    def get_position(self) -> tuple:
        lat = self.__lat_position
        lon = self.__lon_position
        if self.__lat_direction == "S":
            lat = -(self.__lat_position)
        if self.__lon_direction == "W":
            lon = -(self.__lon_position)
        return (lat, lon)

    def get_lat_position(self) -> float:
        return self.__lat_position

    def get_lat_direction(self) -> str:
        return self.__lat_direction

    def get_lon_position(self) -> float:
        return self.__lon_position

    def get_lon_direction(self) -> str:
        return self.__lon_direction

    def get_full_position(self) -> str:
        return f"({self.__lat_position}°{self.__lat_direction}, {self.__lon_position}°{self.__lon_direction})"
