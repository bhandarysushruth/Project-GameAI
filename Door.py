import pygame

WIDTH = 60
HEIGHT = 60
GATE_IMG = pygame.image.load("gate.png")
GATE_IMG = pygame.transform.scale(GATE_IMG, (WIDTH, HEIGHT))


class Door(pygame.sprite.Sprite):
    """ Represents the outer gate to the castle. Five tags by an enemy soldier forces the gate to open """
    image = GATE_IMG
    offset = WIDTH + 20

    def __init__(self, x, y):
        # Call the parent class (Sprite) constructor
        super().__init__()

        # Fetch the rectangle object that has the dimensions of the image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

