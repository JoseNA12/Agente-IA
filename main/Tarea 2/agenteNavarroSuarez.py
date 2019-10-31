# Tarea 2 - IA - ITCR - Agente
# José Navarro - Josué Suárez

import random
import time
from enum import Enum
import os
import copy
        
class CampoJuego:
    def __init__(self):
        self.matriz = []
        self.cant_filas = 0
        self.cant_columnas = 0
        self.matriz_copia = []

    def getMatriz(self):
        return self.matriz

    def getCantFilas(self):
        return self.cant_filas

    def getCantColumnas(self):
        return self.cant_columnas

    def crearCopiaMatriz(self):
        self.matriz_copia = copy.deepcopy(self.matriz)

    def contarMovimientoAgente(self, pFila, pColumna):
        if self.matriz_copia[pFila][pColumna] == " " or self.matriz_copia[pFila][pColumna] == "@":
            self.matriz_copia[pFila][pColumna] = "1"
        else:
            self.matriz_copia[pFila][pColumna] = str(int(self.matriz_copia[pFila][pColumna]) + 1)

    def crearMatriz(self, pFilePath):
        with open(pFilePath) as fp:
            for i, fila in enumerate(fp):
                self.matriz.append(list(fila[:-1])) # [:-1] eliminar el ultimo caracter de cada linea, el salto de linea: \n
        
        self.cant_filas = len(self.matriz)
        self.cant_columnas = len(self.matriz[0])  

    def verMatriz(self):
        temp = "\n"
        for x in range(len(self.matriz)):
            for y in range(len(self.matriz[x])):
                temp += self.matriz[x][y]
            temp += "\n"
        print(temp)

    def verMatrizCopia(self):
        temp = bcolors.WARNING + "\nCeldas visitadas en cantidad:\n" + bcolors.ENDC
        for x in range(len(self.matriz_copia)):
            for y in range(len(self.matriz_copia[x])):
                if self.matriz_copia[x][y].isdigit():
                    temp += bcolors.WARNING + self.matriz_copia[x][y] + bcolors.ENDC
                else:
                    temp += bcolors.HEADER + self.matriz_copia[x][y] + bcolors.ENDC
            temp += "\n"
        print(temp)

class Agente:
    def __init__(self, pPosicion):
        self.agente = "$"
        self.posicion = pPosicion
        self.encendido = True
        self.setMovimientos = {}
        self.memoria = {}
        self.objetivosABuscar = []
        self.objetivosRecolectados = []

    def esObjetivo(self, pValorMatriz):
        return pValorMatriz in self.objetivosABuscar

    def setobjetivosABuscar(self, pObjetivosABuscar):
        self.objetivosABuscar = pObjetivosABuscar

    def verObjetivosRecolectados(self):
        print(bcolors.OKGREEN + "Objetivos recoletados: (" + str(len(self.objetivosRecolectados)) + ") -> " + ', '.join(map(str, self.objetivosRecolectados)) + bcolors.ENDC)

    def recordarMovimiento(self, fila, columna, sensor):
        if self.memoria.get((fila, columna)) != None: # si ya existe un registro, actualice la cantidad de visitas
            contador = self.memoria.get((fila, columna))[1] + 1
            self.memoria.update({(fila, columna) : (sensor, contador)})
        else:
            self.memoria.update({(fila, columna) : (sensor, 1)}) # sino la conoce registre la celda con 1 visita    

    def recolectarObjetivo(self, pObjetivo):
        self.objetivosRecolectados.append(pObjetivo)

    def volverAlPuntoInicial(self):
        i = len(self.memoria) - 1
        while i > -1:
            fila = list(self.memoria.keys())[i][0]
            columna = list(self.memoria.keys())[i][1]
            sensor = list(self.memoria.values())[i][0]
            print(bcolors.FAIL + "Regresando al punto inicial..." + bcolors.ENDC)
            self.registrarMovimiento(self.posicion, Posicion(fila, columna), sensor, False)
            self.posicion.setPosicion(fila, columna)
            i -= 1

        campoJuego.verMatrizCopia()

    def consultarDetenerEjecucion(self):
        campoJuego.verMatrizCopia()
        detenerEjecucion = input(bcolors.HEADER + "¡He encontrado un objetivo!, ¿me detengo? [s/n]\n>>> " + bcolors.ENDC)
        if detenerEjecucion.lower() == "s":
            return True
        elif detenerEjecucion.lower() == "n":
            return False
        else:
            return consultarDetenerEjecucion()

    # determinar si existe colision en un solo movimiento dentro de la matriz
    def detectarColision(self, fila, columna):
        if (campoJuego.getMatriz()[fila][columna] != " ") and (campoJuego.getMatriz()[fila][columna] not in self.objetivosABuscar):
            print(bcolors.WARNING + "Colisión detectada: ("  + str(fila) + ", " + str(columna) + ")" + bcolors.ENDC)
            return True # Hay colision
        return False

    # determinar si existen colisiones en la lista de movimientos
    def evaluarMovimientos(self, listaMovimientos):
        posicionMovimiento = {"fila": self.posicion.getFila(), "columna": self.posicion.getColumna()}
        for movimiento in listaMovimientos:
            nuevoPos = self.getPosicionDelMovimiento(movimiento, posicionMovimiento["fila"], posicionMovimiento["columna"])
            if (self.detectarColision(nuevoPos["fila"], nuevoPos["columna"])): 
                return False # No se puede dar el movimiento
        return True

    # escoger los movimientos a ejecutar de la manera más inteligente
    def determinarMovimientos(self):
        movsPuntos = []
        movsColisiones = []
        movsVisitados = []
        cantCeldasVisitas = []  # misma longitud que movsVisitados 
        movsNuevos = []

        for movimientos in self.setMovimientos:      # analizar cada set de movimiento
            if self.evaluarMovimientos(movimientos): # si alguno tiene colisiones, fuera
                for mov in movimientos:              # obtener las celdas de los alredores y determinar si ya es visitada o no
                    posicionMovimiento = self.getPosicionDelMovimiento(mov, self.posicion.getFila(), self.posicion.getColumna())
                    fila = posicionMovimiento["fila"]
                    columna = posicionMovimiento["columna"]

                    if self.esObjetivo(campoJuego.getMatriz()[fila][columna]):
                        movsPuntos.append(movimientos)
                    elif self.memoria.get((fila, columna)) != None: # si la conozco es celda visitada
                        movsVisitados.append(movimientos)
                        cantCeldasVisitas.append(self.memoria.get((fila, columna))[1])
                    else:
                        movsNuevos.append(movimientos)
            else:
                movsColisiones.append(movimientos)

        # priorizar las celdas nuevas sobre las visitadas
        if movsPuntos != []: # hay celdas con puntos
            return random.choice(movsPuntos)
        elif movsNuevos != []: # existen celdas sin visitar
            return random.choice(movsNuevos)
        elif movsVisitados != []: # no hay celdas sin visitar, toca escoger la celda menos visitada
            i = 0
            i_temp = 0
            menor = cantCeldasVisitas[0]
            for valor in cantCeldasVisitas:
                if valor < menor:
                    i_temp = i
                    menor = valor
                i += 1

            return movsVisitados[i_temp]
        else:
            return [] # existe colisión circular o el movimiento no es válido

    # obtener la futura posición a mover
    def getPosicionDelMovimiento(self, movimiento, pos_fila_temp, pos_columna_temp):
        mensajeSensor = bcolors.OKBLUE + "Sensor: " + bcolors.ENDC
        pos_fila_temp += movimiento.value[0]
        pos_columna_temp += movimiento.value[1]
        mensajeSensor += movimiento.name
        return {"fila": pos_fila_temp, "columna": pos_columna_temp, "sensor": mensajeSensor}
    
    # registrar los movimientos en el campo matricial
    def avanzar(self, listaMovimientos):
        posicionMovimiento = {"fila": self.posicion.getFila(), "columna": self.posicion.getColumna()}
        for movimiento in listaMovimientos:
            posicionMovimiento = self.getPosicionDelMovimiento(movimiento, posicionMovimiento["fila"], posicionMovimiento["columna"])
            self.registrarMovimiento(self.posicion, Posicion(posicionMovimiento["fila"], posicionMovimiento["columna"]), posicionMovimiento["sensor"], True)
            self.posicion.setPosicion(posicionMovimiento["fila"], posicionMovimiento["columna"]) # Actualizar la posicion

    def registrarMovimiento(self, movimiento_1, movimiento_2, sensor, recolectandoObjetivos): # movimiento_1: pos actual, movimiento_2: pos a mover
        time.sleep(1.5)
        cls()
        
        celdaTemp = campoJuego.matriz[movimiento_2.getFila()][movimiento_2.getColumna()] 
        campoJuego.matriz[movimiento_1.getFila()][movimiento_1.getColumna()] = " " # borrar la posicion anterior
        campoJuego.matriz[movimiento_2.getFila()][movimiento_2.getColumna()] = self.agente # ☻
        
        if recolectandoObjetivos:
            self.recordarMovimiento(movimiento_2.getFila(), movimiento_2.getColumna(), sensor)

        self.verObjetivosRecolectados()
        campoJuego.verMatriz() 
        print("Posición actual: (" + str(movimiento_1.getFila()) + ", " + str(movimiento_1.getColumna()) + ")")        
        print("Siguiente posición: (" + str(movimiento_2.getFila()) + ", " + str(movimiento_2.getColumna()) + ")")
        print(sensor)

        if self.esObjetivo(celdaTemp) and recolectandoObjetivos:
            self.recolectarObjetivo(celdaTemp)
            if self.consultarDetenerEjecucion():
                self.volverAlPuntoInicial()
                self.encendido = False

    def iniciar(self):
        if (self.posicion.getFila() > campoJuego.getCantFilas() - 1) or (self.posicion.getColumna() > campoJuego.getCantColumnas() - 1):
            print("Alguna coordenada esta fuera de rango")
            return
        elif self.detectarColision(self.posicion.getFila(), self.posicion.getColumna()) == True:
            print("No puedo iniciar en esa posición")
            return
        else:
            def menuMovimientos():
                opcionMovimiento = input("\nSeleccione el movimiento a utilizar \n [1] Rey \n [2] Caballo \n [3] Alfil \n >>> ")
                if opcionMovimiento == "1":
                    self.setMovimientos = MovimientoRey.getList()
                elif opcionMovimiento == "2":
                    self.setMovimientos = MovimientoCaballo.getList()
                elif opcionMovimiento == "3":
                    self.setMovimientos = MovimientoAlfil.getList()
                else:
                    return menuMovimientos()
            
            menuMovimientos()

            # registrar la posicion inicial del agente
            campoJuego.matriz[self.posicion.getFila()][self.posicion.getColumna()] = self.agente
            self.recordarMovimiento(self.posicion.getFila(), self.posicion.getColumna(), "Punto inicial")
            campoJuego.verMatriz()
            campoJuego.contarMovimientoAgente(self.posicion.getFila(), self.posicion.getColumna())
            
            while(self.encendido):
                listaMovimientos = self.determinarMovimientos()
                if listaMovimientos != []:                   
                    self.avanzar(listaMovimientos)
                    campoJuego.contarMovimientoAgente(self.posicion.getFila(), self.posicion.getColumna())
                else:
                    campoJuego.verMatrizCopia()
                    print(bcolors.FAIL + "\nNo me puedo mover :(" + bcolors.ENDC)
                    break     
             

class Posicion:
    def __init__(self, pFila, pColumna):
        self.fila = pFila
        self.columna = pColumna

    def getFila(self):
        return self.fila

    def getColumna(self):
        return self.columna

    def setPosicion(self, pFila, pColumna):
        self.fila = pFila
        self.columna = pColumna

class Movimiento(Enum): # 8 ejes de movimiento
    NORTE =     [-1, 0]
    SUR =       [1, 0]
    OESTE =     [0, -1]
    ESTE =      [0, 1]
    NORESTE =   [-1, 1]
    NOROESTE =  [-1, -1]
    SURESTE =   [1, 1]
    SUROESTE =  [1, -1]

    @classmethod
    def getList(self):
        return list(map(lambda c: c.value, Movimiento))

class MovimientoRey(Enum):
    NORTE =    [Movimiento.NORTE]
    SUR =     [Movimiento.SUR]
    OESTE = [Movimiento.OESTE]
    ESTE =   [Movimiento.ESTE]
    NORESTE =   [Movimiento.NORESTE]
    NOROESTE =  [Movimiento.NOROESTE]
    SURESTE =   [Movimiento.SURESTE]
    SUROESTE =  [Movimiento.SUROESTE]

    @classmethod
    def getList(self):
        return list(map(lambda c: c.value, MovimientoRey))

class MovimientoCaballo(Enum): # 8 posibles direcciones de movimientos de caballo
    NORESTE =           [Movimiento.NORTE, Movimiento.NORTE, Movimiento.ESTE]
    NOROESTE =          [Movimiento.NORTE, Movimiento.NORTE, Movimiento.OESTE]
    SURESTE =           [Movimiento.SUR, Movimiento.SUR, Movimiento.ESTE]
    SUROESTE =          [Movimiento.SUR, Movimiento.SUR, Movimiento.OESTE]
    IZQUIERDA_ARRIBA =  [Movimiento.OESTE, Movimiento.OESTE, Movimiento.NORTE]
    IZQUIERDA_ABAJO =   [Movimiento.OESTE, Movimiento.OESTE, Movimiento.SUR]
    DERECHA_ARRIBA =    [Movimiento.ESTE, Movimiento.ESTE, Movimiento.NORTE]
    DERECHA_ABAJO =     [Movimiento.ESTE, Movimiento.ESTE, Movimiento.SUR]

    @classmethod
    def getList(self):
        return list(map(lambda c: c.value, MovimientoCaballo))

class MovimientoAlfil(Enum): # 4 posibles direcciones de movimientos de alfil
    NORESTE =   [Movimiento.NORESTE, Movimiento.NORESTE]
    NOROESTE =  [Movimiento.NOROESTE, Movimiento.NOROESTE]
    SURESTE =   [Movimiento.SURESTE, Movimiento.SURESTE]
    SUROESTE =  [Movimiento.SUROESTE, Movimiento.SUROESTE]

    @classmethod
    def getList(self):
        return list(map(lambda c: c.value, MovimientoAlfil))

class bcolors:
    HEADER =    '\033[95m'
    OKBLUE =    '\033[94m'
    OKGREEN =   '\033[92m'
    WARNING =   '\033[93m'
    FAIL =      '\033[91m'
    ENDC =      '\033[0m'
    BOLD =      '\033[1m'
    UNDERLINE = '\033[4m'

def cls():
    os.system("cls" if os.name == "nt" else "clear")


campoJuego = CampoJuego()
campoJuego.crearMatriz("mapa_1.txt")
campoJuego.crearCopiaMatriz()
print("Cantidad de filas: " + str(campoJuego.getCantFilas()))
print("Cantidad de columnas: " + str(campoJuego.getCantColumnas()))

agente = Agente(Posicion(4, 4))
agente.setobjetivosABuscar(["@"]) # objetivos a buscar
agente.iniciar()
