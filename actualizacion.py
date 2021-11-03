import pygame
from math import floor
from time import sleep
from threading import Semaphore, Thread


colores = {
    ' ' : (255,255,255), 
    'X' : (0,0,0), 
    'V' : (0,255,255), 
    'B' : (255,255,0), 
    'C' : (255,0,255), 
}

direcciones={
    'u':(0,1),
    'd':(0,-1),
    'l':(-1,0),
    'r':(1,0),
    's':(0,0)
}


def actualiza_laberinto():
    for i in range(0, filas):
        for j in range(0, columnas):
            dibuja_cuadrado(i, j, colores[matriz[i][j]])
    pygame.display.update()

def dibuja_cuadrado(y, x, color):
    pygame.draw.rect(screen, color, pygame.Rect(150 + x*ancho + 1, 100 + y*largo +1, ancho, largo))


SCREEN_WIDTH = 700
SCREEN_HEIGHT = 600

filas = 50
columnas = 30
filename = 'inputLaberinto.txt'

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

# Fondo blanco
screen.fill([255,255,255])

pygame.display.update()

# El contorno del laberinto
pygame.draw.rect(screen, (230,30,30), pygame.Rect(150,100,400,400), 1)

# Ancho y largo de los cuadros dentro de la matriz
ancho = 400/columnas
largo = 400/filas

# Lineas horizontales
for i in range(1, filas):
        pygame.draw.line(screen, (230, 30, 30), (150,100 + i*largo), (400+150,100 +  i*largo), 1)

# Para líneas verticales
for i in range(1, columnas):
    pygame.draw.line(screen, (230, 30, 30), (150 + i*ancho, 100), (150 +  i*ancho, 100 + 400), 1)


pygame.display.update()


file=open(filename)
lineas=file.readlines()

# Creamos la matriz
matriz = []
for i in range(filas):
    matriz.append([' '] * 30)


# Colocamos las paredes y la ventana
for linea in lineas:
    datos = linea.split(',')
    columna = int(datos[0])
    fila = int(datos[1])
    dato = datos[2]
    matriz[fila][columna] = dato[0]

sem_clones= Semaphore(10)
sem_matriz= Semaphore(1)

run = True
encontrado=False

def cuentaBifurcaciones(x, y):
    direccionesValidas=[]
    for i in ['u', 'd', 'l', 'r']:
        x_=x+direcciones[i][0]
        y_=y+direcciones[i][1]
        if y_>-1 and y_<columnas and x_>-1 and x_<filas:
            if matriz[x_][y_]==' ' or matriz[x_][y_]=='V':
                direccionesValidas.append(i)
    return direccionesValidas

def clon(x, y, direccion):
    global run
    global encontrado
    sem_clones.acquire()
    while run and not encontrado:
        sleep(0.05)
        x=x+direcciones[direccion][0]
        y=y+direcciones[direccion][1]  
        sem_matriz.acquire()
        if matriz[x][y]=='V':
            print(f'La salida está en ({x}, {y})')
            encontrado=True
            sem_matriz.release()
            sem_clones.release()
            return
        if matriz[x][y]!=' ':
            sem_clones.release()
            sem_matriz.release()
            return
        matriz[x][y]='C'
        sem_matriz.release()

        dirs=cuentaBifurcaciones(x, y)
    
        if len(dirs)==0:
            sem_clones.release()
            return

        if len(dirs)>1:
            sem_matriz.acquire()
            matriz[x][y]='B'
            sem_matriz.release()
            hilos=[]
            for i in range(1, len(dirs)):                
                t= Thread(target=clon, args=(x,y,dirs[i]))
                t.setDaemon(True)
                t.start()
                hilos.append(t)

            direccion=dirs[0]

        if len(dirs)==1:
            sem_matriz.acquire()
            matriz[x][y]='B'
            direccion=dir[0]
            sem_matriz.release()


t=Thread(target=clon, args=(0,0,'s'))
t.setDaemon(True)
t.start()


# Loop principal de pygame. Es necesario para que windows no crea que no responde.
while run:
    actualiza_laberinto()
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            run = False

pygame.quit()