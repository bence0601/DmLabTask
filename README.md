Projekt Összefoglaló

Ebben a projektben a DmLab számára készítettem egy házifeladatot a szoftverfejlesztő pozícióra történő jelentkezésem részeként.
A feladat célja az időjárás előrejelzésének modellezése egy adott városra, a WeatherAPI segítségével.
Az alkalmazás a következő fő funkciókat valósítja meg:

**Data-Collection-Service**: Külső API-ból időjárási adatok lekérése.

**Data-Manipulation-Service**: Időjárási jelentés készítése az adatokból.

Mindkét service-hez tartozik egy-egy Postgres adatbázis.


**Architecturális Szempontok**
A projekt mikroszervíz alapú architektúrát követett, 4 fő komponenssel:

Data Collection Service
Data Manipulation Service
Két külön Postgres adatbázis
(Tervezett) Frontend alkalmazás

Az alkalmazás jelenleg AWS EC2-n fut, 4 konténerben, amelyeket egyelőre Docker Compose segítségével kezelek.

**Data Collection Service**

Feladat: Időjárási adatok lekérése a WeatherAPI-ról és tárolása Postgres adatbázisban.
Konfiguráció:

API kulcs és adatbázis kapcsolat az .env fájlban.


**Seeder**:
Mivel az API már nem támogatja a batch lekérést, az első indításkor lefut egy db-seeder, amely generál adatokat az alábbi városokhoz:

Budapest
Bécs
Debrecen
Lisszabon
New York




**Data Manipulation Service**

Feladat: Az adatbázisban tárolt adatokból átlagos értékek számítása (hőmérséklet, csapadék, szél erőssége).
Egyszerűsítés oka:
Az előző megoldásnál lineáris regresszióval jósoltam, de az API változása miatt most csak aggregált átlagokat számolok.


API Endpoint
Az alkalmazás elérhető itt:
http://51.20.70.80:5000/dms/get-forecast/{város}

**Használat**: {város} helyére írd be az egyik támogatott várost (Budapest, Bécs, Debrecen, Lisszabon, New York).
Válasz:

Város neve
Hőmérséklet
Csapadék
Szél erőssége

**Teszteléshez Postman ajánlott**.

**Deployment**

Platform: AWS EC2
Konténerek: 4 Docker konténer (2 service + 2 adatbázis)
Orchestration: Docker Compose (később Kubernetes tervezett)


Refaktorálás és Minőségbiztosítás

A projekt egy korábbi kódbázis refaktorálása volt, a cél a best practice-ek betartása.
Kódminőség:

black és mypy manuális futtatása (CI/CD-be tervezett integráció).


További fejlesztési tervek:

CI/CD pipeline létrehozása (linting, tesztelés, deploy)
Frontend implementálása
Kubernetes alapú skálázás




Megjegyzés
Az előző felvételinél nem a modellkészítés volt a probléma, ezért most a kódminőségre és a deployra fókuszáltam.
