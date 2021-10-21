# with open('inputLaberinto.txt') as myfile:
#     total_lines = sum(1 for line in myfile)

# print(total_lines)
# datos=open('inputLaberinto.txt')
# linea=datos.readlines()
# matriz=[]
# for i in range(50):
#     matriz.append(['C']*30)
# print(matriz)
# filas=int
# columnas=int
# construccion=[]
# for i in range(total_lines):
#     arregloDatos=linea[i].split(sep=',')
#     filas=arregloDatos[0]
#     columnas=arregloDatos[1]
#     construccion=arregloDatos[2]
#     matriz[filas][columnas]=construccion;
# print(matriz)

# cont=0

import pygame
from math import floor
from time import sleep
from threading import Semaphore, Thread

colores={
    ' ':(255,255,255),
    'X':(0,0,0),
    'V':(0,255,255),
    'B':(255,255,0),
    'C':(255,0,255),
}

direcciones={
    'u':(0,1),
    'd':(),
    'l':(),
    'r':(),
    's':(),
}

def actualiza_laverinto():
    for i in range (0,filas):
        for j in range (0,columnas):
            dibuja_cuadrado(i,j,colores[matriz[i][j]])
    pygame.display.update()

def dibuja_cuadrado(y,x,color):
    pygame.draw.rect(screen, color,pygame.Rect(150+x*ancho+1,100+y*largo+1,ancho,largo))

SCREEN_WIDTH=700
SCREEN_HEIGHT=600

filas=50
columnas=30
filename='inputLaberinto.txt'

pygame.init()
screen=pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock=pygame.time.Clock()
screen.fill([255,255,255])
pygame.display.update()

pygame.draw.rect(screen, (130,30,30),pygame.Rect(150,100,400,400),1)

pygame.display.update()

ancho=400/columnas
largo=400/filas

for i in range(1,filas):
    pygame.draw.line(screen, (230,30,30),(150,100+i*largo),(400+150,100+i*largo),1)

for j in range(1,columnas):
    pygame.draw.line(screen, (230,30,30),(150+j*ancho,100),(150+j*ancho,100+400),1)

dibuja_cuadrado(3,2,(48,128,255))
pygame.display.update()

file=open(filename)
lineas=file.readline()

matriz=[]
for i in range (filas):
    matriz.append([' ']*30)

for linea in lineas:
    datos=linea.split(',')
    fila=int(datos[0])
    columna=int(datos[1])
    dato=datos[2]
    matriz[fila][columna]=dato[0]

actualiza_laverinto()

def clone(x,y,direccion):
    global run
    global encontrado
    while run and not encontrado:
        sleep(0.05)
        x=x+direcciones[direccion[0]]
        x=y+direcciones[direccion[1]]

        

run=True
encontrado=False
while(run):
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            run=False

pygame.quit()
