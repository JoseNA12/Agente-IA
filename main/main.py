# Tarea 1 - IA - Snake

class CampoJuego:
    def __init__(self):
        self.matriz = []
        self.cant_filas = 0
        self.cant_columnas = 0

    def getMatriz(self):
        return self.matriz

    def getCantFilas(self):
        return self.cant_filas

    def getCantColumnas(self):
        return self.cant_columnas

    def crearMatriz(self, pFilePath):
        with open(pFilePath) as fp:
            for i, fila in enumerate(fp):
                self.insertarEnFila(fila)
        
        self.cant_filas = len(self.matriz)
        self.cant_columnas = len(self.matriz[0])

    def insertarEnFila(self, fila):
        self.matriz.append(list(fila[:-1])) # [:-1] eliminar el ultimo caracter de cada linea, el salto de linea: \n

    def verMatriz(self):
        temp = ""
        for x in range(len(self.matriz)):
            for y in range(len(self.matriz[x])):
                temp += self.matriz[x][y]
            temp += "\n"
        print(temp)


class Agente:
    def __init__(self):
        self.pos_fila = 0
        self.pos_columna = 0

    def iniciar(self, campo, fila, columna):
        if (fila > campo.getCantFilas() - 1) or (columna > campo.getCantColumnas() - 1):
            print("Alguna coordenada esta fuera de rango")
            return
        elif campo.getMatriz()[fila][columna] != " ":
            print("No puedo iniciar en esa posición")
            return

campoJuego = CampoJuego()
campoJuego.crearMatriz("mapa_1.txt")

agente = Agente()
print("Cantidad de filas: " + str(campoJuego.getCantFilas()))
print("Cantidad de columnas: " + str(campoJuego.getCantColumnas()))

agente.iniciar(campoJuego, 12, 42)


# campoJuego.verMatriz()
