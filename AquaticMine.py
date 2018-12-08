import pygame

DISPLAY_WIDTH = 30
DISPLAY_HEIGHT = 30
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 25, 25)
AQUAMINE_IMG = pygame.image.load("aquamine.png")
AQUAMINE_IMG = pygame.transform.scale(AQUAMINE_IMG, (DISPLAY_WIDTH, DISPLAY_HEIGHT))


class AquaticMine(pygame.sprite.Sprite):
    image = AQUAMINE_IMG

    def __init__(self, x, y, radius):
        # Call the parent class (Sprite) constructor
        super().__init__()

        self.x = x
        self.y = y
        self.radius = radius

        # Fetch the rectangle object that has the dimensions of the image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
