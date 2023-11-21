from typing import Any
import pygame
import random
import Player, Explosion, Enemys, Bullets, BulletsEnemys


from pygame.sprite import _Group

pygame.init()
pygame.mixer.init()

wallpaper = pygame.image.load('imagenes/fondo.png')

shootDefault = pygame.mixer.Sound('audio/shootDefault.mp3')
shootEnemy = pygame.mixer.Sound('audio/shootEnemy.mp3')

width = wallpaper.get_width()
height = wallpaper.get_height()
window = pygame.display.set_mode((width, height))
pygame.display.set_caption('SPACE INVADERS')                  # display1

run = True

fps = 60
clock = pygame.time.Clock()
score = 0
vida = 100
blanco = (255,255,255)
negro = (0,0,0)

def scoreText(frame, text, size, x, y):
    font = pygame.font.SysFont('Consolas', size, bold=True)
    textFrame = font.render(text, True, blanco, negro)
    textRect = textFrame.get_rect()
    textRect.midtop = (x,y)
    frame.blit(textFrame, textRect)


def lifeBar(frame, x, y, nivel):
    widthLifeBar = 100
    heightLifeBar = 20
    fill = int((nivel/100)*widthLifeBar)
    border = pygame.Rect(x, y, widthLifeBar, heightLifeBar)
    fill = pygame.Rect(x, y, fill, heightLifeBar)
    pygame.draw.rect(frame, (255,0,55), fill)
    pygame.draw.rect(frame, negro, border, 4)


####    ####    ####    ####    ####    ####



####    ####    ####    ####    ####    ####


playerGroup = pygame.sprite.Group()
enemysGroup = pygame.sprite.Group()
playerBulletsGroup = pygame.sprite.Group()
enemysBulletsGroup = pygame.sprite.Group()

player = Player()
playerGroup.add(player)
playerBulletsGroup.add(player)


for x in range(10):
    enemigo = Enemys(10,10)
    enemysGroup.add(enemigo)
    playerGroup.add(enemigo)


while run:
    clock.tick(fps)
    window.blit(wallpaper, (0,0))

    for event in pygame.event.get()
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.disparar()

    playerGroup.update()        #grupo_jugador.update()
    enemysGroup.update()        #grupo_enemigos.update()
    playerBulletsGroup.update()        #grupo_balas_jugador.update()
    enemysBulletsGroup.update()        #grupo_balas_enemigos.update()

    playerGroup.draw(window)        #grupo_jugador.draw(window)


    # Coliciones balas_jugador - enemigo
    colicion1 = pygame.sprite.groupcollide(enemysGroup, playerBulletsGroup, True, True)
    for i in colicion1:
        score+=10
        enemigo.disparar_enemigos()
        enemigo = Enemys(300,10)
        grupo_enemigos.add(enemigo)
        grupo_jugador.add(enemigo)

        explo = Explosion(i.rect.center)
        grupo_jugador.add(explo)
        explosion_sonido.set_volume(0.3)            # Sonido explosion
        explosion_sonido.play()

    # Coliciones jugador - balas_enemigo
    colicion2 = pygame.sprite.spritecollide(player, grupo_balas_enemigos, True)
    for j in colicion2:
        player.vida -= 10
        if player.vida <= 0:
            run = False
        explo1 = Explosion(j.rect.center)
        grupo_jugador.add(explo1)
        golpe_sonido.play()                 # Sonido golpe
    
    # Coliciones jugador - enemigo
    hits = pygame.sprite.spritecollide(player, grupo_enemigos, False)
    for hit in hits:
        player.vida -= 100
        enemigos = Enemys(10,10)
        grupo_jugador.add(enemigos)
        grupo_enemigos.add(enemigos)
        if player.vida <= 0:
            run = False
    
    # Indicador y Score
    texto_puntuacion(window, (' SCORE: ' + str(score) + '       '), 30, width-85, )
    barra_vida(window, width-285, 0, player.vida)

    pygame.display.flip()

pygame.quit()


