class Door:
    tagged = 0  # After 5 tags, the door opens

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height