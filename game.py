from typing import Any
import pygame
import random
import sys, subprocess

from pygame.sprite import Group

pygame.init()
pygame.mixer.init()

skin = sys.argv[1]
fondo = pygame.image.load('imagenes/J-fondo-1920x1080.jpg')

laser_sonido = pygame.mixer.Sound('sound/laser.wav')
explosion_sonido = pygame.mixer.Sound('sound/explosion.wav')
golpe_sonido = pygame.mixer.Sound('sound/golpe.wav')

explosion_list = []
for i in range (1,13):
    explosion = pygame.image.load(f'explosion/{i}.png')
    explosion_list.append(explosion)

width = fondo.get_width()
height = fondo.get_height()
window = pygame.display.set_mode((width, height))
pygame.display.set_caption('SPACE INVADERS')

run = True
fps = 60
clock = pygame.time.Clock()
score = 0
vida = 100
blanco = (255,255,255)
negro = (0,0,0)

def texto_puntuacion(frame, text, size, x, y):
    font = pygame.font.SysFont('Small Fonts', size, bold=True)
    text_frame = font.render(text, True, blanco, negro)
    text_rect = text_frame.get_rect()
    text_rect.midtop = (x,y)
    frame.blit(text_frame, text_rect)

def barra_vida(frame, x, y, nivel):
    longitud = 100
    alto = 20
    fill = int((nivel/100)*longitud)
    border = pygame.Rect(x, y, longitud, alto)
    fill = pygame.Rect(x, y, fill, alto)
    pygame.draw.rect(frame, (255,0,255), fill)
    pygame.draw.rect(frame, negro, border, 4)

class Jugador(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        originalImage = pygame.image.load(skin).convert_alpha()
        self.image = pygame.transform.scale(originalImage, (100, 100))

        pygame.display.set_icon(self.image)
        self.rect = self.image.get_rect()
        self.rect.centerx = width//2
        self.rect.centery = height-200
        self.velocidad_x = 0
        self.vida = 100

    def update(self):
        self.velocidad_x = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.velocidad_x = -5
        elif keystate[pygame.K_RIGHT]:
            self.velocidad_x = 5
        
        self.rect.x += self.velocidad_x
        if self.rect.right > width:
            self.rect.right = width
        elif self.rect.left < 0:
            self.rect.left = 0
        
    def disparar(self):
        bala = Balas(self.rect.centerx, self.rect.top)
        grupo_jugador.add(bala)
        grupo_balas_jugador.add(bala)
        laser_sonido.play()

class Enemigos(pygame.sprite.Sprite):
    def __init__(self, a, b):
        super().__init__()
        originalImage = pygame.image.load('imagenes/J-ship1-cazaTipe.png').convert_alpha()
        self.image = pygame.transform.scale(originalImage, (150, 150))
        self.image = pygame.transform.rotate(self.image, 180)
        self.rect = self.image.get_rect()

        # Definir intervalos
        izquierda_intervalo = (0, 50)
        derecha_intervalo = (width - 50, width)

        # Elegir posición y velocidad en base a la dirección
        if random.choice([True, False]):  # True: aparecerá en la izquierda, False: aparecerá en la derecha
            self.rect.x = random.randrange(*izquierda_intervalo)
            self.velocidad_x = 5  # Mover hacia la derecha
        else:
            self.rect.x = random.randrange(*derecha_intervalo)
            self.velocidad_x = -5  # Mover hacia la izquierda

        self.rect.y = 10

    def update(self):
        self.rect.x += self.velocidad_x

        if self.rect.x >= width or self.rect.x <= 0:
            self.velocidad_x = -self.velocidad_x
    
    def disparar_enemigos(self):
        bala = Balas_enemigos(self.rect.centerx, self.rect.bottom)
        grupo_jugador.add(bala)
        grupo_balas_enemigos.add(bala)
        laser_sonido.play()

class Balas(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        originalImage = pygame.image.load('imagenes/J-shootDefaultImage.png').convert_alpha()
        self.image = pygame.transform.scale(originalImage, (50, 50))

        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.y = y
        self.velocidad = -18
    
    def update(self):
        self.rect.y += self.velocidad
        if self.rect.bottom < 0:
            self.kill()

class Balas_enemigos(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        originalImage = pygame.image.load('imagenes/J-shootEnemyImage.png').convert_alpha()
        self.image = pygame.transform.scale(originalImage, (50, 50))

        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.y = 100
        self.velocidad_y = 3
    
    def update(self):
        self.rect.y += self.velocidad_y
        if self.rect.bottom > height:
            self.kill()

class Explosion(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        self.image = explosion_list[0]
        img_scala = pygame.transform.scale(self.image, (20, 20))
        self.rect = img_scala.get_rect()
        self.rect.center = position
        self.time = pygame.time.get_ticks()
        self.velocidad_epxlo = 30
        self.frames = 0
    
    def update(self):
        tiempo = pygame.time.get_ticks()
        if tiempo - self.time > self.velocidad_epxlo:
            self.time = tiempo
            self.frames += 1
            if self.frames == len(explosion_list):
                self.kill()
            else:
                position = self.rect.center
                self.image = explosion_list[self.frames]
                self.rect = self.image.get_rect()
                self.rect.center = position

grupo_jugador = pygame.sprite.Group()
grupo_enemigos = pygame.sprite.Group()
grupo_balas_jugador = pygame.sprite.Group()
grupo_balas_enemigos = pygame.sprite.Group()

player = Jugador()
grupo_jugador.add(player)
grupo_balas_jugador.add(player)

for x in range(10):
    enemigo = Enemigos(10,10)
    grupo_enemigos.add(enemigo)
    grupo_jugador.add(enemigo)

while run:
    clock.tick(fps)
    window.blit(fondo, (0,0))

    for event in pygame.event.get():
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
    
    # Coliciones balas_jugador - enemigo
    colicion1 = pygame.sprite.groupcollide(grupo_enemigos, grupo_balas_jugador, True, True)
    for i in colicion1:
        score += 10
        enemigo.disparar_enemigos()
        enemigo = Enemigos(300, 10)
        grupo_enemigos.add(enemigo)
        grupo_jugador.add(enemigo)

        explo = Explosion(i.rect.center)
        grupo_jugador.add(explo)
        explosion_sonido.set_volume(0.3)
        explosion_sonido.play()
    
    # Coliciones jugador - balas_enemigo
    colicion2 = pygame.sprite.spritecollide(player, grupo_balas_enemigos, True)
    for j in colicion2:
        player.vida -= 10
        if player.vida <= 0:
            run = False
            subprocess.run([sys.executable, 'saveScore.py', str(score), ""])
        explo1 = Explosion(j.rect.center)
        grupo_jugador.add(explo1)
        golpe_sonido.play()
    
    # Coliciones jugador - enemigo
    hits = pygame.sprite.spritecollide(player, grupo_enemigos, False)
    for hit in hits:
        player.vida -= 100
        enemigos = Enemigos(10,10)
        grupo_jugador.add(enemigos)
        grupo_enemigos.add(enemigos)
        if player.vida <= 0:
            run = False
            subprocess.run([sys.executable, 'saveScore.py', str(score), ""])
    
    # Indicador y Score
    texto_puntuacion(window, (' SCORE: ' + str(score) + '       '), 30, width-85, 2)
    barra_vida(window, width-285, 0, player.vida)

    # if not run:
    #     subprocess.run([sys.executable, 'saveScore.py', score, ""])

    pygame.display.flip()

    # if not run:
    #     subprocess.run([sys.executable, 'saveScore.py', score, ""])

# print("LLEGA")
# subprocess.run([sys.executable, 'saveScore.py', score, ""])

pygame.quit()




        
