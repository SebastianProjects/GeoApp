from KDTree.Node import Node
from typing import Callable
from abc import ABC, abstractmethod


class KDTree:
    """
    KDTree data structure which can handle duplicate data.
    """

    def __init__(self, dimension: int):
        """
        Creates KDTree.
        Args:
            dimension (int): dimension of the tree
        """
        self._root: Node = None
        self.__k: int = dimension
        self.__size = 0

    def __len__(self) -> int:
        """
        Size of KDTree
        Returns:
            self.__size (int): size of KDTree
        """
        size = 0

        def add_to_size(data: any):
            nonlocal size
            size += 1

        self.level_order(add_to_size)

        return size

    def rand(self, number: int) -> any:
        """
        Gets node that is at the given position in lever order
        Args:
            number (int): index of the node to get
        Returns:
            node (any): node at the given index
        """
        random_data = None

        position = 0

        def get_data(data: any):
            nonlocal random_data, position
            if position == number:
                random_data = data
                return
            position += 1

        self.level_order(get_data)

        return random_data

    def insert(self, data: any):
        """
        Inserts data into the tree.
        Args:
            data (any): data to insert
        """
        if self._root is None:
            self._root = Node(data=data, left=None, right=None, parent=None, k=0)
            self.__size += 1
            return

        current_node = self._root

        current_k = 0

        while True:
            result = data.compare(current_k, current_node.get_data())
            parent_node = current_node

            if result == 1:
                if current_node.get_right() == None:
                    current_node.set_right(
                        Node(
                            data=data,
                            left=None,
                            right=None,
                            parent=parent_node,
                            k=(current_k + 1) % self.__k,
                        )
                    )
                    self.__size += 1
                    break

                parent_node = current_node
                current_node = current_node.get_right()

            else:
                if current_node.get_left() == None:
                    current_node.set_left(
                        Node(
                            data=data,
                            left=None,
                            right=None,
                            parent=parent_node,
                            k=(current_k + 1) % self.__k,
                        )
                    )
                    self.__size += 1
                    break

                parent_node = current_node
                current_node = current_node.get_left()
            current_k = (current_k + 1) % self.__k

    def find(self, data: any) -> list[any]:
        """
        Finds data in the tree.
        Args:
            data (any): data to find
        Returns:
            data_found (list[any]): list of found data
        """
        current_node = self._root
        level = 0
        data_found: any = []

        current_k = 0

        while current_node != None:
            result = data.compare(current_k, current_node.get_data())

            if result == -1:
                current_node = current_node.get_left()
            elif result == 0:
                data_found.append(current_node.get_data())
                current_node = current_node.get_left()
            else:
                current_node = current_node.get_right()
            current_k = (current_k + 1) % self.__k

        return data_found

    def edit(self, prev_data: any, current_data: any):
        """
        Edits data in tree with given data.
        Args:
            prev_data (any): data to be changed
            current_data (any): data to change
        """
        current_node = self._root

        current_k = 0

        while current_node != None:
            result = prev_data.compare(current_k, current_node.get_data())

            if result == -1:
                current_node = current_node.get_left()
            elif result == 0:
                if prev_data == current_node.get_data():
                    break
                current_node = current_node.get_left()
            else:
                current_node = current_node.get_right()
            current_k = (current_k + 1) % self.__k

        if current_node == None:
            return

        if prev_data.compare(0, current_data) == 0:
            current_node.set_data(current_data)
        else:
            self.delete(current_node.get_data())
            self.insert(current_data)

    def delete(self, data: any) -> any:
        """
        Deletes node with given data.
        Args:
            data (any): data to delete
        Returns:
            deleted data (any): deleted data
        """
        current_node = self._root
        deleted_data = None
        colliding_nodes = []
        colliding_nodes_to_add = []

        current_k = 0

        while current_node != None:
            result = data.compare(current_k, current_node.get_data())

            if result == 1:
                current_node = current_node.get_right()
            elif result == 0 and data == current_node.get_data():
                deleted_data = data
                break
            else:
                current_node = current_node.get_left()

            current_k = (current_k + 1) % self.__k

        if current_node == None:
            return

        # mazanie node
        while current_node != None or colliding_nodes:
            if current_node == None:
                current_node = colliding_nodes.pop()
                while current_node in colliding_nodes_to_add:
                    if len(colliding_nodes) == 0:
                        current_node = None
                        break
                    current_node = colliding_nodes.pop()
                colliding_nodes_to_add.append(current_node)

            # pokial je ako list tak ju vymazem
            if self.__is_leaf(current_node):
                if not current_node.get_parent():
                    self._root = None
                elif self.__is_left_child(current_node):
                    current_node.get_parent().set_left(None)
                else:
                    current_node.get_parent().set_right(None)

                self.__size -= 1
                current_node = None

            # hladam jej mahradu bud ako min alebo max
            elif current_node.get_left() == None:
                new_node = self.__find_min(
                    current_node=current_node.get_right(),
                    k=current_node.get_k(),
                )
                # colliding_data su kolidujuce, duplikaty novej node podla k kluca v pravom podstrome current node
                colliding_nodes += self.__find_colliding_nodes(
                    current_node.get_right(), new_node, current_node.get_k()
                )
                self.__switch_nodes(current_node, new_node)

            else:
                new_node = self.__find_max(
                    current_node=current_node.get_left(),
                    k=current_node.get_k(),
                )
                self.__switch_nodes(current_node, new_node)

        for node in colliding_nodes_to_add:
            self.insert(node.get_data())

        return deleted_data

    def level_order(self, lambda_func: Callable[[any], None]):
        """
        Level order traversal.
        Args:
            lambda_func (Callable[[any], None]): lambda function that executes on each node
        """
        if self._root is None:
            return

        # queue pre nespracovane vrcholy
        queue: list[Node] = [self._root]

        while queue:
            current_node = queue.pop(0)
            lambda_func(current_node.get_data())

            if current_node.get_left() != None:
                queue.append(current_node.get_left())
            if current_node.get_right() != None:
                queue.append(current_node.get_right())

    def __find_colliding_nodes(
        self, current_node: Node, colliding_node: Node, k: int
    ) -> list[Node]:
        """
        Helper method for finding colliding nodes.
        Args:
            current_node (Node): current node from which to start the search
            colliding_node (Node): node to compare with
            k (int): dimension to compare on
        Returns:
            colliding_nodes (list[Node]): list of colliding nodes
        """
        if current_node == None:
            return None

        colliding_nodes: list[any] = []
        base_node = colliding_node

        stack = []
        while current_node != None or stack:
            # prejde do lava az po list
            if current_node != None:
                stack.append(current_node)
                current_node = current_node.get_left()
            # spracuje seba a prejde doprava
            else:
                current_node = stack.pop()

                if (
                    current_node.get_data().compare(k, colliding_node.get_data()) == -1
                    or current_node.get_data().compare(k, colliding_node.get_data())
                    == 0
                ) and current_node != base_node:
                    colliding_nodes.append(current_node)

                if current_node.get_k() == k:
                    current_node = None
                    continue

                current_node = current_node.get_right()

        return colliding_nodes

    def __find_min(self, current_node: Node, k: int) -> Node:
        """
        Helper method for finding min node of subtree.
        Args:
            current_node (Node): current node from which to start the search
            k (int): dimension to compare on
        Returns:
            max_node (Node): min node of subtree
        """
        if current_node == None:
            return None

        min_node = current_node
        i = 0
        stack = []
        while current_node != None or stack:
            if current_node != None:
                stack.append(current_node)
                current_node = current_node.get_left()
            else:
                current_node = stack.pop()
                i += 1
                if (
                    min_node == None
                    or current_node.get_data().compare(k, min_node.get_data()) == -1
                ):
                    min_node = current_node

                if current_node.get_k() == k:
                    current_node = None
                    continue
                current_node = current_node.get_right()

        return min_node

    def __find_max(self, current_node: Node, k: int) -> Node:
        """
        Helper method for finding max node of subtree.
        Args:
            current_node (Node): current node from which to start the search
            k (int): dimension to compare on
        Returns:
            max_node (Node): max node of subtree
        """
        if current_node == None:
            return None

        i = 0
        max_node = current_node

        stack = []
        while current_node != None or stack:
            if current_node != None:
                stack.append(current_node)

                if current_node.get_k() == k:
                    current_node = None
                    continue

                current_node = current_node.get_left()
            else:
                current_node = stack.pop()
                i += 1

                if (
                    max_node == None
                    or current_node.get_data().compare(k, max_node.get_data()) == 1
                ):
                    max_node = current_node

                current_node = current_node.get_right()

        return max_node

    def __switch_nodes(self, node1: Node, node2: Node):
        """
        Switches two nodes.
        Args:
            node1 (Node): first node to be switched
            node2 (Node): second node to be switched
        """
        node1_left = node1.get_left()
        node1.set_left(node2.get_left())
        node2.set_left(node1_left)

        if node1.get_left():
            node1.get_left().set_parent(node1)
        if node2.get_left():
            node2.get_left().set_parent(node2)

        node1_right = node1.get_right()
        node1.set_right(node2.get_right())
        node2.set_right(node1_right)

        if node1.get_right():
            node1.get_right().set_parent(node1)
        if node2.get_right():
            node2.get_right().set_parent(node2)

        node1_parent = node1.get_parent()
        node1.set_parent(node2.get_parent())
        node2.set_parent(node1_parent)

        if node1.get_parent():
            if node1.get_parent().get_left() == node2:
                node1.get_parent().set_left(node1)
            else:
                node1.get_parent().set_right(node1)
        else:
            self._root = node1
        if node2.get_parent():
            if node2.get_parent().get_left() == node1:
                node2.get_parent().set_left(node2)
            else:
                node2.get_parent().set_right(node2)
        else:
            self._root = node2

        node1_k = node1.get_k()
        node1.set_k(node2.get_k())
        node2.set_k(node1_k)

    def __is_leaf(self, node: Node) -> bool:
        """
        Helper method for checking if node is leaf.
        Args:
            node (Node): node to check
        Returns:
            bool: true if node is leaf and false otherwise
        """
        return node.get_left() == None and node.get_right() == None

    def __is_left_child(self, node: Node) -> bool:
        """
        Helper method for checking if node is left child.
        Args:
            node (Node): node to check
        Returns:
            bool: true if node is left child and false otherwise
        """
        if node == None or node.get_parent() == None:
            return False
        return node.get_parent().get_left() == node

class KDTreeIterator(ABC):
    def __init__(self, current_node : Node):
        self._current_node = current_node

    def next(self):
        pass
    
    def prev(self):
        pass
    
    def get_current_data(self) -> any:
        if self._current_node == None:
            return None
        return self._current_node.get_data()
    
class InOrderIterator(KDTreeIterator):
    def __init__(self, kdtree : KDTree):
        self._root = kdtree._root
        super().__init__(self.__begin())

    def next(self):
        if not self._current_node:
            return None

        if self._current_node.right:
            self._current_node = self._current_node.right
            while self._current_node.left:
                self._current_node = self._current_node.left
        else:
            while self._current_node.parent and self._current_node == self._current_node.parent.right:
                self._current_node = self._current_node.parent
            self._current_node = self._current_node.parent
    
    def prev(self):
        if not self._current_node:
            return None

        if self._current_node.left:
            self._current_node = self._current_node.left
            while self._current_node.right:
                self._current_node = self._current_node.right
        else:
            while self._current_node.parent and self._current_node == self._current_node.parent.left:
                self._current_node = self._current_node.parent
            self._current_node = self._current_node.parent
    
    def __begin(self):
        self._current_node = self._root
        if not self._current_node:
            return None

        while self._current_node.left:
            self._current_node = self._current_node.left

        return self._current_node

    """ def end(self):
        self._current_node = self._root
        if not self._current_node:
            return None

        while self._current_node.right:
            self._current_node = self._current_node.right

        return self._current_node """

class PreOrderIterator(KDTreeIterator):
    def __init__(self, kdtree : KDTree):
        self._root = kdtree._root
        super().__init__(self.__begin())

    def next(self):
        if not self._current_node:
            return None

        if self._current_node.left:
            self._current_node = self._current_node.left
        elif self._current_node.right:
            self._current_node = self._current_node.right
        else:
            while self._current_node.parent and self._current_node == self._current_node.parent.right:
                self._current_node = self._current_node.parent
            self._current_node = self._current_node.parent
    
    def prev(self):
        if not self._current_node:
            return None

        if self._current_node.parent and self._current_node == self._current_node.parent.right:
            self._current_node = self._current_node.parent
        elif self._current_node.parent and self._current_node == self._current_node.parent.left:
            self._current_node = self._current_node.parent
        else:
            self._current_node = self._current_node.right
            while self._current_node.right:
                self._current_node = self._current_node.right

    def __begin(self):
        self._current_node = self._root
        return self._current_node