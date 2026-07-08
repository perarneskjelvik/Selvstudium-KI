"""
Modul: sjakk_konstanter.py

Opprettet: 23.2.2022
@author: Per Arne Skjelvik

Modulen inneholder alle konstantene som brukes for å spille sjakk.
"""

############################################################################


AUTO = "auto"
MANUELL = "manuell"
AVSLUTT = "x"
OK = ""



# konstanter for hver brikke

LOEPER = "l"
BONDE = "b"
SPRINGER = "s"
TAARN = "t"
KONGE = "k"
DRONNING = "d"
TOM = "."
HVIT = "hvit"
SORT = "sort"

# konstanter for hver type trekk

KORT_ROKADE = "kort rokade"
LANG_ROKADE = "lang rokade"
EN_PASSANT = "en passant"
BONDEFORVANDLING = "bondeforvandling"
VANLIG_TREKK = ""
AAPNINGSTREKK = "åpningstrekk"

# konstanter for resultat etter et trekk

REMIS_75 = "Partiet endte med remis etter 75 trekk uten slag eller flytting av bonde."
REMIS_5 = "Partiet endte med remis etter fem like stillinger."
REMIS_PATT = "Partiet endte med remis pga patt."
REMIS_MATERIELL = "Partiet endte med remis pga manglende material."
REMIS_DOED_STILLING = "Partiet endte med remis pga død stilling."
SJAKKMATT = "Partiet endte med sjakkmatt."
PAAGAAR = "Pågår."
SJAKK = "Sjakk"
AVSLUTTET = "Partiet ble avsluttet av en av spillerne"
TIDSFRIST = "Partiet ble avsluttet fordi tiden var brukt opp."
FEIL = "FEIL"

# søkemetoder

TILFELDIG = 0
MINIMAX = 1
ALPHABETA = 2
MONTECARLO = 3

# evalueringsmetoder

INGEN_EVALUERING = 0
MATERIELL = 1
MATERIELL_PLASSERING = 2

# andre konstanter som styrer motoren

UTGANGSSTILLING = ""
UTGANGS_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

MINMAX_DYBDE = 2
ALPHABETA_DYBDE = 3
ALPHABETA_ANTALL_TREKK = 100
MAKS_TREKK = 500

ANTALL_REMIS_75 = 150
MAKS_TID = 60

PLASSVERDI  = [[1, 1, 1, 1, 1, 1, 1, 1], 
               [1, 1, 1, 1, 1, 1, 1, 1],
               [1, 1, 2, 2, 2, 2, 1, 1],
               [1, 1, 2, 9, 9, 2, 1, 1],
               [1, 1, 2, 9, 9, 2, 1, 1],
               [1, 1, 2, 2, 2, 2, 1, 1],
               [1, 1, 1, 1, 1, 1, 1, 1],
               [1, 1, 1, 1, 1, 1, 1, 1]]