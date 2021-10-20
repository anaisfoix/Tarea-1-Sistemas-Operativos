with open('inputLaberinto.txt') as myfile:
    total_lines = sum(1 for line in myfile)

print(total_lines)
datos=open('inputLaberinto.txt')
linea=datos.readlines()
matriz=[]
for i in range(50):
    matriz.append(['C']*30)
print(matriz)
filas=int
columnas=int
construccion=[]
for i in range(total_lines):
    arregloDatos=linea[i].split(sep=',')
    filas=arregloDatos[0]
    columnas=arregloDatos[1]
    construccion=arregloDatos[2]
    matriz[filas][columnas]=construccion;
print(matriz)

cont=0