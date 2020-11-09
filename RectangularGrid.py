class RectangularGrid():
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = [[0 for i in range(width)] for j in range(height)]
