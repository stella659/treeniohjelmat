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
  git clone https://github.com/stella659/treeniohjelmat.git ja
  cd treeniohjelmat

2.Luo virtuaaliympäristö:
  python3 -m venv venv ja
  source venv/bin/activate
  
4.Luo tietokanta:
  sqlite3 database.db < schema.sql
  
6.Käynnistä flask virtuaaliympäristössä(venv):
 flask run
  
7. Siirry komennon antamalle http sivustolle selaimessa ja testaa sovellusta
