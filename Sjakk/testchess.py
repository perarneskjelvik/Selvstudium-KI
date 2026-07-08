# -*- coding: utf-8 -*-
"""
Created on Mon Mar  7 12:56:59 2022

@author: 0320

"""


import time
import chess
import sjakk_konstanter as sk
import tid

"""
    
There are different ways castling moves may be encoded. 
The normal way to do it is e1g1 for short castling. 
However this is not always unique in Chess960. 
Therefore python-chess will consistently encode castling moves as a king move to the corresponding rook, 
i.e. e1h1 for normal kingside castling.
    
"""

#############################################################################

class Sjakktest: 

#-----------------------------------------------------------------------------
 
    def __init__(self, ui, motor):
        
        for i in range (0, 5):
            try:
                self.fil = open("debug.txt", "w")
                break
            except:
                time.sleep(3) # Sleep for 3 seconds
        
        for i in range (0, 5):
            try:
                self.fil.close()
                break
            except:
                time.sleep(3) # Sleep for 3 seconds
                
        
        self.brett = chess.Board()
        self.ui = ui
        self.motor = motor
        self.temp1 = 3
        
        self.antall_trekk_1 = 0
        self.antall_trekk_2 = 0
        self.tid_1 = 0
        self.tid_2 = 0
       
        return None
    
#-----------------------------------------------------------------------------
 
    def sett_start(self, fen):
    
        self.brett = chess.Board(fen)
        return None  
    
#-----------------------------------------------------------------------------

    def debug(self, tekst):
        
        # åpner filan debug.txt, skriver en linje (tekst), lukker filen.
        
        for i in range (0, 5):
            try:
                self.fil = open("debug.txt", "a")
                break
            except:
                time.sleep(3) # Sleep for 3 seconds
                
            
        tekst = tekst + "\n"      
        
        for i in range (0, 5):
            try:
                self.fil.write(tekst)
                break
            except:
                time.sleep(3) # Sleep for 3 seconds
        
        for i in range (0, 5):
            try:
                self.fil.close()
                break
            except:
                time.sleep(3) # Sleep for 3 seconds
        
        return None

#-----------------------------------------------------------------------------

    def trekk(self, trekk):
        
        x = trekk.x0
        y = trekk.y0
        fra = chr(x+97) + chr(y+49) 
        x = trekk.x1
        y = trekk.y1
        til = chr(x+97) + chr(y+49) 
        
        if trekk.bondeforvandling != "":
            b = trekk.bondeforvandling
            b = b.replace("T", "r")
            b = b.replace("t", "r")
            b = b.replace("S", "n")
            b = b.replace("s", "n")
            b = b.replace("L", "b")
            b = b.replace("l", "b")
            b = b.replace("D", "q")
            b = b.replace("d", "q")
            til = til + b
        
        uci = chess.Move.from_uci(fra+til)
        self.brett.push(uci)
        
        #self.debug(f"Trekk: {fra} {til}")
        
        return None
    
#----------------------------------------------------------------------------

    def _print_stilling_og_trekk(self, trekk):
        
        x = trekk.x0
        y = trekk.y0
        fra = chr(x+97) + chr(y+49) 
        x = trekk.x1
        y = trekk.y1
        til = chr(x+97) + chr(y+49) 
        
        fen1 = self.brett.fen(en_passant="fen")
        fen2 = self.motor._stilling.hent_FEN()
        print(f"Trekk: {fra} {til}")
        print(f"{self.brett}")
        print(fen1)
        print(fen2) 

        return None
    
#-----------------------------------------------------------------------------

    def trekk_tilbake(self):
        
        move = self.brett.pop()
        
        return None
    
#----------------------------------------------------------------------------- 
    
    def test_mulige_trekk (self, mulige_trekk):
        
        feil = False
        
        # henter brettet før neste trekk og skriver ut brett og antall brikker til debug
        
        """
        self.debug("STILLING ETTER TREKK")
        self.debug("Resultat: " + self.motor._stilling._skjema.hent_resultat())
        self.debug("Vinner: " + self.motor._stilling._skjema.vinner)
        b = self.motor._stilling._skjema.hent_brett()
        self.debug(f"{self.brett}")
        self.debug(f"{b.hvit_antall_dronninger_og_taarn}")
        self.debug(f"{b.hvit_antall_boender}")
        self.debug(f"{b.hvit_antall_loepere}")
        self.debug(f"{b.hvit_antall_springere}")
        self.debug(f"{b.sort_antall_dronninger_og_taarn}")
        self.debug(f"{b.sort_antall_boender}")
        self.debug(f"{b.sort_antall_loepere}")
        self.debug(f"{b.sort_antall_springere}")
        
        """
          
        # tester alle status og skriver til debug hvis feil
        
        feil = False
        fen1 = self.brett.fen(en_passant="fen")
        fen2 = self.motor._stilling.hent_FEN()
        
        if fen1 != fen2:
            self.debug("Feil FEN") 
            feil = True
        if self.motor._stilling._skjema.er_remis_5() != self.brett.is_fivefold_repetition():
            self.debug("Feil remis 5")
            feil = True
        if self.motor._stilling._skjema.er_remis_75() != self.brett.is_seventyfive_moves():
            self.debug("Feil remis 75")
            feil = True
        if self.motor._stilling._skjema.er_remis_materiell() != self.brett.is_insufficient_material():
             self.debug("Feil remis materiell")
             feil = True
        if self.motor._stilling._skjema.er_remis_patt() != self.brett.is_stalemate():
             self.debug("Feil remis patt")
             feil = True
        if self.motor._stilling._skjema.er_sjakk_matt() != self.brett.is_checkmate():
            self.debug("Feil sjakk matt")
            feil = True
       
             
        # tester mulige trekk i denne stillingen
        
       
        antall2 = len(mulige_trekk) # antall mulige trekk funnet av motor
        
       
        self.antall_trekk_2 = antall2 + self.antall_trekk_2 
        
        temp1 = [] # liste med mulge trekk funnet av motor
        
        for i in range(0, len(mulige_trekk)): 
            x = mulige_trekk[i].x0
            y = mulige_trekk[i].y0
            fra = chr(x+97) + chr(y+49) 
            x = mulige_trekk[i].x1
            y = mulige_trekk[i].y1
            til = chr(x+97) + chr(y+49) 
            if mulige_trekk[i].bondeforvandling != "":
                b = mulige_trekk[i].bondeforvandling
                b = b.replace("T", "r")
                b = b.replace("t", "r")
                b = b.replace("S", "n")
                b = b.replace("s", "n")
                b = b.replace("L", "b")
                b = b.replace("l", "b")
                b = b.replace("D", "q")
                b = b.replace("d", "q")
                b = b.lower()
                til = til + b
            temp1.append(fra+til)    
        temp1.sort()
        
        
        klokke = tid.StoppeKlokke()
        klokke.start()
        
        antall = self.brett.legal_moves.count() # antall trekk i fasit
        
        self.antall_trekk_1 = antall + self.antall_trekk_1
        
        temp2 = list(self.brett.legal_moves) # liste med mulige trekk i fasit
        
        self.tid_1 = klokke.stopp() + self.tid_1
        
        #print(f"Antall trekk i denne stillingen: {antall} {antall2}")
        
        #print(f"Akkumulert antall trekk: {self.antall_trekk_1} {self.antall_trekk_2}")
        
        temp3 = [] # liste med trekk i fasit som kan sammenlignes med liste funnat av motor
        for i in range(0, antall): 
            temp3.append(str(temp2[i]))    
        temp3.sort()
      
        if antall != antall2:
            print("Feil i antall mulige trekk i denne stillingen. Se brett under.")
            print(f"Antall trekk i denne stillingen fasit/motor: {antall} {antall2}")
            b = self.motor._stilling._skjema.hent_brett()
            print(f"{b.ASCII()}")
            print("Fasit Feil")
            self.debug("Feil i antall mulige trekk i denne stillingen.")
            feil = True
        else:
            #print("Riktig antall mulige trekk i denne stillingen. Se brett under.")
            #print(f"Antall trekk i denne stillingen motor/fasit: {antall} {antall2}")
            b = self.motor._stilling._skjema.hent_brett()
            #print(f"{b.ASCII()}")
            #print("Fasit Feil")
            #self.debug("Feil i antall mulige trekk i denne stillingen.")
            
    
        for i in range(0, min(antall, antall2)): 
            if temp3[i] != temp1[i]:
                #print(f"{temp3[i]} {temp1[i]}")
                self.debug("Feil i antall mulige trekk i denne stillingen.")
                feil = True
            #else:
            
                #print(f"{temp3[i]} {temp1[i]}")
        
        if feil:
            self.debug("STILLING ETTER TREKK")
            self.debug("Resultat: " + self.motor._stilling._skjema.hent_resultat())
            self.debug("Vinner: " + self.motor._stilling._skjema.vinner)
            b = self.motor._stilling._skjema.hent_brett()
            self.debug(f"{self.brett}")
            self.debug(f"{b.hvit_antall_dronninger_og_taarn}")
            self.debug(f"{b.hvit_antall_boender}")
            self.debug(f"{b.hvit_antall_loepere}")
            self.debug(f"{b.hvit_antall_springere}")
            self.debug(f"{b.sort_antall_dronninger_og_taarn}")
            self.debug(f"{b.sort_antall_boender}")
            self.debug(f"{b.sort_antall_loepere}")
            self.debug(f"{b.sort_antall_springere}")
            self.debug(fen1)
            self.debug(fen2) 
            self.debug(self.motor.hent_status())
            self.debug(f"Trekk nr: {self.brett.fullmove_number}")
            self.debug(f"Halvtrekk nr: {self.brett.ply()}")
            self.debug(f"Remis 5: {self.brett.is_fivefold_repetition()}")
            self.debug(f"Remis 75: {self.brett.is_seventyfive_moves()}")
            self.debug(f"Remis material: {self.brett.is_insufficient_material()}")
            self.debug(f"Remis patt: {self.brett.is_stalemate()}")
            self.debug(f"Sjakkmatt: {self.brett.is_checkmate()}")
            res = self.brett.outcome()
            self.debug(f"Resultat: {res}")
            input("Stillingen inneholder feil.")
      
        
        return None
    
#----------------------------------------------------------------------------- 
    
    def test_sluttstilling (self):
        
        
        #print("SLUTTSTILLING")
        b = self.motor._stilling._skjema.hent_brett()
        fen1 = self.brett.fen(en_passant="fen")
        fen2 = self.motor._stilling.hent_FEN()
        """
        print(f"{self.brett}")
        print(fen1)
        print(fen2) 
        print("Resultat: " + self.motor._stilling._skjema.hent_resultat())
        print("Vinner: " + self.motor._stilling._skjema.vinner)
        print(self.motor.hent_status())
        print(f"Trekk nr: {self.brett.fullmove_number}")
        print(f"Halvtrekk nr: {self.brett.ply()}")
        print(f"Remis 5: {self.brett.is_fivefold_repetition()}")
        print(f"Remis 75: {self.brett.is_seventyfive_moves()}")
        print(f"Remis material: {self.brett.is_insufficient_material()}")
        print(f"Remis patt: {self.brett.is_stalemate()}")
        print(f"Sjakkmatt: {self.brett.is_checkmate()}")
        """
        res = self.brett.outcome()
        #print(f"Resultat: {res}")
        
        """
        self.debug("SLUTTSTILLING")
        self.debug("Resultat: " + self.motor._stilling._skjema.hent_resultat())
        self.debug("Vinner: " + self.motor._stilling._skjema.vinner)
        """
        b = self.motor._stilling._skjema.hent_brett()
        """
        self.debug(f"{self.brett}")
        self.debug(f"{b.hvit_antall_dronninger_og_taarn}")
        self.debug(f"{b.hvit_antall_boender}")
        self.debug(f"{b.hvit_antall_loepere}")
        self.debug(f"{b.hvit_antall_springere}")
        self.debug(f"{b.sort_antall_dronninger_og_taarn}")
        self.debug(f"{b.sort_antall_boender}")
        self.debug(f"{b.sort_antall_loepere}")
        self.debug(f"{b.sort_antall_springere}")
        """
        fen1 = self.brett.fen(en_passant="fen")
        fen2 = self.motor._stilling.hent_FEN()
        """
        self.debug(fen1)
        self.debug(fen2) 
        self.debug(self.motor.hent_status())
        self.debug(f"Trekk nr: {self.brett.fullmove_number}")
        self.debug(f"Halvtrekk nr: {self.brett.ply()}")
        self.debug(f"Remis 5: {self.brett.is_fivefold_repetition()}")
        self.debug(f"Remis 75: {self.brett.is_seventyfive_moves()}")
        self.debug(f"Remis material: {self.brett.is_insufficient_material()}")
        self.debug(f"Remis patt: {self.brett.is_stalemate()}")
        self.debug(f"Sjakkmatt: {self.brett.is_checkmate()}")
        """
        res = self.brett.outcome()
        #self.debug(f"Resultat: {res}")
        
        
        feil = False
      
        if fen1 != fen2:
            self.debug("Feil FEN") 
            feil = True
        if self.motor._stilling._skjema.er_remis_5() != self.brett.is_fivefold_repetition():
            self.debug("Feil remis 5")
            feil = True
        if self.motor._stilling._skjema.er_remis_75() != self.brett.is_seventyfive_moves():
            self.debug("Feil remis 75")
            feil = True
        if self.motor._stilling._skjema.er_remis_materiell() != self.brett.is_insufficient_material():
             self.debug("Feil remis materiell")
             feil = True
        if self.motor._stilling._skjema.er_remis_patt() != self.brett.is_stalemate():
             self.debug("Feil remis patt")
             feil = True
        if self.motor._stilling._skjema.er_sjakk_matt() != self.brett.is_checkmate():
             self.debug("Feil remis 5")
             feil = True
   
        
     
        if feil:
            self.debug("Parti avsluttet med feil.")
            self.debug("STILLING ETTER TREKK")
            self.debug("Resultat: " + self.motor._stilling._skjema.hent_resultat())
            self.debug("Vinner: " + self.motor._stilling._skjema.vinner)
            b = self.motor._stilling._skjema.hent_brett()
            self.debug(f"{self.brett}")
            self.debug(f"{b.hvit_antall_dronninger_og_taarn}")
            self.debug(f"{b.hvit_antall_boender}")
            self.debug(f"{b.hvit_antall_loepere}")
            self.debug(f"{b.hvit_antall_springere}")
            self.debug(f"{b.sort_antall_dronninger_og_taarn}")
            self.debug(f"{b.sort_antall_boender}")
            self.debug(f"{b.sort_antall_loepere}")
            self.debug(f"{b.sort_antall_springere}")
            self.debug(fen1)
            self.debug(fen2) 
            self.debug(self.motor.hent_status())
            self.debug(f"Trekk nr: {self.brett.fullmove_number}")
            self.debug(f"Halvtrekk nr: {self.brett.ply()}")
            self.debug(f"Remis 5: {self.brett.is_fivefold_repetition()}")
            self.debug(f"Remis 75: {self.brett.is_seventyfive_moves()}")
            self.debug(f"Remis material: {self.brett.is_insufficient_material()}")
            self.debug(f"Remis patt: {self.brett.is_stalemate()}")
            self.debug(f"Sjakkmatt: {self.brett.is_checkmate()}")
            res = self.brett.outcome()
            self.debug(f"Resultat: {res}")
            print("Stillingen inneholder feil.")
            self.debug(self.motor.hent_status())
        else:
            self.debug("Parti avsluttet OK. Resultat: " + self.motor._stilling._skjema.hent_resultat() + " Vinner: " + self.motor._stilling._skjema.vinner + ". Antall trekk: " + (f"{self.brett.fullmove_number}"))
        
        # print(f"antall1: {self.antall_trekk_1} tid1: {self.tid_1}")
        # print(f"antall2: {self.antall_trekk_2} tid2: {self.tid_2}")
        
        return None
    
    
