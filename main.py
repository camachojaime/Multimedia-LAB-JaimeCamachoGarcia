from typing import Any
import pygame
import random

from pygame.sprite import _Group

pygame.init()
pygame.mixer.init()

fondo = pygame.image.load('imagenes/fondo.png')

shootDefault = pygame.mixer.Sound('audio/shootDefault.mp3')
shootEnemy = pygame.mixer.Sound('audio/shootEnemy.mp3')

width = fondo.get_width()
height = fondo.get_height()
window = pygame.display.set_mode((width, height))
pygame.display.set_caption('display1')

run = True

fps = 60
clock = pygame.time.Clock()
score = 0
vida = 100
blanco = (255,255,255)
negro = (0,0,0)

def textoPuntuacion(frame, text, size, x, y):
    font = pygame.font.SysFont('Consolas', size, bold=True)
    textFrame = font.render(text, True, blanco, negro)
    textRect = textFrame.get_rect()
    textRect.midtop = (x,y)
    frame.blit(textFrame, textRect)


def barraVida(frame, x, y, nivel):
    longitud = 100
    alto = 20
    fill = int((nivel/100)*longitud)
    border = pygame.Rect(x, y, logitud, alto)
    fill = pygame.Rect(x, y, fill, alto)
    pygame.draw.rect(frame, (255,0,55), fill)
    pygame.draw.rect(frame, negro, border, 4)


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

class Balas(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('imagenes/shootDefaultImage.png')
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.y = y
        self.velocidad = -18

    def update(self):
        self.rect.y += self.velocidad
        if self.rect.bottom < 0:
            self.kill()


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


# class Explosion(pygame.sprite.Sprite):
#     def __init__(self, position):
#         super().__init__()
#         self.image = Explosion_list[0]
#         img_scala = pygame.transform.scale(self.image, (20,20))
#         self.rect = img_scala.get_rect()
#         self.rect.center = position
#         self.time = pygame.time.get_ticks()
#         self.velocidad_explo = 30
#         self.frames = 0
    
#     def update(self):
#         tiempo = pygame.time.get_ticks()
#         if tiempo - self.time > self.velocidad_explo:
#             self.time = tiempo
#             self.frames += 1
#             if self.frames == len(explosion_list):
#                 self.kill()
#             else:
#                 position = self.rect.center
#                 self.image = Explosion_list[self.frames]
#                 self.rect = self.image.get_rect()
#                 self.rect.center = position


grupo_jugador = pygame.sprite.Group()
grupo_enemigos = pygame.sprite.Group()
grupo_balas_jugador = pygame.sprite.Group()
grupo_balas_enemigos = pygame.sprite.Group()

player = Jugador()
grupo_jugador.add(player)
grupo_balas_jugador.add(player)

for x in range(10):
    enemigo = Enemys(10,10)
    grupo_enemigos.add(enemigo)
    grupo_jugador.add(enemigo)

while run:
    clock.tick(fps)
    window.blit(fondo, (0,0))

    for event in pygame.event.get()
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.disparar()

    grupo_jugador.update()
    grupo_enemigos.update()
    grupo_balas_jugador.update()
    grupo_balas_enemigos.update()

    grupo_jugador.draw(window)

    

