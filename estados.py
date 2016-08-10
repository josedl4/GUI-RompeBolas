#!/usr/bin/python
# -*- coding: utf-8 -*-

import gtk
import os, sys
import subprocess
import time
from imagen import Foto
import random
import gobject

#########
try:
    import pygame
    from pygame.locals import *
    pygame.mixer.init(44100, -16,2,2048)
except:                             #Importamos librerias de Pygame
    print"Pygame no encontrado"
#########

from game import Game
from rank import Ranking
from resume import Resume


class control_tablero():
   
    def __init__(self, matriz, puntos, modo):
        ruta = random.randrange(1,6)
        self.rutacom="fondo"+str(ruta)
        self.SONIDO_DIR = "music"
        self.time1=time.time()
        self.matriz=matriz
        self.puntos=puntos
        self.modo=modo
        self.resumen = Resume()
        
        self.glade=gtk.Builder()
        self.glade.add_from_file('tablero.glade')
        self.ventana=self.glade.get_object('win_tab')
        self.tabla=self.glade.get_object('tabla_juego')
	

        ###################
        for i in range(9):
            label = gtk.Label()
            label.set_text(str(self.convertircoordenadas(i,9)+1))
            self.tabla.attach(label,0,1,i,i+1,gtk.EXPAND,gtk.EXPAND,0,0)
            label.show()
        for i in range(9):
            label = gtk.Label()
            label.set_text(str(i+1))
            self.tabla.attach(label,i+1,i+2,9,10,gtk.EXPAND,gtk.EXPAND,0,0)
            label.show()
	####################
        band=0
        self.bolas = [gtk.Button() for x in range(81)]

        for i in range(1,10):
            for j in range(9):
                boton = gtk.Button()
                cad=str(band)
                
                #cad=(str(self.convertircoordenadas(j,10))+", "+str(i))
                #boton.set_label(cad)
                boton.connect("clicked",self.on_bola_clicked)
                self.bolas[band]= boton
                
                self.tabla.attach(boton,i,i+1,j,j+1,gtk.FILL,gtk.FILL,0,0)
                boton.show()
                band += 1

	####################
        if(self.modo==0):
            self.matriz.facil()
        elif(self.modo==1):
            self.matriz.intermedio()
        elif(self.modo==2):
            self.matriz.dificil()
        elif(self.modo==3):
            self.matriz.tf1()
        elif(self.modo==4):
            self.matriz.tf2()
        elif(self.modo==5):
            self.matriz.tf3()
            
            
        self.llenar()        
        self.glade.connect_signals(self)
        self.ventana.show_all()

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

    def convert(self, numero):
        cor =[0, 0]
        band=0
        for j in range(1,10):
            for i in range(9,0,-1):
                if(band==numero):
                    cor[0]=i
                    cor[1]=j
                band +=1
        #print "convert",str(numero),"es",str(cor[0]),str(cor[1])
        return cor

    def llenar(self):
        for z in range(len(self.bolas)):
            cor=self.convert(z)
            i=cor[0]-1
            j=cor[1]-1

            if(self.matriz.mat[i][j]==1):
                rojo = gtk.Image()
                rojo.set_from_file("icons/ball-red-min.png")
                self.bolas[z].set_image(rojo)
            elif(self.matriz.mat[i][j]==2):
                amarillo = gtk.Image()
                amarillo.set_from_file("icons/ball-yel-min.png")
                self.bolas[z].set_image(amarillo)
            elif(self.matriz.mat[i][j]==3):
                verde = gtk.Image()
                verde.set_from_file("icons/ball-green-min.png")
                self.bolas[z].set_image(verde)
            elif(self.matriz.mat[i][j]==4):
                azul = gtk.Image()
                azul.set_from_file("icons/ball-blue-min.png")
                self.bolas[z].set_image(azul)
            elif(self.matriz.mat[i][j]==5):
                morado = gtk.Image()
                morado.set_from_file("icons/ball-purple-min.png")
                self.bolas[z].set_image(morado)
            else:
                try:
                    cad=self.rutacom+"/region"+str(i)+str(j)+".jpg"
                    im=gtk.Image()
                    im.set_from_file(cad)
                    self.bolas[z].set_image(im)
                except:
                    blanco = gtk.Image()
                    blanco.set_from_file("icons/ball-hollow-min.png")
                    self.bolas[z].set_image(blanco)

        et1=self.glade.get_object('punt_max')
        et1.set_text(str(self.puntos.listapuntos[self.modo][1]))
        et2=self.glade.get_object('punt_act')
        et2.set_text(str(self.matriz.puntos))       

    def on_bola_clicked(self,widget):
        prebolas = self.matriz.nceros           
        self.matriz.njugadas += 1
        
        for i in range(len(self.bolas)):
            if(self.bolas[i]==widget):
                pos=i
        cor=self.convert(pos)
        i=cor[0]-1
        j=cor[1]-1
        
        print "Jugada"
        self.matriz.jugada(i,j)
        postbolas = self.matriz.nceros
        
        if(prebolas != postbolas):
            try:
                sonido_jugada = self.load_sound("bubble.ogg", self.SONIDO_DIR)
                sonido_jugada.play()
            except:
                print "Error Sonido"
        else:
            try:
                sonido_jugada = self.load_sound("tea.ogg", self.SONIDO_DIR)
                sonido_jugada.play()
            except:
                print "Error Sonido"

        self.llenar()

        fin=self.matriz.fin(self.modo, self.puntos)

        if(fin==1):
            #lanzamos fin de partida
            self.resumen.puntos1=str(self.matriz.puntos)
            self.resumen.puntos2=str(self.matriz.puntosfinal)
            self.resumen.bolas=str(self.matriz.numerobolas())
            self.resumen.njugadas=str(self.matriz.njugadas)
            time2=time.time()
            tiempo = time2-self.time1
            self.resumen.settiempo(tiempo)
            
            print "fin partida"
            self.matriz.reset()

            nex=control_nueva(self.matriz,self.puntos,self.modo,self.resumen, self.ventana)
            
        
    
    def on_button1_clicked(self,widget):
        # Para las señales nos envían sólo el widget
        print "Pulsación en el botón"

    def on_bt_salir_clicked(self,widget):
        self.tab2menu()
        print "Pulsación en el botón salir"

    def on_win_tab_delete_event(self,widget,event):
        print "Señal para cerrar la ventana"
        gtk.main_quit()
        print "Fuera del bucle de control de eventos"
    
    def convertircoordenadas(self, i, maximo):
		return (maximo-1-i)

    def tab2menu(self):
		self.ventana.destroy()
		next=control_menu(self.matriz, self.puntos)

    def mostrar(self, matriz):
        print "Motrar matriz"

class control_menu():
   
    def __init__(self,  matriz, puntos):
        self.puntos=puntos
        self.matriz=matriz
        self.glade=gtk.Builder()
        self.glade.add_from_file('MenuPrincipal.glade')
        self.ventana=self.glade.get_object('vista_menuprincipal')
        self.glade.connect_signals(self)
        self.ventana.show_all()
    
    def on_bt_exit_clicked(self,widget):
        print "Pulsación en el botón"
        self.puntos.guardar()
        gtk.main_quit()

  
    def on_bt_mf_clicked(self,widget):
	self.menu2tab(0)
	print "Modo Facil"

    def on_bt_mi_clicked(self,widget):
	self.menu2tab(1)
	print "Modo Intermedio"

    def on_bt_md_clicked(self,widget):
	self.menu2tab(2)
	print "Modo Dificil"

    def on_bt_sm_clicked(self,widget):
	self.menu2sub()
	print "Sub Menu"

    def on_bt_mp_clicked(self,widget):
	self.menu2mp()
	print "Maximas Puntuaciones"

    def on_bt_bp_clicked(self,widget):
        widget = self.ventana
        widget.set_sensitive(False)
	next=control_borrar(widget,self.puntos)
	print "Borrar Puntuaciones"
  
    def on_vista_menuprincipal_delete_event(self,widget,event):
        print "Señal para cerrar la ventana"
        gtk.main_quit()
        print "Fuera del bucle de control de eventos"

    def menu2tab(self,modo):
        next=control_tablero(self.matriz, self.puntos,modo)	
        self.ventana.destroy()

    def menu2sub(self):
        next=control_sub_menu(self.matriz, self.puntos)
        self.ventana.destroy()

    def menu2mp(self):
        next=control_max_pun(self.matriz, self.puntos)
        self.ventana.destroy()

class control_sub_menu():
   
    def __init__(self,matriz,puntos):
        self.matriz=matriz
        self.puntos=puntos
        self.glade=gtk.Builder()
        self.glade.add_from_file('submenu.glade')
        self.ventana=self.glade.get_object('sub_menu')
        self.glade.connect_signals(self)
        self.ventana.show_all()
    
    def on_bt_volver_clicked(self,widget):
        self.ventana.destroy()
        next=control_menu(self.matriz, self.puntos)

  
    def on_bt_cuadrado_clicked(self,widget):
	self.menu2tab(3)
	print "Modo Cuadrado"
	
    def on_bt_rombo_clicked(self,widget):
        self.menu2tab(4)
        print "Modo Rombo"

    def on_bt_damero_clicked(self,widget):
	self.menu2tab(5)
	print "Modo Damero"
  
    def on_sub_menu_delete_event(self,widget,event):
        print "Señal para cerrar la ventana"
        gtk.main_quit()
        print "Fuera del bucle de control de eventos"

    def menu2tab(self,modo):
	next=control_tablero(self.matriz, self.puntos,modo)	
	self.ventana.destroy()

class control_max_pun():
   
    def __init__(self, matriz, puntos):
        self.matriz=matriz
        self.puntos=puntos
        self.glade=gtk.Builder()
        self.glade.add_from_file('maximas_pun.glade')
        self.ventana=self.glade.get_object('max_pun')

        self.et1=self.glade.get_object('label1')
        self.et1.set_text(str(self.puntos.listapuntos[0][1]))
        self.et2=self.glade.get_object('label2')
        self.et2.set_text(str(self.puntos.listapuntos[1][1]))
        self.et3=self.glade.get_object('label3')
        self.et3.set_text(str(self.puntos.listapuntos[2][1]))
        self.et4=self.glade.get_object('label4')
        self.et4.set_text(str(self.puntos.listapuntos[3][1]))
        self.et5=self.glade.get_object('label5')
        self.et5.set_text(str(self.puntos.listapuntos[4][1]))
        self.et6=self.glade.get_object('label6')
        self.et6.set_text(str(self.puntos.listapuntos[5][1]))
        
        self.glade.connect_signals(self)
        self.ventana.show_all()
    
    def on_bt_volver_clicked(self,widget):
        self.ventana.destroy()
        next=control_menu(self.matriz, self.puntos)
  
    def on_max_pun_delete_event(self,widget,event):
        print "Señal para cerrar la ventana"
        gtk.main_quit()
        print "Fuera del bucle de control de eventos"

class control_borrar():      #Ventana Emergente
   
    def __init__(self, x, puntos):
        self.puntos=puntos
        self.menu=x
        self.glade=gtk.Builder()
        self.glade.add_from_file('borrar.glade')
        self.ventana=self.glade.get_object('borrar_pun')
        self.glade.connect_signals(self)
        self.ventana.show_all()
    
    def on_bt_no_clicked(self,widget):
        self.ventana.destroy()
        self.menu.set_sensitive(True)

    def on_bt_si_clicked(self,widget):
        print "Puntuaciones borradas"
        self.puntos.borrar()
        self.ventana.destroy()
        self.menu.set_sensitive(True)
  
    def on_borrar_pun_delete_event(self,widget,event):
        print "Señal para cerrar la ventana"
        self.ventana.destroy()
        self.menu.set_sensitive(True)

class control_nueva():      #Ventana Emergente
   
    def __init__(self, matriz, puntos, modo, estado, anterior):
        self.pre=anterior
        self.pre.set_sensitive(False)
        self.matriz=matriz
        self.puntos=puntos
        self.modo=modo
        self.estado=estado

        
        
        self.glade=gtk.Builder()
        self.glade.add_from_file('nueva.glade')
        self.ventana=self.glade.get_object('nueva')
        et1=self.glade.get_object('puntos1')
        et1.set_text(self.estado.puntos1)
        et2=self.glade.get_object('puntos2')
        et2.set_text(self.estado.puntos2)
        et3=self.glade.get_object('bolas')
        et3.set_text(self.estado.bolas)
        et4=self.glade.get_object('jugadas')
        et4.set_text(self.estado.njugadas)
        et5=self.glade.get_object('tiempo')
        et5.set_text(self.estado.tiempo)
        self.glade.connect_signals(self)
        self.ventana.show_all()
    
    def on_bt_no_clicked(self,widget):
        self.pre.destroy()
        next=control_menu(self.matriz, self.puntos)
        self.ventana.destroy()

    def on_bt_si_clicked(self,widget):
        self.pre.destroy()
        next=control_tablero(self.matriz, self.puntos, self.modo)
        self.ventana.destroy()
  
    def on_nueva_delete_event(self,widget,event):
        self.ventana.destroy()

class control_inicio():      #Ventana Emergente
   
    def __init__(self, mimatriz, mispuntos):
        self.matriz = mimatriz
        self.puntos = mispuntos

        self.glade=gtk.Builder()
        self.glade.add_from_file('inicio.glade')
        self.ventana=self.glade.get_object('ventana_inicio')
        self.glade.connect_signals(self)
        self.ventana.show_all()

        #######
        gobject.timeout_add(70,self.cargar)
        #######
        
        siguiente=control_menu(mimatriz, mispuntos)

    def cargar(self):
        crear=True
        for i in range(1,6):
            ficheros = os.listdir("fondo"+str(i))
            if (len(ficheros)==81):
                print "fondo"+str(i),"si tiene"
            else:
                crear=False
                
        if(crear==False):
            mifoto = Foto()
        else:
            time.sleep(2)
        self.ventana.destroy()


if __name__=='__main__':
    #Objeros de puntuaciones y tableros#
    
    mimatriz= Game()
    mispuntos= Ranking()
    
    #   #   #
        
    app=control_inicio(mimatriz, mispuntos)
    gtk.main()


