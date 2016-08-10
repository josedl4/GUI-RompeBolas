#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time

class Resume():

    def __init__(self):
        self.puntos1= "00000"
        self.puntos2= "00000"
        self.bolas= "0"
        self.njugadas= "00"
        self.tiempo= "00:00,00"

    def settiempo(self, time):
        tf= float(time)
        if(tf<300):
            min= int(tf/60)
            sec= int(tf-(min*60))
            mili=tf-(min*60)-sec
            mili=mili*100
            mili=int(mili)
            cad = str(min)+"' : "+str(sec)+"'' , "+str(mili)
            self.tiempo=cad
            print self.tiempo
        else:
            self.tiempo ="+5 min"
            print self.tiempo

