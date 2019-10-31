# Tarea 1 - IA - ITCR - Agente
# José Navarro - Josué Suárez

import random
import time
from enum import Enum
import os
        
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

class Agente:
    def __init__(self, pCampo, pPosicion):
        self.agente = "❇"
        self.campo = pCampo
        self.posicion = pPosicion
        self.encendido = True

    def detectarColision(self, fila, columna):
        if (self.campo.getMatriz()[fila][columna] != " "):
            print(bcolors.WARNING + "Colisión detectada: ("  + str(fila) + ", " + str(columna) + ")" + bcolors.ENDC)
            return True # Hay colision

    def evaluarMovimiento(self, listaMovimientos):
        posicionMovimiento = {"fila": self.posicion.getFila(), "columna": self.posicion.getColumna()}
        for movimiento in listaMovimientos:
            posicionMovimiento = self.getPosicionDelMovimiento(movimiento, posicionMovimiento["fila"], posicionMovimiento["columna"])
            if (self.detectarColision(posicionMovimiento["fila"], posicionMovimiento["columna"])): 
                return False # No se puede dar el movimiento
        return True

    # Retorna el primer movimiento encontrado que sea válido de acuerdo al tipo de movimiento.
    # El valor de retorno es la fila y columna a mover
    def selecTipoMovimiento(self, numeroMov):
        for i in range(8):
            if numeroMov == "1":
                movimiento = random.choice(list(MovimientoRey)) #[random.randint(0, 7)]
            elif numeroMov == "2":
                movimiento = random.choice(list(MovimientoCaballo))
            elif numeroMov == "3":
                movimiento = random.choice(list(MovimientoAlfil))
            else:
                return []
            
            if self.evaluarMovimiento(movimiento.value): # Movimiento valido
                return movimiento.value
        return []
        #return self.selecTipoMovimiento(numeroMov) # iterar recursivamente hasta encontrar uno válido

    def getPosicionDelMovimiento(self, movimiento, pos_fila_temp, pos_columna_temp):
        mensajeSensor = bcolors.OKBLUE + "Sensor: " + bcolors.ENDC
        if isinstance(movimiento.value[0], list):
            pos_fila_temp += movimiento.value[0][0]
            pos_columna_temp += movimiento.value[0][1]
            mensajeSensor += movimiento.name
        return {"fila": pos_fila_temp, "columna": pos_columna_temp, "sensor": mensajeSensor}
    
    def avanzar(self, listaMovimientos):
        posicionMovimiento = {"fila": self.posicion.getFila(), "columna": self.posicion.getColumna()}
        for movimiento in listaMovimientos:
            posicionMovimiento = self.getPosicionDelMovimiento(movimiento, posicionMovimiento["fila"], posicionMovimiento["columna"])
            self.registrarMovimiento(self.posicion, Posicion(posicionMovimiento["fila"], posicionMovimiento["columna"]), posicionMovimiento["sensor"])
            self.posicion.setPosicion(posicionMovimiento["fila"], posicionMovimiento["columna"]) # Actualizar la posicion
            
            print(posicionMovimiento["sensor"]) 
            self.campo.verMatriz()
            time.sleep(1.5)
            cls()

    def registrarMovimiento(self, movimiento_1, movimiento_2, sensor): # movimiento_1: pos actual, movimiento_2: pos a mover
        self.campo.matriz[movimiento_1.getFila()][movimiento_1.getColumna()] = " " # borrar la posicion anterior
        self.campo.matriz[movimiento_2.getFila()][movimiento_2.getColumna()] = self.agente # ☻
        print("Posición actual: (" + str(movimiento_1.getFila()) + ", " + str(movimiento_1.getColumna()) + ")")        
        print("Siguiente posición: (" + str(movimiento_2.getFila()) + ", " + str(movimiento_2.getColumna()) + ")")  

    def iniciar(self):
        if (self.posicion.getFila() > self.campo.getCantFilas() - 1) or (self.posicion.getColumna() > self.campo.getCantColumnas() - 1):
            print("Alguna coordenada esta fuera de rango")
            return
        elif self.detectarColision(self.posicion.getFila(), self.posicion.getColumna()) == True:
            print("No puedo iniciar en esa posición")
            return
        else:
            while(self.encendido):
                opcionMovimiento = input("\nSeleccione el movimiento a utilizar \n [1] Rey \n [2] Caballo \n [3] Alfil \n $")
                while True:
                    listaMovimientos = self.selecTipoMovimiento(opcionMovimiento)
                    if listaMovimientos != []:                   
                        self.avanzar(listaMovimientos)
                    else:
                        print("\nNo es posible realizar ese movimiento, intente con otro.")
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
    DETENIDO =  [0, 0],
    ARRIBA =    [-1, 0], 
    ABAJO =     [1, 0],
    IZQUIERDA = [0, -1],
    DERECHA =   [0, 1],
    NORESTE =   [-1, 1],
    NOROESTE =  [1, -1],
    SURESTE =   [1, 1],
    SUROESTE =  [-1, -1]

class MovimientoRey(Enum):
    ARRIBA =    [Movimiento.ARRIBA]
    ABAJO =     [Movimiento.ABAJO]
    IZQUIERDA = [Movimiento.IZQUIERDA]
    DERECHA =   [Movimiento.DERECHA]
    NORESTE =   [Movimiento.NORESTE]
    NOROESTE =  [Movimiento.NOROESTE]
    SURESTE =   [Movimiento.SURESTE]
    SUROESTE =  [Movimiento.SUROESTE]

class MovimientoCaballo(Enum): # 8 posibles direcciones de movimientos de caballo
    NORESTE =           [Movimiento.ARRIBA, Movimiento.ARRIBA, Movimiento.DERECHA]
    NOROESTE =          [Movimiento.ARRIBA, Movimiento.ARRIBA, Movimiento.IZQUIERDA]
    SURESTE =           [Movimiento.ABAJO, Movimiento.ABAJO, Movimiento.DERECHA]
    SUROESTE =          [Movimiento.ABAJO, Movimiento.ABAJO, Movimiento.IZQUIERDA]
    IZQUIERDA_ARRIBA =  [Movimiento.IZQUIERDA, Movimiento.IZQUIERDA, Movimiento.ARRIBA]
    IZQUIERDA_ABAJO =   [Movimiento.IZQUIERDA, Movimiento.IZQUIERDA, Movimiento.ABAJO]
    DERECHA_ARRIBA =    [Movimiento.DERECHA, Movimiento.DERECHA, Movimiento.ARRIBA]
    DERECHA_ABAJO =     [Movimiento.DERECHA, Movimiento.DERECHA, Movimiento.ABAJO]

class MovimientoAlfil(Enum): # 4 posibles direcciones de movimientos de alfil
    NORESTE =   [Movimiento.NORESTE, Movimiento.NORESTE]
    NOROESTE =  [Movimiento.NOROESTE, Movimiento.NOROESTE]
    SURESTE =   [Movimiento.SURESTE, Movimiento.SURESTE]
    SUROESTE =  [Movimiento.SUROESTE, Movimiento.SUROESTE]

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
print("Cantidad de filas: " + str(campoJuego.getCantFilas()))
print("Cantidad de columnas: " + str(campoJuego.getCantColumnas()))

agente = Agente(campoJuego, Posicion(4, 4))
agente.iniciar()
