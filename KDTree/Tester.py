from KDTree.KDTree import KDTree
from KDTree.IKey import IKey
from global_values import float_compare_tolerance
import random
import string
import time


class Tester:
    def __init__(self):
        self.__kdtree: KDTree[Test_data] = KDTree(dimension=2)
        self.__k = 2
        self.__test_data: list[Test_data] = []
        self.__seed = random.randint(0, 1000000)
        random.seed(self.__seed)

    def insert_for_performance(
        self, replication_count: int = 0, step_size: int = 0, step_count: int = 0
    ) -> tuple:
        data_count_list = []
        average_time_list = []
        operation_count = 0

        for i in range(step_count):
            average_time_per_step = 0
            operation_count += step_size
            data_count_list.append(operation_count)

            for j in range(replication_count):
                self.__kdtree: KDTree = KDTree(dimension=2)
                total_time = 0

                for i in range(operation_count):
                    generated_data = Test_data()
                    start_time = time.perf_counter()
                    self.__kdtree.insert(generated_data)
                    end_time = time.perf_counter()
                    total_time += end_time - start_time

                average_time_per_step += total_time / operation_count

            average_time_list.append(average_time_per_step / replication_count)

        return (data_count_list, average_time_list)

    def insert(self, operation_count: int = 0) -> str:
        data_str = ""
        total_time = 0

        for i in range(operation_count):
            if random.randint(0, 5) == 0:
                if self.__test_data:
                    generated_data = random.choice(self.__test_data)
                    generated_data = Test_data(
                        position=(
                            generated_data.get_position()[0],
                            generated_data.get_position()[1],
                        )
                    )
                else:
                    generated_data = Test_data()
            else:
                generated_data = Test_data()

            self.__test_data.append(generated_data)

            start_time = time.perf_counter()
            self.__kdtree.insert(generated_data)
            end_time = time.perf_counter()

        return f"Inserted {len(self.__test_data)} data\nwhile in KDTree is {len(self.__kdtree)} data in time {total_time}.\n\n{data_str}\n\n"

    def delete(self, operation_count: int = 0):
        print(self.__seed)
        insert_str = self.insert(operation_count=operation_count)
        data_str = ""
        total_time = 0
        deleted_count = 0
        random_data_count = 0

        for i in range(operation_count):
            generate_random_data = random.randint(0, 3)

            if generate_random_data == 0:
                generated_data = Test_data()
                data_str += "R"
                random_data_count += 1
            else:
                generated_data = random.choice(self.__test_data)
                data_str += "L"

            data_deleted_in_list = None
            try:
                self.__test_data.remove(generated_data)
                data_deleted_in_list = generated_data
            except ValueError:
                pass

            start_time = time.perf_counter()
            deleted_data = self.__kdtree.delete(generated_data)
            end_time = time.perf_counter()
            data_str += (
                f"{i + 1}.\n delete -> {generated_data.get_full_description()}\n"
            )

            if deleted_data and data_deleted_in_list:
                deleted_count += 1
                data_str += f"In KDTree {deleted_data.get_full_description()} In list: {data_deleted_in_list.get_full_description()}\n"
            elif deleted_data:
                data_str += "Not found in list\n"
            elif data_deleted_in_list:
                data_str += "Not found in KDTree\n"
            else:
                data_str += "Data not found\n"
            total_time += end_time - start_time

        return f"Deleted {deleted_count} data with {random_data_count} random data in time {total_time}. Size of KDTree is {len(self.__kdtree)} and size of list is {len(self.__test_data)}.\n\n{data_str}\n\n{insert_str}"

    def find(self, operation_count: int = 0):
        self.insert(operation_count=operation_count)
        data_str = ""
        total_time = 0
        random_data_count = 0
        found_count = 0
        found_random_data = 0
        is_random = False

        for i in range(operation_count):
            generate_data = random.randint(0, 3)
            if generate_data == 0:
                generated_data = Test_data()
                data_str += "R"
                random_data_count += 1
                is_random = True
            else:
                generated_data = random.choice(self.__test_data)
                is_random = False

            data_str += f"{i + 1}. FIND:\n{generated_data.get_full_description()}\n"

            start_time = time.perf_counter()
            data_found_in_kdtree = self.__kdtree.find(generated_data)
            end_time = time.perf_counter()

            data_found_in_list = []
            for data in self.__test_data:
                if data.compare(0, generated_data) == 0:
                    data_found_in_list.append(data)

            if len(data_found_in_kdtree) == 0 and len(data_found_in_list) == 0:
                data_str += "Data not found\n"
            elif len(data_found_in_kdtree) == 0:
                data_str += "Not found in KDTree\n"
            elif len(data_found_in_list) == 0:
                data_str += "Not found in list\n"
            else:
                if len(data_found_in_kdtree) != len(data_found_in_list):
                    data_str += f"ERROR -> {len(data_found_in_kdtree)} != {len(data_found_in_list)}\n"
                else:
                    if is_random:
                        found_random_data += 1
                    else:
                        found_count += 1
                    for i in range(len(data_found_in_kdtree)):
                        data_str += f"Found in KDTree: {data_found_in_kdtree[i].get_full_description()} \nFound in list: {data_found_in_list[i].get_full_description()}\n\n"

            total_time += end_time - start_time

        return f"Successfully did {found_count} found operations and did {found_random_data} random found operations with {random_data_count} random data in time {total_time}.\n\n{data_str}\n\n"

    def all(self, operation_count):
        error_count = 0
        insert_count = 0
        find_count = 0
        delete_count = 0
        data_str = ""
        total_time_insert = 0
        total_time_find = 0
        total_time_delete = 0

        self.insert(operation_count=20000)

        start_overall_time = time.perf_counter()
        for i in range(operation_count):
            print(f"{i}-----------------------------------\n")
            random_operation = random.randint(0, 2)
            data_str += f"{i + 1}. "

            if random_operation == 0:
                insert_count += 1

                if random.randint(0, 5) == 0:
                    if self.__test_data:
                        generated_data = random.choice(self.__test_data)
                        generated_data = Test_data(
                            position=(
                                generated_data.get_position()[0],
                                generated_data.get_position()[1],
                            )
                        )
                    else:
                        generated_data = Test_data()
                else:
                    generated_data = Test_data()

                self.__test_data.append(generated_data)

                start_time = time.perf_counter()
                self.__kdtree.insert(generated_data)
                end_time = time.perf_counter()

                data_str += f"INSERT: \n{len(self.__kdtree)}(KDTree) = {len(self.__test_data)}(Datalist)\n"
                total_time_insert += end_time - start_time

            elif random_operation == 1:
                find_count += 1
                data_str += f"FIND: \n"

                if self.__test_data:
                    if random.randint(0, 9) == 0:
                        generated_data = Test_data()
                    else:
                        generated_data = random.choice(self.__test_data)
                else:
                    generated_data = Test_data()

                start_time = time.perf_counter()
                data_found_in_kdtree = self.__kdtree.find(generated_data)
                end_time = time.perf_counter()

                data_found_in_list = []
                for data in self.__test_data:
                    if data.compare(0, generated_data) == 0:
                        data_found_in_list.append(data)

                data_str += f"{len(data_found_in_kdtree)}(KDTree) = {len(data_found_in_list)}(Datalist)\n"
                total_time_find += end_time - start_time
                if len(data_found_in_kdtree) != len(data_found_in_list):
                    error_count += 1
                    data_str += "ERROR\n"
                    print("ERROR\n")
            else:
                delete_count += 1
                data_str += f"DELETE: \n"

                if self.__test_data:
                    if random.randint(0, 9) == 0:
                        generated_data = Test_data()
                    else:
                        generated_data = random.choice(self.__test_data)
                        generated_data = Test_data(
                            name=generated_data.get_name(),
                            position=(
                                generated_data.get_position()[0],
                                generated_data.get_position()[1],
                            ),
                        )
                else:
                    generated_data = Test_data()

                try:
                    self.__test_data.remove(generated_data)
                except ValueError:
                    pass

                start_time = time.perf_counter()
                self.__kdtree.delete(generated_data)
                end_time = time.perf_counter()

                if len(self.__kdtree) != len(self.__test_data):
                    error_count += 1
                    data_str += "ERROR\n"
                    continue

                data_str += f"{len(self.__kdtree)}(KDTree) = {len(self.__test_data)}(Datalist)\n"
                total_time_delete += end_time - start_time

            end_overall_time = time.perf_counter()
            overall_time = end_overall_time - start_overall_time

        if error_count > 0:
            return "error"
            """ print(self.__seed) """

        return f"Errors: {error_count}\nOverall time: {overall_time}.\nInserted {insert_count} in time {total_time_insert}.\nDeleted {delete_count} in time {total_time_delete}.\nFound {find_count} in time {total_time_find}.\n{len(self.__kdtree)}(KDTree) = {len(self.__test_data)}(DataList)\n\n{data_str}"


class Test_data(IKey):

    def __init__(self, name="", position=None):
        if name == "":
            self.__name: str = "".join(random.choices(string.ascii_letters, k=10))
        else:
            self.__name = name
        if position == None:
            self.__position: tuple = (random.randint(1, 50), random.randint(1, 50))
        else:
            self.__position = position

    def __eq__(self, other: "Test_data") -> bool:
        return (
            self.__position[0] == other.get_position()[0]
            and self.__position[1] == other.get_position()[1]
            and self.__name == other.__name
        )

    def compare(self, dimension: int, test_data: "Test_data") -> int:
        if (
            self.__position[0] == test_data.get_position()[0]
            and self.__position[1] == test_data.get_position()[1]
        ):
            return 0
        elif self.__position[dimension] <= test_data.get_position()[dimension]:
            return -1
        else:
            return 1

    def get_name(self) -> str:
        return self.__name

    def get_position(self) -> tuple:
        return self.__position

    def get_full_description(self) -> str:
        return f"[{self.__name} -> ({self.__position[0]}, {self.__position[1]})]"


class Test_data2(IKey):
    def __init__(self):
        # kedze random.choices vracia list, tak ho musim spojit do stringu cez join
        self.__A: float = random.uniform(0, 50)
        self.__B: str = "".join(random.choices(string.ascii_letters, k=5))
        self.__C: int = random.randint(0, 100)
        self.__D: float = random.uniform(0, 50)

    def __eq__(self, other: "Test_data") -> bool:
        return (
            abs((self.__A - other.__A)) < float_compare_tolerance
            and self.__B == other.__B
            and self.__C == other.__C
            and abs((self.__D - other.__D)) < float_compare_tolerance
        )

    def compare(self, dimension: int, test_data: "Test_data") -> int:
        if dimension == 0:
            if abs((self.__A - test_data.__A)) < float_compare_tolerance:
                if self.__B > test_data.__B:
                    return 1
                elif self.__B == test_data.__B:
                    return 0
            elif self.__A < test_data.__A:
                return -1
            else:
                return 1

        elif dimension == 1:
            if self.__C <= test_data.__C:
                if self.__C == test_data.__C:
                    return 0
                return -1
            else:
                return 1

        elif dimension == 2:
            if abs((self.__D - test_data.__D)) < float_compare_tolerance:
                return 0
            elif self.__D < test_data.__D:
                return -1
            else:
                return 1

        else:
            if self.__B <= test_data.__B:
                if self.__B == test_data.__B:
                    if self.__C > test_data.__C:
                        return 1
                    elif self.__C == test_data.__C:
                        return 0
                return -1
            else:
                return 1

    def get_full_description(self) -> str:
        return f"A: {self.__A} B: {self.__B} C: {self.__C} D: {self.__D}"
