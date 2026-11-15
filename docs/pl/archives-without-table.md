---
title: "Archiwa bez tabeli plików"
nav_order: 6
lang: "pl"
source: archives-without-table.md
source_hash: "58c4c46721e5"
nav_exclude: true
search_exclude: true
---
# Gra, której archiwa nie mają tabeli plików {#a-game-whose-archives-have-no-file-table}

IL-2 Series: Korea nie zachowuje czytelnej tabeli plików w swoich archiwach (nazwy są zahaszowane
w bloku na końcu każdego archiwum), a jej pliki ustawień nie są zapisane czytelnie. `list` pokazuje jej mapę
z grą `Korea`. Zatem:

- jej mapa wysokości i mapa wody są znajdowane po nagłówku (układ `height.dat`, sektory po 128 próbek;
  bardzo duża siatka przy drobnej komórce);
- jest umieszczana na Ziemi przez dopasowanie lotnisk, które umieszczają jej misje
  (`data/Missions/**/*.Mission`, czytane na twoim komputerze), do opublikowanych współrzędnych prawdziwych lotnisk
  (`korea.py`): odchyłki rzędu dziesiątek do kilkuset metrów. JSON wymienia każdy punkt orientacyjny i jego odchyłkę;
- heightMul i SeaLevel są szacowane: okręty w misjach stoją na morzu, więc ich wysokość nad najczęstszą
  (morską) wartością mapy wody daje skalę. Wysokości wychodzą wiarygodne (morze poniżej poziomu morza,
  miasta nadbrzeżne kilka metrów nad nim), nie sprawdzane dalej. JSON oznacza je jako szacowane.
