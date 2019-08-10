# Tarea 1 - IA - Snake

import random
import time
import os
from enum import Enum


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

    def registrarMovimiento(self, movimiento_1, movimiento_2):
        self.matriz[movimiento_1.getFila()][movimiento_1.getColumna()] = " " # borrar la posicion anterior
        self.matriz[movimiento_2.getFila()][movimiento_2.getColumna()] = "°"

    def verMatriz(self):
        temp = ""
        for x in range(len(self.matriz)):
            for y in range(len(self.matriz[x])):
                temp += self.matriz[x][y]
            temp += "\n"
        print(temp)


class Agente:
    def __init__(self, pCampo, pPosicion):
        self.campo = pCampo
        self.posicion = pPosicion
        self.direccion = Movimiento.DETENIDO
        self.encendido = True

    def detectarColision(self, fila, columna):
        self.campo.verMatriz()
        if self.campo.getMatriz()[fila][columna] != " ":
            return True # hay colision
        return False

    def elegirDireccion(self):
        return list(Movimiento)[random.randint(1, 8)]

    def avanzar(self, movimiento):
        pos_fila_temp = self.posicion.getFila()
        pos_columna_temp = self.posicion.getColumna()

        if movimiento == Movimiento.ARRIBA:
            pos_fila_temp += 1
        elif movimiento == Movimiento.ABAJO:
            pos_fila_temp -= 1
        elif movimiento == Movimiento.IZQUIERDA:
            pos_columna_temp += 1
        elif movimiento == Movimiento.DERECHA:
            pos_columna_temp += 1
        elif movimiento == Movimiento.ARRIBA_DERECHA:
            pos_fila_temp += 1
            pos_columna_temp += 1
        elif movimiento == Movimiento.ARRIBA_IZQUIERDA:
            pos_fila_temp += 1
            pos_columna_temp -= 1
        elif movimiento == Movimiento.ABAJO_DERECHA:
            pos_fila_temp -= 1
            pos_columna_temp += 1
        elif movimiento == Movimiento.ABAJO_IZQUIERDA:
            pos_fila_temp -= 1
            pos_columna_temp -= 1

        if self.detectarColision(pos_fila_temp, pos_columna_temp) != True:
            self.campo.registrarMovimiento(self.posicion, Posicion(pos_fila_temp, pos_columna_temp))
            self.posicion.setPosicion(pos_fila_temp, pos_columna_temp) # actualizar la posicion
            
            self.campo.verMatriz()
            
            time.sleep(0.2)


    def iniciar(self):
        if (self.posicion.getFila() > self.campo.getCantFilas() - 1) or (self.posicion.getColumna() > self.campo.getCantColumnas() - 1):
            print("Alguna coordenada esta fuera de rango")
            return
        elif self.detectarColision(self.posicion.getFila(), self.posicion.getColumna()) == True:
            print("No puedo iniciar en esa posición")
            return
        else:
            while self.encendido:
                self.avanzar(self.elegirDireccion())


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


class Movimiento(Enum):
    DETENIDO = 0
    ARRIBA = 1 # 8 ejes de movimiento
    ABAJO = 2
    IZQUIERDA = 3
    DERECHA = 4
    ARRIBA_DERECHA = 5
    ARRIBA_IZQUIERDA = 6
    ABAJO_DERECHA = 7
    ABAJO_IZQUIERDA = 8


campoJuego = CampoJuego()
campoJuego.crearMatriz("mapa_1.txt")
print("Cantidad de filas: " + str(campoJuego.getCantFilas()))
print("Cantidad de columnas: " + str(campoJuego.getCantColumnas()))

agente = Agente(campoJuego, Posicion(4, 4))
agente.iniciar()