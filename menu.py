import subprocess
import sys
import pygame
import json


def drawText(text, font, color, x, y):
    textSurface = font.render(text, True, color)
    textRect = textSurface.get_rect()
    textRect.midtop = (x, y)
    window.blit(textSurface, textRect)

def readData():
    with open('top5Scores.json', 'r') as file:
        data = json.load(file)

    return data


pygame.init()

width, height = 600, 400
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("MENU")

white = (255, 255, 255)
black = (0, 0, 0)
gray = (200, 200, 200)

font = pygame.font.Font(None, 36)


img1 = pygame.image.load('imagenes/ship3-Xwing.png')
img2 = pygame.image.load('imagenes/ship2-halcon.png')

btnSize = (100,100)
imgBtnShip1 = pygame.transform.scale(img1, btnSize)
imgBtnShip2 = pygame.transform.scale(img2, btnSize)

btnShip1 = {"image": imgBtnShip1, "rect": pygame.Rect(50, height // 2 - 25, *btnSize), "pressed": True}
btnShip2 = {"image": imgBtnShip2, "rect": pygame.Rect(width - 150, height // 2 - 25, *btnSize), "pressed": False}


run = True
while run:
    window.fill(gray)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if playButtonRect.collidepoint(event.pos):
                if btnShip1["pressed"] == True:
                    subprocess.run([sys.executable, 'game.py', 'imagenes/ship3-Xwing.png', ""])

                    yOffset = 50
                    for i in readData():
                        drawText(f"{i['Player']}   {i['Score']}", font, black, width//2, yOffset)
                        yOffset += 50


                elif btnShip2["pressed"] == True:
                    subprocess.run([sys.executable, 'game.py', 'imagenes/ship2-halcon.png', ""])

                    yOffset = 50
                    for i in readData():
                        drawText(f"{i['Player']}   {i['Score']}", font, black, width//2, yOffset)
                        yOffset += 50



            elif btnShip1["rect"].collidepoint(event.pos):
                btnShip1["pressed"] = True
                btnShip2["pressed"] = False

            elif btnShip2["rect"].collidepoint(event.pos):
                btnShip1["pressed"] = False
                btnShip2["pressed"] = True


    # Poner boton play
    playButtonRect = pygame.Rect(200, 300, 200, 50)
    pygame.draw.rect(window, white, playButtonRect)
    drawText("PLAY", font, black, playButtonRect.centerx, playButtonRect.centery - 10)

    # Poner Top5
    yOffset = 50
    for i in readData():
        drawText(f"{i['Player']}   {i['Score']}", font, black, width//2, yOffset)
        yOffset += 50

    # Poner botones naves
    borde = 3
    pygame.draw.rect(window, white, btnShip1["rect"], borde) if btnShip1["pressed"] else pygame.draw.rect(window, white, btnShip2["rect"], borde)
    window.blit(btnShip1["image"], btnShip1["rect"])
    window.blit(btnShip2["image"], btnShip2["rect"])


    pygame.display.flip()

pygame.quit()
sys.exit()