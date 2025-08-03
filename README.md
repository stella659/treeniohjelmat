# treeniohjelmat
Sovelluksen idea:
  * Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään sovellukseen.
  * Käyttäjä pystyy lisäämään, muokkaamaan ja poistamaan lisäämiään treeniohjelmia.
  * Käyttäjä näkee sovellukseen lisätyt treeniohjelmat (omat ja muiden laittamat).
  * Käyttäjä pystyy etsimään treeniohjelmia hakusanalla.
  * Sovelluksessa on käyttäjäsivut, jotka näyttävät tilastoja käyttäjän lisäämistä treeniohjelmista. (kesken)
  * Käyttäjä pystyy valitsemaan keskustelulle tai viestille yhden tai useamman luokittelun (esim. voimaharjoittelu, cardio, yhdistelmä) (kesken)
  * Käyttäjä voi jättää kommenteja ja arvioita treeniohjelmista ja nämä näkyvät myös muille. (kesken)

Ohjeet sovelluksen testaamiseen:
Sovellukseen tarvitsee Pythonia ja tietokantaa
 
1. Sovelluksen asennus komentotulkilla:
  git clone https://github.com/kayttaja/treeniohjelmat.git
  cd treeniohjelmat

2.Luo virtuaaliympäristö:
  python3 -m venv venv
  source venv/bin/activate
  
3.avaa tietokanta:
  sqlite3 database.db
  
4.Kirjoita tietokantaan:
  sqlite3 database.db < schema.sql
  
5.poistu tietokannasta:
  .quit
  
6.Virtuaaliympäristössä(venv):
 flask run
  
7. siirry komennon antamalle http sivustolle selaimessa ja testaa sovellusta
