import sys

class Cuadricula():
    def __init__(self, tamaño):
        self.tamaño = tamaño
        self.matriz = [['.'for _ in range(tamaño)] for _ in range(tamaño)]
        self.inicio = None
        self.fin = None


    def imprimir_cuadricula(self):
        print("Mapa con ruta:")
        encabezado = "  " + " ".join(str(i) for i in range(self.tamaño))
        print(encabezado)
        
        for i in range(self.tamaño):
            fila = str(i) + " "
            for j in range(self.tamaño):
                fila += self.matriz[i][j] + " "
            print(fila)
    
    def insertar_inicioFin(self):
        x_inicio = int(input("Ingrese la coordenada x del inicio: "))
        y_inicio = int(input("Ingrese la coordenada y del inicio: "))
        if 0 <= x_inicio < self.tamaño and 0 <= y_inicio < self.tamaño:
            self.matriz[x_inicio][y_inicio] = 'I'
            self.inicio = (x_inicio, y_inicio)
        
        x_fin = int(input("Ingrese la coordenada x del fin: "))
        y_fin = int(input("Ingrese la coordenada y del fin: "))
        if 0 <= x_fin < self.tamaño and 0 <= y_fin < self.tamaño:
            self.matriz[x_fin][y_fin] = 'F'
            self.fin = (x_fin, y_fin)
            
    def insertar_obstaculos(self):
        num_obstaculos = int(input("¿Cuántos obstáculos desea insertar? "))
        for _ in range(num_obstaculos):
            x_obstaculo = int(input("Ingrese la coordenada x del obstaculo: "))
            y_obstaculo = int(input("Ingrese la coordenada y del obstaculo: "))
            if 0 <= x_obstaculo < self.tamaño and 0 <= y_obstaculo < self.tamaño:
                self.matriz[x_obstaculo][y_obstaculo] = 'X'
                
    def marcar_camino(self, camino):
        for (x,y) in camino:
            if self.matriz[x][y] not in ('I','F', 'X'):
                self.matriz[x][y] = '*'

class Grafo():
    def __init__(self, cuadricula):
        self.cuadricula = cuadricula
        self.vertices, self.aristas = self.obtener_verticesAristas()
        self.num_vertices = len(self.vertices)
        self.matriz = self.generar_matriz()
        
    def obtener_verticesAristas(self):
    #(Agregado)Identifica todos los vértices accesibles en la cuadrícula (celdas que no son obstáculos).
    # y crea aristas entre celdas adyacentes accesibles
        vertices = []
        aristas = []
        num_matriz = self.cuadricula.tamaño
        
        for i in range(num_matriz):
            for j in range(num_matriz):
                if self.cuadricula.matriz[i][j] != 'X':
                    vertices.append((i, j))
                    # Crear aristas solo si la celda adyacente también es accesible
                    if i > 0 and self.cuadricula.matriz[i-1][j] != 'X':
                        aristas.append(((i, j), (i-1, j)))
                    if i < num_matriz - 1 and self.cuadricula.matriz[i+1][j] != 'X':
                        aristas.append(((i, j), (i+1, j)))
                    if j > 0 and self.cuadricula.matriz[i][j-1] != 'X':
                        aristas.append(((i, j), (i, j-1)))
                    if j < num_matriz - 1 and self.cuadricula.matriz[i][j+1] != 'X':
                        aristas.append(((i, j), (i, j+1)))
        return vertices, aristas
                
    def generar_matriz(self):
        matriz =  [[0 for _ in range(self.num_vertices)] for _ in range(self.num_vertices)]
        for arista in self.aristas:
            i, j = self.convertir_a_indice(arista[0]), self.convertir_a_indice(arista[1])
            matriz[i][j] = 1
            matriz[j][i] = 1
        return matriz
    
    def convertir_a_indice(self, coordenadas): #Se crea esta funcion para acceder a las coordenadas a partir de su indice dentro de la matriz
        return self.vertices.index(coordenadas)
    
    
    def dijkstra(self, origen):
        distancia = [sys.maxsize] * self.num_vertices
        distancia[origen] = 0
        shortPathSet = [False] * self.num_vertices
        predecessor = [-1] * self.num_vertices
        
        for _ in range(self.num_vertices):
            min_vertice = self.mindistancia(distancia, shortPathSet)
            shortPathSet[min_vertice] = True
            
            for actual_vertice in range(self.num_vertices):
                if self.matriz[min_vertice][actual_vertice] > 0 and not shortPathSet[actual_vertice] and \
                    distancia[actual_vertice] > distancia[min_vertice] + self.matriz[min_vertice][actual_vertice]:
                    distancia[actual_vertice] = distancia[min_vertice] + self.matriz[min_vertice][actual_vertice]
                    predecessor[actual_vertice] = min_vertice
        return distancia, predecessor
                
    def mindistancia(self, distancia, shortPathSet):
        min_distancia = sys.maxsize
        min_index = -1
        
        for vertice in range(self.num_vertices):
            if distancia[vertice] < min_distancia and not shortPathSet[vertice]:
                min_distancia = distancia[vertice]
                min_index = vertice
        return min_index
    
    def caminoMasCorto(self, predecessor, inicio, fin):
        camino = []
        while fin != -1:
            camino.append(fin)
            fin = predecessor[fin]
        camino.reverse()
        return camino
    
def main():
     num_matriz = int(input("Inserte el número de matriz: "))
     cuadricula = Cuadricula(num_matriz)
     cuadricula.imprimir_cuadricula()
     cuadricula.insertar_obstaculos()
     cuadricula.insertar_inicioFin()
     cuadricula.imprimir_cuadricula()
     
     grafo = Grafo(cuadricula)
     inicio_idx = grafo.convertir_a_indice(cuadricula.inicio)
     fin_idx = grafo.convertir_a_indice(cuadricula.fin)
     
     distancias, predecessor = grafo.dijkstra(inicio_idx)
     camino_indices = grafo.caminoMasCorto(predecessor, inicio_idx, fin_idx)
     camino = [grafo.vertices[i] for i in camino_indices]
     
     cuadricula.marcar_camino(camino)
     cuadricula.imprimir_cuadricula()


if __name__ == "__main__":
    main()