"""

Module: hovedprogram.py.
Opprettet: 5.1.2022
@author: Per Arne Skjelvik

Hovedprogram som spiller sjakk.

Bruker modulene:
   sjakkmotpr.py - en sjakkmotor
   brukerdialog.py - windows cmd brukergrensesnitt
   sjakk_konstanter.py - inneholder en rekke globale konstanter
   
   testchess.py - tester korrekte trekk og stillinger

Har klassene:
    Spiller - gjennomfører neste trekk

"""

import sjakk_konstanter as sk
import brukerdialog as ui
import sjakkmotor as pd

# testformål
# import testchess as t
import tid 


class Spiller:

    """

    Spiller.
    Et objekt av klassen Spiller vet hviken farge den har (HVIT/SORT), hvilken
    spillertype den er (AUTO/MANUELL), hvilken sjakkmotor den kommuniserer med
    for å trekke/finne beste trekk og hvilket brett den kommuniserer med for å
    hente og vise trekket (brukerdialogen).

    Et objekt har følgende eksterne attributter og metoder:
    - farge
    - trekk ()

    """

# -----------------------------------------------------------------------------

    def __init__(self, farge, spillertype, sjakk_motor, ui_brett):

        self.farge = farge
        self._spillertype = spillertype
        self._motor = sjakk_motor
        self._brett = ui_brett
        self.stilling = [None] *  50
        self.stilling[0] = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
        self.stilling[1] = "r1bqkb1r/pppp1ppp/2n2n2/4p2Q/2B1P3/8/PPPP1PPP/RNB1K1NR w - - 0 1"
        self.stilling[2] = "r1r1q1k1/6p1/3b1p1p/1p1PpP2/1Pp5/2P4P/R1B2QP1/R5K1 w - - 0 1"
        return None

# -----------------------------------------------------------------------------

    def trekk(self):

        """
        Gjennomfører neste trekk, enten manuelt ved å hente et trekk fra bruker
        eller automatisk ved å be sjakkmotoren om å gjøre det beste trekket.
        """

        farge = self._motor.hent_neste_trekk_farge()
        trekk_nr = self._motor.hent_neste_trekk_nr()

        if self._spillertype == sk.MANUELL:
            feilmelding = sk.FEIL
            while feilmelding == sk.FEIL:
                melding, spesialtrekk, fra, til = self._brett.hent_trekk(farge, trekk_nr)
                if melding == sk.AVSLUTT:
                    self._motor.trekk(melding, spesialtrekk, fra, til)
                else:
                    feilmelding, test_brett = self._motor.sjekk_trekk(melding, spesialtrekk, fra, til)
                    if feilmelding == sk.OK:
                         resultat = self._motor.trekk(melding, spesialtrekk, fra, til)
                         evaluering = ""
                         self._brett.vis_trekk(farge, trekk_nr, spesialtrekk, fra, til, resultat, evaluering)
                    else:
                        self._brett.vis_feilmelding(feilmelding)

        else:
            trekktype, bondeforvandling, farge, grad, fra, til, resultat, evaluering = self._motor.beste_trekk()
            #self._brett.vis_trekk(farge, grad, trekk_nr, trekktype, bondeforvandling, fra, til)

        return None

# -----------------------------------------------------------------------------

    def hent_stilling(self, i):

        """
        Henter en forhåndsdefinert stilling. FEN
        """

        return self.stilling[i]

# -----------------------------------------------------------------------------

# Hovedprogram

# lokale variabler

sjakk_motor = None
ui_brett = None
hvit_spiller = None
sort_spiller = None
spiller = None
resultat = ""


# tellere for resultat ved massetest

hvit_vinner = 0
sort_vinner = 0
remis_patt = 0
remis_5 = 0
remis_75 = 0
remis_material = 0
remis_doed_stilling = 0


# initierer lokale variabler

INGEN_EVALUERING = 0
MATERIELL = 1

sjakk_motor = pd.SjakkMotor()
ui_brett = ui.UI_Brett()
hvit_spiller = Spiller(sk.HVIT, sk.AUTO, sjakk_motor, ui_brett)
sort_spiller = Spiller(sk.SORT, sk.AUTO, sjakk_motor, ui_brett)
# sjakk_motor.sett_spillere(1, sk.ALPHABETA, 0, sk.TILFELDIG)
sjakk_motor.sett_spillere(sk.INGEN_EVALUERING, sk.ALPHABETA, sk.INGEN_EVALUERING, sk.TILFELDIG)

# testformål
#test = t.Sjakktest(ui_brett, sjakk_motor)
start = tid.naa()

#test.debug(f"{start}")

for i in range(0, 10):

    spiller = hvit_spiller
    fen = spiller.hent_stilling(0)

    sjakk_motor.sett_utgangsstilling()
    # sjakk_motor.sett_stilling(fen)

    # testformål
    #sjakk_motor.sett_test(test, fen)

    # if sjakk_motor.hent_neste_trekk_farge() == sk.HVIT:
    spiller = hvit_spiller
    # else:
    #    spiller = sort_spiller

    print(f"Starter parti {i+1}")
   # test.debug(f"Starter parti {i+1}")


    while not sjakk_motor.parti_er_ferdig():
        #print("")
        #print(f"Trekk {sjakk_motor.hent_neste_trekk_nr()} {sjakk_motor.hent_neste_trekk_farge()} i stilling:")
        #print(sjakk_motor.ASCII_trekk_brett_fen())
        
        spiller.trekk()
        if spiller.farge == sk.HVIT:
            spiller = sort_spiller
        else:
            spiller = hvit_spiller

    print(sjakk_motor.ASCII_trekk_brett_fen())
    resultat = sjakk_motor.hent_resultat()
    ui_brett.vis_resultat(resultat)
    
    #test.test_sluttstilling()

    
    # tellere for resultat ved massetest
    if resultat == sk.SJAKKMATT and sjakk_motor._stilling._skjema.vinner == sk.HVIT:
        hvit_vinner = hvit_vinner + 1
    elif resultat == sk.SJAKKMATT and sjakk_motor._stilling._skjema.vinner == sk.SORT:
        sort_vinner = sort_vinner + 1
    elif resultat == sk.REMIS_PATT:
        remis_patt = remis_patt + 1
    elif resultat == sk.REMIS_5:
        remis_5 = remis_5 + 1
    elif resultat == sk.REMIS_75:
        remis_75 = remis_75 + 1
    elif resultat == sk.REMIS_MATERIELL:
        remis_material = remis_material + 1
    else:
        remis_doed_stilling = remis_doed_stilling + 1
    vinner = hvit_vinner + sort_vinner
    remis = (i+1) - vinner
    if vinner > 0:
        vinner = round(100*vinner/(i+1))
    if remis > 0:
        remis = round(100*remis/(i+1))
    
    
    

# tellere for resultat ved massetest
print(f" ")
print(f"Antall parti: {i+1}")
print(f"Vinner vs Remis: {vinner}% vs {remis}%")
print(f"Hvit vinner: {hvit_vinner}")
print(f"Sort vinner: {sort_vinner}")
print(f"Remis patt: {remis_patt}")
print(f"Remis 5: {remis_5}")
print(f"Remis 75: {remis_75}")
print(f"Remis materiell: {remis_material}")
print(f"Remis død stilling: {remis_doed_stilling}")

