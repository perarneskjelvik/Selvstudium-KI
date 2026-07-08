# Sjakk

Jeg har aldri spilt sjakk. Da jeg skulle lære med Python tenkte jeg imidlertid at det ville være en grei oppgave å lage en sjakkmotor.
Som sagt så gjort. Målet var selvsagt å slå Stockfish, men resultatet ble en motor som akkurat greier å slå en spiller som trekker helt tilfeldig.
I ettertid ser jeg at jeg selvsagt skulle løst dette vha bitmaps istedenfor rett-fram-programmering, men jeg lærte meg ihvertfall Python.

En sentral del av en sjakkmotor er søkealgoritmen (i tillegg til evalueringsfunksjonen selvsagt). Her har jeg implementeret Alpha-Beta pruning i minimax algoritmen.

Teoretisk bakgrunn fra boken "Neural Networks For Chess" (Dominik Klein, 2022).

https://github.com/asdfjkl/neural_network_chess

<img src="./images/chess.jpg" width="300">
