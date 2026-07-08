# -*- coding: utf-8 -*-
"""
Created on Tue Feb 15 10:36:47 2022

@author: 03207967
"""

#############################################################################

from datetime import datetime
from datetime import timedelta
import sjakk_konstanter as sk

#############################################################################
   
#-----------------------------------------------------------------------------

def naa():
    
        return datetime.now() 

#-----------------------------------------------------------------------------

def tid_til_sek(tid):
    
        temp = str(tid)
        t = int(temp[0])
        m = int(temp[2:4])
        s = int(temp[5:7])
        if len(temp) > 8:
            d = int(temp[8:12])
        else:
            d = 0
        sek = t * 3600 + m * 60 + s + d/10000
        return sek
    
#-----------------------------------------------------------------------------

def sek_til_tid(sekunder):
    
        t = int(sekunder // 3600)
        m = int((sekunder - t * 3600) // 60)
        sd = (sekunder - t * 3600 - m * 60) 
        return str(t)+":"+str(m)+":"+str(sd)[0:7]
  
############################################################################## 

class StoppeKlokke:
    
    """
    Klassen har kunnskap om ..... og gjør...
    Klassen har følgende eksterne metoder:    
    Klassen bruker følgende klasser:
    """

#-----------------------------------------------------------------------------

    def __init__(self):
        
        self._starttid = None 
        self._stopptid = None
        self._hittiltid = None
        self._pausestart =  None
        self._pause = None
        return None     
    
#-----------------------------------------------------------------------------

    def start(self):
        
        self._starttid = datetime.now() 
        self._stopptid = self._starttid
        self._hittiltid = self._starttid
        self._pausestart =  self._starttid
        self._pause = self._starttid - self._starttid
        return None
    
#-----------------------------------------------------------------------------

    def pause(self):
        
        self._pausestart = datetime.now() 
        intervall = self._pausestart - self._starttid - self._pause
        return tid_til_sek(intervall)

#-----------------------------------------------------------------------------

    def fortsett(self):
        
        self._pause = self._pause + datetime.now() - self._pausestart
        return tid_til_sek(self._pause)
    
#-----------------------------------------------------------------------------

    def hittil(self):
        
        self._hittiltid = datetime.now()
        intervall = self._hittiltid - self._starttid - self._pause
        return tid_til_sek(intervall)
    
#-----------------------------------------------------------------------------

    def stopp(self):
        
        self._stopptid = datetime.now()
        intervall = self._stopptid - self._starttid - self._pause
        return tid_til_sek(intervall)
    
  
############################################################################## 
 
class SjakkKlokke:
    
    """
    Klassen har kunnskap om ..... og gjør...
    Klassen har følgende eksterne metoder:    
    Klassen bruker følgende klasser:
    """

#-----------------------------------------------------------------------------

    def __init__(self):
        
        self._tid_hvit = None 
        self._tid_sort  = None
        self._tid_trekk = None
        self._trekk_farge = None
        self._pause = None
        self._pausestart = None
        return None     

#-----------------------------------------------------------------------------

    def start(self, minutter):
        
        self._tid_trekk = datetime.now()
        self._tid_hvit = timedelta(minutes=minutter) 
        self._tid_sort = timedelta(minutes=minutter)
        self._pause = timedelta(0)
        self._trekk_farge = sk.HVIT
        return "", 0, tid_til_sek(self._tid_hvit), tid_til_sek(self._tid_sort)      

#-----------------------------------------------------------------------------

    def sett(self, tidhvit, tidsort, trekkfarge):
        
        self._tid_trekk = datetime.now()
        self._tid_hvit = timedelta(seconds=tidhvit) 
        self._tid_sort = timedelta(seconds=tidsort)
        self._trekk_farge = trekkfarge
        self._pause = timedelta(0)
        return None

#-----------------------------------------------------------------------------

    def skift(self):
        
        tid_trekk = datetime.now() - self._tid_trekk - self._pause
        self._tid_trekk = datetime.now()
        trekk_farge = self._trekk_farge
        if self._trekk_farge == sk.HVIT:
            self._tid_hvit = self._tid_hvit - tid_trekk
            self._trekk_farge = sk.SORT
        else:
            self._tid_sort = self._tid_sort - tid_trekk
            self._trekk_farge = sk.HVIT
        self._pause = timedelta(0)
        return trekk_farge, tid_til_sek(tid_trekk), tid_til_sek(self._tid_hvit), tid_til_sek(self._tid_sort)

#-----------------------------------------------------------------------------

    def status(self):
        
        tid_trekk = datetime.now() - self._tid_trekk - self._pause
        if self._trekk_farge == sk.HVIT:
            tid_hvit = self._tid_hvit - tid_trekk
            tid_sort = self._tid_sort
        else:
            tid_sort = self._tid_sort - tid_trekk
            tid_hvit = self._tid_hvit
        return self._trekk_farge, tid_til_sek(tid_trekk), tid_til_sek(tid_hvit), tid_til_sek(tid_sort)
    
#-----------------------------------------------------------------------------

    def pause(self):
        
        self._pausestart = datetime.now() 
        return None

#-----------------------------------------------------------------------------

    def fortsett(self):
        
        self._pause = self._pause + datetime.now() - self._pausestart
        return None

