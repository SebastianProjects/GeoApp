import string
from LocationProcessor.Location import (
    Real_estate,
    Land,
    Location,
    Land_Prop,
    Real_estate_prop,
    Location_point,
)
from LocationProcessor.GPS_position import GPS_position
from KDTree.KDTree import KDTree
from typing import Literal, Union
import random


class Location_router:
    """
    Location router where you can find, insert, edit and delete real estates and lands.
    """

    def __init__(self):
        self.__lands: KDTree[Location_point] = KDTree(dimension=2)
        self.__real_estates: KDTree[Location_point] = KDTree(dimension=2)
        self.__all: KDTree[Location_point] = KDTree(dimension=2)

    def find_location(
        self,
        location_type: Literal["l", "re", "b"] = None,
        lat_position1: float = None,
        lat_direction1: str = None,
        lon_position1: float = None,
        lon_direction1: str = None,
        lat_position2: float = None,
        lat_direction2: str = None,
        lon_position2: float = None,
        lon_direction2: str = None,
    ) -> Union[Land_Prop, Real_estate_prop]:
        """
        Find location type based on the given coordinates.
        Args:
            location_type (Literal["l", "re", "b"]): l for land, re for real estate and b for both
            lat_position1 (float): left upper latitude position
            lat_direction1 (str): left upper latitude direction
            lon_position1 (float): left upper longitude position
            lon_direction1 (str): left upper longitude direction
            lat_position2 (float): right lower latitude position
            lat_direction2 (str): right lower latitude direction
            lon_position2 (float): right lower longitude position
            lon_direction2 (str): right lower longitude direction
        Returns:
            props Union[Land_Prop, Real_estate_prop]: found props
        """
        props: list[Union[Land_Prop, Real_estate_prop]] = []

        locations = self.__find_location(
            location_type=location_type,
            lat_position1=lat_position1,
            lat_direction1=lat_direction1,
            lon_position1=lon_position1,
            lon_direction1=lon_direction1,
            lat_position2=lat_position2,
            lat_direction2=lat_direction2,
            lon_position2=lon_position2,
            lon_direction2=lon_direction2,
        )

        if location_type == "b":
            for location in locations:
                if isinstance(location, Land):
                    props.append(
                        self.__create_location_prop(
                            location_type="l", location=location, hasReferences=True
                        )
                    )
                else:
                    props.append(
                        self.__create_location_prop(
                            location_type="re", location=location, hasReferences=True
                        )
                    )
        else:
            for location in locations:
                props.append(
                    self.__create_location_prop(
                        location_type=location_type,
                        location=location,
                        hasReferences=True,
                    )
                )

        return props

    def get_all_locations(self) -> list[Union[Land_Prop, Real_estate_prop]]:
        """
        Get all locations.
        Returns:
            props list[Union[Land_Prop, Real_estate_prop]]: all props
        """
        props: list[Union[Land_Prop, Real_estate_prop]] = []

        def get_location(location_point: Location_point):
            location = location_point.get_location()
            if location_point.get_position() == location.get_positions()[0]:
                if isinstance(location, Land):
                    props.append(
                        self.__create_location_prop(
                            location_type="l", location=location, hasReferences=True
                        )
                    )

                else:
                    props.append(
                        self.__create_location_prop(
                            location_type="re", location=location, hasReferences=True
                        )
                    )

        self.__all.level_order(get_location)

        return props

    def insert_location(
        self,
        location_type: Literal["l", "re"] = "l",
        number: int = "None",
        description: str = "None",
        left_upper_lat_position: float = "None",
        left_upper_lat_direction: str = "None",
        left_upper_lon_position: float = "None",
        left_upper_lon_direction: str = "None",
        right_lower_lat_position: float = "None",
        right_lower_lat_direction: str = "None",
        right_lower_lon_position: float = "None",
        right_lower_lon_direction: str = "None",
    ):
        """
        Insert location type based on the given coordinates.
        Args:
            location_type (Literal["l", "re"]): l for land and re for real estate
            number (int): location number
            description (str): location description
            left_upper_lat_position (float): left upper latitude position
            left_upper_lat_direction (str): left upper latitude direction
            left_upper_lon_position (float): left upper longitude position
            left_upper_lon_direction (str): left upper longitude direction
            right_lower_lat_position (float): right lower latitude position
            right_lower_lat_direction (str): right lower latitude direction
            right_lower_lon_position (float): right lower longitude position
            right_lower_lon_direction (str): right lower longitude direction
        """
        self.__insert_location(
            location_type=location_type,
            number=number,
            description=description,
            left_upper_lat_position=left_upper_lat_position,
            left_upper_lat_direction=left_upper_lat_direction,
            left_upper_lon_position=left_upper_lon_position,
            left_upper_lon_direction=left_upper_lon_direction,
            right_lower_lat_position=right_lower_lat_position,
            right_lower_lat_direction=right_lower_lat_direction,
            right_lower_lon_position=right_lower_lon_position,
            right_lower_lon_direction=right_lower_lon_direction,
        )

    def edit_location(
        self,
        location_type: Literal["l", "re"] = "l",
        prev_prop: Union[Land_Prop, Real_estate_prop] = "None",
        number: int = "None",
        description: str = "None",
        left_upper_lat_position: float = "None",
        left_upper_lat_direction: str = "None",
        left_upper_lon_position: float = "None",
        left_upper_lon_direction: str = "None",
        right_lower_lat_position: float = "None",
        right_lower_lat_direction: str = "None",
        right_lower_lon_position: float = "None",
        right_lower_lon_direction: str = "None",
    ):
        """
        Edit existing location type.
        Args:
            location_type (Literal["l", "re"]): l for land and re for real estate
            prev_prop (Union[Land_Prop, Real_estate_prop]): previous existing location prop
            number (int): location number
            description (str): location description
            left_upper_lat_position (float): left upper latitude position
            left_upper_lat_direction (str): left upper latitude direction
            left_upper_lon_position (float): left upper longitude position
            left_upper_lon_direction (str): left upper longitude direction
            right_lower_lat_position (float): right lower latitude position
            right_lower_lat_direction (str): right lower latitude direction
            right_lower_lon_position (float): right lower longitude position
            right_lower_lon_direction (str): right lower longitude direction
        """
        prev_position1 = GPS_position(
            lat_position=prev_prop.get_positions()[0].get_lat_position(),
            lat_direction=prev_prop.get_positions()[0].get_lat_direction(),
            lon_position=prev_prop.get_positions()[0].get_lon_position(),
            lon_direction=prev_prop.get_positions()[0].get_lon_direction(),
        )

        prev_position2 = GPS_position(
            lat_position=prev_prop.get_positions()[1].get_lat_position(),
            lat_direction=prev_prop.get_positions()[1].get_lat_direction(),
            lon_position=prev_prop.get_positions()[1].get_lon_position(),
            lon_direction=prev_prop.get_positions()[1].get_lon_direction(),
        )

        current_position1 = GPS_position(
            lat_direction=left_upper_lat_direction,
            lat_position=left_upper_lat_position,
            lon_direction=left_upper_lon_direction,
            lon_position=left_upper_lon_position,
        )
        current_position2 = GPS_position(
            lat_direction=right_lower_lat_direction,
            lat_position=right_lower_lat_position,
            lon_direction=right_lower_lon_direction,
            lon_position=right_lower_lon_position,
        )

        prev_location = None
        current_location = None
        if location_type == "l":

            prev_location = Land(
                unique_id=prev_prop.get_unique_id(),
                land_number=prev_prop.get_land_number(),
                description=prev_prop.get_description(),
                positions=(prev_position1, prev_position2),
            )

            current_location = Land(
                unique_id=prev_prop.get_unique_id(),
                land_number=number,
                description=description,
                positions=(current_position1, current_position2),
            )
        else:
            prev_location = Real_estate(
                unique_id=prev_prop.get_unique_id(),
                real_estate_number=prev_prop.get_real_estate_number(),
                description=prev_prop.get_description(),
                positions=(prev_position1, prev_position2),
            )

            current_location = Real_estate(
                unique_id=prev_prop.get_unique_id(),
                real_estate_number=number,
                description=description,
                positions=(current_position1, current_position2),
            )

        prev_location_point1 = Location_point(
            location=prev_location, position=prev_position1
        )
        prev_location_point2 = Location_point(
            location=prev_location, position=prev_position2
        )
        current_location_point1 = Location_point(
            location=current_location, position=current_position1
        )
        current_location_point2 = Location_point(
            location=current_location, position=current_position2
        )

        if location_type == "l":
            self.__lands.edit(
                prev_data=prev_location_point1, current_data=current_location_point1
            )
            self.__lands.edit(
                prev_data=prev_location_point2, current_data=current_location_point2
            )

            prev_colliding_real_estates = self.__real_estates.find(prev_location_point1)
            prev_colliding_real_estates += self.__real_estates.find(prev_location_point2)

            colliding_real_estates = self.__real_estates.find(current_location_point1)
            colliding_real_estates += self.__real_estates.find(current_location_point2)

            current_location.remove_real_estates()
            
            for prev_colliding_real_estate in prev_colliding_real_estates:
                prev_colliding_real_estate.get_location().remove_land(prev_location)
            
            for colliding_real_estate in colliding_real_estates:
                current_location.add_real_estate(colliding_real_estate.get_location())
                colliding_real_estate.get_location().add_land(current_location)

        else:
            self.__real_estates.edit(
                prev_data=prev_location_point1, current_data=current_location_point1
            )
            self.__real_estates.edit(
                prev_data=prev_location_point2, current_data=current_location_point2
            )

            prev_colliding_lands = self.__real_estates.find(prev_location_point1)
            prev_colliding_lands += self.__real_estates.find(prev_location_point2)
            
            colliding_lands = self.__lands.find(current_location_point1)
            colliding_lands += self.__lands.find(current_location_point2)

            current_location.remove_lands()
            
            for prev_colliding_land in prev_colliding_lands:
                prev_colliding_land.get_location().remove_land(prev_location)
            
            for colliding_land in colliding_lands:
                current_location.add_land(colliding_land.get_location())
                colliding_land.get_location().remove_real_estate(prev_location)
                colliding_land.get_location().add_real_estate(current_location)

        self.__all.edit(
            prev_data=prev_location_point1, current_data=current_location_point1
        )
        self.__all.edit(
            prev_data=prev_location_point2, current_data=current_location_point2
        )
            
            

    def delete_location(
        self,
        location_type: Literal["l", "re"],
        prop: Union[Land_Prop, Real_estate_prop],
    ):
        """
        Delete exsisting location type.
        Args:
            location_type (Literal["l", "re"]): l for land and re for real estate
            prop (Union[Land_Prop, Real_estate_prop]): existing location prop
        """
        positions = prop.get_positions()

        if location_type == "l":
            land = Land(
                unique_id=prop.get_unique_id(),
                land_number=prop.get_land_number(),
                description=prop.get_description(),
                positions=positions,
            )

            location_point_left_upper = Location_point(
                location=land, position=positions[0]
            )
            location_point_right_lower = Location_point(
                location=land, position=positions[1]
            )

            colliding_real_estates = self.__find_location(
                location_type="re",
                lat_position1=land.get_positions()[0].get_lat_position(),
                lat_direction1=land.get_positions()[0].get_lat_direction(),
                lon_position1=land.get_positions()[0].get_lon_position(),
                lon_direction1=land.get_positions()[0].get_lon_direction(),
            )

            colliding_real_estates += self.__find_location(
                location_type="re",
                lat_position1=land.get_positions()[1].get_lat_position(),
                lat_direction1=land.get_positions()[1].get_lat_direction(),
                lon_position1=land.get_positions()[1].get_lon_position(),
                lon_direction1=land.get_positions()[1].get_lon_direction(),
            )

            if colliding_real_estates:
                for colliding_real_estate in colliding_real_estates:
                    colliding_real_estate.remove_land(land)

            self.__lands.delete(location_point_left_upper)
            self.__lands.delete(location_point_right_lower)

        elif location_type == "re":
            real_estate = Real_estate(
                unique_id=prop.get_unique_id(),
                real_estate_number=prop.get_real_estate_number(),
                description=prop.get_description(),
                positions=positions,
            )

            location_point_left_upper = Location_point(
                location=real_estate, position=positions[0]
            )
            location_point_right_lower = Location_point(
                location=real_estate, position=positions[1]
            )

            colliding_lands = self.__find_location(
                location_type="l",
                lat_position1=real_estate.get_positions()[0].get_lat_position(),
                lat_direction1=real_estate.get_positions()[0].get_lat_direction(),
                lon_position1=real_estate.get_positions()[0].get_lon_position(),
                lon_direction1=real_estate.get_positions()[0].get_lon_direction(),
            )

            colliding_lands += self.__find_location(
                location_type="l",
                lat_position1=real_estate.get_positions()[1].get_lat_position(),
                lat_direction1=real_estate.get_positions()[1].get_lat_direction(),
                lon_position1=real_estate.get_positions()[1].get_lon_position(),
                lon_direction1=real_estate.get_positions()[1].get_lon_direction(),
            )

            if colliding_lands:
                for colliding_land in colliding_lands:
                    colliding_land.remove_real_estate(real_estate)

            self.__real_estates.delete(location_point_left_upper)
            self.__real_estates.delete(location_point_right_lower)

        else:
            raise ValueError("Invalid type!")

        self.__all.delete(location_point_left_upper)
        self.__all.delete(location_point_right_lower)

    def delete_all_locations(self):
        """
        Delete all locations.
        """
        self.__lands = KDTree(dimension=2)
        self.__real_estates = KDTree(dimension=2)
        self.__all = KDTree(dimension=2)
        Location.unique_id = 0

    def save_locations_to_csv(self, filename: str = "lands.csv"):
        """
        Save all lands to csv file.
        Args:
            filename (str): path to csv file
        """
        with open(filename, mode="w", newline="") as file:
            file.write(
                "Type,Unique id,Land number,Description,Left upper lat position,Left upper lat direction,Left upper lon position,Left upper lon direction,Right lower lat position,Right lower lat direction,Right lower lon position,Right lower lon direction\n"
            )
            
            has_been_saved = [None] * Location.unique_id

            def write_land(location_point: Location_point):
                location: Location = location_point.get_location()
                unique_id = int(location.get_unique_id())
                location_type = "re"
                number = 0

                if isinstance(location, Land):
                    location_type = "l"
                    number = location.get_land_number()
                else:
                    number = location.get_real_estate_number()

                if not has_been_saved[location.get_unique_id()]:
                    
                    has_been_saved[location.get_unique_id()] = f"{location_type},{unique_id},{number},{location.get_description()},{location.get_positions()[0].get_lat_position()},{location.get_positions()[0].get_lat_direction()},{location.get_positions()[0].get_lon_position()},{location.get_positions()[0].get_lon_direction()},{location.get_positions()[1].get_lat_position()},{location.get_positions()[1].get_lat_direction()},{location.get_positions()[1].get_lon_position()},{location.get_positions()[1].get_lon_direction()}\n"

            self.__all.level_order(write_land)
            for i in range(Location.unique_id):
                if has_been_saved[i]:
                    file.write(has_been_saved[i])

    def load_locations_from_csv(self, filename: str = "lands.csv"):
        """
        Loads all locations from csv file.
        Args:
            filename (str): path to csv file
        """
        with open(filename, mode="r") as file:
            next(file)

            highest_id = Location.unique_id

            for line in file:
                row = line.strip().split(",")
                unique_id = int(row[1]) + Location.unique_id
                if row[0] == "l":
                    self.__insert_location(
                        unique_id=unique_id,
                        location_type="l",
                        number=int(row[2]),
                        description=row[3],
                        left_upper_lat_position=float(row[4]),
                        left_upper_lat_direction=row[5],
                        left_upper_lon_position=float(row[6]),
                        left_upper_lon_direction=row[7],
                        right_lower_lat_position=float(row[8]),
                        right_lower_lat_direction=row[9],
                        right_lower_lon_position=float(row[10]),
                        right_lower_lon_direction=row[11],
                    )
                else:
                    self.__insert_location(
                        unique_id=unique_id,
                        location_type="re",
                        number=int(row[2]),
                        description=row[3],
                        left_upper_lat_position=float(row[4]),
                        left_upper_lat_direction=row[5],
                        left_upper_lon_position=float(row[6]),
                        left_upper_lon_direction=row[7],
                        right_lower_lat_position=float(row[8]),
                        right_lower_lat_direction=row[9],
                        right_lower_lon_position=float(row[10]),
                        right_lower_lon_direction=row[11],
                    )

                if unique_id > highest_id:
                    highest_id = unique_id

            Location.unique_id = highest_id + 1

    def generate_locations(
        self, locations_count: int = 0, prob_of_colliding: float = 0.2
    ):
        """
        Generates and inserts random locations.
        Args:
            locations_count (int): number of locations to insert
            prob_of_colliding (float): colliding probability
        """
        for i in range(locations_count):
            location_point = None
            location = None
            location_type = ""

            if random.randint(0, 1) == 0:
                if len(self.__lands) == 0:
                    location_point = self.__lands.rand(random.randint(0, len(self.__lands)))
                else:
                    location_point = self.__lands.rand(random.randint(0, len(self.__lands) - 1))
                
                if location_point:
                    location = location_point.get_location()

                location_type = "re"

            else:
                if len(self.__real_estates) == 0:
                    location_point = self.__real_estates.rand(
                        random.randint(0, len(self.__real_estates))
                    )
                else:
                    location_point = self.__real_estates.rand(
                        random.randint(0, len(self.__real_estates) -1 )
                    )
                    
                if location_point:
                    location = location_point.get_location()

                location_type = "l"

            number = random.randint(0, 100000)
            description = "".join(random.choices(string.ascii_letters, k=10))
            left_upper_lat_position = random.uniform(0, 85)
            left_upper_lat_direction = random.choice(["N", "S"])
            left_upper_lon_position = random.uniform(0, 175)
            left_upper_lon_direction = random.choice(["E", "W"])
            right_lower_lat_position = random.uniform(0, 85)
            right_lower_lat_direction = random.choice(["N", "S"])
            right_lower_lon_position = random.uniform(0, 175)
            right_lower_lon_direction = random.choice(["E", "W"])

            if random.random() < prob_of_colliding and location:

                if random.randint(0, 1) == 0:
                    location_position = location.get_positions()[0]
                    left_upper_lat_position = location_position.get_lat_position()
                    left_upper_lat_direction = location_position.get_lat_direction()
                    left_upper_lon_position = location_position.get_lon_position()
                    left_upper_lon_direction = location_position.get_lon_direction()

                else:
                    location_position = location.get_positions()[1]
                    right_lower_lat_position = location_position.get_lat_position()
                    right_lower_lat_direction = location_position.get_lat_direction()
                    right_lower_lon_position = location_position.get_lon_position()
                    right_lower_lon_direction = location_position.get_lon_direction()

            self.__insert_location(
                location_type=location_type,
                number=number,
                description=description,
                left_upper_lat_position=left_upper_lat_position,
                left_upper_lat_direction=left_upper_lat_direction,
                left_upper_lon_position=left_upper_lon_position,
                left_upper_lon_direction=left_upper_lon_direction,
                right_lower_lat_position=right_lower_lat_position,
                right_lower_lat_direction=right_lower_lat_direction,
                right_lower_lon_position=right_lower_lon_position,
                right_lower_lon_direction=right_lower_lon_direction,
            )

    def __insert_location(
        self,
        unique_id: int = None,
        location_type: Literal["l", "re"] = "l",
        number: int = "None",
        description: str = "None",
        left_upper_lat_position: float = "None",
        left_upper_lat_direction: str = "None",
        left_upper_lon_position: float = "None",
        left_upper_lon_direction: str = "None",
        right_lower_lat_position: float = "None",
        right_lower_lat_direction: str = "None",
        right_lower_lon_position: float = "None",
        right_lower_lon_direction: str = "None",
    ):
        """
        Helper function for inserting location.
        Args:
            unique_id (int): location unique id
            location_type (Literal["l", "re"]): l for land and re for real estate
            number (int): location number
            description (str): location description
            left_upper_lat_position (float): left upper latitude position
            left_upper_lat_direction (str): left upper latitude direction
            left_upper_lon_position (float): left upper longitude position
            left_upper_lon_direction (str): left upper longitude direction
            right_lower_lat_position (float): right lower latitude position
            right_lower_lat_direction (str): right lower latitude direction
            right_lower_lon_position (float): right lower longitude position
            right_lower_lon_direction (str): right lower longitude direction
        """
        if (
            location_type == "None"
            or number == "None"
            or description == "None"
            or left_upper_lat_position == "None"
            or left_upper_lat_direction == "None"
            or left_upper_lon_position == "None"
            or left_upper_lon_direction == "None"
            or right_lower_lat_position == "None"
            or right_lower_lat_direction == "None"
            or right_lower_lon_position == "None"
            or right_lower_lon_direction == "None"
        ):
            print(
                f"Location type: {location_type}\n Number: {number}\n Description: {description}\n Left upper lat position: {left_upper_lat_position}\n Left upper lat direction: {left_upper_lat_direction}\n Left upper lon position: {left_upper_lon_position}\n Left upper lon direction: {left_upper_lon_direction}\n Right lower lat position: {right_lower_lat_position}\n Right lower lat direction: {right_lower_lat_direction}\n Right lower lon position: {right_lower_lon_position}\n Right lower lon direction: {right_lower_lon_direction}"
            )
            raise ValueError("Invalid parameters!")

        else:
            left_upper_position = GPS_position(
                lat_direction=left_upper_lat_direction,
                lat_position=left_upper_lat_position,
                lon_direction=left_upper_lon_direction,
                lon_position=left_upper_lon_position,
            )
            right_lower_position = GPS_position(
                lat_direction=right_lower_lat_direction,
                lat_position=right_lower_lat_position,
                lon_direction=right_lower_lon_direction,
                lon_position=right_lower_lon_position,
            )

            if location_type == "l":
                colliding_real_estates = self.__find_location(
                    location_type="re",
                    lat_position1=left_upper_lat_position,
                    lat_direction1=left_upper_lat_direction,
                    lon_position1=left_upper_lon_position,
                    lon_direction1=left_upper_lon_direction,
                )
                colliding_real_estates += self.__find_location(
                    location_type="re",
                    lat_position2=right_lower_lat_position,
                    lat_direction2=right_lower_lat_direction,
                    lon_position2=right_lower_lon_position,
                    lon_direction2=right_lower_lon_direction,
                )

                land = Land(
                    unique_id=unique_id,
                    land_number=number,
                    description=description,
                    positions=(left_upper_position, right_lower_position),
                    real_estate_list=colliding_real_estates,
                )

                location_point_left_upper = Location_point(
                    location=land, position=left_upper_position
                )
                location_point_right_lower = Location_point(
                    location=land, position=right_lower_position
                )

                for colliding_real_estate in colliding_real_estates:
                    colliding_real_estate.add_land(land)

                self.__lands.insert(location_point_left_upper)
                self.__lands.insert(location_point_right_lower)
                self.__all.insert(location_point_left_upper)
                self.__all.insert(location_point_right_lower)

            elif location_type == "re":
                colliding_lands = self.__find_location(
                    location_type="l",
                    lat_position1=left_upper_lat_position,
                    lat_direction1=left_upper_lat_direction,
                    lon_position1=left_upper_lon_position,
                    lon_direction1=left_upper_lon_direction,
                )
                colliding_lands += self.__find_location(
                    location_type="l",
                    lat_position2=right_lower_lat_position,
                    lat_direction2=right_lower_lat_direction,
                    lon_position2=right_lower_lon_position,
                    lon_direction2=right_lower_lon_direction,
                )

                real_estate = Real_estate(
                    unique_id=unique_id,
                    real_estate_number=number,
                    description=description,
                    positions=(left_upper_position, right_lower_position),
                    land_list=colliding_lands,
                )

                location_point_left_upper = Location_point(
                    location=real_estate, position=left_upper_position
                )
                location_point_right_lower = Location_point(
                    location=real_estate, position=right_lower_position
                )

                for colliding_land in colliding_lands:
                    colliding_land.add_real_estate(real_estate)

                self.__real_estates.insert(location_point_left_upper)
                self.__real_estates.insert(location_point_right_lower)
                self.__all.insert(location_point_left_upper)
                self.__all.insert(location_point_right_lower)

            else:
                raise ValueError("Invalid type!")

    def __create_location_prop(
        self,
        location_type: Literal["l", "re"],
        location: Union[Land, Real_estate],
        hasReferences: bool = False,
    ) -> Union[Land_Prop, Real_estate_prop]:
        """
        Helper function for creating location prop.
        Args:
            location_type (Literal["l", "re"]): l for land and re for real estate
            location (Union[Land, Real_estate]): location to be tranformed to prop
            hasReferences (bool): has references on other locations
        """
        location_position1, location_position2 = location.get_positions()
        position1 = GPS_position(
            lat_position=location_position1.get_lat_position(),
            lat_direction=location_position1.get_lat_direction(),
            lon_position=location_position1.get_lon_position(),
            lon_direction=location_position1.get_lon_direction(),
        )
        position2 = GPS_position(
            lat_position=location_position2.get_lat_position(),
            lat_direction=location_position2.get_lat_direction(),
            lon_position=location_position2.get_lon_position(),
            lon_direction=location_position2.get_lon_direction(),
        )

        if hasReferences:
            if location_type == "l":
                colliding_real_estates = location.get_real_estate_list()
                colliding_real_estates_props = []
                if colliding_real_estates:
                    for colliding_real_estate in colliding_real_estates:
                        colliding_real_estates_props.append(
                            self.__create_location_prop(
                                location_type="re",
                                location=colliding_real_estate,
                                hasReferences=False,
                            )
                        )

                return Land_Prop(
                    unique_id=location.get_unique_id(),
                    description=location.get_description(),
                    positions=(position1, position2),
                    land_number=location.get_land_number(),
                    real_estate_list=colliding_real_estates_props,
                )

            elif location_type == "re":
                colliding_lands = location.get_land_list()
                colliding_lands_props = []
                if colliding_lands:
                    for colliding_land in colliding_lands:
                        colliding_lands_props.append(
                            self.__create_location_prop(
                                location_type="l",
                                location=colliding_land,
                                hasReferences=False,
                            )
                        )
                return Real_estate_prop(
                    unique_id=location.get_unique_id(),
                    description=location.get_description(),
                    positions=(position1, position2),
                    real_estate_number=location.get_real_estate_number(),
                    land_list=colliding_lands_props,
                )

            else:
                raise ValueError("Invalid location type!")

        else:
            if location_type == "l":
                return Land_Prop(
                    unique_id=location.get_unique_id(),
                    description=location.get_description(),
                    positions=(position1, position2),
                    land_number=location.get_land_number(),
                )

            elif location_type == "re":
                return Real_estate_prop(
                    unique_id=location.get_unique_id(),
                    description=location.get_description(),
                    positions=(position1, position2),
                    real_estate_number=location.get_real_estate_number(),
                )

            else:
                raise ValueError("Invalid location type!")

    def __create_location(
        self,
        location_type: Literal["l", "re"],
        location: Union[Land_Prop, Real_estate_prop],
        hasReferences: bool = False,
    ):
        """
        Helper function for creating location from prop.
        Args:
            location_type (Literal["l", "re"]): l for land and re for real estate
            location (Union[Land_Prop, Real_estate_prop]): location prop to be tranformed to location
            hasReferences (bool): has references on other locations
        """
        location_position1, location_position2 = location.get_positions()
        position1 = GPS_position(
            lat_position=location_position1.get_lat_position(),
            lat_direction=location_position1.get_lat_direction(),
            lon_position=location_position1.get_lon_position(),
            lon_direction=location_position1.get_lon_direction(),
        )
        position2 = GPS_position(
            lat_position=location_position2.get_lat_position(),
            lat_direction=location_position2.get_lat_direction(),
            lon_position=location_position2.get_lon_position(),
            lon_direction=location_position2.get_lon_direction(),
        )

        if hasReferences:
            if location_type == "l":
                colliding_real_estates = location.get_real_estate_list()
                colliding_real_estates_props = []
                if colliding_real_estates:
                    for colliding_real_estate in colliding_real_estates:
                        colliding_real_estates_props.append(
                            self.__create_location(
                                location_type="re",
                                location=colliding_real_estate,
                                hasReferences=False,
                            )
                        )

                return Land(
                    unique_id=location.get_unique_id(),
                    description=location.get_description(),
                    positions=(position1, position2),
                    land_number=location.get_land_number(),
                    real_estate_list=colliding_real_estates_props,
                )

            elif location_type == "re":
                colliding_lands = location.get_land_list()
                colliding_lands_props = []
                if colliding_lands:
                    for colliding_land in colliding_lands:
                        colliding_lands_props.append(
                            self.__create_location(
                                location_type="l",
                                location=colliding_land,
                                hasReferences=False,
                            )
                        )
                return Real_estate(
                    unique_id=location.get_unique_id(),
                    description=location.get_description(),
                    positions=(position1, position2),
                    real_estate_number=location.get_real_estate_number(),
                    land_list=colliding_lands_props,
                )

            else:
                raise ValueError("Invalid location type!")

        else:
            if location_type == "l":
                return Land(
                    unique_id=location.get_unique_id(),
                    description=location.get_description(),
                    positions=(position1, position2),
                    land_number=location.get_land_number(),
                )

            elif location_type == "re":
                return Real_estate(
                    unique_id=location.get_unique_id(),
                    description=location.get_description(),
                    positions=(position1, position2),
                    real_estate_number=location.get_real_estate_number(),
                )

            else:
                raise ValueError("Invalid location type!")

    def __find_location(
        self,
        location_type: Literal["l", "re", "b"] = None,
        lat_position1: int = None,
        lat_direction1: str = None,
        lon_position1: int = None,
        lon_direction1: str = None,
        lat_position2: int = None,
        lat_direction2: str = None,
        lon_position2: int = None,
        lon_direction2: str = None,
    ) -> list[Location]:
        """
        Helper function for finding location.
        Args:
            location_type (Literal["l", "re", "b"]): l for land, re for real estate and b for both
            lat_position1 (int): latitude position
            lat_direction1 (str): latitude direction
            lon_position1 (int): longitude position
            lon_direction1 (str): longitude direction
            lat_position2 (int): latitude position
            lat_direction2 (str): latitude direction
            lon_position2 (int): longitude position
            lon_direction2 (str): longitude direction
        Returns:
            locations list[Location]: locations
        """
        locations: list[Union[Land_Prop, Real_estate_prop]] = []

        if (
            location_type == "b"
            and lat_position1
            and lat_direction1
            and lon_position1
            and lon_direction1
            and lat_position2
            and lat_direction2
            and lon_position2
            and lon_direction2
        ):

            position1: GPS_position = GPS_position(
                lat_position=lat_position1,
                lat_direction=lat_direction1,
                lon_position=lon_position1,
                lon_direction=lon_direction1,
            )
            position2: GPS_position = GPS_position(
                lat_position=lat_position2,
                lat_direction=lat_direction2,
                lon_position=lon_position2,
                lon_direction=lon_direction2,
            )

            location_point1 = Location_point(position=position1)
            location_point2 = Location_point(position=position2)
            location_points = self.__all.find(location_point1)
            location_points += self.__all.find(location_point2)

            for location_point in location_points:
                if (
                    location_point.get_position()
                    == location_point.get_location().get_positions()[0]
                ):
                    locations.append(location_point.get_location())

        elif (
            lat_position1 and lat_direction1 and lon_position1 and lon_direction1
        ) or (lat_position2 and lat_direction2 and lon_position2 and lon_direction2):
            if lat_position1 and lat_direction1 and lon_position1 and lon_direction1:
                position: GPS_position = GPS_position(
                    lat_position=lat_position1,
                    lat_direction=lat_direction1,
                    lon_position=lon_position1,
                    lon_direction=lon_direction1,
                )
            else:
                position: GPS_position = GPS_position(
                    lat_position=lat_position2,
                    lat_direction=lat_direction2,
                    lon_position=lon_position2,
                    lon_direction=lon_direction2,
                )

            location_point: Location_point = Location_point(position=position)
            location_points: list[Location_point] = None

            if location_type == "b":
                raise ValueError("Missing position!")

            elif location_type == "l":
                location_points = self.__lands.find(location_point)
                for location_point in location_points:
                    locations.append(location_point.get_location())

            elif location_type == "re":
                location_points = self.__real_estates.find(location_point)
                for location_point in location_points:
                    locations.append(location_point.get_location())

            else:
                raise ValueError("Invalid type!")

        else:
            raise ValueError("Invalid position!")
        return locations
