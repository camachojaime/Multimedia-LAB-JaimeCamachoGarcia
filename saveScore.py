import pygame
import sys
import json
import subprocess

# Inicializar Pygame
pygame.init()

# Configuración de la ventana
width, height = 245, 120
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Save score")

# Colores
white = (255, 255, 255)
gray = (200, 200, 200)
black = (0, 0, 0)
blackPY = pygame.Color(0, 0, 0)

# Fuente y tamaño del texto
font = pygame.font.Font(None, 36)

# Inicializar variables
# score = 125
score = int(sys.argv[1])

# Cuadro introducir texto
textBlock = pygame.Rect(90, 35, 140, 32)
colorInactiveTB = pygame.Color('lightskyblue3')
colorActiveTB = pygame.Color('dodgerblue2')
colorTB = colorInactiveTB
activeTB = False
textTB = ''
textSurface = font.render(textTB, True, colorTB)


# Función para dibujar el texto
def draw_text(text, x, y, color):
    text_surface = font.render(text, True, color)
    window.blit(text_surface, (x, y))

    # # Poner boton play
    # playButtonRect = pygame.Rect(200, 300, 200, 50)
    # pygame.draw.rect(window, gray, playButtonRect)
    # drawText("PLAY", font, black, playButtonRect.centerx, playButtonRect.centery - 10)

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
    
    # subprocess.run([sys.executable, 'menu.py'])



# # Poner boton Guardar
# saveBtn = pygame.Rect(200, 300, 200, 50)
# pygame.draw.rect(window, gray, saveBtn)
# drawBtn("SAVE", font, black, width//2, height-20)


run = True
# Bucle principal
while run:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if saveBtn.collidepoint(event.pos) and textTB != "":
                # Eliminar
                # print(textTB)
                
                save(textTB)
                run = False
                # Eliminar
                # textTB = ''

            if textBlock.collidepoint(event.pos):
                activeTB = not activeTB
            else:
                activeTB = False
            # colorTB = colorActiveTB if activeTB else colorInactiveTB
            colorTB = blackPY if activeTB else colorInactiveTB

        if event.type == pygame.KEYDOWN:
            if activeTB:
                if event.key == pygame.K_RETURN:
                    # Eliminar
                    # print(textTB)

                    save(textTB)
                    run = False
                    # Eliminar
                    # textTB = ''
                elif event.key == pygame.K_BACKSPACE:
                    textTB = textTB[:-1]
                else:
                    textTB += event.unicode
                textSurface = font.render(textTB, True, colorTB)

            



    # Lógica del juego (aquí puedes actualizar el score, etc.)

    # Limpiar la pantalla
    window.fill(white)

    # Dibujar etiquetas y score
    draw_text("Score: " + str(score), 10, 10, black)
    draw_text("Name: ", 10, 40, black)
    #draw_text(str(score), width-100, 10, black)

    # Dibuja textBlock
    pygame.draw.rect(window, colorTB, textBlock, 2)
    window.blit(textSurface, (textBlock.x + 5, textBlock.y + 5))

    # Poner boton Guardar
    saveBtn = pygame.Rect(width//2 - 40, height - 40, 80, 40)
    pygame.draw.rect(window, gray, saveBtn)
    drawBtn("SAVE", font, black, width//2, height-30)

    # Actualizar la pantalla
    pygame.display.flip()

    # Controlar la velocidad de actualización
    pygame.time.Clock().tick(60)


pygame.quit()
sys.exit()