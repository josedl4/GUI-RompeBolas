#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Practica 1 de Paradigmas de programacion. Autores: Jose Luis Martin Martin y Daniel Jimenez Cubo.
#objeto game

import random
import gtk
import os, sys
import subprocess
import time

#########
try:
    import pygame
    from pygame.locals import *
    pygame.mixer.init(44100, -16,2,2048)
except:                             #Importamos librerias de Pygame
    print"Pygame no encontrado"
#########

class Game():

    def __init__(self):
        #Incicializamos objeto Game con la matriz de juego y el numero de 0s y puntos actuales
        #inicialmente como valor por defecto a 0
        self.SONIDO_DIR = "music"

        self.mat=[[0 for x in range(9)] for x in range(9)]
        self.nceros=0
        self.puntos=0
        self.puntosfinal=0
        self.njugadas=0

    ###############
    def load_sound(self, nombre, dir_sonido):
        ruta = os.path.join(dir_sonido, nombre)
        # Intentar cargar el sonido
        try:
           sonido = pygame.mixer.Sound(ruta)
        except pygame.error, message:
            print "No se pudo cargar el sonido:", ruta
            sonido = None
        return sonido
    ################


    def reset(self):
        self.mat=[[0 for x in range(9)] for x in range(9)]
        self.nceros=0
        self.puntos=0
        self.puntosfinal=0
        self.njugadas=0

    def numerobolas(self):
        nbolas=0
        for i in range(len(self.mat)):
            for j in range(len(self.mat[0])):
                if(self.mat[i][j]!=0):
                    nbolas += 1
        return nbolas
    
    def facil(self):
        #llena la matriz para el modo facil numeros entre 1-3

        self.nceros=0
        self.puntos=0
        for i in range(len(self.mat)):
            for j in range(len(self.mat[0])):
                self.mat[i][j]= random.randrange(1,4)

    def intermedio(self):
        #llena la matriz para el modo facil numeros entre 1-4
        self.nceros=0
        self.puntos=0
        for i in range(len(self.mat)):
            for j in range(len(self.mat[0])):
                self.mat[i][j]= random.randrange(1,5)

    def dificil(self):
        #llena la matriz para el modo facil numeros entre 1-5

        self.nceros=0
        self.puntos=0
        for i in range(len(self.mat)):
            for j in range(len(self.mat[0])):
                self.mat[i][j]= random.randrange(1,6)

    def tf1(self):
        #llena la matriz para el modo tablero fijo 1

        self.nceros=0
        self.puntos=0
        x=0
        while(x<5): # va recorriendo por capas la matriz y llenandola de cuadrados cada vez ms pequeños
            for i in range(x,len(self.mat)-x,1):
                for j in range(x,len(self.mat[0])-x,1):
                    if(x==0):
                        self.mat[i][j]=1
                    elif(x==1):
                        self.mat[i][j]=2
                    elif(x==2):
                        self.mat[i][j]=3
                    elif(x==3):
                        self.mat[i][j]=1
                    else:
                        self.mat[i][j]=2
            x += 1

    def tf2(self):
        #llena la matriz para el modo tablero fijo 2, llenamos toda la matriz de 4s bolas mas bundantes y el resto
        #se introducen a mano

        self.nceros=0
        self.puntos=0
        for i in range(len(self.mat)):
            for j in range(len(self.mat[0])):
                self.mat[i][j]= 4
        #1
        self.mat[0][4]=1
        self.mat[1][3]=1
        self.mat[1][5]=1
        self.mat[2][6]=1
        self.mat[2][2]=1
        self.mat[3][7]=1
        self.mat[3][1]=1
        self.mat[4][8]=1
        self.mat[4][0]=1
        self.mat[5][1]=1
        self.mat[5][7]=1
        self.mat[6][2]=1
        self.mat[6][6]=1
        self.mat[7][3]=1
        self.mat[7][5]=1
        self.mat[8][4]=1

        self.mat[3][4]=1
        self.mat[4][5]=1
        self.mat[4][3]=1
        self.mat[5][4]=1

        #2
        self.mat[1][4]=2
        self.mat[2][5]=2
        self.mat[2][3]=2
        self.mat[3][2]=2
        self.mat[3][6]=2
        self.mat[4][1]=2
        self.mat[4][7]=2
        self.mat[5][2]=2
        self.mat[5][6]=2
        self.mat[6][3]=2
        self.mat[6][5]=2
        self.mat[7][4]=2

        self.mat[4][4]=2

        #3
        self.mat[2][4]=3
        self.mat[3][5]=3
        self.mat[3][3]=3
        self.mat[4][2]=3
        self.mat[4][6]=3
        self.mat[5][3]=3
        self.mat[5][5]=3
        self.mat[6][4]=3

    def tf3(self):
        #recorre la matriz de la partida y la va llenando en funcion a la pariedad de la suma de sus cordenadas
        #dejando un damero

        self.nceros=0
        self.puntos=0
        for i in range(len(self.mat)):
            for j in range(len(self.mat[0])):
                if(((i+j)%2)==0):
                    self.mat[i][j]=1
                else:
                    self.mat[i][j]=2
        i=random.randrange(0,9)
        j=random.randrange(0,9)
        if(self.mat[i][j]==1): self.mat[i][j]=2         #dejamos un valor que permita jugar ya que sin el no tendriamos movimientos
        else: self.mat[i][j]=1

    def niveloculto(self):
        #llena la matriz de juego para el nivel oculto.

        self.nceros=0
        self.puntos=0
        for i in range(len(self.mat)):
            for j in range(len(self.mat[0])):
                self.mat[i][j]=1
                if(((float(i+j)/2)==i)|((float(i+j)/2)==4)):
                    self.mat[i][j]=4
                if((i==0)|(i==8)):
                    self.mat[i][j]=3
                if((j==0)|(j==8)):
                    self.mat[i][j]=2
        self.mat[0][8]=3

    def mostrar(self, modo, mispuntos):
        #procedimiento para mostrar por pantalla como esta la matriz actual del juego y las puntuaciones actuales e historicas

        if(modo=="facil"):
            x=0
        elif(modo=="intermedio"):
            x=1
        elif(modo=="dificil"):
            x=2
        elif(modo=="tfijo1"):
            x=3
        elif(modo=="tfijo2"):
            x=4
        elif(modo=="tfijo3"):
            x=5
        else:
            x=6

        print "      -----------------------------------"
        for i in range((len(self.mat))-1,-1,-1):
            print (i+1),"  |",
            for j in range(len(self.mat[0])):
                if(self.mat[i][j]==1):
                    #print " 1 ",
                    print "\033[31m ❶ \033[0m",
                elif(self.mat[i][j]==2):
                    #print " 2 ",
                    print "\033[32m ❷ \033[0m",
                elif(self.mat[i][j]==3):
                    #print " 3 ",
                    print "\033[33m ❸ \033[0m",
                elif(self.mat[i][j]==4):
                    #print " 4 ",
                    print "\033[34m ❹ \033[0m",
                elif(self.mat[i][j]==5):
                    #print " 5 ",
                    print "\033[35m ❺ \033[0m",
                else:
                    #print "   ",
                    print " ○ ",

            if(i==7):
                print "|","  La puntuacion actual es",self.puntos
            elif(i==3):
                print "|","  La puntuacion maxima es", mispuntos.listapuntos[x][1]      #segun el modo pasado como parametro cargamos la puntuacion maxima
            else:                                                                       #correspondiente
                print "|"

        print "      -----------------------------------"
        print "       1   2   3   4   5   6   7   8   9 "
        print"\n"

    def cerosup(self):
        #deplaza los ceros a la parte superior de la pantalla

        cer=[0 for x in range(len(self.mat))]       #en una lista de longitud el numero de columnas de la matriz de juego introducimos el numero de
        for i in range(len(self.mat)):              #0s que hay por columna.
            for j in range(len(self.mat[0])):
                if(self.mat[i][j]==0):
                    cer[j]=cer[j]+1

        for x in range(len(self.mat)):              #independientemente de lo que  haya encima de los ceros se despazan las bolas superiores hacia abajo,
            for i in range(len(self.mat)):          #cuando se encuentre un 0. Este proceso se repite hasta estar seguros de no dejar ningun 0 entre medias.
                for j in range(len(self.mat[0])):
                    if(self.mat[i][j]==0):
                        for k in range(i,len(self.mat[0])-1):
                            self.mat[k][j]=self.mat[k+1][j]

        for j in range(len(self.mat[0])):               #finalmente como contamos al principio el numero de 0s por columna y al terminar debemos tener el
            for i in range(len(self.mat)-1,-1,-1):      #mismo numero de 0s los añadimos en las partes superiores de la columna tantos como teniamos en un
                if(cer[j]!=0):                          #principio
                    self.mat[i][j]=0
                    cer[j]=cer[j]-1

    def columns(self):
        #desplaza las columnas hacia la derecha de la pantalla
        c=0
        for j in range(len(self.mat[0])):           #funcionamiento muy similar al utilizado en la funcion cerosup, se cuenta el numero de columnas en el que todos
            x=0                                     #sus elementos son 0s para despues de los desplazamientos el numero de columnas de ceros debe ser el mismo.
            for i in range(len(self.mat)):          #en la variable c se almacenan las columnas todas de 0s
                x=x+self.mat[i][j]
            if(x==0):
                c=c+1

        for r in range(len(self.mat)):
            for j in range(len(self.mat)):          #cada vez que encontramos una columna de ceros desplazamos todas las columnas que tiene a su derecha
                x=0                                 #hacia la izquierda.
                for i in range(len(self.mat[0])):
                    x=x+self.mat[i][j]
                if(x==0):
                    for b in range(j,len(self.mat[0])-1):
                        for a in range(len(self.mat)):
                            self.mat[a][b]=self.mat[a][b+1]

        for j in range(len(self.mat[0])-1,(8-c),-1):        #finalmente introducimos tantas columnas de 0s a la derecha como las que contamos en un principio.
            for i in range(len(self.mat)):
                self.mat[i][j]=0

    def comparar(self,i,j,valor):
        #cuando se realiza una jugada comprueba si es una jugada que reializa alguna modificacion al tablero y elimina bloques de bolas.
        if(self.mat[i][j]!=0):
            if(((j+1)<len(self.mat[0]))):               #comprueba en las 4 posiciones que rodean a cada bola, pueden ser menos si la bola se encuentra en uno
                if((valor==(self.mat[i][j+1]))):        #de los bordes y esquinas
                    self.mat[i][j]=0
                    self.comparar(i,j+1,valor)          #borra la bola del mismo valor que esta junto a la bola señalada y vuelve a llamarse al metodo comprobar
                    if((j+1)<len(self.mat[0])):         #con las cordenadas de donde estaba la bola borrada.
                        self.mat[i][j+1]=0

            if((0<=(j-1))):
                if(valor==(self.mat[i][j-1])):
                    self.mat[i][j]=0
                    self.comparar(i,j-1,valor)
                    if((j-1)>=0):
                        self.mat[i][j-1]=0

            if(((i+1)<len(self.mat))):
                if(valor==(self.mat[i+1][j])):
                    self.mat[i][j]=0
                    self.comparar(i+1,j,valor)
                    if((i+1)<len(self.mat)):
                        self.mat[i+1][j]=0

            if((0<=(i-1))):
                if(valor==(self.mat[i-1][j])):
                    self.mat[i][j]=0
                    self.comparar(i-1,j,valor)
                    if((i-1)>=0):
                        self.mat[i-1][j]=0

    def point(self):
        #funcion encargada de incrementar los puntos en cada jugada.
        x=0
        for i in range(len(self.mat)):              #cuenta el numero de ceros totales en la matriz, y los compara con el momento junto anterior, si hay mayor
            for j in range(len(self.mat[0])):       #numero de ceros calcula los puntos a incrementar por dicha diferencia
                if(self.mat[i][j]==0):
                    x=x+1
        self.puntos=self.puntos+((x-self.nceros)*(x-self.nceros)*5)
        self.nceros=x

    def fin(self, md, mispuntos):
        #funcion encargada de comprobar si se ha llegado al final de la partida,tambien suma los puntos extra por terminar la partida

        end=1
        for i in range(len(self.mat)):          #recorremos la matriz y por cada bola que tengamos comprobamos si alguna de las posibles 4 posiciones a su
            for j in range(len(self.mat[0])):   #alrededor es del mismo valor
                if(self.mat[i][j]!=0):
                    if(((j+1)<len(self.mat[0]))and(self.mat[i][j]==self.mat[i][j+1])):
                        end=0
                    if((0<=(j-1))and(self.mat[i][j]==self.mat[i][j-1])):
                        end=0
                    if(((i+1)<len(self.mat))and(self.mat[i][j]==self.mat[i+1][j])):
                        end=0
                    if((0<=(i-1))and(self.mat[i][j]==self.mat[i-1][j])):
                        end=0

        if(end==1):                                 #si no hay mas movimientos entonces es contamos el numero de bolas y enfuncion de las bolas que nos queden
            print "No hay mas movimientos.\n"       #dependera el numero extra de puntos.
            x=0
            for i in range(len(self.mat)):
                for j in range(len(self.mat[0])):
                    if(self.mat[i][j]!=0):
                        x=x+1

            self.puntosfinal=self.puntos
            if((2000-(x*x*10))>=0):
                self.puntosfinal=self.puntos+(2000-(x*x*10))

            if(mispuntos.listapuntos[md][1]<self.puntosfinal):                   #si has superado la puntuacion maxima del modo la almacena e informa de ello.
                print"Enhorabuena has superado la puntuacion maxima!!!"
                mispuntos.listapuntos[md][1]=self.puntosfinal
                try:
                    sonido_record = self.load_sound("bt_mine.ogg", self.SONIDO_DIR)
                    sonido_record.play()
                except:
                    print "Error Sonido"
            else:
                print "No superaste tu mejor marca."

        return end

    def jugada(self, i,j):
        #funcion que reune varias funciones del objeto game y realiza la simulacion de cada jugada.
        
        #print ""
        valor=self.mat[i][j]
        self.comparar(i,j,valor)                    #llama a la funcion comprobar, cerosup, columns, point, y mostrar.
        self.cerosup()                              #de esta formas elimina bloques, reordena los ceros, incrementa la puntuacion necesraia y muestra el estado
        self.columns()                              #actual del tablero tras la jugada
        self.point()
        #self.mostrar(modo, mispuntos)
        return 1

    def partida(self, modo,mispuntos):
        #simula el funcionamiento de una partida, carga el tablero y va obligando al usuario a realizar jugadas hasta el momento  en que no tengamos mas
        self.puntos=0
        self.nceros=0
        self.mostrar(modo, mispuntos)

        end=0
        while(end==0):
            x=self.jugada(modo,mispuntos)           #en cada jugada no puede retornar un 0 o un 1, si nos llega una 0 significa que se quiere forzar la salida
            end=self.fin(modo, mispuntos)           #y el programa vuelve al menu.
            if(x==0):
                end=2
        if(end==1):
            print "Tu puntuacion final es:",self.puntos,"\n"        #muestra la puntuacion final y pregunta si quiere jugar una nueva partida
            comprobar=False
            while(comprobar==False):
                nueva=raw_input("Nueva partida (1=Si 0=Menu)?  ")
                try:
                    new= int(nueva)
                except:
                    new=2
                if(new==0):
                    comprobar=True
                if(new==1):
                    comprobar=True
            return new
        else:
            return 0
