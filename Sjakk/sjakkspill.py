"""

Module: skjelvik.py

Opprettet: 5.1.2022
@author: Per Arne Skjelvik

Spiller sjakk - sjakkmotor basert på .... 
  
Har klassene:
    Brikke
    Stilling
    Sjakkmotor

"""
##############################################################################

import sjakk_konstanter as sk
import sjakkskjema as sjakkskjema
import sjakk_brett_brikke_trekk as sjakk_brett_brikke_trekk
import tid

# testformål
#import test as test

##############################################################################
        
class Stilling:
    
    """

    Klassen har kunnskap om ..... og gjør...

    Klassen har følgende eksterne metoder:

        sett_utgangsstilling() 
        sett_stilling(r7,r6,r5,r4,r3,r2,r1,r0) 
        hent_brett() 
    
        er_hvit(x, y) 
        samme_farge(b1, b2) 
        sjakk() 
        trekk(fra_x, fra_y, til_x, til_y) 
        mulige_trekk_brikke(x1, y1) 
    
    Klassen har følgende interne metoder:

    _hent_xy(brett, x, y) 
    _sett_xy(brett, x, y , verdi) 
    
        
    Klassen bruker følgende klasser:

    """

#-----------------------------------------------------------------------------
 
    def __init__(self):
        self._skjema = None
        self._evalueringsfarge = ""
        return None    
    
#-----------------------------------------------------------------------------
          
    def sett_utgangsstilling(self):
        self._skjema = sjakkskjema.NoteringsSkjema()
        self._skjema.sett_utgangsstilling()
        return None
    
#-----------------------------------------------------------------------------
          
    def sett_stilling(self, fen):
        self._skjema = sjakkskjema.NoteringsSkjema()
        self._skjema.sett_stilling(fen)
        return None
    
#----------------------------------------------------------------------------
                       
    def hent_brett_ASCII(self):   
        b = self._skjema.hent_brett()
        r8,r7,r6,r5,r4,r3,r2,r1 = b.hent_ASCII()
        return r8,r7,r6,r5,r4,r3,r2,r1

    def ASCII_trekk(self):
        return self._skjema.ASCII_trekk()
        
    def ASCII_brett(self):
        return self._skjema.ASCII_brett()
    
    def ASCII_fen(self):
        return self._skjema.ASCII_fen()
    
#----------------------------------------------------------------------------
                       
    def hent_resultat(self):   
        return self._skjema.hent_resultat()
                       
    def hent_FEN(self):   
        return self._skjema.hent_FEN()
                       
    def hent_trekktype(self):   
        return self._skjema.hent_trekktype()
                       
    def hent_neste_trekk_nr(self):   
        return self._skjema.hent_neste_trekk_nr()    
                       
    def hent_neste_trekk_farge(self):   
        return self._skjema.hent_neste_trekk_farge()    
                       
    def hent_evaluering(self):   
       return self._skjema.hent_evaluering() 
   

#----------------------------------------------------------------------------

    def trekk(self, trekk):
               
        self._skjema.noter_trekk(trekk)
        
        # sjekker om trekket medførte matt eller patt
        farge = self._skjema.hent_neste_trekk_farge()
        
        if self.antall_mulige_trekk(0, farge) == 0: # hvis det ikke er mulig å gjøre noen trekk, hvorfor hvit???
            brett = self._skjema.hent_brett()
            farge = self._skjema.hent_neste_trekk_farge()
            if self._er_sjakk(brett, farge):
                self._skjema.sett_matt()
                trekk.resultat = sk.SJAKKMATT
            else:
                self._skjema.sett_patt()
                trekk.resultat = sk.REMIS_PATT
        
        # testformål
        #self._test.trekk(trekk)
       
        return None

#----------------------------------------------------------------------------

    def trekk2(self, trekk):
               
        self._skjema.noter_trekk(trekk)
        brett = self._skjema.hent_brett()
        
        if self._er_sjakk(brett, trekk.farge):
            trekk.resultat = sk.FEIL
            return None
        
        # sjekker om trekket medførte matt eller patt
        
        if self.antall_mulige_trekk(0, sk.HVIT) == 0:
            brett = self._skjema.hent_brett()
            neste_farge = self._skjema.hent_neste_trekk_farge()
            if self._er_sjakk(brett, neste_farge):
                self._skjema.sett_matt()
                trekk.resultat = sk.SJAKKMATT
            else:
                self._skjema.sett_patt()
                trekk.resultat = sk.REMIS_PATT
        
        # testformål
        #self._test.trekk(trekk)
       
        return None
    
#----------------------------------------------------------------------------

    def trekk_tilbake(self):
        
        self._skjema.noter_trekk_tilbake()
        
        # testformål
        #self._test.trekk_tilbake()
       
        return None

#----------------------------------------------------------------------------

    def mulig_trekk(self, fra_x, fra_y, til_x, til_y):
       
        mulige_trekk = []
        mulige_trekk = self.hent_mulige_trekk_brikke(fra_x, fra_y)
        for i in range (len(mulige_trekk)):  
            if mulige_trekk[i] == [fra_x, fra_y, til_x, til_y]:
                return True
        return False
    
#----------------------------------------------------------------------------

    def sjekk_trekk(self, spesialtrekk, fra_x, fra_y, til_x, til_y):
       
        mulige_trekk = []
        mulige_trekk = self.hent_mulige_trekk_brikke(fra_x, fra_y)
        for i in range (len(mulige_trekk)):  
            if mulige_trekk[i] == [fra_x, fra_y, til_x, til_y]:
                return True
        return False

#----------------------------------------------------------------------------

    def hent_mulige_trekk(self, evalueringsmetode, evalueringsfarge):
        
        # Finner alle mulige trekk som kan gjøres i stillingen
        # Trekkene evalueres
        # Det sjekkes ikke om trekket medfører matt eller patt, det gjøres
        # først når trekket gjennomføres
       
        
        self._evalueringsfarge = evalueringsfarge # er det ikke gitt hvilken farge som skal evalueres?
        
        brett = self._skjema.hent_brett()
        farge = self._skjema.hent_neste_trekk_farge()
        mulige_trekk = self._hent_mulige_trekk(farge, brett)
        
        # testformål
        #self._test.test_mulige_trekk(mulige_trekk)
        
        return mulige_trekk
    
#----------------------------------------------------------------------------

    def hent_potensielle_trekk(self, evalueringsmetode, evalueringsfarge):
        
        # Finner alle mulige trekk som kan gjøres i stillingen
        # Trekkene evalueres
        # Det sjekkes ikke om trekket medfører matt eller patt, det gjøres
        # først når trekket gjennomføres
        # sjekker heller ikke sjakk eller remis
        
        self._evalueringsfarge = evalueringsfarge
        
        brett = self._skjema.hent_brett()
        farge = self._skjema.hent_neste_trekk_farge()
        potensielle_trekk = self._hent_potensielle_trekk(farge, brett)
        
        # testformål
        #self._test.test_mulige_trekk(mulige_trekk)
        
        return potensielle_trekk    

#----------------------------------------------------------------------------

    def antall_mulige_trekk(self, evalueringsmetode, evalueringsfarge):
        
        # Finner alle mulige trekk som kan gjøres i stillingen
        # Trekkene skal iKKE evalueres!!! må legge inn det som parameter
        
        #print(f"evalueringsfarge {evalueringsfarge}")
        self._evalueringsfarge = evalueringsfarge
        
        brett = self._skjema.hent_brett()
        farge = self._skjema.hent_neste_trekk_farge()
        mulige_trekk = self._hent_mulige_trekk(farge, brett)
        
        return len(mulige_trekk)

    
#----------------------------------------------------------------------------

    def _hent_mulige_trekk(self, farge, brett):
        
        # Finner alle mulige trekk som kan gjøres av en farge på brett.
             
        mulige_trekk = []
        
        for x in range (0, 8):
            for y in range (0,8):
                if brett.hent_farge(x,y) == farge:
                    mulige_trekk = mulige_trekk + self._hent_mulige_trekk_brikke(x, y)
        
        # sjekker om rokade er et mulig trekk 
        
        trekk = sjakk_brett_brikke_trekk.Trekk()
        
        if farge == sk.HVIT and self._skjema.hent_hvit_kort_rokade(): # sjekkerhvit  kort rokade
            b1 = brett.hent_brikke(5, 0)
            b2 = brett.hent_brikke(6, 0)
            if b1.farge == sk.TOM and b2.farge == sk.TOM:
                if not self._blir_anrepet(brett, farge, 4, 0):
                    if not self._blir_anrepet(brett, farge, 5, 0):
                        if not self._blir_anrepet(brett, farge, 6, 0):
                           trekk = self._resultat_trekk(sk.KORT_ROKADE, "", 4, 0, 6, 0, farge, sk.KONGE, brett)
                           if not trekk.resultat == sk.FEIL:
                               mulige_trekk.append(trekk) 
                               
        if farge == sk.HVIT and self._skjema.hent_hvit_lang_rokade(): # sjekker hvit lang rokade
            b1 = brett.hent_brikke(2, 0)
            b2 = brett.hent_brikke(3, 0)
            b3 = brett.hent_brikke(1, 0)
            if b1.farge == sk.TOM and b2.farge == sk.TOM and b3.farge == sk.TOM:
                if not self._blir_anrepet(brett, farge, 4, 0):
                    if not self._blir_anrepet(brett, farge, 2, 0):
                        if not self._blir_anrepet(brett, farge, 3, 0):
                           trekk = self._resultat_trekk(sk.LANG_ROKADE, "", 4, 0, 2, 0, farge, sk.KONGE, brett)
                           if not trekk.resultat == sk.FEIL:
                                mulige_trekk.append(trekk)         
       
        if farge == sk.SORT and self._skjema.hent_sort_kort_rokade():
            b1 = brett.hent_brikke(5, 7)
            b2 = brett.hent_brikke(6, 7)
            if b1.farge == sk.TOM and b2.farge == sk.TOM:
                if not self._blir_anrepet(brett, farge, 4, 7):
                    if not self._blir_anrepet(brett, farge, 5, 7):
                        if not self._blir_anrepet(brett, farge, 6, 7):
                           trekk = self._resultat_trekk(sk.KORT_ROKADE, "", 4, 7, 6, 7, farge, sk.KONGE, brett)
                           if not trekk.resultat == sk.FEIL:
                               mulige_trekk.append(trekk) 
                  
        if farge == sk.SORT and self._skjema.hent_sort_lang_rokade():
            b1 = brett.hent_brikke(2, 7)
            b2 = brett.hent_brikke(3, 7)
            b3 = brett.hent_brikke(1, 7)
            if b1.farge == sk.TOM and b2.farge == sk.TOM and b3.farge == sk.TOM:
                if not self._blir_anrepet(brett, farge, 4, 7):
                    if not self._blir_anrepet(brett, farge, 2, 7):
                        if not self._blir_anrepet(brett, farge, 3, 7):
                           trekk = self._resultat_trekk(sk.LANG_ROKADE, "", 4, 7, 2, 7, farge, sk.KONGE, brett)
                           if not trekk.resultat == sk.FEIL:
                               mulige_trekk.append(trekk)
        
        return mulige_trekk

#----------------------------------------------------------------------------

    def _hent_potensielle_trekk(self, farge, brett):
        
        # Finner alle potensielle trekk som kan gjøres av en farge på brett.
        # Hva er forskjellen på mulige trekk og potensielle trekk?
             
        mulige_trekk = []
        
        for x in range (0, 8):
            for y in range (0,8):
                if brett.hent_farge(x,y) == farge:
                    mulige_trekk = mulige_trekk + self._hent_mulige_trekk_brikke(x, y)
        
        # sjekker om rokade er et mulig trekk 
        
        trekk = sjakk_brett_brikke_trekk.Trekk()
        
        if farge == sk.HVIT and self._skjema.hent_hvit_kort_rokade(): # sjekkerhvit  kort rokade
            b1 = brett.hent_brikke(5, 0)
            b2 = brett.hent_brikke(6, 0)
            if b1.farge == sk.TOM and b2.farge == sk.TOM:
                if not self._blir_anrepet(brett, farge, 4, 0):
                    if not self._blir_anrepet(brett, farge, 5, 0):
                        if not self._blir_anrepet(brett, farge, 6, 0):
                           trekk = self._resultat_trekk(sk.KORT_ROKADE, "", 4, 0, 6, 0, farge, sk.KONGE, brett)
                           if not trekk.resultat == sk.FEIL:
                               mulige_trekk.append(trekk) 
                               
        if farge == sk.HVIT and self._skjema.hent_hvit_lang_rokade(): # sjekker hvit lang rokade
            b1 = brett.hent_brikke(2, 0)
            b2 = brett.hent_brikke(3, 0)
            b3 = brett.hent_brikke(1, 0)
            if b1.farge == sk.TOM and b2.farge == sk.TOM and b3.farge == sk.TOM:
                if not self._blir_anrepet(brett, farge, 4, 0):
                    if not self._blir_anrepet(brett, farge, 2, 0):
                        if not self._blir_anrepet(brett, farge, 3, 0):
                           trekk = self._resultat_trekk(sk.LANG_ROKADE, "", 4, 0, 2, 0, farge, sk.KONGE, brett)
                           if not trekk.resultat == sk.FEIL:
                                mulige_trekk.append(trekk)         
       
        if farge == sk.SORT and self._skjema.hent_sort_kort_rokade():
            b1 = brett.hent_brikke(5, 7)
            b2 = brett.hent_brikke(6, 7)
            if b1.farge == sk.TOM and b2.farge == sk.TOM:
                if not self._blir_anrepet(brett, farge, 4, 7):
                    if not self._blir_anrepet(brett, farge, 5, 7):
                        if not self._blir_anrepet(brett, farge, 6, 7):
                           trekk = self._resultat_trekk(sk.KORT_ROKADE, "", 4, 7, 6, 7, farge, sk.KONGE, brett)
                           if not trekk.resultat == sk.FEIL:
                               mulige_trekk.append(trekk) 
                  
        if farge == sk.SORT and self._skjema.hent_sort_lang_rokade():
            b1 = brett.hent_brikke(2, 7)
            b2 = brett.hent_brikke(3, 7)
            b3 = brett.hent_brikke(1, 7)
            if b1.farge == sk.TOM and b2.farge == sk.TOM and b3.farge == sk.TOM:
                if not self._blir_anrepet(brett, farge, 4, 7):
                    if not self._blir_anrepet(brett, farge, 2, 7):
                        if not self._blir_anrepet(brett, farge, 3, 7):
                           trekk = self._resultat_trekk(sk.LANG_ROKADE, "", 4, 7, 2, 7, farge, sk.KONGE, brett)
                           if not trekk.resultat == sk.FEIL:
                               mulige_trekk.append(trekk)
        
        return mulige_trekk
    


#----------------------------------------------------------------------------

    def _hent_mulige_trekk_brikke(self, x0, y0):
        
        # Finner alle mulige trekk som kan gjøres av en brikke på brettet 
        # med posisjon x0 y0. 
      
       
        bondeforvandling = ""
        brett = self._skjema.hent_brett()
        mulige_trekk = []
        b0 = brett.hent_brikke(x0, y0)
                
        # sjekker bonde NB sjekk en passant!!!
        
        if b0.grad == sk.BONDE: 
            antall = 1
            if b0.farge == sk.HVIT:
                dy = 1
                if y0 == 1:
                    antall = 2
            else:
                dy = -1 
                if y0 == 6:
                    antall = 2
                        
            # sjekker trekk rett fram
            
            x1 = x0 
            y1 = y0
            for steg in range (0, antall): # maks 2 steg
                y1 = y1 + dy
                if self._innenfor_brettet(x0, y0, x1, y1):
                    b1 = brett.hent_brikke(x1, y1)
                    if b1.farge == sk.TOM: # tomt felt - fortsetter ett steg
                        if y1 == 0 or y1 == 7:
                            if b0.farge == sk.HVIT:
                                trekk = self._resultat_trekk(sk.BONDEFORVANDLING, "D", x0, y0, x1, y1, b0.farge, b0.grad, brett)
                                if not trekk.resultat == sk.FEIL:
                                    mulige_trekk.append(trekk)   
                                trekk = self._resultat_trekk(sk.BONDEFORVANDLING, "L", x0, y0, x1, y1, b0.farge, b0.grad, brett)
                                if not trekk.resultat == sk.FEIL:
                                    mulige_trekk.append(trekk) 
                                trekk = self._resultat_trekk(sk.BONDEFORVANDLING, "S", x0, y0, x1, y1, b0.farge, b0.grad, brett)
                                if not trekk.resultat == sk.FEIL:
                                    mulige_trekk.append(trekk) 
                                trekk = self._resultat_trekk(sk.BONDEFORVANDLING, "T", x0, y0, x1, y1, b0.farge, b0.grad, brett)
                                if not trekk.resultat == sk.FEIL:
                                     mulige_trekk.append(trekk) 
                            else:
                                trekk = self._resultat_trekk(sk.BONDEFORVANDLING, "d", x0, y0, x1, y1, b0.farge, b0.grad, brett)
                                if not trekk.resultat == sk.FEIL:
                                    mulige_trekk.append(trekk)   
                                trekk = self._resultat_trekk(sk.BONDEFORVANDLING, "l", x0, y0, x1, y1, b0.farge, b0.grad, brett)
                                if not trekk.resultat == sk.FEIL:
                                    mulige_trekk.append(trekk) 
                                trekk = self._resultat_trekk(sk.BONDEFORVANDLING, "s", x0, y0, x1, y1, b0.farge, b0.grad, brett)
                                if not trekk.resultat == sk.FEIL:
                                    mulige_trekk.append(trekk) 
                                trekk = self._resultat_trekk(sk.BONDEFORVANDLING, "t", x0, y0, x1, y1, b0.farge, b0.grad, brett)
                                if not trekk.resultat == sk.FEIL:
                                     mulige_trekk.append(trekk) 
                           
                        else:
                            trekk = self._resultat_trekk(sk.VANLIG_TREKK, bondeforvandling, x0, y0, x1, y1, b0.farge, b0.grad, brett)
                            if not trekk.resultat == sk.FEIL:
                                mulige_trekk.append(trekk)        
                    else: #ikke tomt felt - avbryt
                       break     
                   
            # sjekker mulige slag skrått til sidene
            
            y1 = y0 + dy
            dx = 1
            for retning in range (0, 2): # to retninger skrå venstre og høyre
                dx = dx * (-1)
                x1 = x0 + dx   
                if self._innenfor_brettet(x0, y0, x1, y1):
                    b1 = brett.hent_brikke(x1, y1)
                    if b0.farge == b1.farge:
                        pass # brikke med samme farge 
                    elif b1.farge == sk.TOM:
                        if self._skjema.hent_en_passant() == True :
                            x, y = self._skjema.hent_en_passant_xy()
                            if x == x1 and y == y1:
                                trekk = self._resultat_trekk(sk.EN_PASSANT, bondeforvandling, x0, y0, x1, y1, b0.farge, b0.grad, brett)
                                if not trekk.resultat == sk.FEIL:
                                    mulige_trekk.append(trekk)   
                        else:
                            pass # brikke tom
                    else: # brikke motsatt farge - slag
                       if y1 == 0 or y1 == 7:
                           if b0.farge == sk.HVIT:
                               trekk = self._resultat_trekk(sk.BONDEFORVANDLING, "D", x0, y0, x1, y1, b0.farge, b0.grad, brett)
                               if not trekk.resultat == sk.FEIL:
                                   mulige_trekk.append(trekk)   
                               trekk = self._resultat_trekk(sk.BONDEFORVANDLING, "L", x0, y0, x1, y1, b0.farge, b0.grad, brett)
                               if not trekk.resultat == sk.FEIL:
                                   mulige_trekk.append(trekk) 
                               trekk = self._resultat_trekk(sk.BONDEFORVANDLING, "S", x0, y0, x1, y1, b0.farge, b0.grad, brett)
                               if not trekk.resultat == sk.FEIL:
                                   mulige_trekk.append(trekk) 
                               trekk = self._resultat_trekk(sk.BONDEFORVANDLING, "T", x0, y0, x1, y1, b0.farge, b0.grad, brett)
                               if not trekk.resultat == sk.FEIL:
                                   mulige_trekk.append(trekk) 
                           else:
                               trekk = self._resultat_trekk(sk.BONDEFORVANDLING, "d", x0, y0, x1, y1, b0.farge, b0.grad, brett)
                               if not trekk.resultat == sk.FEIL:
                                   mulige_trekk.append(trekk)   
                               trekk = self._resultat_trekk(sk.BONDEFORVANDLING, "l", x0, y0, x1, y1, b0.farge, b0.grad, brett)
                               if not trekk.resultat == sk.FEIL:
                                   mulige_trekk.append(trekk) 
                               trekk = self._resultat_trekk(sk.BONDEFORVANDLING, "s", x0, y0, x1, y1, b0.farge, b0.grad, brett)
                               if not trekk.resultat == sk.FEIL:
                                   mulige_trekk.append(trekk) 
                               trekk = self._resultat_trekk(sk.BONDEFORVANDLING, "t", x0, y0, x1, y1, b0.farge, b0.grad, brett)
                               if not trekk.resultat == sk.FEIL:
                                   mulige_trekk.append(trekk) 
                           
                         
                       else:
                           trekk = self._resultat_trekk(sk.VANLIG_TREKK, bondeforvandling, x0, y0, x1, y1, b0.farge, b0.grad, brett)
                           if not trekk.resultat == sk.FEIL:
                               mulige_trekk.append(trekk)           
                else:
                    pass # utenfor brettet
    
        else:  # alle gradene bortsett fra bonde
            
            for retning in range(0, b0.antall_retninger): 
                x1 = x0 
                y1 = y0
                dx, dy = b0.hent_steg(retning)
                for steg in range (0, b0.antall_steg): 
                    x1 = x1 + dx
                    y1 = y1 + dy
                    if self._innenfor_brettet(x0, y0, x1, y1): 
                        b1 = brett.hent_brikke(x1, y1)
                        if (b0.farge == b1.farge): # brikke med samme farge
                            break
                        if not b1.grad == sk.TOM: # motsatt farge - slag
                            trekk = self._resultat_trekk(sk.VANLIG_TREKK, bondeforvandling,  x0, y0, x1, y1, b0.farge, b0.grad, brett)
                            if not trekk.resultat == sk.FEIL:
                                mulige_trekk.append(trekk)
                            break
                        
                        else: #tomt felt - sjekk og fortsett
                            trekk = self._resultat_trekk(sk.VANLIG_TREKK, bondeforvandling,  x0, y0, x1, y1, b0.farge, b0.grad, brett)
                            if not trekk.resultat == sk.FEIL:
                                mulige_trekk.append(trekk)        
                    else:
                        break # utenfor brettet
         
        return mulige_trekk
    
#----------------------------------------------------------------------------

    def _hent_potensielle_trekk_brikke(self, x0, y0):
        
        # Finner alle potensielle trekk som kan gjøres av en brikke på brettet 
        # med posisjon x0 y0. 
        # sjekker ikke om sjakk/ulovlig eller remis
      
       
        bondeforvandling = ""
        brett = self._skjema.hent_brett()
        potensielle_trekk = []
        b0 = brett.hent_brikke(x0, y0)
                
        # sjekker bonde NB sjekk en passant!!!
        
        if b0.grad == sk.BONDE: 
            antall = 1
            if b0.farge == sk.HVIT:
                dy = 1
                if y0 == 1:
                    antall = 2
            else:
                dy = -1 
                if y0 == 6:
                    antall = 2
                        
            # sjekker trekk rett fram
            
            x1 = x0 
            y1 = y0
            for steg in range (0, antall): # maks 2 steg
                y1 = y1 + dy
                if self._innenfor_brettet(x0, y0, x1, y1):
                    b1 = brett.hent_brikke(x1, y1)
                    if b1.farge == sk.TOM: # tomt felt - fortsetter ett steg
                        if y1 == 0 or y1 == 7:
                            if b0.farge == sk.HVIT:
                                trekk = self._nytt_trekk(sk.BONDEFORVANDLING, "D", x0, y0, x1, y1, b0.farge, b0.grad, brett)
                                potensielle_trekk.append(trekk)   
                                trekk = self._nytt_trekk(sk.BONDEFORVANDLING, "L", x0, y0, x1, y1, b0.farge, b0.grad, brett)
                                potensielle_trekk.append(trekk) 
                                trekk = self._nytt_trekk(sk.BONDEFORVANDLING, "S", x0, y0, x1, y1, b0.farge, b0.grad, brett)
                                potensielle_trekk.append(trekk) 
                                trekk = self._nytt_trekk(sk.BONDEFORVANDLING, "T", x0, y0, x1, y1, b0.farge, b0.grad, brett)
                                potensielle_trekk.append(trekk) 
                            else:
                                trekk = self._nytt_trekk(sk.BONDEFORVANDLING, "d", x0, y0, x1, y1, b0.farge, b0.grad, brett)
                                potensielle_trekk.append(trekk)   
                                trekk = self._nytt_trekk(sk.BONDEFORVANDLING, "l", x0, y0, x1, y1, b0.farge, b0.grad, brett)
                                potensielle_trekk.append(trekk) 
                                trekk = self._nytt_trekk(sk.BONDEFORVANDLING, "s", x0, y0, x1, y1, b0.farge, b0.grad, brett)
                                potensielle_trekk.append(trekk) 
                                trekk = self._nytt_trekk(sk.BONDEFORVANDLING, "t", x0, y0, x1, y1, b0.farge, b0.grad, brett)
                                potensielle_trekk.append(trekk) 
                           
                        else:
                            trekk = self._nytt_trekk(sk.VANLIG_TREKK, bondeforvandling, x0, y0, x1, y1, b0.farge, b0.grad, brett)
                            potensielle_trekk.append(trekk)        
                    else: #ikke tomt felt - avbryt
                       break     
                   
            # sjekker mulige slag skrått til sidene
            
            y1 = y0 + dy
            dx = 1
            for retning in range (0, 2): # to retninger skrå venstre og høyre
                dx = dx * (-1)
                x1 = x0 + dx   
                if self._innenfor_brettet(x0, y0, x1, y1):
                    b1 = brett.hent_brikke(x1, y1)
                    if b0.farge == b1.farge:
                        pass # brikke med samme farge 
                    elif b1.farge == sk.TOM:
                        if self._skjema.hent_en_passant() == True :
                            x, y = self._skjema.hent_en_passant_xy()
                            if x == x1 and y == y1:
                                trekk = self._nytt_trekk(sk.EN_PASSANT, bondeforvandling, x0, y0, x1, y1, b0.farge, b0.grad, brett)
                                potensielle_trekk.append(trekk)   
                        else:
                            pass # brikke tom
                    else: # brikke motsatt farge - slag
                       if y1 == 0 or y1 == 7:
                           if b0.farge == sk.HVIT:
                               trekk = self._nytt_trekk(sk.BONDEFORVANDLING, "D", x0, y0, x1, y1, b0.farge, b0.grad, brett)
                               potensielle_trekk.append(trekk)   
                               trekk = self._nytt_trekk(sk.BONDEFORVANDLING, "L", x0, y0, x1, y1, b0.farge, b0.grad, brett)
                               potensielle_trekk.append(trekk) 
                               trekk = self._nytt_trekk(sk.BONDEFORVANDLING, "S", x0, y0, x1, y1, b0.farge, b0.grad, brett)
                               potensielle_trekk.append(trekk) 
                               trekk = self._nytt_trekk(sk.BONDEFORVANDLING, "T", x0, y0, x1, y1, b0.farge, b0.grad, brett)
                               potensielle_trekk.append(trekk) 
                           else:
                               trekk = self._nytt_trekk(sk.BONDEFORVANDLING, "d", x0, y0, x1, y1, b0.farge, b0.grad, brett)
                               potensielle_trekk.append(trekk)   
                               trekk = self._nytt_trekk(sk.BONDEFORVANDLING, "l", x0, y0, x1, y1, b0.farge, b0.grad, brett)
                               potensielle_trekk.append(trekk) 
                               trekk = self._nytt_trekk(sk.BONDEFORVANDLING, "s", x0, y0, x1, y1, b0.farge, b0.grad, brett)
                               potensielle_trekk.append(trekk) 
                               trekk = self._nytt_trekk(sk.BONDEFORVANDLING, "t", x0, y0, x1, y1, b0.farge, b0.grad, brett)
                               potensielle_trekk.append(trekk) 
                           
                         
                       else:
                           trekk = self._nytt_trekk(sk.VANLIG_TREKK, bondeforvandling, x0, y0, x1, y1, b0.farge, b0.grad, brett)
                           potensielle_trekk.append(trekk)           
                else:
                    pass # utenfor brettet
    
        else:  # alle gradene bortsett fra bonde
            
            for retning in range(0, b0.antall_retninger): 
                x1 = x0 
                y1 = y0
                dx, dy = b0.hent_steg(retning)
                for steg in range (0, b0.antall_steg): 
                    x1 = x1 + dx
                    y1 = y1 + dy
                    if self._innenfor_brettet(x0, y0, x1, y1): 
                        b1 = brett.hent_brikke(x1, y1)
                        if (b0.farge == b1.farge): # brikke med samme farge
                            break
                        if not b1.grad == sk.TOM: # motsatt farge - slag
                            trekk = self._nytt_trekk(sk.VANLIG_TREKK, bondeforvandling,  x0, y0, x1, y1, b0.farge, b0.grad, brett)
                            potensielle_trekk.append(trekk)
                            break
                        else: #tomt felt - sjekk og fortsett
                            trekk = self._nytt_trekk(sk.VANLIG_TREKK, bondeforvandling,  x0, y0, x1, y1, b0.farge, b0.grad, brett)
                            potensielle_trekk.append(trekk)        
                    else:
                        break # utenfor brettet
         
        return potensielle_trekk
    



#----------------------------------------------------------------------------

    def _angrep_og_forsvar(self, brett, x0, y0):
        
        # Finner alle brikker som angripes eller forsvares av brikke på felt x0, y0
        # bør kanskje også telle frie felt = mobilitet?
        # trenger man i det hele tatt sjekke sjakk?
        # kanskje på angrep og forsvar 1?
            
        angrep = 0
        angrep2 = 0
        angrep3 = 0
        forsvar = 0
        forsvar2 = 0
        forsvar3 = 0
        
        sjakkfarge = sk.TOM # i utgangspunktet angriper brikke x0 y0 ikke en konge og setter denne i sjakk
        
        b0 = brett.hent_brikke(x0, y0) # henter birkke x0 y0 som skal vurderes
                
        # sjekker bonde NB sjekk en passant!!!
        
        if b0.grad == sk.BONDE: 
            antall = 1
            if b0.farge == sk.HVIT:
                dy = 1
                if y0 == 1:
                    antall = 2
            else:
                dy = -1 
                if y0 == 6:
                    antall = 2
                        
            # sjekker ikke trekk rett fram
            
            # sjekker mulige slag skrått til sidene
            
            y1 = y0 + dy
            dx = 1
            for retning in range (0, 2): # to retninger skrå venstre og høyre
                dx = dx * (-1)
                x1 = x0 + dx   
                if self._innenfor_brettet(x0, y0, x1, y1):
                    b1 = brett.hent_brikke(x1, y1)
                    if b0.farge == b1.farge:
                        forsvar = forsvar + b1.verdi
                    elif b1.farge == sk.TOM:
                        if self._skjema.hent_en_passant() == True :
                            x, y = self._skjema.hent_en_passant_xy()
                            if x == x1 and y == y1:
                                angrep = angrep + b1.verdi  
                        else:
                            pass # brikke tom
                    else: # brikke motsatt farge - slag
                       angrep = angrep + b1.verdi    
                       if b1.grad == sk.KONGE:
                           sjakkfarge = b1.farge
                else:
                    pass # utenfor brettet
    
        else:  # alle gradene bortsett fra bonde
        
        #må sjekke konge spesielt pga sjakk!
            
            for retning in range(0, b0.antall_retninger): 
                x1 = x0 
                y1 = y0
                dx, dy = b0.hent_steg(retning)
                for steg in range (0, b0.antall_steg): 
                    x1 = x1 + dx
                    y1 = y1 + dy
                    if self._innenfor_brettet(x0, y0, x1, y1): 
                        b1 = brett.hent_brikke(x1, y1)
                        if (b0.farge == b1.farge): # brikke med samme farge
                            forsvar = forsvar + b1.verdi # denne brikken blir forsvart av brikke på x0 y0
                            break
                        if not b1.grad == sk.TOM: # motsatt farge - slag, denne brikken kan slås av brikken på x0 y0
                            angrep = angrep + b1.verdi
                            if b1.grad == sk.KONGE: # brikken som kan slås er konge, dvs trekket medfører SJAKK
                                sjakkfarge = b1.farge # brikke x0 y0 angriper en konge med denne fargen
                            break
                        else: #tomt felt -  fortsett
                            pass    
                    else:
                        break # utenfor brettet
         
        return angrep, forsvar, sjakkfarge
    


#----------------------------------------------------------------------------

    def _resultat_trekk(self, trekktype, bondeforvandling, x0, y0, x1, y1, farge, grad, brett):
        
        # Returnerer et trekk med resultatet hvis trekket hadde blitt gjort.
        # initierer trekket med parametrene i kallet
        # sjakkmatt eller patt oppdages ikke her - først når trekket gjøres
       
        
        
        # bør sjekke om det skal evalueres eller ikke!!! ikke nødvendig ved trekk !!!
        
        trekk = sjakk_brett_brikke_trekk.Trekk()
        trekk.resultat = sk.PAAGAAR # resultat hvis ikke matt eller remis
        trekk.type = trekktype
        trekk.bondeforvandling = bondeforvandling
        trekk.farge = farge
        trekk.grad = grad
        trekk.x0 = x0
        trekk.y0 = y0
        trekk.x1 = x1
        trekk.y1 = y1
       
        # gjennomfører trekket på et midlertidig brett 
        temp_brett = brett.kopi()
        temp_brett.trekk(trekktype, bondeforvandling, x0, y0, x1, y1)
        
        # evaluerer trekket (den nye stillingen)
        self.evaluer(trekk, temp_brett, 1)
        
        # sjekker om trekket setter seg selv i sjakk (som er ulovlig)
        # hva med patt?
        
        if trekk.resultat == sk.FEIL:
            return trekk
    
            
        # sjekker remis etter 75 trekk uten slag eller bondetrekk
        if  self._skjema.er_remis_75_etter_trekk(brett, trekk):
            trekk.resultat = sk.REMIS_75
            trekk.evaluering = -9999
            return trekk     
        
        # sjekker remis pga for få brikker
        if  not temp_brett.er_nok_materiell():
            trekk.resultat = sk.REMIS_MATERIELL
            trekk.evaluering = -9999
            return trekk
       
        # sjekker til slutt remis pga 5 like trekk
        if  self._skjema.er_remis_5_etter_trekk(trekk):
            trekk.resultat = sk.REMIS_5
            trekk.evaluering = -9999
            return trekk 
        
    
        # hvis vi kommer hit så går spillet videre, dv resultat = sk.PAAGAAR
        return trekk # PAAGAAR    

#----------------------------------------------------------------------------

    def _nytt_trekk(self, trekktype, bondeforvandling, x0, y0, x1, y1, farge, grad, brett):
        
        #Returnerer et trekk med resultatet hvis trekket hadde blitt gjort.
        #initierer trekket med parametrene i kallet
        # sjakk eller patt oppdages ikke her - først når trekket gjøres
        
        
        # bør sjekke om det skal evalueres eller ikke!!! ikke nødvendig ved trekk
        
        trekk = sjakk_brett_brikke_trekk.Trekk()
        trekk.resultat = sk.PAAGAAR # resultat hvis ikke matt eller remis
        trekk.type = trekktype
        trekk.bondeforvandling = bondeforvandling
        trekk.farge = farge
        trekk.grad = grad
        trekk.x0 = x0
        trekk.y0 = y0
        trekk.x1 = x1
        trekk.y1 = y1
       
        return trekk 



#----------------------------------------------------------------------------

    def _er_sjakk(self, brett, farge):
        
        x, y = brett.hent_konge_xy(farge)
    
        if self._blir_anrepet(brett, farge, x, y):
            return True
        else:
            return False
        
    
#----------------------------------------------------------------------------

    def _motsatt(self, farge):
        if farge == sk.HVIT:
            return sk.SORT
        else:
            return sk.HVIT
  
#----------------------------------------------------------------------------
      
    def _innenfor_brettet(self, x0, y0, x1, y1):
        
        if x1 < 8 and x1 > -1 and y1 < 8 and y1 > -1: 
            return True
        else:
            return False
 


#----------------------------------------------------------------------------
   
    def _blir_anrepet(self, brett, farge, x0, y0):
        
        # Sjekker om felt x0, y0 blir angrepet av motsatt farge på brett
        # Retur True/False
        
        
        #----- 4 retninger å sjekke - på skrå 
        #----- dronning, konge og løper kan angripe
        
        loeper = sjakk_brett_brikke_trekk.Brikke(sk.LOEPER)
        
        for retning in range(0, 4): 
            x1 = x0
            y1 = y0
            dx, dy = loeper.hent_steg(retning)
            for steg in range (0, 7): # maksimalt 7 steg i hver retning 
                x1 = x1 + dx
                y1 = y1 + dy
                if x1 > 7 or x1 < 0 or y1 > 7 or y1 < 0:
                    break # utenfor brettet
                b1 = brett.hent_brikke(x1, y1) #brikken som testes
                if b1.grad == sk.TOM: # ingen brikke - fortsett å lete
                    pass
                elif farge == b1.farge: # samme farge forsvar:
                    break
                else: #motsatt farge mulig angrep
                    if b1.grad == sk.DRONNING or b1.grad == sk.LOEPER:
                        return True
                    elif b1.grad == sk.KONGE and steg == 0:
                        return True
                    else:
                        break
        
        #----- # 4 retninger å sjekke - opp/ned - til siden
        #----- # konge, dronning eller tårn kan slå eller forsvare
        
        taarn = sjakk_brett_brikke_trekk.Brikke(sk.TAARN)
        
        for retning in range(0, 4): 
            x1 = x0
            y1 = y0
            dx, dy = taarn.hent_steg(retning)
            for steg in range (0, 7):  
                x1 = x1 + dx
                y1 = y1 + dy
                if x1 > 7 or x1 < 0 or y1 > 7 or y1 < 0:
                    break # utenfor brettet
                b1 = brett.hent_brikke(x1, y1)
                if b1.grad == sk.TOM: # ingen brikke - fortsett å lete
                    pass
                elif farge == b1.farge: # samme farge forsvar:
                    break
                else: #motsatt farge mulig angrep
                    if b1.grad == sk.DRONNING or b1.grad == sk.TAARN:
                        return True
                    elif b1.grad == sk.KONGE and steg == 0:
                        return True
                    else:
                        break
                
        #----- sjekk springer - 8 retninger 
         
        springer = sjakk_brett_brikke_trekk.Brikke(sk.SPRINGER)
        for retning in range(0, 8): 
            x1 = x0
            y1 = y0
            dx, dy = springer.hent_steg(retning)     
            x1 = x1 + dx
            y1 = y1 + dy
            if x1 < 8 and x1 > -1 and y1 < 8 and y1 > -1: 
                b1 = brett.hent_brikke(x1, y1)
                if b1.grad == sk.TOM: # ingen brikke - fortsett å lete
                    pass
                if farge == b1.farge: # samme farge forsvar:
                    pass
                else: #motsatt farge mulig angrep
                    if b1.grad == sk.SPRINGER:
                        return True
       
         #----- sjekk bonde - 4 retninger IKKE IMPLEMENTERT? en passant?
         
        if farge == sk.HVIT:
            dy = 1
        else:
            dy = -1  
        
        y1 = y0 + dy
        dx = 1
        
        for retning in range (0, 2): # to retninger skrå venstre og høyre
            dx = dx * (-1)
            x1 = x0 + dx   
            if x1 < 8 and x1 > -1 and y1 < 8 and y1 > -1:
                b1 = brett.hent_brikke(x1, y1)
                if (farge == b1.farge):
                    pass # brikke med samme farge 
                elif b1.grad == sk.BONDE:
                    return True
                else:
                    pass
            else:
                pass
        
        return False




#----------------------------------------------------------------------------
    
    def evaluer(self, trekk, brett, metode):
        
        # evaluerer alle brikker på brettet etter metode og setter trekkresultat PAAGAAR/SJAKK/FEIL
        
        # evaluerer både sort og hvit og beregner forholdet mellom dem
           
        # evaluerer materiell og angrep/forsvar
        
        materiell = 0
        angrep1 = 1
        angrep2 = 0
        angrep3 = 0
        forsvar1 = 1
        forsvar2= 0
        forsvar3 = 0
        bondebytte = 0
        kongeforsvar = 0
        
        anti_materiell = 0
        anti_angrep1 = 1
        anti_angrep2 = 0
        anti_angrep3 = 0
        anti_forsvar1 = 1
        anti_forsvar2= 0
        anti_forsvar3 = 0
        anti_bondebytte = 0
        anti_kongeforsvar = 0
    
        for x in range(0, 8): 
            for y in range (0, 8): 
                br = brett.hent_brikke(x, y) # evaluerer alle brikker på brettet
                if br.farge != sk.TOM:  # har funnet en brikke på brettet
                  
                    if br.farge == self._evalueringsfarge: #har funnet en brikke med fargen til den som trekker og som skal evalueres
                        materiell = materiell + br.verdi
                        a, f, sjakkfarge = self._angrep_og_forsvar(brett, x, y) # finner hvor mange brikker denne brikken angriper og forsvarer, og om den setter en konge i sjakk
                        if sjakkfarge == trekk.farge: # denne brikken setter en konge i sjakk, og kongen tilhører den som skal trekke, dermed er ikke dette en lovlig stilling og et lovlig trekk
                            trekk.resultat = sk.FEIL # trekket/stillingen er uovlig og resultatet settes FEIL
                            return
                        elif sjakkfarge != sk.TOM: # denne brikken setter en konge i sjakk, og kongen tilhører ikke den som skal trekke, dermed er  dette en lovlig stilling og et lovlig trekk
                            trekk.resultat = sk.SJAKK # trekket setter den som ikke trekker i sjakk, og resultatet er SJAKK
                        angrep1 = angrep1 + a
                        forsvar1 = forsvar1 + f 
                        if br.grad == sk.BONDE:
                            if br.farge == sk.HVIT:
                                bondebytte = bondebytte + 8 - y
                            else:
                                bondebytte = bondebytte + y
                    else:
                        anti_materiell = anti_materiell + br.verdi
                        a, f, sjakkfarge = self._angrep_og_forsvar(brett, x, y)
                        if sjakkfarge == trekk.farge:
                            trekk.resultat = sk.FEIL
                            return
                        elif sjakkfarge != sk.TOM:
                            #trekk.evaluering = -9998
                            trekk.resultat = sk.SJAKK
                        anti_angrep1 = anti_angrep1 + a
                        anti_forsvar1 = anti_forsvar1 + f 
                        if br.grad == sk.BONDE:
                            if br.farge == sk.HVIT:
                                anti_bondebytte = anti_bondebytte + 8 - y
                            else:
                                anti_bondebytte = anti_bondebytte + y
            
        if metode == 1:
            if materiell > anti_materiell:
                ev1 = (materiell/anti_materiell-1)
            else:
                ev1 = -(anti_materiell/materiell-1)
                
            if angrep1 > anti_angrep1:
                ev2 = (angrep1/anti_angrep1-1)
            else:
                ev2 = -(anti_angrep1/angrep1-1)
                
            if forsvar1 > anti_forsvar1:
                ev3 = (forsvar1/anti_forsvar1-1)
            else:
                ev3 = -(anti_forsvar1/forsvar1-1)
                
            ev4 = 0
            #if bondebytte > anti_bondebytte:
            #    ev4 = (bondebytte/anti_bondebytte-1)
            #else:
            #    ev4 = -(anti_bondebytte/bondebytte-1)
                 
                
            #trekk.evaluering = ev1 + ev2 + ev3
            trekk.evaluering = (3*ev1 + 1*ev2 + ev3 + 20*ev4)/8
            #input(f"{trekk.evaluering} {ev1} {ev2} {ev3} {ev4} ")
            #trekk.evaluering = (ev2)
           
                        
                #trekk.evaluering = trekk.ev_materiell + trekk.ev_angrep1 + trekk.ev_forsvar1 + trekk.ev_angrep2 + trekk.ev_forsvar2 + trekk.ev_angrep3 + trekk.ev_forsvar3
        elif metode == 2:
           trekk.evaluering = self._evaluer2(brett, self._evalueringsfarge)
        else:
           trekk.evaluering = 0
        return None

    
#----------------------------------------------------------------------------
    
    def _evaluer0(self):
        # ingen evaluering
        return 0
    
#----------------------------------------------------------------------------
    
    def _evaluer1(self, brett, farge): 
        
        # evaluerer materiell
        ev = 0
      
        for x in range(0, 8): 
            for y in range (0, 8): 
                br = brett.hent_brikke(x, y)
                if br.farge != sk.TOM:  
                    
                    if br.farge == farge:
                        fortegn = 1
                    else:
                        fortegn = -1
                        
                    if br.grad == sk.KONGE:
                        pass
                    elif br.grad == sk.DRONNING:
                        ev = ev + ((1 * fortegn) * br.verdi)
                    elif br.grad == sk.TAARN:
                        ev = ev + ((1 * fortegn) * br.verdi)
                    elif br.grad == sk.LOEPER:
                        ev = ev + ((1 * fortegn) * br.verdi)
                    elif br.grad == sk.SPRINGER:
                        ev = ev + ((1 * fortegn) * br.verdi)
                    else:
                        ev = ev + ((1 * fortegn) * br.verdi)
        
        return ev

#----------------------------------------------------------------------------
    
    def _evaluer2(self, brett, farge): #materiell og posisjon
        
        ev = 0
      
        for x in range(0, 8): 
            for y in range (0, 8): 
                br = brett.hent_brikke(x, y)
                if br.farge != sk.TOM:  
                    
                    if br.farge == farge:
                        fortegn = 1
                    else:
                        fortegn = -1
                        
                    if br.grad == sk.KONGE:
                        pass
                    elif br.grad == sk.DRONNING:
                        ev = ev + ((1 * fortegn) * br.verdi)*sk.PLASSVERDI[x][y]
                    elif br.grad == sk.TAARN:
                        ev = ev + ((1 * fortegn) * br.verdi)*sk.PLASSVERDI[x][y]
                    elif br.grad == sk.LOEPER:
                        ev = ev + ((1 * fortegn) * br.verdi)*sk.PLASSVERDI[x][y]
                    elif br.grad == sk.SPRINGER:
                        ev = ev + ((1 * fortegn) * br.verdi)*sk.PLASSVERDI[x][y]
                    else:
                        ev = ev + ((1 * fortegn) * br.verdi)*sk.PLASSVERDI[x][y]
        
        return ev       

#-----------------------------------------------------------------------------

# testformål
 
    def sett_test(self, test):
        
        # testformål
        self._testbrett = sjakk_brett_brikke_trekk.Brett()
        self._test = test
        return None    