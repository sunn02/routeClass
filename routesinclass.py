import sys 
def generar_empty_matrix(n):
    return [['.' for _ in range(n)] for _ in range(n)]

def imprimir_cuadricula(matrix):
    n = len(matrix)
    print("Mapa con Ruta:")
    encabezado = "  " + " ".join(str(i) for i in range(n))
    print(encabezado)
    
    for i in range(n):
        fila = str(i) + " "
        for j in range(n):
            fila += matrix[i][j] + " "
        print(fila)

def insertar_inicio_fin(matrix): 
    x_inicio = int(input("Ingrese la coordenada x del inicio: "))
    y_inicio = int(input("Ingrese la coordenada y del inicio: "))
    if 0 <= x_inicio < len(matrix) and 0 <= y_inicio < len(matrix[0]):
            matrix[x_inicio][y_inicio] = 'S'

    x_fin = int(input("Ingrese la coordenada x del fin: "))
    y_fin = int(input("Ingrese la coordenada y del fin: "))
    if 0 <= x_fin < len(matrix) and 0 <= y_fin < len(matrix[0]):
            matrix[x_fin][y_fin] = 'D'
    return (x_inicio, y_inicio), (x_fin, y_fin)

def insertar_obstaculos(matrix):
    num_obstaculos = int(input("¿Cuántos obstáculos desea insertar? "))
    for _ in range(num_obstaculos):
        x = int(input("Ingrese la coordenada x del obstáculo: "))
        y = int(input("Ingrese la coordenada y del obstáculo: "))
        if 0 <= x < len(matrix) and 0 <= y < len(matrix[0]):
            matrix[x][y] = 'X'

def generar_matrix(num_vertices,aristas): 
    matrix = [[0 for _ in range(num_vertices)] for _ in range(num_vertices)]
    for arista in aristas:
        i, j = arista
        matrix[i][j] = 1
        matrix[j][i] = 1
    return matrix

def mindistancia(distancia, shortPathSet):
    min_distancia = sys.maxsize #Sirve para asegurar que todos los vertices procesados sean menores
    min_index = -1 #Sirve para que despues de la iteracion se devuelva el menor valor para confirmar que se haya recorrido todos los vertices con valores positivos

    for vertice in range(len(distancia)):
        if distancia[vertice] < min_distancia and not shortPathSet[vertice]: #Confirma si la distancia del vertice actual es menor que infinito y no esta dentro del arbol de caminos cortos
            min_distancia = distancia[vertice] #esa distancia recorrida se convierte en la minima distancia que se ha visitado
            min_index = vertice #se actualiza el vertice como el minimo visitado 
    return min_index

def dijkstra(num_vertices, grafo, source):
    distancia = [sys.maxsize] * num_vertices #Se asigna un valor inicial como infinito a la distancia con todos los vertices
    distancia[source] = 0 #Se asume que la distancia desde el primer vertice consigo mismo es O 
    shortPathSet = [False] * num_vertices #Inicialmente no se incluye los vertices al arbol
    predecessor = [-1] * num_vertices #en este caso es escencial el uso de precesores para construir el camino mas corto desde el origen, 
    #se parte del nodo destino y seguimos los predecesores hasta el origen
    for _ in range(num_vertices):
        min_vertice = mindistancia(distancia, shortPathSet) #Escoge al vertice con la menor distancia
        shortPathSet[min_vertice] = True #Agrega al arbol de caminos 
        for actual_vertice in range(num_vertices):
            #verifica si entre el minimo valor procesado y el que esta siendo procesado existe una arista,
            # que sera mayor que cero en una matriz de adyacencia; y que ese nodo no este todavia en el arbol de caminos
            # la otra condicion verifica si la distancia calculada de origen al actual vertice a traves de min vertice 
            # es menor que la distancia anterior o actual conocida para luego actualizar si es de ser asi
            if grafo[min_vertice][actual_vertice] > 0 and not shortPathSet[actual_vertice] and \
                distancia[actual_vertice] > distancia[min_vertice] + grafo[min_vertice][actual_vertice]:
                distancia[actual_vertice] = distancia[min_vertice] + grafo[min_vertice][actual_vertice]
                predecessor[actual_vertice] = min_vertice 
#
    return distancia, predecessor

def obtener_vertices_aristas(matrix):
    #vertices: Cada celda accesible (no un obstáculo) en la matriz se convierte en un vértice.
    vertices = []
    #Cada par de celdas adyacentes accesibles (horizontal o vertical) se convierte en una arista. 
    # Esto implica que puedes moverte entre estas celdas.
    aristas = []
    n = len(matrix)
    for i in range(n):
        for j in range(n):
            if matrix[i][j] != 'X':
                vertices.append((i, j))
                if i > 0 and matrix[i-1][j] != 'X':
                    aristas.append(((i, j), (i-1, j)))
                if i < n-1 and matrix[i+1][j] != 'X':
                    aristas.append(((i, j), (i+1, j)))
                if j > 0 and matrix[i][j-1] != 'X':
                    aristas.append(((i, j), (i, j-1)))
                if j < n-1 and matrix[i][j+1] != 'X':
                    aristas.append(((i, j), (i, j+1)))
    return vertices, aristas

def convertir_a_indice(vertices, coord):
    return vertices.index(coord) # la funcion integrada index permite acceder al indice de las coordenadas,
    #ya que al trabajar con la matriz se utiliza los indices en vez de coordenadas

def get_shortest_path(predecessor, start, end):
    path = [] #se crea una lista vacia para almacenar el camino que se creo
    #a partir de los predecedores obtenidos en el algoritmo
    while end != -1:
        # Inicia un bucle que continuará hasta que end sea -1. 
        # -1 indica que se ha llegado al nodo de inicio, que no tiene predecesor.
        path.append(end)
        end = predecessor[end] #actualiza end al predecesor del nodo actual. 
        #Esto sigue el enlace al nodo anterior en el camino más corto.
    path.reverse()
    return path

def marcar_camino(matrix, path):
    for (x, y) in path:
        if matrix[x][y] not in ('S', 'D', 'X'):
            matrix[x][y] = '*'

n = int(input("Inserte el número de matriz: "))

matrix = generar_empty_matrix(n)
imprimir_cuadricula(matrix)

insertar_obstaculos(matrix)
inicio, fin = insertar_inicio_fin(matrix)
imprimir_cuadricula(matrix)

vertices, aristas = obtener_vertices_aristas(matrix)
num_vertices = len(vertices)

aristas = [(convertir_a_indice(vertices, arista[0]), convertir_a_indice(vertices, arista[1])) for arista in aristas]
grafo = generar_matrix(num_vertices, aristas)

inicio_idx = convertir_a_indice(vertices, inicio)
fin_idx = convertir_a_indice(vertices, fin)

distancias, predecessor = dijkstra(num_vertices, grafo, inicio_idx)

# Obtener el camino más corto
path_indices = get_shortest_path(predecessor, inicio_idx, fin_idx)
path = [vertices[i] for i in path_indices]

# Marcar el camino más corto en la matriz
marcar_camino(matrix, path)

# Imprimir la cuadrícula con el camino más corto
imprimir_cuadricula(matrix)
