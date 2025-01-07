from matplotlib import pyplot as plt
from MapShapes.Shapes.Shape import Shape

class MatplotlibRectangle(Shape):
    def __init__(self, ax, x, y, width, height):
        self.ax = ax
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def draw(self):
        self.ax.add_patch(plt.Rectangle((self.x, self.y), self.width, self.height, color="blue"))

class MatplotlibCircle(Shape):
    def __init__(self, ax, x, y, radius):
        self.ax = ax
        self.x = x
        self.y = y
        self.radius = radius

    def draw(self):
        self.ax.add_patch(plt.Circle((self.x, self.y), self.radius, color="red"))