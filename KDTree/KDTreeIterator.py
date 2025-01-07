from KDTree.Node import Node
from abc import ABC, abstractmethod
from KDTree.KDTree import KDTree

class KDTreeIterator(ABC):
    def __init__(self, current_node : Node):
        self._current_node = current_node
    
    def __iadd__(self, other):
        pass
    
    def __isub__(self, other):
        pass
    
    def next(self):
        pass
    
    def prev(self):
        pass
    
    def begin(self):
        pass
        
    def end(self):
        pass
    
    def get_current_data(self) -> any:
        if self._current_node == None:
            return None
        return self._current_node.get_data()
    
class InOrderIterator(KDTreeIterator):
    def __init__(self, kdtree : KDTree):
        super().__init__(None)
        self._root = kdtree.get_root()
        self.begin()  # Initialize to the first node

    def __iadd__(self, other):
        self._current_node = self.next()
        return self

    def __isub__(self, other):
        self._current_node = self.prev()
        return self

    def next(self):
        """Move to the next node in in-order traversal."""
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

        return self._current_node

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

        return self._current_node
    