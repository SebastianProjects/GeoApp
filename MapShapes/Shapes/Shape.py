from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def draw(self):
        pass

class Rectangle(Shape):
    def __init__(self, upper_left_position : tuple[float, float], bottom_right_position : tuple[float, float]):
        self._upper_left_position = upper_left_position
        self._bottom_right_position = bottom_right_position
        
    def draw(self):
        pass
    
class Circle(Shape):
    def __init__(self, center_position : tuple[float, float], radius : float):
        self._center_position = center_position
        
    def draw(self):
        pass
    