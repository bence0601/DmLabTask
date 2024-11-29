# DmLabTask
This is a project to show of my skills in Python, Scraping from API-s, visualizing data, the way I solve problems
- jobb lett volna egy virtual env-ben elkezdeni az egészet
- Data collector servicenél nem igazán lett bonyolult a mappa szerkezet a kevés endpoint miatt elég volt egy routes.py file, nyilván lehetne szükség esetén többet is létrehozni, de ez a project nem lesz annyira komplex, hogy kelljen
- Lehetne több unit test, integration test, de most csak azt szerettem volna megmutatni, hogy fontosnak tartom a tesztelést, ezért TDD elven fejlesztettem
- CI/CD pipeline jó lenne, hogy ne kelljen minden alkalommal kitörölni majd újrabuildelni az imageket és a konténereket
- Data-Collection-Service routes.py-ban nem tudtam eldönteni, hogy jó ötlet lenne-e a class használata. Mivel ugyanarról az endpointról fetchelek mindig, és ehhez tartozik egy api kulcs, nem lenne rossz, mert akkor példányosításnál megadhatnám ezeket, viszont összesen 2 endpoint van ebben a szervízben, így kicsit feleslegesnek érzem
- lehetne egy admin felület is akár, regisztációval/bejelentkezéssel, de most nem akartam ezzel bonyolítani a dolgokat, inkább az MLOps részéré akartam kitérni, hogy egy jól működő/könnnyen karbantartható koncepcióval tudjak előállni
- db-t módosítani nem lehet, nincs rá szüksége egy usernek aki az időjárást szeretné megtudni, egyébként a yaml összerakja ezt is
- 
