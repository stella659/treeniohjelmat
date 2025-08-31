# Treeniohjelmat
## Sovelluksen toiminnot

  * Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään sovellukseen.
  * Käyttäjä pystyy lisäämään, muokkaamaan ja poistamaan treeniohjelmia.
  * Käyttäjä näkee sovellukseen lisätyt treeniohjelmat.
  * Käyttäjä pystyy etsimään treeniohjelmia hakusanalla.
  * Sovelluksessa on käyttäjäsivut, jotka näyttävät tilastoja käyttäjän lisäämistä treeniohjelmista.
  * Käyttäjä pystyy valitsemaan treenille yhden tai useamman luokittelun Esim. intensiteetin tai tyypin.
  * Käyttäjä voi jättää kommentteja ja arvioita treeniohjelmista.

## Sovelluksen asennus

Asenna `flask`-kirjasto
```
$ pip install flask
```
Luo tietokannan taulut ja lisää alkutiedot:
``` 
$ sqlite3 database.db < schema.sql
$ sqlite3 database.db < init.sql
```
Käynnistä sovellus:
```
$ flask run
``` 
