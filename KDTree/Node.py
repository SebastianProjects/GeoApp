from KDTree.IKey import IKey


class Node:
    def __init__(
        self,
        data: IKey,
        left: "Node" = None,
        right: "Node" = None,
        parent: "Node" = None,
        k: int = 0,
    ):
        self.__data: IKey = data
        self.__left: Node = left
        self.__right: Node = right
        self.__parent: Node = parent
        self.__k: int = k

    def set_data(self, data: IKey):
        self.__data = data

    def set_parent(self, parent: "Node"):
        self.__parent = parent

    def set_k(self, k: int):
        self.__k = k

    def set_left(self, left: "Node" = None):
        self.__left = left

    def set_right(self, right: "Node" = None):
        self.__right = right

    def get_data(self) -> IKey:
        return self.__data

    def get_parent(self) -> "Node":
        return self.__parent

    def get_k(self) -> int:
        return self.__k

    def get_left(self) -> "Node":
        return self.__left

    def get_right(self) -> "Node":
        return self.__right
