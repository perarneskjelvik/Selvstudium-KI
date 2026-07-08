"""

Module: brukerdialog.py

Opprettet: 5.1.2022
@author: Per Arne Skjelvik

Tekstbasert brukergrensesnitt for å spille sjakk. 
Bruker CMD / Konsollet på datamaskinen.
Modulen kan ingenting om sjakk, den bare skriver ut tekst den mottar og
henter tekst den blir bedt om å hente.

Har klassene:
    Brett

"""

############################################################################## 

class UI_Brett:

    """
    Klassen skriver ut et tekstbaserte sjakkbrett, henter og skriver ut
    informasjon om et trekk og skriver ut diverse meldinger.

    Klassen har følgende eksterne metoder:
  
    vis_ASCII() 
    hent_trekk(farge, trekk_nr) 
    vis_trekk(farge, trekk_nr, melding, fra, til) 
    vis_resultat(tekst) 
    vis_feilmelding(tekst) 
    """

#-----------------------------------------------------------------------------
 
    def __init__(self):
        
        return None    

#-----------------------------------------------------------------------------  
      
    def vis_ASCII(self, r8, r7, r6, r5, r4, r3, r2, r1):
        
        """
        Skriver ut et tekstbasert sjakkbrett på skjermen/kommandolinjen.
        Sett fra hvits side.
        Input er 8 tekststrenger, en for hver rad på sjakkbrettet.        
        """
      
        print("")
        print("   a b c d e f g h")
        print("")
        print(f"8  {r8}  8")
        print(f"7  {r7}  7")
        print(f"6  {r6}  6")
        print(f"5  {r5}  5")
        print(f"4  {r4}  4")
        print(f"3  {r3}  3")
        print(f"2  {r2}  2")
        print(f"1  {r1}  1")
        print("")
        print("   a b c d e f g h")
        print("")
        return None
  
#-----------------------------------------------------------------------------  
  
    def vis_trekk(self, farge, grad, trekk_nr, trekktype, bondeforvandling, fra, til):
      
        print(f"Trekk {trekk_nr} {farge} {grad} {trekktype} {bondeforvandling} {fra} {til}")
        return None
  
#-----------------------------------------------------------------------------  
     
    def vis_resultat(self, tekst):
        
        print(f"Resultat: {tekst}")
        return None 
#-----------------------------------------------------------------------------  
     
    def vis_evaluering(self, tekst):
      
        print(f"Evaluering: {tekst}")
        return None 
#-----------------------------------------------------------------------------  
     
    def vis_status(self, tekst):
      
        print(f"Status: {tekst}")
        return None 
 #-----------------------------------------------------------------------------  
    
    def vis_feilmelding(self, tekst):
      
        print(f"Feilmelding: {tekst}")
        return None 
    
#-----------------------------------------------------------------------------   
     
    def hent_trekk(self, farge, trekk_nr):
        
        melding = ""
        spesialtrekk = ""
        fra = ""
        til = ""
        bondebytte = ""
        print(f"Trekk {trekk_nr} {farge}")
        print(f"Melding: x")
        melding = input("Melding: ").strip().lower()
        if not melding == "x":
            print(f"Trekktype: vanlig/kort rokade/lang rokade/bondeforvandling/en passant")
            trekktype = input("Spesialtrekk: ").strip().lower()
            print(f"Fra/til: a1-g8")
            fra = input("Fra: ").strip().lower()
            til = input("Til: ").strip().lower()
        return melding, spesialtrekk, fra, til