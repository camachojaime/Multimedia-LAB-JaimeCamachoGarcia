import pygame
import random

class Jugador(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('imagenes/naveDefault.jpg').convert_alpha()
        pygame.display.set_icon(self.image)
        self.rect = self.image.get_rect()
        self.rect.centerx = width//2
        self.rect.centery = height-50
        self.velocidad_X = 0
        self.vida = 100

    def update(self):
        self.velocidad_X = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.velocidad_X = -5
        elif keystate[pygame.K_RIGHT]:
            self.velocidad_X = 5
    
        self.rect.x +=self.velocidad_X
        if self.rect.right > width:
            self.rect.right = width
        elif self.rect.left < 0:
            self.rect.left = 0
    
    def disparar(self):
        bala = Balas(self.rect.centerx, self.rect.top)
        grupo_jugador.add(bala)
        grupo_balas_jugador.add(bala)
        shootDefault.play()