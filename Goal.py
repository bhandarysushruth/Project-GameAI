class Goal:
    tagged = 0  # After 5 tags, the player loses

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height