from MapShapes.Shapes.Shape import Shape

class PILRectangle(Shape):
    def __init__(self, image_draw, x, y):
        self.image_draw = image_draw
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def draw(self):
        self.image_draw.rectangle([self.x, self.y, self.x + self.width, self.y + self.height], fill="blue")

class PILCircle(Shape):
    def __init__(self, image_draw, x, y, radius):
        self.image_draw = image_draw
        self.x = x
        self.y = y
        self.radius = radius

    def draw(self):
        self.image_draw.ellipse([self.x - self.radius, self.y - self.radius,
                                 self.x + self.radius, self.y + self.radius], fill="red")