Projekt Összefoglaló
Ebben a projektben a DmLab számára készítettem egy házifeladatot a szoftverfejlesztő/MLOps pozícióra történő jelentkezésem részeként. A feladat célja az időjárás előrejelzésének modellezése egy adott városra, a WeatherAPI segítségével. Az alkalmazás a következő funkciókat valósítja meg:

- Az API használatával időjárási adatokat gyűjt városonként.
- A begyűjtött adatok alapján készít egy modellt, amely megjósolja az időjárást a következő három napra.
- Az időjárási adatokat oszlopdiagramokon jeleníti meg.


**Architecturális Szempontok**
A projekt mikroszervíz alapú architektúrát követett, három fő komponenssel:

**Data Collection Service:**

Feladata: Időjárási adatok lekérése a WeatherAPI-ról és az adatok tárolása egy MSSQL adatbázisba.
Az API kulcs és az adatbázis kapcsolat az .env fájlban tárolódik.

**Data Manipulation Service (ML Model):**

Feladata: Az összegyűjtött időjárási adatok feldolgozása és a háromnapos előrejelzés elkészítése.
A modellt lineáris regresszió segítségével készítettem el.

**Frontend**:

A frontend még nem készült el teljesen, de az alapötletet megvalósítottam. Az oszlopdiagramok elkészítéséhez külső könyvtárat terveztem használni, és feltételes renderelést valósítottam volna meg a különböző típusú adatmegjelenítéshez.

**Technikai Részletek**
1. Előkészületek
API Kulcs: A WeatherAPI oldalán regisztrálva API kulcsot kaptunk, amit az alkalmazás az .env fájlban tárol.
Adatbázis: MSSQL adatbázist használtam, amelyet konténerizáltam, és az adatbázis kapcsolatot szintén az .env fájlban adtam meg.
Base URL: A WeatherAPI History URL verizóját szintén az .env fájlban tároljuk.
2. Konténerizálás és CI/CD
A projekt konténerizált verzióját egy Dockerfile tartalmazza a Data Collection Service számára.
A CI/CD pipeline megépítése nem történt meg, de szükséges lett volna a projekt többi szervizének konténerizálása és egy megfelelő pipeline kialakítása, hogy automatikusan épüljön és deploy-olódjon a projekt.
3. Backend
A backend a következőképpen működik:

**Időjárás Jelentés Generálása: A data manipulation szerviz tartalmaz egy app.py fájlt, amely felelős az időjárás előrejelzésért. A backend jól működik, és képes generálni az előrejelzést, ha megfelelő mennyiségű adat áll rendelkezésre. Az előrejelzéshez minimum 7 napnyi adat szükséges, de több adatot is felhasznál, amennyiben az eltérés nem haladja meg a 3 napot.**

**4. Frontend**

A frontend elkészítése során a következőket terveztem:

Oszlopdiagramok: A hőmérsékletet, csapadékot és széladatokat oszlopdiagramokon ábrázoltam volna, hogy az adatok könnyen értelmezhetők legyenek.
Feltételes Renderelés: A megjelenítést úgy alakítottam volna ki, hogy a felhasználó döntése szerint aktuális időjárást vagy előrejelzést lásson.
A frontend még nem készült el teljesen, de az alapjaiban kész volt. Jelenleg hibát dob, ha backend kérést küldünk, de egy npm start-tal elindítható lenne.

**5. Fejlesztési és Tesztelési Módszertan**

TDD (Test Driven Development) alapelv alapján fejlesztettem, azonban mivel egyszer újra kellett kezdenem a projektet, a unit tesztek és integrációs teszteK az egyik szerviznél nem az első lépéként kerültek be. Ezt a Data-Manipulation-Servize-nél orvosoltam. Jelenleg néhány teszt érhető el, de a tesztelés bővítése szükséges lenne.

6. Javaslatok és Fejlesztési Lehetőségek

Virtuális Környezet Használata: A projektet érdemes lett volna egy virtuális környezetben (virtualenv) elkészíteni, hogy a requirements.txt csak a szükséges függőségeket tartalmazza.
További Tesztelés: A unit és integrációs tesztek bővítése elengedhetetlen a projekt stabilitásának növelése érdekében.
Admin Felület: A fejlesztők munkáját segítené egy admin felület, amely lehetővé teszi az adatbázis könnyű dumpolását és kezelését.
Model Tuning: A lineáris regresszió alapú előrejelzés javítása érdekében a jövőben érdemes lenne további adatokat (például légnyomást vagy szélirányt) figyelembe venni. Illetve még több adat kéne, hogy pontos előrejelzést kapjunk, viszont Az API ingyenes verziója miatt jelenleg legfeljebb 7 napnyi adat áll rendelkezésre
Automatikus Adatlekérés: Lehetőség lenne arra, hogy a rendszer automatikusan kérje le az adatokat egy előre meghatározott időszakban, hogy folyamatosan frissek maradjanak az előrejelzések.
Refaktorálás: A kódban számos komment található, amelyek tisztítandók lennének, hogy megfeleljenek a Clean Code elveinek.
Adatbázis Indexelés: Nagyobb adatmennyiség esetén érdemes lenne az adatbázist indexelni, hogy gyorsabb lekérdezéseket lehessen végrehajtani.
7. Jövőbeli Fejlesztések
CI/CD Pipeline: Automatikus build és deployment pipeline kialakítása Docker és Kubernetes használatával.
Docker Compose: Több szerviz konténerizálása és a projekt teljes körű konténer menedzselése.
Dokumentáció: A fejlesztés során elért eredmények és a jövőbeli tervekkel kapcsolatos dokumentáció további részletes kiegészítése.
