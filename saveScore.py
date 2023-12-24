import pygame
import sys
import json
import subprocess

pygame.init()

width, height = 245, 120
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Save score")

# Colores
white = (255, 255, 255)
gray = (200, 200, 200)
black = (0, 0, 0)
blackPY = pygame.Color(0, 0, 0)

font = pygame.font.Font(None, 36)

score = int(sys.argv[1])


textBlock = pygame.Rect(90, 35, 140, 32)
colorInactiveTB = pygame.Color('lightskyblue3')
colorActiveTB = pygame.Color('dodgerblue2')
colorTB = colorInactiveTB
activeTB = False
textTB = ''
textSurface = font.render(textTB, True, colorTB)


def draw_text(text, x, y, color):
    text_surface = font.render(text, True, color)
    window.blit(text_surface, (x, y))

def drawBtn(text, font, color, x, y):
    textSurface = font.render(text, True, color)
    textRect = textSurface.get_rect()
    textRect.midtop = (x, y)
    window.blit(textSurface, textRect)

def save(text):
    newScore = {"Player": text, "Score": score}

    with open('top5Scores.json', 'r') as file:
        data = json.load(file)
    
    for i in range(len(data)):
        if score >= data[i]['Score']:
            data.insert(i, newScore)
            data.pop(len(data)-1)
            break
    
    with open('top5Scores.json', "w") as file:
        json.dump(data, file, indent=2)


run = True
while run:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if saveBtn.collidepoint(event.pos) and textTB != "":
                save(textTB)
                run = False

            if textBlock.collidepoint(event.pos):
                activeTB = not activeTB

            else:
                activeTB = False

            colorTB = blackPY if activeTB else colorInactiveTB

        if event.type == pygame.KEYDOWN:
            if activeTB:
                if event.key == pygame.K_RETURN:
                    save(textTB)
                    run = False

                elif event.key == pygame.K_BACKSPACE:
                    textTB = textTB[:-1]

                else:
                    textTB += event.unicode

                textSurface = font.render(textTB, True, colorTB)


    window.fill(white)

    # Dibujar etiquetas y score
    draw_text("Score: " + str(score), 10, 10, black)
    draw_text("Name: ", 10, 40, black)

    # Dibuja textBlock
    pygame.draw.rect(window, colorTB, textBlock, 2)
    window.blit(textSurface, (textBlock.x + 5, textBlock.y + 5))

    # Poner boton Guardar
    saveBtn = pygame.Rect(width//2 - 40, height - 40, 80, 40)
    pygame.draw.rect(window, gray, saveBtn)
    drawBtn("SAVE", font, black, width//2, height-30)

    pygame.display.flip()
    pygame.time.Clock().tick(60)


pygame.quit()
sys.exit()