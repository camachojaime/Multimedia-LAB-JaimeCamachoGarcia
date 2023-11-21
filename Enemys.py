import pygame
import random

class Enemys(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('imagenes/enemyA.pnf').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(1, width-50)
        self.rect.y = 10
        self.velocidad_y = random.randrange(-5, 20)

    def updat(self):
        self.time = random.randrange(-1, pygame.time.get_ticks()//5000)
        self.rect.x += self.time
        if self.rect.x >= width:
            self.rect.x = 0
            self.rect.y += 50