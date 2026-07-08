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

import tid as tid
import sjakk_konstanter as sk
import sjakk_brett_brikke_trekk as  sjakk_brett_brikke_trekk

#-----------------------------------------------------------------------------
class NoteringsSkjema:
    
    """
    Klassen har kunnskap om ..... og gjør...
    klassen holder styr på historikk og status i partiet
    Klassen har følgende eksterne metoder:    
    Klassen bruker følgende klasser:
    """
#-----------------------------------------------------------------------------
    def __init__(self):
        
        self._i = None # indeks i tabellene - halvtrekknummer (ply)
        self._klokke = tid.SjakkKlokke()
        self.vinner = None
        
        self._remis5sjekk = {} # nøkkel = FEN og innhold = antall forekomsetr
        self._brett = [None] *  sk.MAKS_TREKK * 2
        self._trekk = [None] *  sk.MAKS_TREKK * 2
  
        self.trekk_farge = [None] *  sk.MAKS_TREKK * 2 # siste trekk
        self.trekk_nr = [None] *  sk.MAKS_TREKK * 2 # siste trekk
        self.antall_trekk_75 = [None] *  sk.MAKS_TREKK * 2
        
        self.tid_trekk = [None] *  sk.MAKS_TREKK * 2
        self.tid_hvit = [None] *  sk.MAKS_TREKK * 2
        self.tid_sort = [None] *  sk.MAKS_TREKK * 2
        
        self.hvit_kort_rokade = [None] *  sk.MAKS_TREKK * 2  
        self.sort_kort_rokade = [None] *  sk.MAKS_TREKK * 2
        self.hvit_lang_rokade = [None] *  sk.MAKS_TREKK * 2  
        self.sort_lang_rokade = [None] *  sk.MAKS_TREKK * 2
        
        self.en_passant = [None] *  sk.MAKS_TREKK * 2    
        self.en_passant_x = [None] *  sk.MAKS_TREKK * 2  
        self.en_passant_y = [None] *  sk.MAKS_TREKK * 2  
        
        self.remis_5 = [None] *  sk.MAKS_TREKK * 2  
        self.remis_75 = [None] *  sk.MAKS_TREKK * 2  
        self.remis_patt = [None] *  sk.MAKS_TREKK * 2  
        self.remis_materiell = [None] *  sk.MAKS_TREKK * 2  
        self.sjakk_matt = [None] *  sk.MAKS_TREKK * 2  
        
        self.resultat = [None] *  sk.MAKS_TREKK * 2  
        self.evaluering = [None] *  sk.MAKS_TREKK * 2  
        
        return None    
    
#-----------------------------------------------------------------------------  
    def sett_utgangsstilling(self):
        
        self._i = 0 # indeks i tabellene - halvtrekknummer
        self.vinner = "Uavgjort"
        
        b = sjakk_brett_brikke_trekk.Brett()
        b.sett_utgangsstilling()
        self._brett[self._i] = b
        self.trekk_farge[0] = sk.SORT
        self.trekk_nr[0] = 0
        self.antall_trekk_75[0] = 0  

        farge, trekktid, tidhvit, tidsort = self._klokke.start(sk.MAKS_TID)
        self.tid_trekk[0] = 0
        self.tid_hvit[0] = tidhvit
        self.tid_sort[0] = tidsort
        
        self.hvit_kort_rokade[0] = True  
        self.sort_kort_rokade[0] = True
        self.hvit_lang_rokade[0] = True  
        self.sort_lang_rokade[0] = True
        
        self.en_passant[0] = False  
        self.en_passant_x[0] = 0
        self.en_passant_y[0] = 0
        
        self.remis_5[0] = False
        self.remis_75[0] = False
        self.remis_patt[0] = False
        self.remis_materiell[0] = False
        self.sjakk_matt[0] = False
        
        self.resultat[0] = sk.PAAGAAR
        self.evaluering[0] = 0
        
        return None    
    
#-----------------------------------------------------------------------------
    
    def sett_stilling(self, fen):
        
           
        """
        rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1

        rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq e3 0 1

        rnbqkbnr/pp1ppppp/8/2p5/4P3/8/PPPP1PPP/RNBQKBNR w KQkq c6 0 2

        rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 1 2

        4k3/8/8/8/8/8/4P3/4K3 w - - 5 39
        """
        
        self._i = 0 # indeks i tabellene - halvtrekknummer
        self.vinner = "Uavgjort"
        
        b = sjakk_brett_brikke_trekk.Brett()
        b.sett_stilling(fen)
        self._brett[self._i] = b
        
        trekk_farge, hvit_kort_rokade, sort_kort_rokade, hvit_lang_rokade, sort_lang_rokade, en_passant, en_passant_x, en_passant_y, trekk_nr_75, antall_trekk = self.fen_til_skjema(fen)
       
        self.trekk_farge[0] = trekk_farge
        
        self.trekk_nr[0] = antall_trekk
        self.antall_trekk_75[0] = trekk_nr_75

        farge, trekktid, tidhvit, tidsort = self._klokke.start(sk.MAKS_TID)
        self.tid_trekk[0] = 0
        self.tid_hvit[0] = tidhvit
        self.tid_sort[0] = tidsort
        
        self.hvit_kort_rokade[0] = hvit_kort_rokade
        self.sort_kort_rokade[0] = sort_kort_rokade
        self.hvit_lang_rokade[0] = hvit_lang_rokade
        self.sort_lang_rokade[0] = sort_lang_rokade
        
        self.en_passant[0] = en_passant 
        self.en_passant_x[0] = en_passant_x
        self.en_passant_y[0] = en_passant_y
        
        self.remis_5[0] = False
        self.remis_75[0] = False
        self.remis_patt[0] = False
        self.remis_materiell[0] = False
        self.sjakk_matt[0] = False
        
        self.resultat[0] = sk.PAAGAAR
        self.evaluering[0] = 0
        
        return None    


#-----------------------------------------------------------------------------
    
    def noter_trekk(self, trekk):
        
        self._i = self._i + 1
        
        farge, trekktid, tidhvit, tidsort = self._klokke.skift()
        self.tid_trekk[self._i] = trekktid
        self.tid_hvit[self._i] = tidhvit
        self.tid_sort[self._i] = tidsort
        
        self._trekk[self._i] = trekk.kopi() 
        self._trekk[self._i].nr = self._i
        
        
        self.trekk_farge[self._i] = trekk.farge
        self.resultat[self._i] = trekk.resultat
        self.evaluering[self._i] = trekk.evaluering
            
        if trekk.farge == sk.HVIT:
            self.trekk_nr[self._i] = self.trekk_nr[self._i-1] + 1 
        else:
            self.trekk_nr[self._i] = self.trekk_nr[self._i-1] 
            
        self._trekk[self._i].nr = self.trekk_nr[self._i] 
            
        temp_brett = self._brett[self._i-1].kopi()
        slag = temp_brett.hent_brikke(trekk.x1,trekk.y1)
        temp_brett.trekk(trekk.type, trekk.bondeforvandling, trekk.x0, trekk.y0, trekk.x1, trekk.y1)
        self._brett[self._i] = temp_brett
        
       
        # ---- sjekker om trekket medførte en passant ----------------------
 
        self.en_passant[self._i] = False
        if trekk.grad == sk.BONDE and trekk.y0 == 1 and trekk.y1 == 3:
            self.en_passant[self._i] = True
            self.en_passant_x[self._i] = trekk.x1
            self.en_passant_y[self._i] = 2
        if trekk.grad == sk.BONDE and trekk.y0 == 6 and trekk.y1 == 4:
            self.en_passant[self._i] = True
            self.en_passant_x[self._i] = trekk.x1
            self.en_passant_y[self._i] = 5
                
        # ---- sjekker om trekket gjør rokade ulovlig dvs konge eller tårn flyttes/slås---------
        
        self.hvit_lang_rokade[self._i] = self.hvit_lang_rokade[self._i-1]
        self.sort_lang_rokade[self._i] = self.sort_lang_rokade[self._i-1]
        self.hvit_kort_rokade[self._i] = self.hvit_kort_rokade[self._i-1]
        self.sort_kort_rokade[self._i] = self.sort_kort_rokade[self._i-1]
        
        if trekk.grad == sk.KONGE: # kongen flytter
            if trekk.farge == sk.HVIT:
                self.hvit_lang_rokade[self._i] = False
                self.hvit_kort_rokade[self._i] = False
            else:
                self.sort_lang_rokade[self._i] = False
                self.sort_kort_rokade[self._i] = False
                
        if trekk.grad == sk.TAARN: # tårnet flytter fra utgangsposisjon
            if trekk.farge == sk.HVIT and self.hvit_lang_rokade[self._i]:
                if trekk.x0 == 0 and trekk.y0 == 0:
                    self.hvit_lang_rokade[self._i] = False
            if trekk.farge == sk.HVIT and self.hvit_kort_rokade[self._i]:
                 if trekk.x0 == 7 and trekk.y0 == 0:
                     self.hvit_kort_rokade[self._i] = False   
            if trekk.farge == sk.SORT and self.sort_kort_rokade[self._i]:
                 if trekk.x0 == 7 and trekk.y0 == 7:
                     self.sort_kort_rokade[self._i] = False   
            if trekk.farge == sk.SORT and self.sort_lang_rokade[self._i]:
                 if trekk.x0 == 0 and trekk.y0 == 7:
                     self.sort_lang_rokade[self._i] = False   
                     
        if slag.grad == sk.TAARN: # tårnet blir slått i utgangsposisjon
            if slag.farge == sk.HVIT and self.hvit_lang_rokade[self._i]:
                if trekk.x1 == 0 and trekk.y1 == 0:
                    self.hvit_lang_rokade[self._i] = False
            if slag.farge == sk.HVIT and self.hvit_kort_rokade[self._i]:
                 if trekk.x1 == 7 and trekk.y1 == 0:
                    self.hvit_kort_rokade[self._i] = False   
            if slag.farge == sk.SORT and self.sort_kort_rokade[self._i]:
                 if trekk.x1 == 7 and trekk.y1 == 7:
                    self.sort_kort_rokade[self._i] = False   
            if slag.farge == sk.SORT and self.sort_lang_rokade[self._i]:
                 if trekk.x1 == 0 and trekk.y1 == 7:
                    self.sort_lang_rokade[self._i] = False   
    
                   
        # ---- sjekker om trekket medførte remis pga 5 like stillinger ---- 
         
        if trekk.resultat == sk.REMIS_5:
            self.remis_5[self._i] = True
        else:
            self.remis_5[self._i] = False
             
        # ---- sjekker om trekket medførte remis pga 75 trekk uten bonde/slag 
         
        if trekk.resultat == sk.REMIS_75:
            self.remis_75[self._i] = True
            self.antall_trekk_75[self._i] = self.antall_trekk_75[self._i-1] + 1
        else:
            self.remis_75[self._i] = False
            # sjekk slag eller bonde om denne skal nullstilles NB!! husk halvtrekk her
            if trekk.grad == sk.BONDE or slag.farge != sk.TOM:
                self.antall_trekk_75[self._i] = 0
            else:
                self.antall_trekk_75[self._i] = self.antall_trekk_75[self._i-1] + 1

        # ---- sjekker om trekket medførte remis pga materiell ----------------------------
         
        if trekk.resultat == sk.REMIS_MATERIELL:
            self.remis_materiell[self._i] = True  
        else:
            self.remis_materiell[self._i] = False 

        # ---- sjekker om trekket medførte remis pga patt--------------
         
     
    
        if trekk.resultat == sk.REMIS_PATT:
            self.remis_patt[self._i] = True  
        else:
            self.remis_patt[self._i] = False 

        # ---- sjekker om trekket medførte sjakkmatt ----------------------------
          
        if trekk.resultat == sk.SJAKKMATT:
            self.sjakk_matt[self._i] = True
            self.vinner = trekk.farge
        else:
            self.sjakk_matt[self._i] = False
        
        
        fen = self.hent_FEN2()
        if fen in self._remis5sjekk.keys():
            self._remis5sjekk[fen] =  self._remis5sjekk[fen] + 1
        else:
            self._remis5sjekk[fen] = 1
        
        
        return None    
    
#-----------------------------------------------------------------------------
    
    def sett_matt(self):   
    
        self.sjakk_matt[self._i] = True
        self.resultat[self._i] = sk.SJAKKMATT
        self.vinner =  self.trekk_farge[self._i]
        return None
    
#-----------------------------------------------------------------------------
    
    def sett_patt(self):   
    
        self.remis_patt[self._i] = True  
        self.resultat[self._i] = sk.REMIS_PATT
        return None
    
#-----------------------------------------------------------------------------

        
    def er_remis_5_etter_trekk(self, trekk):
        
        # skal kun sjekke om remis 5 er tilfellet etter trekket
        # vet at ingen andre alternative resultater kan skje
        # må lage fen for å sjekke
        
        self._i = self._i + 1
                   
        if trekk.farge == sk.HVIT:
            self.trekk_nr[self._i] = self.trekk_nr[self._i-1] + 1 
        else:
            self.trekk_nr[self._i] = self.trekk_nr[self._i-1] 
            
        temp_brett = self._brett[self._i-1].kopi()
        slag = temp_brett.hent_brikke(trekk.x1,trekk.y1)
        temp_brett.trekk(trekk.type, trekk.bondeforvandling, trekk.x0, trekk.y0, trekk.x1, trekk.y1)
        self._brett[self._i] = temp_brett
        
       
        # ---- sjekker om trekket medførte en passant ----------------------
 
        self.en_passant[self._i] = False
        if trekk.grad == sk.BONDE and trekk.y0 == 1 and trekk.y1 == 3:
            self.en_passant[self._i] = True
            self.en_passant_x[self._i] = trekk.x1
            self.en_passant_y[self._i] = 2
        if trekk.grad == sk.BONDE and trekk.y0 == 6 and trekk.y1 == 4:
            self.en_passant[self._i] = True
            self.en_passant_x[self._i] = trekk.x1
            self.en_passant_y[self._i] = 5
                
        # ---- sjekker om trekket gjør rokade ulovlig dvs konge eller tårn flyttes/slås---------
        
        self.hvit_lang_rokade[self._i] = self.hvit_lang_rokade[self._i-1]
        self.sort_lang_rokade[self._i] = self.sort_lang_rokade[self._i-1]
        self.hvit_kort_rokade[self._i] = self.hvit_kort_rokade[self._i-1]
        self.sort_kort_rokade[self._i] = self.sort_kort_rokade[self._i-1]
        
        if trekk.grad == sk.KONGE: 
            if trekk.farge == sk.HVIT:
                self.hvit_lang_rokade[self._i] = False
                self.hvit_kort_rokade[self._i] = False
            else:
                self.sort_lang_rokade[self._i] = False
                self.sort_kort_rokade[self._i] = False
                
        if trekk.grad == sk.TAARN:
            if trekk.farge == sk.HVIT and self.hvit_lang_rokade[self._i]:
                if trekk.x0 == 0:
                    self.hvit_lang_rokade[self._i] = False
            if trekk.farge == sk.HVIT and self.hvit_kort_rokade[self._i]:
                 if trekk.x0 == 7:
                     self.hvit_kort_rokade[self._i] = False   
            if trekk.farge == sk.SORT and self.sort_kort_rokade[self._i]:
                 if trekk.x0 == 7:
                     self.sort_kort_rokade[self._i] = False   
            if trekk.farge == sk.SORT and self.sort_lang_rokade[self._i]:
                 if trekk.x0 == 0:
                     self.sort_lang_rokade[self._i] = False   
                     
        if slag.grad == sk.TAARN:
            if slag.farge == sk.HVIT and self.hvit_lang_rokade[self._i]:
                if trekk.x1 == 0 and trekk.y1 == 0:
                    self.hvit_lang_rokade[self._i] = False
            if slag.farge == sk.HVIT and self.hvit_kort_rokade[self._i]:
                 if trekk.x1 == 7 and trekk.y1 == 0:
                    self.hvit_kort_rokade[self._i] = False   
            if slag.farge == sk.SORT and self.sort_kort_rokade[self._i]:
                 if trekk.x1 == 7 and trekk.y1 == 7:
                    self.sort_kort_rokade[self._i] = False   
            if slag.farge == sk.SORT and self.sort_lang_rokade[self._i]:
                 if trekk.x1 == 0 and trekk.y1 == 7:
                    self.sort_lang_rokade[self._i] = False
             
      
        
        er_remis = False
        fen = self.hent_FEN2()
        if fen in self._remis5sjekk.keys():
            if self._remis5sjekk[fen] == 4:
                er_remis = True  
        
        self._i = self._i - 1
        
        return er_remis    

#-----------------------------------------------------------------------------
    
    def noter_trekk_tilbake(self):
        
        
        fen = self.hent_FEN2()
        
        if self._remis5sjekk[fen] > 1:
            self._remis5sjekk[fen] =  self._remis5sjekk[fen] - 1
        else:
            del self._remis5sjekk[fen]
       
        self._i = self._i - 1
        self._klokke.sett(self.tid_hvit[self._i], self.tid_sort[self._i], self.hent_neste_trekk_farge())
        return None    

#-----------------------------------------------------------------------------
    
    def er_remis_5(self):
        
        return self.remis_5[self._i] 
    
#-----------------------------------------------------------------------------
    
    def er_remis_75(self):

        return self.remis_75[self._i] 

    
#-----------------------------------------------------------------------------
    
    def er_remis_75_etter_trekk(self, brett, trekk):
        
        slag = brett.hent_brikke(trekk.x1,trekk.y1)
        if trekk.grad == sk.BONDE or slag.farge != sk.TOM:
            return False
        else:
            if self.antall_trekk_75[self._i] < (sk.ANTALL_REMIS_75-1):
                return False
            else:
                return True


#-----------------------------------------------------------------------------
    
    def er_remis_materiell(self):
        
        return self.remis_materiell[self._i] 
    
    
#-----------------------------------------------------------------------------
    
    def hent_status(self):
            
        status = "\n Halvtrekk nr: " + str(self._i) \
        + "\n Trekk nr:" + str(self.trekk_nr[self._i] ) \
        + "\n Trekk 75:" + str(self.antall_trekk_75[self._i]) \
        + "\n Neste trekk farge:" + str(self.hent_neste_trekk_farge()) \
        + "\n Tid trekk:" + str(self.tid_trekk[self._i]) \
        + "\n Tid hvit:" + str(self.tid_hvit[self._i]) \
        + "\n Tid sort:" + str(self.tid_sort[self._i]) \
        + "\n Hvit lang rokade:" + str(self.hvit_lang_rokade[self._i]) \
        + "\n Hvit kort rokade:" + str(self.hvit_kort_rokade[self._i]) \
        + "\n Sort lang rokade:" + str(self.sort_lang_rokade[self._i]) \
        + "\n Sort kort rokade:" + str(self.sort_kort_rokade[self._i]) \
        + "\n En passant:" + str(self.en_passant[self._i]) \
        + "\n En passant x:" + str(self.en_passant_x[self._i]) \
        + "\n En passant y:" + str(self.en_passant_y[self._i]) \
        + "\n Remis 5:" + str(self.remis_5[self._i]) \
        + "\n Remis 75:" + str(self.remis_75[self._i]) \
        + "\n Remis materiell:" + str(self.remis_materiell[self._i]) \
        + "\n Remis patt:" + str(self.remis_patt[self._i]) \
        + "\n Sjakk matt:" + str(self.sjakk_matt[self._i]) \
        + "\n Resultat::" + str(self.resultat[self._i]) \
        + "\n Vinner:" + str(self.vinner)
        return status       
    
#-----------------------------------------------------------------------------
    
    def hent_resultat(self):
        
        return self.resultat[self._i]       
    
#-----------------------------------------------------------------------------
    
    def hent_trekktype(self):
        
        return self._trekk[self._i].trekktype       

#-----------------------------------------------------------------------------
    
    def hent_en_passant(self):
        
        return self.en_passant[self._i] 
    
#-----------------------------------------------------------------------------
    
    def er_sjakk_matt(self):
        
        return self.sjakk_matt[self._i] 
    
#-----------------------------------------------------------------------------
    
    def er_remis_patt(self):
        
        return self.remis_patt[self._i] 
    
#-----------------------------------------------------------------------------
    
    def hent_en_passant_xy(self):
        
        return self.en_passant_x[self._i], self.en_passant_y[self._i]  

#-----------------------------------------------------------------------------
    
    def hent_trekk(self):
    
        return self._trekk[self._i]       
    
    
#-----------------------------------------------------------------------------
    
    def hent_brett(self):
        
        return self._brett[self._i].kopi()       
    
#-----------------------------------------------------------------------------
    
    def hent_FEN(self):
        
        fen = self._brett[self._i].hent_fen_brett()
        if self.hent_neste_trekk_farge() == sk.HVIT:
            c = "w"
        else:
            c = "b" 
            
        if self.en_passant[self._i] == True:
            x = self.en_passant_x[self._i]
            y = self.en_passant_y[self._i]
            enp = " " + chr(x+97) + chr(y+49) + " "
        else:
            enp = " - "
        hmc75 = self.antall_trekk_75[self._i] 
        trknr = self.hent_neste_trekk_nr()
        castling = ""
        if self.hent_hvit_kort_rokade():
            castling = "K"
        if self.hent_hvit_lang_rokade():
            castling = castling + "Q"
        if self.hent_sort_kort_rokade():
            castling = castling + "k"
        if self.hent_sort_lang_rokade():
             castling = castling + "q"  
        if castling == "":
            castling = "-"
        fen = fen + " " + c + " " + castling + enp  + str(hmc75) + " " + str(trknr)
        return fen 

#-----------------------------------------------------------------------------

    def hent_FEN2(self):
        
        fen = self._brett[self._i].hent_fen_brett()
        if self.hent_neste_trekk_farge() == sk.HVIT:
            c = "w"
        else:
            c = "b" 
            
        if self.en_passant[self._i] == True:
            x = self.en_passant_x[self._i]
            y = self.en_passant_y[self._i]
            enp = " " + chr(x+97) + chr(y+49) + " "
        else:
            enp = " - "
        castling = ""
        if self.hent_hvit_kort_rokade():
            castling = "K"
        if self.hent_hvit_lang_rokade():
            castling = castling + "Q"
        if self.hent_sort_kort_rokade():
            castling = castling + "k"
        if self.hent_sort_lang_rokade():
             castling = castling + "q"  
        if castling == "":
            castling = "-"
        fen = fen + " " + c + " " + castling + enp  
        return fen 

#----------------------------------------------------------------------------

    def fen_til_skjema(self, fen):
        

      lengde =  len(fen)
      i = fen.find(" ")
      farge = fen[i+1]
      
      if farge == "w":
          trekk_farge = sk.SORT
      else:
          trekk_farge = sk.HVIT
      
      for j in range (i+3, i+7):
          k = j
          if fen[j] == "-":
              hvit_kort_rokade = False  
              sort_kort_rokade = False
              hvit_lang_rokade = False  
              sort_lang_rokade = False
          elif fen[j] == "K":
              hvit_kort_rokade = True  
          elif fen[j] == "Q":
              hvit_lang_rokade = True  
          elif fen[j] == "k":
              sort_kort_rokade = True  
          elif fen[j] == "q":
              sort_lang_rokade = True 
          else:
              k = j - 1
              break

      if fen[k+2] == "-":
          en_passant = False
          en_passant_x = 0
          en_passant_y = 0
          rest = fen[-(lengde-k-4):]
      else:
          en_passant = True
          en_passant_x = ord(fen[k+2]) - 97
          en_passant_y = int(fen[k+3]) - 1
          rest = fen[-(lengde-k-5):]
      
      i = rest.find(" ")
      
      trekk_nr_75 = int(rest[0:i])
      antall_trekk = int(rest[i+1:len(rest)])
       
      return trekk_farge, hvit_kort_rokade, sort_kort_rokade, hvit_lang_rokade, sort_lang_rokade, en_passant, en_passant_x, en_passant_y, trekk_nr_75, antall_trekk 

#-----------------------------------------------------------------------------
      
    def ASCII_trekk(self):
        return self._trekk[self._i].ASCII()
    
    def ASCII_brett(self):
        return self._brett[self._i].ASCII()
    
    def ASCII_fen(self):
        return self.hent_FEN()
        

#-----------------------------------------------------------------------------
    
    def sett_brett(self, b):
        
        self._brett[self._i] = b
        return None    
    
#-----------------------------------------------------------------------------
    
    def hent_evaluering(self):
        
        return self.evaluering[self._i]       
    
#-----------------------------------------------------------------------------
    
    def hent_hvit_kort_rokade(self):
        
        return self.hvit_kort_rokade[self._i]      
    
#-----------------------------------------------------------------------------
    
    def hent_sort_kort_rokade(self):
        
        return self.sort_kort_rokade[self._i]      
    
#-----------------------------------------------------------------------------
    
    def hent_hvit_lang_rokade(self):
        
        return self.hvit_lang_rokade[self._i]      
    
#-----------------------------------------------------------------------------
    
    def hent_sort_lang_rokade(self):
        
        return self.sort_lang_rokade[self._i]      

#-----------------------------------------------------------------------------
    
    def hent_trekk_farge(self):
        
        return self.trekk_farge[self._i]  
    
#-----------------------------------------------------------------------------
    
    def hent_neste_trekk_farge(self):
        
        if self.trekk_farge[self._i] == sk.HVIT:
            return sk.SORT
        else:
            return sk.HVIT
        
#-----------------------------------------------------------------------------
    
    def hent_neste_trekk_nr(self):
        
        if self.trekk_farge[self._i] == sk.HVIT:
            return self.trekk_nr[self._i]
        else:
            return self.trekk_nr[self._i] + 1
    
