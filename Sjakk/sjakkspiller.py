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

import random as random
import sjakkspill as sjakkspill
import sjakkskjema as sjakkskjema
import sjakk_brett_brikke_trekk as sjakk_brett_brikke_trekk 
import sjakk_konstanter as sk
import tid as tid


class Node:
   
    def __init__(self):
        self.antall = 0
        return None     
 
    def inkr(self):
        self.antall = self.antall + 1
        return None



class AISpiller:
    
    """
    Klassen har kunnskap om ..... og gjør...
    Klassen har følgende eksterne metoder:    
    Klassen bruker følgende klasser:
    """

#-----------------------------------------------------------------------------

    def __init__(self, farge, evalueringsmetode, soekemetode):
        
        self._farge = farge
        self._evalueringsmetode = evalueringsmetode
        self._soekemetode = soekemetode
        return None     
    
#-----------------------------------------------------------------------------
 
    def beste_trekk(self, stilling):
        
        # gjennomfører beste trekk
        
        beste_trekk = self.hent_beste_trekk(stilling)
        if beste_trekk.resultat != sk.FEIL:
            stilling.trekk(beste_trekk)
        return beste_trekk
    
#-----------------------------------------------------------------------------

    def hent_beste_trekk(self, stilling):
        
        # Finner det beste trekket (returnerer altså bare ett trekk)

        bt = sjakk_brett_brikke_trekk.Trekk() 
        
        if not (stilling.hent_resultat() == sk.PAAGAAR or stilling.hent_resultat() == sk.SJAKK):
            # For å kunne ta et nytt trekk må resultatet etter forrige trekk være PAAGAAR eller SJAKK
            bt.resultat = sk.FEIL
            return bt
           
        # åpningstrekk ----------------
        
        if stilling.hent_neste_trekk_nr() == 1 and stilling.hent_neste_trekk_farge() == sk.HVIT:
            bt.trekktype = sk.AAPNINGSTREKK
            bt.farge = sk.HVIT
            bt.grad = sk.BONDE
            bt.evaluering = "ingen evaluering"
            bt.resultat = sk.PAAGAAR
            bt.x0 = 3
            bt.y0 = 1
            bt.x1 = 3
            bt.y1 = 3
            return bt
        
        
        # vanlig trekk ----------------
        
        #kanskje mulige trekk allerede er generert fordi vi bør sjekke patt/matt?
        
        mulige_trekk = stilling.hent_mulige_trekk(self._evalueringsmetode, stilling.hent_neste_trekk_farge())
  
        # ingen trekk har resultat matt eller patt, det sjekkes først når et trekk gjennomføres  - stemmer dette?
  
        if mulige_trekk == [] and stilling.hent_resultat() == sk.PAAGAAR : # fant ingen mulige trekk i stillingen    
            print("Død stilling - fant ingen mulige trekk.")
            bt.resultat = sk.REMIS_DOED_STILLING
            return bt
        
        if mulige_trekk == [] and stilling.hent_resultat() == sk.SJAKK : # fant ingen mulige trekk i stillingen, burde ikke dette allerede vært sjekket når forrige trekk ble gjort?    
            print("Sjakk matt - fant ingen mulige trekk.")
            bt.resultat = sk.SJAKKMATT
            return bt
        
        if self._soekemetode == sk.TILFELDIG:
            posisjon = random.randint(0, len(mulige_trekk)-1)    
            bt = mulige_trekk[posisjon]
        elif self._soekemetode == sk.MINIMAX:
            farge = stilling.hent_neste_trekk_farge()
            bt = self.minimax(stilling, mulige_trekk, farge)
        elif self._soekemetode == sk.ALPHABETA:
            farge = stilling.hent_neste_trekk_farge()
            bt = self.alphabeta(stilling, mulige_trekk, farge, sk.ALPHABETA_DYBDE, sk.MAKS_TREKK)
      
        return bt

#-----------------------------------------------------------------------------

    def hent_beste_trekk2(self, stilling):
        
        # Finner det beste trekket (returnerer altså bare ett trekk)

        bt = sjakk_brett_brikke_trekk.Trekk() 
        
        if not (stilling.hent_resultat() == sk.PAAGAAR or stilling.hent_resultat() == sk.SJAKK):
            bt.resultat = sk.FEIL
            return bt
           
        # åpningstrekk ----------------
        
        if stilling.hent_neste_trekk_nr() == 1 and stilling.hent_neste_trekk_farge() == sk.HVIT:
            bt.trekktype = sk.AAPNINGSTREKK
            bt.farge = sk.HVIT
            bt.grad = sk.BONDE
            bt.evaluering = "ingen evaluering"
            bt.resultat = sk.PAAGAAR
            bt.x0 = 3
            bt.y0 = 1
            bt.x1 = 3
            bt.y1 = 3
            return bt
        
        
        # vanlig trekk ----------------
        
        #kanskje mulige trekk allerede er generert fordi vi bør sjekke patt/matt?
        
        potensielle_trekk = stilling.hent_potensielle_trekk(self._evalueringsmetode, stilling.hent_neste_trekk_farge())
  
        # ingen trekk har resultat matt eller patt, det sjekkes først når et trekk gjennomføres  
  
        if potensielle_trekk == [] and stilling.hent_resultat() == sk.PAAGAAR : # fant ingen mulige trekk i stillingen    
            print("Død stilling - fant ingen mulige trekk.")
            bt.resultat = sk.REMIS_DOED_STILLING
            return bt
        
        if potensielle_trekk == [] and stilling.hent_resultat() == sk.SJAKK : # fant ingen mulige trekk i stillingen    
            print("Sjakk matt - fant ingen mulige trekk.")
            bt.resultat = sk.SJAKKMATT
            return bt
        
        if self._soekemetode == sk.TILFELDIG:
            # denne vil feile, må luke ut ulovlig sjakk
            posisjon = random.randint(0, len(potensielle_trekk)-1)    
            bt = potensielle_trekk[posisjon]
        elif self._soekemetode == sk.MINIMAX:
            farge = stilling.hent_neste_trekk_farge()
            bt = self.minimax(stilling, potensielle_trekk, farge)
        elif self._soekemetode == sk.ALPHABETA:
            farge = stilling.hent_neste_trekk_farge()
            bt = self.alphabeta(stilling, potensielle_trekk, farge, sk.ALPHABETA_DYBDE, sk.MAKS_TREKK)
      
        return bt          

#-----------------------------------------------------------------------------
 
    def alphabeta(self, stilling, mulige_trekk, farge, dybde, maks_trekk):
        
        node = Node()
               
        alpha = -9999 # beste verdi funnet så langt
        beta = 9999 # dårligste verdi funnet så langt
        beste_verdi = -1000000
        beste_trekk = None
        
        
        # sorterer trekkene slik at de antatt beste trekkene vurderes først, bør sjakk evalueres høyest?
        mulige_trekk.sort(key=lambda t: t.evaluering, reverse = True)
        
        #print("")
        #print(f"Alphabeta start {farge} {len(mulige_trekk)} mulige trekk.")

        
        i = 0
        for trekk in mulige_trekk:
    
            i = i + 1
            if i > sk.ALPHABETA_ANTALL_TREKK:
                break # sjekker bare de potensielt beste trekkene (de første, men kan da gå glipp av sjakkmatt?)
                 
            foer = "{:10.2f}".format(trekk.evaluering)
            resultat_foer = trekk.resultat
            if resultat_foer == sk.PAAGAAR:
                resultat_foer = ""
                
            #print(f" {i} {trekk.ASCII()}")
            
            stilling.trekk(trekk) # gjennomfører trekket og får en ny stilling
            verdi = self.min_value_ab(stilling, trekk, farge, 1, alpha, beta, maks_trekk, node)
            resultat_etter = trekk.resultat
            stilling.trekk_tilbake()
    
            if resultat_etter == sk.PAAGAAR:
                resultat_etter = ""
            etter = "{:10.2f}".format(verdi)
            
            #print(f" {i} {trekk.ASCII()} før {foer} {resultat_foer} etter {etter} {resultat_etter}")
            
            if beste_verdi < verdi: 
                beste_verdi = verdi
                alpha = beste_verdi
                beste_trekk = trekk
           
        evaluering = "{:10.2f}".format(beste_verdi)
        
        #print("")
        print(f"Beste trekk: {beste_trekk.ASCII()} evaluering {evaluering}.")
        print(f"Alphabeta sjekket {node.antall} noder.")
        #print("ENTER for å fortsette")
      
        return beste_trekk

#-----------------------------------------------------------------------------
 
    def alphabeta2(self, stilling, potensielle_trekk, farge, dybde, maks_trekk):
        
        node = Node()
               
        alpha = -9999 # beste verdi funnet så langt
        beta = 9999 # dårligste verdi funnet så langt
        beste_verdi = -1000000
        beste_trekk = None
        
        potensielle_trekk.sort(key=lambda t: t.evaluering, reverse = True)
        
        print("")
        print(f"Alphabeta 2 start {farge} {len(potensielle_trekk)} potensielle trekk.")

        
        i = 0
        for trekk in potensielle_trekk:
    
            i = i + 1
            if i > sk.ALPHABETA_ANTALL_TREKK:
                break # sjekker bare de potensielt beste trekkene (de første)
                 
            foer = "{:10.2f}".format(trekk.evaluering)
            resultat_foer = trekk.resultat
            if resultat_foer == sk.PAAGAAR:
                resultat_foer = ""
            
            stilling.trekk2(trekk)
            if trekk.resultat == sk.FEIL: # trekkfarge står i sjakk
                stilling.trekk_tilbake()
            else:
                verdi = self.min_value_ab(stilling, trekk, farge, 1, alpha, beta, maks_trekk, node)
                resultat_etter = trekk.resultat
                stilling.trekk_tilbake()
    
                if resultat_etter == sk.PAAGAAR:
                    resultat_etter = ""
                etter = "{:10.2f}".format(verdi)
            
                print(f" {i} {trekk.ASCII()} før {foer} {resultat_foer} etter {etter} {resultat_etter}")
            
                if beste_verdi < verdi: 
                    beste_verdi = verdi
                    alpha = beste_verdi
                    beste_trekk = trekk
           
        evaluering = "{:10.2f}".format(beste_verdi)
        
        print("")
        print(f"Beste trekk: {beste_trekk.ASCII()} evaluering {evaluering}.")
        print(f"Alphabeta sjekket {node.antall} noder.")
        #input("ENTER for å fortsette")
      
        return beste_trekk
    
    
#-----------------------------------------------------------------------------
 
    def min_value_ab(self, stilling, trekk, farge, dybde, alpha, beta, maks_trekk, node):
        
        node.inkr()
        
        if trekk.resultat == sk.REMIS_5 or trekk.resultat == sk.REMIS_75 or trekk.resultat == sk.REMIS_MATERIELL or trekk.resultat == sk.REMIS_PATT:
            return -9999
        
        if trekk.resultat == sk.SJAKKMATT:
            return 9999
       
        if dybde == sk.ALPHABETA_DYBDE:
            # her kan vi sjekke om sjakk, og evt endr evaluering
            return trekk.evaluering
        
        daarligste_verdi = 9999
        mulige_trekk = stilling.hent_mulige_trekk(self._evalueringsmetode, farge)
        mulige_trekk.sort(key=lambda t: t.evaluering, reverse = False)
       
        for i in range(0, min(len(mulige_trekk), sk.ALPHABETA_ANTALL_TREKK)):
            # finner motstanderens beste mottrekk (laveste evaluering)
            
            stilling.trekk(mulige_trekk[i])
            
            verdi = self.max_value_ab(stilling, mulige_trekk[i], farge, dybde + 1 , alpha, beta, maks_trekk, node) 
            stilling.trekk_tilbake()
            
            if daarligste_verdi > verdi:
                daarligste_verdi = verdi   
            
            if beta > daarligste_verdi:
                beta = daarligste_verdi            
            
            if alpha >= beta:
                return daarligste_verdi
        
        return daarligste_verdi

#-----------------------------------------------------------------------------
 
    def min_value_ab2(self, stilling, trekk, farge, dybde, alpha, beta, maks_trekk, node):
        
        node.inkr()
        
        if trekk.resultat == sk.REMIS_5 or trekk.resultat == sk.REMIS_75 or trekk.resultat == sk.REMIS_MATERIELL or trekk.resultat == sk.REMIS_PATT:
            return -9999
        
        if trekk.resultat == sk.SJAKKMATT:
            return 9999
       
        if dybde == sk.ALPHABETA_DYBDE:
            return trekk.evaluering
        
        daarligste_verdi = 9999
        potensielle_trekk = stilling.hent_potensielle_trekk(self._evalueringsmetode, farge)
        potensielle_trekk.sort(key=lambda t: t.evaluering, reverse = False)
       
        for i in range(0, min(len(potensielle_trekk), sk.ALPHABETA_ANTALL_TREKK)):
            # finner motstanderens beste mottrekk (laveste evaluering)
            
            # sjekk om ulovlig trekk pga sjakk her?
            
            stilling.trekk2(potensielle_trekk[i])
            if potensielle_trekk[i].resultat == sk.FEIL: # trekkfarge er i sjakk
                stilling.trekk_tilbake()
            # sjekk om matt eller patt her?
            
                verdi = self.max_value_ab2(stilling, potensielle_trekk[i], farge, dybde + 1 , alpha, beta, maks_trekk, node) 
                stilling.trekk_tilbake()
            
                if daarligste_verdi > verdi:
                    daarligste_verdi = verdi   
            
                if beta > daarligste_verdi:
                    beta = daarligste_verdi            
            
                if alpha >= beta:
                    return daarligste_verdi
        #sjekk rokade her?
        
        return daarligste_verdi
    
    
    
#-----------------------------------------------------------------------------
 
    def max_value_ab(self, stilling, trekk, farge, dybde, alpha, beta, maks_trekk, node):
        
        node.inkr()
        
        if trekk.resultat == sk.REMIS_5 or trekk.resultat == sk.REMIS_75 or trekk.resultat == sk.REMIS_MATERIELL or trekk.resultat == sk.REMIS_PATT:
            return -9999
       
        if trekk.resultat == sk.SJAKKMATT:
            return 9999
      
        if dybde == sk.ALPHABETA_DYBDE:
            return trekk.evaluering
        
        beste_verdi = -9999
        mulige_trekk = stilling.hent_mulige_trekk(self._evalueringsmetode, farge)
        mulige_trekk.sort(key=lambda t: t.evaluering, reverse = True)
        
        for i in range(0, min(len(mulige_trekk),  sk.ALPHABETA_ANTALL_TREKK)):
            stilling.trekk(mulige_trekk[i])
            verdi = self.min_value_ab(stilling, mulige_trekk[i], farge, dybde + 1, alpha, beta, maks_trekk, node) 
            stilling.trekk_tilbake()
            
            if beste_verdi < verdi:
                beste_verdi = verdi    
            if alpha < beste_verdi:
                alpha = beste_verdi                
            if alpha >= beta:
                return beste_verdi
       
        return beste_verdi
        
       
#-----------------------------------------------------------------------------
 
    def max_value_ab2(self, stilling, trekk, farge, dybde, alpha, beta, maks_trekk, node):
        
        node.inkr()
        
        if trekk.resultat == sk.REMIS_5 or trekk.resultat == sk.REMIS_75 or trekk.resultat == sk.REMIS_MATERIELL or trekk.resultat == sk.REMIS_PATT:
            return -9999
       
        if trekk.resultat == sk.SJAKKMATT:
            return 9999
      
        if dybde == sk.ALPHABETA_DYBDE:
            return trekk.evaluering
        
        beste_verdi = -9999
        potensielle_trekk = stilling.hent_potensielle_trekk(self._evalueringsmetode, farge)
        potensielle_trekk.sort(key=lambda t: t.evaluering, reverse = True)
        
        for i in range(0, min(len(potensielle_trekk),  sk.ALPHABETA_ANTALL_TREKK)):
            stilling.trekk2(potensielle_trekk[i])
            verdi = self.min_value_ab2(stilling, potensielle_trekk[i], farge, dybde + 1, alpha, beta, maks_trekk, node) 
            stilling.trekk_tilbake()
            
            if beste_verdi < verdi:
                beste_verdi = verdi    
            if alpha < beste_verdi:
                alpha = beste_verdi                
            if alpha >= beta:
                return beste_verdi
       
        return beste_verdi
        
               
        