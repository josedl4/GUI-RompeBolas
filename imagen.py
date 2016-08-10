#!/usr/bin/python
# -*- coding: utf-8 -*-


import gtk
import os, sys
import subprocess
import time
import PIL
from PIL import Image
import random


class Foto():

    def __init__(self):
        for i in range(1,6):
            self.im = Image.open("fondos/fondo"+str(i)+".jpg")
            self.matriz(self.im, 9, i)

    def cortarImagen(self,im, a, b, x, y, cor_i, cor_j, ruta):
	region = im.crop((a,b,x,y))

        i = region.size[0]
        j = region.size[1]
        
        reg = region.resize((30, 30), Image.ANTIALIAS)
	
	rut="fondo"+str(ruta)+"/region"+str(cor_i)+str(cor_j)+".jpg"
	reg.save(rut)

    def matriz(self, im, n, ruta):
        x=im.size[0]
        y=im.size[1]
        tx= x/n
        ty= y/n
    
        a=0
        b=0
    
        tam_x=tx
        tam_y=ty
        num=0
    
        for i in range(n):
            for j in range(n):
                self.cortarImagen(im, a, b, tam_x, tam_y, (8-i),j, ruta)
                a += tx
                tam_x += tx
                num+=1
            a=0
            tam_x=tx
            b += ty
            tam_y += ty


        



