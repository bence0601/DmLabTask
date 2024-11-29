# DmLabTask
This is a project to show of my skills in Python, Scraping from API-s, visualizing data, the way I solve problems
- jobb lett volna egy virtual env-ben elkezdeni az egészet
- Data collector servicenél nem igazán lett bonyolult a mappa szerkezet a kevés endpoint miatt elég volt egy routes.py file, nyilván lehetne szükség esetén többet is létrehozni, de ez a project nem lesz annyira komplex, hogy kelljen
- Lehetne több unit test, integration test, de most csak azt szerettem volna megmutatni, hogy fontosnak tartom a tesztelést, ezért TDD elven fejlesztettem
- CI/CD pipeline jó lenne, hogy ne kelljen minden alkalommal kitörölni majd újrabuildelni az imageket és a konténereket
- Data-Collection-Service routes.py-ban nem tudtam eldönteni, hogy jó ötlet lenne-e a class használata. Mivel ugyanarról az endpointról fetchelek mindig, és ehhez tartozik egy api kulcs, nem lenne rossz, mert akkor példányosításnál megadhatnám ezeket, viszont összesen 2 endpoint van ebben a szervízben, így kicsit feleslegesnek érzem
- lehetne egy admin felület is akár, regisztációval/bejelentkezéssel, de most nem akartam ezzel bonyolítani a dolgokat, inkább az MLOps részéré akartam kitérni, hogy egy jól működő/könnnyen karbantartható koncepcióval tudjak előállni
- db-t módosítani nem lehet, nincs rá szüksége egy usernek aki az időjárást szeretné megtudni, egyébként a yaml összerakja ezt is
- utolag lehet ugy csinalnam, hogy az adatok db-bol valo lekereset is athelyeznem a data-collection-service-be, és a data-manipulation-service csak megkapna api-n keresztul az adatokat feldolgozásra
- utolag: a fetch_for_today vagy fetch_for_Week functiont lehetett volna megírni ugy is, hogy a frontendrol beolvassa, mi van a gombon, ezt atadom egy parameterkent a functionnek, és ettől függően fordul le a kód. Bár ezt nem lett volna utólag implementálni, szerintem átláthatóbb két külön function+ Clean Code könyvre hivatkoznek itt, ha elolvassuk a function nevet, nem kell a functiont végigolvassuk, és pontosan az fog történni, amire számítunk
-api key-t lehetne ugye egy sessionstorage-ban tárolni, vagy mégjobb lenne mondjuk egy JWT token, amiben a user data mellé bedobjuk a tokent
