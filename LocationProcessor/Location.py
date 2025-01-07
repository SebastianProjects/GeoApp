from LocationProcessor.GPS_position import GPS_position
from abc import ABC
from KDTree.IKey import IKey
from global_values import float_compare_tolerance


class Location(ABC):
    unique_id = 0

    def __init__(
        self,
        unique_id: int = None,
        description: str = "",
        positions: tuple[GPS_position, GPS_position] = None,
    ):
        self.__description: str = description
        self.__positions: tuple[GPS_position, GPS_position] = positions
        if unique_id == None:
            self.__unique_id: int = Location.unique_id
            Location.unique_id += 1
        else:
            self.__unique_id: int = unique_id

    def __eq__(self, other: "Location") -> bool:
        return self.__unique_id == other.__unique_id

    def get_unique_id(self) -> int:
        return self.__unique_id

    def get_description(self) -> str:
        return self.__description

    def get_positions(self) -> tuple[GPS_position, GPS_position]:
        return self.__positions

    def set_description(self, description: str):
        self.__description = description

    def get_full_decsription(self) -> str:
        return f"{self.__description} ({self.__positions[0].get_full_position()}, {self.__positions[1].get_full_position()}) | {self.__unique_id}"


class Land(Location):
    def __init__(
        self,
        unique_id: int = None,
        description: str = "",
        positions: tuple[GPS_position, GPS_position] = None,
        land_number: int = 0,
        real_estate_list: list["Real_estate"] = [],
    ):
        super().__init__(
            unique_id=unique_id, description=description, positions=positions
        )
        self.__land_number: int = land_number
        self.__real_estate_list: list["Real_estate"] = real_estate_list

    def add_real_estate(self, real_estate: "Real_estate"):
        self.__real_estate_list.append(real_estate)

    def add_real_estates(self, real_estates: list["Real_estate"]):
        self.__real_estate_list.extend(real_estates)

    def remove_real_estate(self, real_estate: "Real_estate"):
        for i in range(len(self.__real_estate_list)):
            if self.__real_estate_list[i].get_unique_id() == real_estate.get_unique_id():
                self.__real_estate_list.pop(i)
                break

    def remove_real_estates(self):
        self.__real_estate_list = []

    def get_real_estate_list(self):
        return self.__real_estate_list

    def get_land_number(self) -> int:
        return self.__land_number

    def set_land_number(self, land_number: int):
        self.__land_number = land_number

    def get_full_decsription(self) -> str:
        return f"LAND {self.__land_number} -> {super().get_full_decsription()}"


class Land_Prop(Land):
    def __init__(
        self,
        unique_id: int = None,
        description: str = "",
        positions: tuple[GPS_position, GPS_position] = None,
        land_number: int = 0,
        real_estate_list: list["Real_estate"] = [],
    ):
        super().__init__(
            unique_id=unique_id,
            description=description,
            positions=positions,
            land_number=land_number,
            real_estate_list=real_estate_list,
        )


class Real_estate(Location):
    def __init__(
        self,
        unique_id: int = None,
        description: str = "",
        positions: tuple[GPS_position, GPS_position] = None,
        real_estate_number: int = 0,
        land_list: list["Land"] = [],
    ):
        super().__init__(
            unique_id=unique_id, description=description, positions=positions
        )
        self.__real_estate_number: int = real_estate_number
        self.__land_list: list["Land"] = land_list

    def add_land(self, land: Land):
        self.__land_list.append(land)

    def add_lands(self, lands: list[Land]):
        self.__land_list.extend(lands)

    def remove_land(self, land: Land):
        for i in range(0, len(self.__land_list)):
            if self.__land_list[i].get_unique_id() == land.get_unique_id():
                self.__land_list.pop(i)
                break

    def remove_lands(self):
        self.__land_list = []

    def get_land_list(self) -> list[Land]:
        return self.__land_list

    def get_real_estate_number(self) -> int:
        return self.__real_estate_number

    def get_full_decsription(self) -> str:
        return f"REAL ESTATE {self.__real_estate_number} -> {super().get_full_decsription()}"


class Real_estate_prop(Real_estate):
    def __init__(
        self,
        unique_id: int = None,
        description: str = "",
        positions: tuple[GPS_position, GPS_position] = None,
        real_estate_number: int = 0,
        land_list: list[Land] = [],
    ):
        super().__init__(
            unique_id=unique_id,
            description=description,
            positions=positions,
            real_estate_number=real_estate_number,
            land_list=land_list,
        )


class Location_point(IKey):
    def __init__(self, location: Location = None, position: GPS_position = None):
        self.__location: Location = location
        self.__position: GPS_position = position

    def __eq__(self, other: "Location_point"):
        return self.__location == other.__location

    def compare(self, dimension: int, other_location_point: "Location_point"):
        if (
            abs(
                self.__position.get_position()[0]
                - other_location_point.get_position().get_position()[0]
            )
            < float_compare_tolerance
            and abs(
                self.__position.get_position()[1]
                - other_location_point.get_position().get_position()[1]
            )
            < float_compare_tolerance
        ):
            return 0
        elif (
            self.__position.get_position()[dimension]
            < other_location_point.get_position().get_position()[dimension]
        ):
            return -1

        else:
            return 1

    def set_position(self, position: GPS_position):
        self.__position = position

    def set_location(self, location: Location):
        self.__location = location

    def get_location(self) -> Location:
        return self.__location

    def get_position(self) -> GPS_position:
        return self.__position
