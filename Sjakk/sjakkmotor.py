"""

Module: sjakkmotor.py

Opprettet: 5.1.2022
@author: Per Arne Skjelvik

Modulen inneholder.... 
  
Har klassen:
    Sjakkmotor

"""

import sjakk_konstanter as sk
import sjakkspill as sjakkspill
import sjakk_brett_brikke_trekk as sjakk_brett_brikke_trekk
import sjakkspiller as sjakkspiller

#-----------------------------------------------------------------------------
class SjakkMotor:  
    """
    Klassen har kunnskap om ..... og gjør...

    Eksterne metoder:
        sett_spillere(hvit_evaluering, hvit_soek, sort_evaluering, sort_soek)
        sett_utgangsstilling(spilletid)
        sett_stilling(fen, spilletid)
        * hent_brett()
        * hent_FEN()
        hent_neste_trekk_nr()
        hent_neste_trekk_farge()
        * hent_trekktype()
        * hent_resultat()
        * hent_evaluering()
        * hent_status()
        sjekk_trekk(spesialtrekk, fra, til)
        trekk(melding, spesialtrekk, fra, til)
        * hent_beste_trekk()
        beste_trekk()
        trekk_tilbake()
        parti_er_ferdig()

    Interne metoder:
        _tekst_til_pos(tekst)
        _pos_til_tekst(x, y):
            
    Testmetoder:
        sett_test(test)

    Bruker klassene:
    """
#----------------------------------------------------------------------------- 
    def __init__(self):
        self._ekspert_hvit = None    
        self._ekspert_sort = None
        self._stilling = None
        return None    
 
#-----------------------------------------------------------------------------    
    def sett_spillere(self, hvit_evaluering, hvit_soek, sort_evaluering, sort_soek):
        """
        Setter opp hvit og sort spiller med å angi hvilken evalueringsmetode
        og hvilken søkemetode de skal bruke for å finne beste trekk.
        Parti kan spilles med både en og to manuelle spillere.
        """
        self._ekspert_hvit = sjakkspiller.AISpiller(sk.HVIT, hvit_evaluering, hvit_soek)    
        self._ekspert_sort = sjakkspiller.AISpiller(sk.SORT, sort_evaluering, sort_soek)
        return None        
    
#-----------------------------------------------------------------------------        
    def sett_utgangsstilling(self):
        """
        Setter opp motoren med standard utgangsstilling i sjakk.
        """
        self._stilling = sjakkspill.Stilling()
        self._stilling.sett_utgangsstilling()
        return None
    
#-----------------------------------------------------------------------------        
    def sett_stilling(self, fen):
        """
        Setter opp motoren med en stilling angitt i fen.
        Forsyth–Edwards Notation (FEN) er en standard notasjon for å beskrive
        en stilling i et sjakkparti. Den inneholder all info for å starte
        et parti fra en gitt stilling. Eks fen for utgangsstillingen:
        rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1
        """
        self._stilling = sjakkspill.Stilling()
        self._stilling.sett_stilling(fen)
        return None
    
#-----------------------------------------------------------------------------    
    def hent_brett(self):
        r8,r7,r6,r5,r4,r3,r2,r1 = self._stilling.hent_brett_ASCII()
        return r8,r7,r6,r5,r4,r3,r2,r1
    
    def hent_FEN(self):
        return self._stilling.hent_FEN()
   
    def hent_neste_trekk_nr(self):
        return self._stilling.hent_neste_trekk_nr()
        
    def hent_neste_trekk_farge(self):
        return self._stilling.hent_neste_trekk_farge()
        
    def hent_trekktype(self):
        return self._stilling.hent_trekktype()
     
    def hent_resultat(self):
        return self._stilling.hent_resultat()
     
    def hent_evaluering(self):
        return self._stilling.hent_evaluering()
        
    def hent_status(self):
        return self._stilling._skjema.hent_status()
    
#-----------------------------------------------------------------------------  

    def ASCII_trekk_brett_fen(self):
        #trekk = self._stilling.ASCII_trekk()
        stilling = self._stilling.ASCII_brett()
        fen = self._stilling.ASCII_fen()
        #return trekk + "\n" + stilling + "\n" + fen
        return "\n" + stilling + "\n" + fen
  
    def sjekk_trekk(self, spesialtrekk, fra, til): 
        fra_x, fra_y = self.tekst_til_pos(fra)
        til_x, til_y = self.tekst_til_pos(til)
        return self._stilling.sjekk_trekk(spesialtrekk, fra_x, fra_y, til_x, til_y)
    
    
    def trekk(self, melding, spesialtrekk, fra, til):
        if melding == sk.AVSLUTTET: # spiller avslutter
            self._stilling.resultat = sk.AVSLUTTET
            return sk.AVSLUTTET
        else:
            fra_x, fra_y = self._tekst_til_pos(fra)
            til_x, til_y = self._tekst_til_pos(til)            
            return self.stilling.trekk(spesialtrekk, fra_x, fra_y, til_x, til_y)
     
        
    def hent_beste_trekk(self):
        # henter det beste trekket - gjennomfører det ikke
        spesialtrekk, fra_x, fra_y, til_x, til_y, resultat, evaluering = self._ekspert.hent_beste_trekk(self._stilling)
        fra = self._pos_til_tekst(fra_x, fra_y)
        til = self._pos_til_tekst(til_x, til_y)
        return spesialtrekk, fra, til, resultat, evaluering
     
        
    def beste_trekk(self):
        # gjennomfører det beste trekket
        if self._stilling.hent_neste_trekk_farge() == sk.HVIT:
            t = self._ekspert_hvit.beste_trekk(self._stilling)
        else:
            t = self._ekspert_sort.beste_trekk(self._stilling)
        fra = self._pos_til_tekst(t.x0, t.y0)
        til = self._pos_til_tekst(t.x1, t.y1)
        return t.type, t.bondeforvandling, t.farge, t.grad, fra, til, t.resultat, t.evaluering
  
    
    def trekk_tilbake(self):
        t = sjakk_brett_brikke_trekk.Trekk()   
        t = self._stilling.trekk_tilbake()
        fra = self._pos_til_tekst(t.x0, t.y0)
        til = self._pos_til_tekst(t.x1, t.y1)
        return t.type, t.farge, t.grad, fra, til, t.resultat, t.evaluering


    def parti_er_ferdig(self):
        if self._stilling.hent_resultat() == sk.PAAGAAR or self._stilling.hent_resultat() == sk.SJAKK:
            return False
        else:
            return True
   
    def _tekst_til_pos (self,tekst):
         y = int(tekst[1]) - 1
         x = ord(tekst[0]) - 97
         return x, y     
     
    def _pos_til_tekst (self, x, y):
        tekst = chr(x+97) + chr(y+49) 
        return tekst

# testformål

    def sett_test(self, test, fen): 
        self._test = test
        self._stilling.sett_test(test)
        if fen != "":
            self._test.sett_start(fen)
        return None
