import pygame
import random
import math
from pygame import mixer

#inicializar pygame
pygame.init()

#crear la pantalla
pantalla = pygame.display.set_mode((800, 600))

#titulo e icono
pygame.display.set_caption("INVASION ESPACIAL")
icono = pygame.image.load("/Users/ceci/Documents/python/Día 10/ovni.png")
pygame.display.set_icon(icono)
fondo = pygame.image.load("/Users/ceci/Documents/python/Día 10/Fondo.jpg")

#agregar musica
mixer.music.load("/Users/ceci/Documents/python/Día 10/MusicaFondo.mp3")
mixer.music.set_volume(0.5)
mixer.music.play(-1)

#variables del jugador
img_jugador = pygame.image.load("/Users/ceci/Documents/python/Día 10/astronave.png")
jugador_x = 368
jugador_y = 500
jugador_x_cambio = 0

#variables del enemigo
img_enemigo = []
enemigo_x = []
enemigo_y = []
enemigo_x_cambio = []
enemigo_y_cambio = []
cantidad_enemigo = 8

for e in range(cantidad_enemigo):
    img_enemigo.append(pygame.image.load("/Users/ceci/Documents/python/Día 10/nave-espacial.png"))
    enemigo_x.append(random.randint(0, 736))
    enemigo_y.append(random.randint(50, 200))
    enemigo_x_cambio.append(0.5)
    enemigo_y_cambio.append(50)

#variables de la bala
balas = []
img_bala = pygame.image.load("/Users/ceci/Documents/python/Día 10/bala.png")
bala_x = 0
bala_y = 500
bala_x_cambio = 0
bala_y_cambio = 3
bala_visible = False

#puntaje
puntaje = 0
fuente = pygame.font.Font('freesansbold.ttf', 32)
texto_x = 10
texto_y = 10

#texto final del juego
fuente_final = pygame.font.Font('freesansbold.ttf', 40)

def texto_final():
    mi_fuente_final = fuente_final.render("JUEGO TERMINADO", True, (255, 255, 255))
    pantalla.blit(mi_fuente_final, (200, 200))

#funcion mostrar puntaje
def mostrar_puntaje(x, y):
    texto = fuente.render(f"Puntaje: {puntaje}", True, (225, 225, 225))
    pantalla.blit(texto, (x, y))

#funcion del jugador
def jugador(x, y):
    pantalla.blit(img_jugador,(x, y))

#funcion del enemigo
def enemigo(x, y, ene):
    pantalla.blit(img_enemigo[ene],(x, y))

#funcion disparar bala
def disparar_bala(x, y):
    global bala_visible
    bala_visible = True
    pantalla.blit(img_bala, (x + 16, y + 10))

#funcion detectar coliciones
def hay_colision(x_1, y_1, x_2, y_2):
    distancia = math.sqrt(math.pow(x_1 - x_2, 2) + math.pow(y_2 - y_1, 2))
    if distancia < 27:
        return True
    else:
        return False



#loop del juego
se_ejecuta = True
while se_ejecuta:
    #imagen de fondo
    pantalla.blit(fondo, (0, 0))

    #iterar eventos
    for evento in pygame.event.get():

        #evento cerrar
        if evento.type == pygame.QUIT:
            se_ejecuta = False

        #evento presionar teclas
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_LEFT:
                jugador_x_cambio = -1
            if evento.key == pygame.K_RIGHT:
                jugador_x_cambio = 1
            if evento.key == pygame.K_SPACE:
                sonido_bala = mixer.Sound("/Users/ceci/Documents/python/Día 10/disparo.mp3")
                sonido_bala.play()
                nueva_bala = {
                    "x": jugador_x,
                    "y": jugador_y,
                    "velocidad": -5
                }
                balas.append(nueva_bala)

        #evento soltar flechas
        if evento.type == pygame.KEYUP:
            if evento.key == pygame.K_LEFT or evento.key == pygame.K_RIGHT:
                jugador_x_cambio = 0

    #modificar ubicacion del jugador
    jugador_x += jugador_x_cambio

    #mantener dentro de bordes al jugador
    if jugador_x <= 0:
        jugador_x = 0
    elif jugador_x >=  736:
        jugador_x = 736

    #modificar ubicacion del enemigo
    for e in range(cantidad_enemigo):

        #fin del juego
        if enemigo_y[e] > 500:
            for k in range(cantidad_enemigo):
                enemigo_y[k] = 1000
            texto_final()
            break

        enemigo_x[e] += enemigo_x_cambio[e]

    #mantener dentro de bordes al enemigo
        if enemigo_x[e] <= 0:
            enemigo_x_cambio[e] = 1
            enemigo_y[e] += enemigo_y_cambio[e]
        elif enemigo_x[e] >=  736:
            enemigo_x_cambio[e] = -1
            enemigo_y[e] += enemigo_y_cambio[e]

        #colision
        for bala in balas:
            colision_bala_enemigo = hay_colision(enemigo_x[e], enemigo_y[e], bala["x"], bala["y"])
            if colision_bala_enemigo:
                sonido_colision = mixer.Sound("/Users/ceci/Documents/python/Día 10/Golpe.mp3")
                sonido_colision.play()
                bala_y = 500
                bala_visible = False
                puntaje += 1
                enemigo_x[e] = random.randint(0, 736)
                enemigo_y[e] = random.randint(50, 200)
                balas.clear()
                break

        enemigo(enemigo_x[e], enemigo_y[e], e)

    # Movimiento bala
    for bala in balas:
        bala["y"] += bala["velocidad"]
        pantalla.blit(img_bala, (bala["x"] + 16, bala["y"] + 10))
        if bala["y"] < 0:
            balas.remove(bala)

    

    jugador(jugador_x, jugador_y)
    
    mostrar_puntaje(texto_x, texto_y)

    #actualizar
    pygame.display.update()