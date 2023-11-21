import pygame
import random

class BalasEnemigos(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('imagenes/shootEnemyImagePNG.png').convert_alpha()
        self.image = pygame.transform.rotate(self.image, 180)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.y = random.randrange(10, width)
        self.velocidad_y = 4
    
    def update(self):
        self.rect.y += self.velocidad_y
        if self.rect.bottom > height:
            self.kill()