"""
Module: skjelvik.py.

Opprettet: 5.1.2022
@author: Per Arne Skjelvik

Spiller sjakk - sjakkmotor basert på ....

Har klassene:
    Brikke
    Stilling
    Sjakkmotor
"""

# #############################################################################

import sjakk_konstanter as sk

# #############################################################################


class Trekk:
    """
    Klassen har kunnskap om ..... og gjør...

    Klassen har følgende eksterne metoder:
    Klassen bruker følgende klasser:

    """

# -----------------------------------------------------------------------------

    def __init__(self):

        self.nr = ""
        self.type = ""
        self.bondeforvandling = ""
        self.x0 = 0
        self.y0 = 0
        self.x1 = 0
        self.y1 = 0
        self.grad = ""
        self.farge = ""
        self.retning = ""
        self.slag = None
        self.offensivt = None
        self.resultat = ""  # etter trekket
        self.evaluering = 0  # etter trekket
        self.ev_materiell = 0  # 1
        self.ev_angrep1 = 0  # 2
        self.ev_angrep2 = 0  # 2
        self.ev_angrep3 = 0  # 2
        self.ev_forsvar1 = 0  # 3
        self.ev_forsvar2 = 0  # 3
        self.ev_forsvar3 = 0  # 3
        self.ev_bondeforvandling = 0  # 4
        self.ev_kongeforsvar = 0  # 5

        return None

# -----------------------------------------------------------------------------

    def kopi(self):

        t = Trekk()
        t.nr = self.nr
        t.type = self.type
        t.bondeforvandling = self.bondeforvandling
        t.x0 = self.x0
        t.y0 = self.y0
        t.x1 = self.x1
        t.y1 = self.y1
        t.resultat = self.resultat
        t.evaluering = self.evaluering
        t.grad = self.grad
        t.farge = self.farge
        t.retning = self.retning
        t.slag = self.slag
        t.offensivt = self.offensivt
        return t


    def ASCII(self):

        tekst = self.type + " " + self.grad + " "
        fra = chr(self.x0 + 97) + chr(self.y0 + 49)
        til = chr(self.x1 + 97) + chr(self.y1 + 49)
        if self.type == sk.BONDEFORVANDLING:
            til = til + self.bondeforvandling
        tekst = tekst + fra + " " + til
        return tekst



##############################################################################

class Brikke:

    """
    Klassen har kunnskap om ..... og gjør...
    Klassen har følgende eksterne metoder:
    Klassen bruker følgende klasser:
    """

#-----------------------------------------------------------------------------

    def __init__(self, grad_og_farge):

        """
        Input grad_og_farge er en bokstav som representerer både brikkens
        grad og farge. Hvis bokstaven er liten så er fargen sort. Selve
        bokstaven angir grad som er definert som konstanter i denne modulen.
        """

        # mulige_trekk = [] endres kun hvis mulige felt påvirkes
        # mulige_felt = [] oppslag for å sjekke om blir påvirket


        self._grad_og_farge = grad_og_farge
        if grad_og_farge.islower():
            self.farge = sk.SORT
        else:
            self.farge = sk.HVIT

        b = grad_og_farge.lower()

        if b == sk.LOEPER:
            self.grad = sk.LOEPER
            self.antall_retninger = 4
            self.antall_steg = 7
            self.steg = [[1,1], [-1,1], [1,-1], [-1,-1]]
            self.verdi = 5
        elif b == sk.SPRINGER:
            self.grad = sk.SPRINGER
            self.antall_retninger = 8
            self.antall_steg = 1
            self.steg = [[1,-2], [1,2], [2,-1], [2,1],[-1,2], [-1,-2], [-2,1], [-2,-1]]
            self.verdi = 4
        elif b == sk.KONGE:
            self.grad = sk.KONGE
            self.antall_retninger = 8
            self.antall_steg = 1
            self.steg = [[1,1], [1,0], [1,-1], [-1,1],[-1,0], [-1,-1], [0,1], [0,-1]]
            self.verdi = 1
        elif b == sk.DRONNING:
            self.grad = sk.DRONNING
            self.antall_retninger = 8
            self.antall_steg = 7
            self.steg = [[1,1], [1,0], [1,-1], [-1,1],[-1,0], [-1,-1], [0,1], [0,-1]]
            self.verdi = 10
        elif b == sk.TAARN:
            self.grad = sk.TAARN
            self.antall_retninger = 4
            self.antall_steg = 7
            self.steg = [[1,0], [-1,0], [0,-1], [0,1]]
            self.verdi = 3
        elif b == sk.BONDE:
            self.grad = sk.BONDE
            self.verdi = 1
        else:
            self.grad = sk.TOM
            self.farge = sk.TOM
            self.verdi = 0

        return None

#-----------------------------------------------------------------------------

    def hent_steg(self, retning):

        return self.steg[retning][0], self.steg[retning][1]

##############################################################################

class Brett:

    """
    Klassen har kunnskap om ..... og gjør...
    Klassen har følgende eksterne metoder:
    Klassen bruker følgende klasser:
    """

#-----------------------------------------------------------------------------

    def __init__(self):

        self.brett = None
        self.hvit_konge_x = None
        self.hvit_konge_y = None
        self.sort_konge_x = None
        self.sort_konge_y = None

        self.hvit_antall_dronninger_og_taarn = None
        self.hvit_antall_boender = None
        self.hvit_antall_loepere = None
        self.hvit_antall_springere = None
        self.sort_antall_dronninger_og_taarn = None
        self.sort_antall_boender = None
        self.sort_antall_loepere = None
        self.sort_antall_springere = None

        return None

#-----------------------------------------------------------------------------

    def sett_utgangsstilling(self):

        self.brett = []
        self._sett_stilling("tsldklst",
                           "bbbbbbbb",
                           "........",
                           "........",
                           "........",
                           "........",
                           "BBBBBBBB",
                           "TSLDKLST")

        self.hvit_konge_x = 4
        self.hvit_konge_y = 0
        self.sort_konge_x = 4
        self.sort_konge_y = 7

        self.hvit_antall_dronninger_og_taarn = 3
        self.hvit_antall_boender = 8
        self.hvit_antall_loepere = 2
        self.hvit_antall_springere = 2
        self.sort_antall_dronninger_og_taarn = 3
        self.sort_antall_boender = 8
        self.sort_antall_loepere = 2
        self.sort_antall_springere = 2


        return None

#-----------------------------------------------------------------------------

    def sett_stilling(self, fen):

        r7, r6, r5, r4, r3, r2, r1, r0 = self.fen_til_brett(fen)
        self._sett_stilling(r7, r6, r5, r4, r3, r2, r1, r0)

        self.tell_antall_brikker()

        for i in range (0,8):
            for j in range (0,8):
                b = self.hent_brikke(i, j)
                if b.grad == sk.KONGE and b.farge == sk.HVIT:
                    self.hvit_konge_x = i
                    self.hvit_konge_y = j
                elif b.grad == sk.KONGE and b.farge == sk.SORT:
                    self.sort_konge_x = i
                    self.sort_konge_y = j

        return None


#-----------------------------------------------------------------------------

    def _sett_stilling(self,r7,r6,r5,r4,r3,r2,r1,r0):

     self.brett = []
     r7 = r7.replace(" ", "")
     r6 = r6.replace(" ", "")
     r5 = r5.replace(" ", "")
     r4 = r4.replace(" ", "")
     r3 = r3.replace(" ", "")
     r2 = r2.replace(" ", "")
     r1 = r1.replace(" ", "")
     r0 = r0.replace(" ", "")

     self.brett  = [[r0[0], r0[1], r0[2], r0[3], r0[4], r0[5], r0[6], r0[7]],
                    [r1[0], r1[1], r1[2], r1[3], r1[4], r1[5], r1[6], r1[7]],
                    [r2[0], r2[1], r2[2], r2[3], r2[4], r2[5], r2[6], r2[7]],
                    [r3[0], r3[1], r3[2], r3[3], r3[4], r3[5], r3[6], r3[7]],
                    [r4[0], r4[1], r4[2], r4[3], r4[4], r4[5], r4[6], r4[7]],
                    [r5[0], r5[1], r5[2], r5[3], r5[4], r5[5], r5[6], r5[7]],
                    [r6[0], r6[1], r6[2], r6[3], r6[4], r6[5], r6[6], r6[7]],
                    [r7[0], r7[1], r7[2], r7[3], r7[4], r7[5], r7[6], r7[7]]]
     return None

#----------------------------------------------------------------------------

    def hent_ASCII (self):

        # brettet returneres som 8 tekststrenger - en for hver rad (1-8)

        brett = self.brett
        r8 = brett[7][0]+" "+brett[7][1]+" "+brett[7][2]+" "+brett[7][3]+" "+brett[7][4]+" "+brett[7][5]+" "+brett[7][6]+" "+brett[7][7]
        r7 = brett[6][0]+" "+brett[6][1]+" "+brett[6][2]+" "+brett[6][3]+" "+brett[6][4]+" "+brett[6][5]+" "+brett[6][6]+" "+brett[6][7]
        r6 = brett[5][0]+" "+brett[5][1]+" "+brett[5][2]+" "+brett[5][3]+" "+brett[5][4]+" "+brett[5][5]+" "+brett[5][6]+" "+brett[5][7]
        r5 = brett[4][0]+" "+brett[4][1]+" "+brett[4][2]+" "+brett[4][3]+" "+brett[4][4]+" "+brett[4][5]+" "+brett[4][6]+" "+brett[4][7]
        r4 = brett[3][0]+" "+brett[3][1]+" "+brett[3][2]+" "+brett[3][3]+" "+brett[3][4]+" "+brett[3][5]+" "+brett[3][6]+" "+brett[3][7]
        r3 = brett[2][0]+" "+brett[2][1]+" "+brett[2][2]+" "+brett[2][3]+" "+brett[2][4]+" "+brett[2][5]+" "+brett[2][6]+" "+brett[2][7]
        r2 = brett[1][0]+" "+brett[1][1]+" "+brett[1][2]+" "+brett[1][3]+" "+brett[1][4]+" "+brett[1][5]+" "+brett[1][6]+" "+brett[1][7]
        r1 = brett[0][0]+" "+brett[0][1]+" "+brett[0][2]+" "+brett[0][3]+" "+brett[0][4]+" "+brett[0][5]+" "+brett[0][6]+" "+brett[0][7]
        return r8,r7,r6,r5,r4,r3,r2,r1

#----------------------------------------------------------------------------

    def ASCII (self):

        # brettet returneres som 1 tekststreng

        brett = self.brett
        r9 = "   a b c d e f g h\n   ---------------\n"
        r8 = "8  "+ brett[7][0]+" "+brett[7][1]+" "+brett[7][2]+" "+brett[7][3]+" "+brett[7][4]+" "+brett[7][5]+" "+brett[7][6]+" "+brett[7][7]+"  8\n"
        r7 = "7  "+ brett[6][0]+" "+brett[6][1]+" "+brett[6][2]+" "+brett[6][3]+" "+brett[6][4]+" "+brett[6][5]+" "+brett[6][6]+" "+brett[6][7]+"  7\n"
        r6 = "6  "+ brett[5][0]+" "+brett[5][1]+" "+brett[5][2]+" "+brett[5][3]+" "+brett[5][4]+" "+brett[5][5]+" "+brett[5][6]+" "+brett[5][7]+"  6\n"
        r5 = "5  "+brett[4][0]+" "+brett[4][1]+" "+brett[4][2]+" "+brett[4][3]+" "+brett[4][4]+" "+brett[4][5]+" "+brett[4][6]+" "+brett[4][7]+"  5\n"
        r4 = "4  "+brett[3][0]+" "+brett[3][1]+" "+brett[3][2]+" "+brett[3][3]+" "+brett[3][4]+" "+brett[3][5]+" "+brett[3][6]+" "+brett[3][7]+"  4\n"
        r3 = "3  "+brett[2][0]+" "+brett[2][1]+" "+brett[2][2]+" "+brett[2][3]+" "+brett[2][4]+" "+brett[2][5]+" "+brett[2][6]+" "+brett[2][7]+"  3\n"
        r2 = "2  "+brett[1][0]+" "+brett[1][1]+" "+brett[1][2]+" "+brett[1][3]+" "+brett[1][4]+" "+brett[1][5]+" "+brett[1][6]+" "+brett[1][7]+"  2\n"
        r1 = "1  "+brett[0][0]+" "+brett[0][1]+" "+brett[0][2]+" "+brett[0][3]+" "+brett[0][4]+" "+brett[0][5]+" "+brett[0][6]+" "+brett[0][7]+"  1\n"
        r0 = "   ---------------\n   a b c d e f g h"
        return r9+r8+r7+r6+r5+r4+r3+r2+r1+r0

#----------------------------------------------------------------------------

    def hent_ASCII2 (self):

        # brettet returneres som en lang tekststreng - radene(1-8) er konkatenert

        brett = self.brett
        r8 = brett[7][0]+" "+brett[7][1]+" "+brett[7][2]+" "+brett[7][3]+" "+brett[7][4]+" "+brett[7][5]+" "+brett[7][6]+" "+brett[7][7]
        r7 = brett[6][0]+" "+brett[6][1]+" "+brett[6][2]+" "+brett[6][3]+" "+brett[6][4]+" "+brett[6][5]+" "+brett[6][6]+" "+brett[6][7]
        r6 = brett[5][0]+" "+brett[5][1]+" "+brett[5][2]+" "+brett[5][3]+" "+brett[5][4]+" "+brett[5][5]+" "+brett[5][6]+" "+brett[5][7]
        r5 = brett[4][0]+" "+brett[4][1]+" "+brett[4][2]+" "+brett[4][3]+" "+brett[4][4]+" "+brett[4][5]+" "+brett[4][6]+" "+brett[4][7]
        r4 = brett[3][0]+" "+brett[3][1]+" "+brett[3][2]+" "+brett[3][3]+" "+brett[3][4]+" "+brett[3][5]+" "+brett[3][6]+" "+brett[3][7]
        r3 = brett[2][0]+" "+brett[2][1]+" "+brett[2][2]+" "+brett[2][3]+" "+brett[2][4]+" "+brett[2][5]+" "+brett[2][6]+" "+brett[2][7]
        r2 = brett[1][0]+" "+brett[1][1]+" "+brett[1][2]+" "+brett[1][3]+" "+brett[1][4]+" "+brett[1][5]+" "+brett[1][6]+" "+brett[1][7]
        r1 = brett[0][0]+" "+brett[0][1]+" "+brett[0][2]+" "+brett[0][3]+" "+brett[0][4]+" "+brett[0][5]+" "+brett[0][6]+" "+brett[0][7]
        return r8+r7+r6+r5+r4+r3+r2+r1

#-----------------------------------------------------------------------------

    def kopi(self):

        b = Brett()
        temp=[]
        for i in range(8):
            rad = []
            for j in range(8):
                rad.append(self.brett[i][j])
            temp.append(rad)

        b.brett = temp
        b.hvit_konge_x = self.hvit_konge_x
        b.hvit_konge_y = self.hvit_konge_y
        b.sort_konge_x = self.sort_konge_x
        b.sort_konge_y = self.sort_konge_y

        b.hvit_antall_dronninger_og_taarn = self.hvit_antall_dronninger_og_taarn
        b.hvit_antall_boender = self.hvit_antall_boender
        b.hvit_antall_loepere = self.hvit_antall_loepere
        b.hvit_antall_springere = self.hvit_antall_springere
        b.sort_antall_dronninger_og_taarn = self.sort_antall_dronninger_og_taarn
        b.sort_antall_boender = self.sort_antall_boender
        b.sort_antall_loepere = self.sort_antall_loepere
        b.sort_antall_springere = self.sort_antall_springere

        return b

 #----------------------------------------------------------------------------

    def hent_brikke(self, x, y):

        grad_og_farge = self.brett[y][x]
        brikke = Brikke(grad_og_farge)
        return brikke

#----------------------------------------------------------------------------

    def hent_farge(self, x, y):

       if self.brett[y][x] == sk.TOM:
           return sk.TOM
       elif self.brett[y][x].isupper():
           return sk.HVIT
       else:
           return sk.SORT

#----------------------------------------------------------------------------

    def hent_fen_brett(self):

       fen_brett = ""

       for i in range(7, -1, -1):
           k = 0
           for j in range(8):
               if self.brett[i][j] == sk.TOM:
                   k = k + 1
               else:
                   if k == 0:
                       fen_brett = fen_brett + self.brett[i][j]
                   else:
                       fen_brett = fen_brett + str(k) + self.brett[i][j]
                       k = 0
           if k != 0:
                fen_brett = fen_brett + str(k)
           if i != 0:
                fen_brett = fen_brett + "/"

       fen_brett = fen_brett.replace("B", "P")
       fen_brett = fen_brett.replace("b", "p")
       fen_brett = fen_brett.replace("T", "R")
       fen_brett = fen_brett.replace("t", "r")
       fen_brett = fen_brett.replace("S", "N")
       fen_brett = fen_brett.replace("s", "n")
       fen_brett = fen_brett.replace("L", "B")
       fen_brett = fen_brett.replace("l", "b")
       fen_brett = fen_brett.replace("D", "Q")
       fen_brett = fen_brett.replace("d", "q")



       return fen_brett

#----------------------------------------------------------------------------

    def fen_til_brett(self, fen):

      fen = fen.replace("1", ".")
      fen = fen.replace("2", "..")
      fen = fen.replace("3", "...")
      fen = fen.replace("4", "....")
      fen = fen.replace("5", ".....")
      fen = fen.replace("6", "......")
      fen = fen.replace("7", ".......")
      fen = fen.replace("8", "........")

      lengde = fen.find(" ")
      temp = fen[0:lengde]
      temp = temp + "/"

      temp = temp.replace("B", "L")
      temp = temp.replace("b", "l")
      temp = temp.replace("P", "B")
      temp = temp.replace("p", "b")
      temp = temp.replace("R", "T")
      temp = temp.replace("r", "t")
      temp = temp.replace("N", "S")
      temp = temp.replace("n", "s")
      temp = temp.replace("Q", "D")
      temp = temp.replace("q", "d")

      temp = temp.split("/")

      r7 = temp[0]
      r6 = temp[1]
      r5 = temp[2]
      r4 = temp[3]
      r3 = temp[4]
      r2 = temp[5]
      r1 = temp[6]
      r0 = temp[7]


      return r7, r6, r5, r4, r3, r2, r1, r0




 #----------------------------------------------------------------------------

    def hent_konge_xy(self, farge):

        if farge == sk.HVIT:
            return self.hvit_konge_x, self.hvit_konge_y
        else:
            return self.sort_konge_x, self.sort_konge_y



#----------------------------------------------------------------------------

    def sett_konge(self, farge, x, y):

       if farge == sk.HVIT:
           self.hvit_konge_x = x
           self.hvit_konge_y = y
       else:
           self.sort_konge_x = x
           self.sort_konge_y = y
       return None


 #----------------------------------------------------------------------------

    def sett_brikke(self, x, y, brikke):

        self.brett[y][x] = brikke._grad_og_farge
        return None

#----------------------------------------------------------------------------

    def trekk(self, trekktype, bondeforvandling, x0, y0, x1, y1):

        tom = Brikke(sk.TOM)
        b = self.hent_brikke(x0, y0)
        b1 = self.hent_brikke(x1, y1)
        if b.grad == sk.KONGE:
            self.sett_konge(b.farge, x1, y1)

        if trekktype == sk.VANLIG_TREKK or trekktype == sk.AAPNINGSTREKK:
            grad_og_farge = self.brett[y0][x0]
            self.oppdater_antall_brikker(b1, -1)
            self.brett[y1][x1] = grad_og_farge
            self.brett[y0][x0] = sk.TOM
        elif trekktype == sk.KORT_ROKADE:
            konge = self.hent_brikke(x0, y0)
            if konge.farge == sk.HVIT:
                taarn = self.hent_brikke(7,0)
                self.sett_brikke(7, 0, tom)
                self.sett_brikke(4, 0, tom)
                self.sett_brikke(5, 0, taarn)
                self.sett_brikke(6, 0, konge)
                self.sett_konge(sk.HVIT, 6, 0)
            else:
                taarn = self.hent_brikke(7,7)
                self.sett_brikke(7, 7, tom)
                self.sett_brikke(4, 7, tom)
                self.sett_brikke(5, 7, taarn)
                self.sett_brikke(6, 7, konge)
                self.sett_konge(sk.SORT, 6, 7)
        elif trekktype == sk.LANG_ROKADE:
            konge = self.hent_brikke(x0, y0)
            if konge.farge == sk.HVIT:
                taarn = self.hent_brikke(0,0)
                self.sett_brikke(0, 0, tom)
                self.sett_brikke(4, 0, tom)
                self.sett_brikke(3, 0, taarn)
                self.sett_brikke(2, 0, konge)
                self.sett_konge(sk.HVIT, 2, 0)
            else:
                taarn = self.hent_brikke(0,7)
                self.sett_brikke(0, 7, tom)
                self.sett_brikke(4, 7, tom)
                self.sett_brikke(3, 7, taarn)
                self.sett_brikke(2, 7, konge)
                self.sett_konge(sk.SORT, 2, 7)
        elif trekktype == sk.BONDEFORVANDLING:
            self.oppdater_antall_brikker(b, -1)
            self.oppdater_antall_brikker(b1, -1)
            self.brett[y1][x1] = bondeforvandling
            b1 = self.hent_brikke(x1, y1)
            self.oppdater_antall_brikker(b1, 1)
            self.brett[y0][x0] = sk.TOM
        elif trekktype == sk.EN_PASSANT:
            bonde = self.hent_brikke(x0,y0)
            grad_og_farge = bonde._grad_og_farge
            self.brett[y1][x1] = grad_og_farge
            self.brett[y0][x0] = sk.TOM
            dx = x1 - x0
            b1 = self.hent_brikke(x0+dx, y0)
            self.brett[y0][x0+dx] = sk.TOM
            self.oppdater_antall_brikker(b1, -1)

        else:
            print (f"trekktype {trekktype}")
            input ("feil trekktype")

        return None

#----------------------------------------------------------------------------

    def oppdater_antall_brikker(self, brikke, inkr):

        if brikke.grad == sk.TOM:
            return

        if brikke.farge == sk.HVIT:
            if brikke.grad == sk.BONDE:
                self.hvit_antall_boender = self.hvit_antall_boender + inkr
            elif brikke.grad == sk.DRONNING or brikke.grad == sk.TAARN:
                self.hvit_antall_dronninger_og_taarn = self.hvit_antall_dronninger_og_taarn + inkr
            elif brikke.grad == sk.LOEPER:
                self.hvit_antall_loepere = self.hvit_antall_loepere + inkr
            else:
                self.hvit_antall_springere = self.hvit_antall_springere + inkr
        else:
            if brikke.grad == sk.BONDE:
                self.sort_antall_boender = self.sort_antall_boender + inkr
            elif brikke.grad == sk.DRONNING or brikke.grad == sk.TAARN:
                self.sort_antall_dronninger_og_taarn = self.sort_antall_dronninger_og_taarn + inkr
            elif brikke.grad == sk.LOEPER:
                self.sort_antall_loepere =  self.sort_antall_loepere + inkr
            else:
                self.sort_antall_springere =  self.sort_antall_springere + inkr

        #print("sjekk telling etter oppdatering")
        #self.sjekk_telling()

        return None

#-----------------------------------------------------------------------------


    def er_nok_materiell(self):

        # det finnes bønder = nok materiell
        if self.hvit_antall_boender > 0 or self.sort_antall_boender > 0:
            return True

        # det finnes dronning eller tårn = nok materiell
        if self.hvit_antall_dronninger_og_taarn > 0 or self.sort_antall_dronninger_og_taarn > 0:
            return True

        # kun 2 konger igjen = ikke nok materiell
        if (self.hvit_antall_loepere == 0 and self.hvit_antall_springere == 0 and
            self.sort_antall_loepere == 0 and self.sort_antall_springere == 0):
            return False

        # konge mot konge + springer eller løper = ikke nok materiell
        if ((self.hvit_antall_loepere == 1 and self.hvit_antall_springere == 0 and
             self.sort_antall_loepere == 0 and self.sort_antall_springere == 0) or

            (self.hvit_antall_loepere == 0 and self.hvit_antall_springere == 1 and
             self.sort_antall_loepere == 0 and self.sort_antall_springere == 0) or

            (self.hvit_antall_loepere == 0 and self.hvit_antall_springere == 0 and
             self.sort_antall_loepere == 1 and self.sort_antall_springere == 0) or

            (self.hvit_antall_loepere == 0 and self.hvit_antall_springere == 0 and
             self.sort_antall_loepere == 0 and self.sort_antall_springere == 1)):
            return False

        """
        # konge og løper mot konge og løper, med løpere på samme farge = ikke nok materiell
        if (self.hvit_antall_loepere == 1 and self.hvit_antall_springere == 0 and
            self.sort_antall_loepere == 1 and self.sort_antall_springere == 0):
            if self.loepere_paa_samme_farge():
                return False

        # konge mot konge og 2 løpere, med løpere på samme farge = ikke nok materiell
        if ((self.hvit_antall_loepere == 2 and self.hvit_antall_springere == 0 and
             self.sort_antall_loepere == 0 and self.sort_antall_springere == 0 ) or
            (self.hvit_antall_loepere == 0 and self.hvit_antall_springere == 0 and
             self.sort_antall_loepere == 2 and self.sort_antall_springere == 0)):
            if self.loepere_paa_samme_farge():
                return False

        # konge og løper mot konge og 2 løpere, med løpere på samme farge = ikke nok materiell
        if ((self.hvit_antall_loepere == 2 and self.hvit_antall_springere == 0 and
             self.sort_antall_loepere == 1 and self.sort_antall_springere == 0 ) or
            (self.hvit_antall_loepere == 1 and self.hvit_antall_springere == 0 and
             self.sort_antall_loepere == 2 and self.sort_antall_springere == 0)):
            if self.loepere_paa_samme_farge():
                return False
        """
        
        # konger og kun løpere på samme farge = ikke nok materiell
        if (self.hvit_antall_springere == 0 and self.sort_antall_springere == 0):
            if self.loepere_paa_samme_farge():
                return False



        # ellers er det nok materiale
        return True


#-----------------------------------------------------------------------------

    def loepere_paa_samme_farge(self):
        
        # tester om alle løperne står på samme farge

        funnet = False # har funnet første løper
        rute1 = False # løperne er ikke på samme farge ved start
        rute2 = True
        for i in range (0,8):
            for j in range (0,8):
                b = self.hent_brikke(i, j)
                if b.grad == sk.LOEPER:
                    if not funnet: # første løper er funnet
                        funnet = True
                        rute1 = (((i+j) % 2) == 0) # hvis rest = 0, sort rute = True, hvis ikke, hvit rute = False
                        rute2 = rute1 # hvis bare en løper så er det samme farge
                    else: # flere løpere er funnet
                        rute2 = (((i+j) % 2) == 0)
                        if not rute1 == rute2: # har funnet løpere på ulik farge og avslutter
                            return False                
        return rute1 == rute2

#-----------------------------------------------------------------------------

    def tell_antall_brikker(self):

        self.hvit_antall_dronninger_og_taarn = 0
        self.hvit_antall_boender = 0
        self.hvit_antall_loepere = 0
        self.hvit_antall_springere = 0
        self.sort_antall_dronninger_og_taarn = 0
        self.sort_antall_boender = 0
        self.sort_antall_loepere = 0
        self.sort_antall_springere = 0

        for i in range (0,8):
            for j in range (0,8):
                b = self.hent_brikke(i, j)
                if b.farge == sk.HVIT:
                    if b.grad == sk.DRONNING or b.grad == sk.TAARN:
                        self.hvit_antall_dronninger_og_taarn = self.hvit_antall_dronninger_og_taarn + 1
                    elif b.grad == sk.BONDE:
                        self.hvit_antall_boender = self.hvit_antall_boender + 1
                    elif b.grad == sk.LOEPER:
                        self.hvit_antall_loepere = self.hvit_antall_loepere + 1
                    elif b.grad == sk.SPRINGER:
                        self.hvit_antall_springere =  self.hvit_antall_springere + 1

                elif b.farge == sk.SORT:
                    if b.grad == sk.DRONNING or b.grad == sk.TAARN:
                        self.sort_antall_dronninger_og_taarn = self.sort_antall_dronninger_og_taarn + 1
                    elif b.grad == sk.BONDE:
                        self.sort_antall_boender = self.sort_antall_boender + 1
                    elif b.grad == sk.LOEPER:
                        self.sort_antall_loepere = self.sort_antall_loepere + 1
                    elif b.grad == sk.SPRINGER:
                        self.sort_antall_springere =  self.sort_antall_springere + 1


        return None



