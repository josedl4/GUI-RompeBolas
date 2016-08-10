#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Practica 1 de Paradigmas de programacion. Autores: Jose Luis Martin Martin y Daniel Jimenez Cubo.
#objeto ranking

class Ranking():

    def __init__(self):
        #incializacion del objeto ranking, contine una lista con los modos de juegos y sus mejores puntuaciones.
        self.listapuntos=[["Facil: ",0],["Intermedio: ",0],["Dificil: ",0],["Tablero Fijo 1: ",0],["Tablero Fijo 2: ",0],["Tablero Fijo 3: ",0],["Nivel oculto: ",0]]
        try:
            fread=open("puntuaciones.txt")              #abre el archivo y lee las maximas puntuaciones que guarda en la lista en sus respectivos modos.

            for i in range(len(self.listapuntos)):
                try:
                    self.listapuntos[i][1]=int(fread.readline())
                except:
                    self.listapuntos[i][1]=0
        except:
            print "No hay archivo exixtente se creara nuevo archivo."       #si no puede acceder al archivo informa al usuario y partimos con todas las puntuaciones a 0

    def mostrar(self):
        print "\n\tEl Ranking de maximas pruntuaciones es: "        #mostramos la lista de puntuaciones recorriendo el modo de juego y junto a el su puntuacion
        print "\t_______________________________________\n"         #maxima.
        for i in range(len(self.listapuntos)):
            for j in range(len(self.listapuntos[0])):
                if(i==0):
                    print self.listapuntos[i][j],"\t\t",
                elif(i==1):
                    print self.listapuntos[i][j],"\t\t",
                elif(i==2):
                    print self.listapuntos[i][j],"\t\t",
                elif(i==6):
                    print self.listapuntos[i][j],"\t\t",
                else:
                    print self.listapuntos[i][j],"\t",
            print ""

    def borrar(self):
        for i in range(len(self.listapuntos)):          #recorre las posiciones de la lista de puntos y las devuelve a 0
            self.listapuntos[i][1]=0
        print "Se han borrado las puntuaciones."

    def guardar(self):
        fwrite=open("puntuaciones.txt", "w")            #guarde de nuevo las puntuaciones en el archivo al terminar la partida, sobrescribiendo lo anterior
        for i in range(len(self.listapuntos)):
            puntos=str(self.listapuntos[i][1])
            fwrite.write(puntos+"\n")
        fwrite.close()

    def niveloculto(self):
        activar = True                                  #comprobante de que se puede acceder al nivel oculto, simplenete comprueba que en todas las puntuaciones
        for i in range(len(self.listapuntos)-1):        #menos la del nivel oculto la puntuacion sea distinta de 0
            if (self.listapuntos[i][1]==0):
                activar = False

        return activar
