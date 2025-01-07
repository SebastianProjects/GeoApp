from abc import ABC, abstractmethod
import tkinter as tk
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt
from MapShapes.Shapes.MatplotlibShape import MatplotlibRectangle, MatplotlibCircle
from MapShapes.Shapes.PILMapShape import PILRectangle, PILCircle
from MapShapes.Shapes.TkinterMapShape import TkinterMapRectangle, TkinterMapCircle
from GUI.myMapWidget import MyMapWidget

class ShapeFactory(ABC):
    @abstractmethod
    def create_rectangle(self, left_upper_position: tuple[float, float], right_bottom_position: tuple[float, float]):
        pass

    @abstractmethod
    def create_circle(self, center_position: tuple[float, float], radius: float):
        pass


class TkinterMapShapeFactory(ShapeFactory):
    def __init__(self, map_widget):
        self.__map_widget : MyMapWidget = map_widget

    def create_rectangle(self, left_upper_position: tuple[float, float],
                         right_bottom_position: tuple[float, float]):
        map_rectangle = TkinterMapRectangle(self.__map_widget,
                                            left_upper_position,
                                            right_bottom_position)
        self.__map_widget.append_canvas_object_list(map_rectangle)
        return map_rectangle

    def create_circle(self, center_position: tuple[float, float],
                      radius: float):
        map_circle = TkinterMapCircle(self.__map_widget,
                                      center_position,
                                      radius)
        self.__map_widget.append_canvas_object_list(map_circle)
        return map_circle


class PILShapeFactory(ShapeFactory):
    def __init__(self, image_draw):
        self.image_draw = image_draw

    def create_rectangle(self, left_upper_position: tuple[float, float], right_bottom_position: tuple[float, float]):
        return PILRectangle(self.image_draw, left_upper_position, right_bottom_position)

    def create_circle(self, center_position: tuple[float, float], radius: float):
        return PILCircle(self.image_draw, center_position, radius)


class MatplotlibShapeFactory(ShapeFactory):
    def __init__(self, ax):
        self.ax = ax

    def create_rectangle(self, left_upper_position: tuple[float, float], right_bottom_position: tuple[float, float]):
        return MatplotlibRectangle(self.ax, left_upper_position, right_bottom_position)

    def create_circle(self, center_position: tuple[float, float], radius: float):
        return MatplotlibCircle(self.ax, center_position, radius)


"""      
root = tk.Tk()
canvas = tk.Canvas(root, width=500, height=500)
canvas.pack()

tk_factory = TkinterMapShapeFactory(canvas)
rect = tk_factory.create_rectangle(50, 50, 100, 200)
circle = tk_factory.create_circle(300, 300, 50)

rect.draw()
circle.draw()
root.mainloop()

# PIL Example
image = Image.new("RGB", (500, 500), "white")
draw = ImageDraw.Draw(image)

pil_factory = PILShapeFactory(draw)
rect = pil_factory.create_rectangle(50, 50, 100, 200)
circle = pil_factory.create_circle(300, 300, 50)

rect.draw()
circle.draw()
image.show()

# Matplotlib Example
fig, ax = plt.subplots()
ax.set_xlim(0, 500)
ax.set_ylim(0, 500)

mpl_factory = MatplotlibShapeFactory(ax)
rect = mpl_factory.create_rectangle(50, 50, 100, 200)
circle = mpl_factory.create_circle(300, 300, 50)

rect.draw()
circle.draw()
plt.gca().set_aspect('equal', adjustable='box')
plt.show()
 """
