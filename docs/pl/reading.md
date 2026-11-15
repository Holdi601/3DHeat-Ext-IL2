---
title: "Jak czytane są pliki"
nav_order: 5
lang: pl
source: reading.md
source_hash: "3c0d5d19e02e"
nav_exclude: true
search_exclude: true
---
# Jak czytane są pliki {#how-the-files-are-read}

| Część | Stan |
|---|---|
| Archiwa (`data/*.gtp`, Great Battles) | tabela plików (rekordy `S16R`, `STRMFAT?`, `DIR!`/`FILE`) i wpisy (nagłówek `STRMFILE`, dane zapisane tak, jak są); każdy `Maps*.gtp` testowej instalacji |
| `height.hini` | `height_map`, `water_map`, `heightMul`, `SeaLevel`, limity obszaru gry i `MapNW/NE/SE/SW`; każdy z testowej instalacji |
| Mapy wysokości (`height.dat`) | kodek opisany niżej; każdy sektor map zdekodowany w całości podczas jego opracowywania wykorzystuje swój strumień bitów dokładnie (co najwyżej dopełnienie bajtem), reszta sprawdzona po nagłówku. Sprawdzone bit w bit względem nieskompresowanych plików `distlod.raw`, które gra dostarcza obok `distlod.dat`, oraz względem własnej mapy wysokości z odległym LOD mapy (korelacja 0,999) |
| Wysokości | metry = surowe x heightMul / 256 - SeaLevel x heightMul. Morze mapy dekoduje się dokładnie do wysokości podanej w komentarzach jej hini; granica innej - do jej `bounds_level` |
| Umieszczenie | dwuliniowe między czterema rogami hini, wiersz 0 na północ, kolumna 0 na zachód. Sprawdzone na mapie względem znanych miast, wybrzeży i mórz (wysokości miast w granicach około 10 m od prawdziwych, morza poniżej poziomu morza). Rogi tworzą czworokąt, a nie projekcję gry, więc w środku dużej mapy spodziewaj się błędu rzędu kilkuset metrów. Hini jednej rodziny map niesie rogi innej mapy (rozpinają ułamek jej prawdziwego rozmiaru); jest to wykrywane, a ta rodzina zamiast tego jest umieszczana dopasowaniem do punktów orientacyjnych: miast i lotnisk z własnych baz położeń gry (`*.ldfbin`) względem ich prawdziwych pozycji, błąd średniokwadratowy rzędu kilku kilometrów (miasta względem lotnisk nazwanych od nich, a współrzędne prawdziwych miejsc z dokładnością do około kilometra); JSON wymienia każdy punkt orientacyjny i jego błąd |
| Maska wody (`water.wtr`: cztery poziomy piramidy kafli, każdy kafel to tabela bloków po 400 m, każdy blok jest lądem, pełny albo częściowo wodny z kształtem w strumieniu bitów) | kontener jest czytany na każdej mapie (w plikach zdekodowanych w całości nie zostaje żaden bajt); kształt wewnątrz bloku częściowo wodnego **nie jest dekodowany**. Pełne bloki są wodą; w blokach częściowo wodnych próbka jest wodą tam, gdzie mapa wody (`height_w.dat`, ten sam kodek co mapa wysokości) leży powyżej terenu, albo, przy jeziorze, tam, gdzie teren nie jest wyższy niż jezioro; bloki lądowe są suche. To usuwa bagno, które sama mapa wody uznaje za wodę. Rzeki węższe niż siatka wyjściowa wychodzą pocięte na kawałki |
| Obrysy miast (siatki naklejek, które wymienia `textures.tini`: `towns.mesh`, `cities.mesh`, `city_*.mesh`, `roads_fields.mesh`, ...: kafle 25,6 km płaskich, teksturowanych trójkątów) | czytane na każdej mapie; zachowywane są ściany, których tekstura to miasto, wieś albo teren przemysłowy. Sprawdzone względem prawdziwych miast na kilku mapach (miasto po obu brzegach rzeki, ujście). To obrysy: budynki gra umieszcza w czasie działania, a pliki nie zawierają budynków |
| Lotniska, mosty, budynki | **nieodczytane**: lotniska to obiekty misji, budynki pochodzą z umieszczania przez samą grę |
| Lasy (`forest_map.wtr`) | jego bloki czyta się tak samo, ale prawie każdy blok to „częściowo las”, więc bez strumienia bitów nie ma użytecznej maski lasu; nie jest rysowany |
| Tekstury terenu | nieodczytane |

## Kodek mapy wysokości {#the-heightmap-codec}

Opracowany wyłącznie z plików danych; nie czytano ani nie dezasemblowano kodu gry.
Little-endian:

```text
u32 width, u32 height, u32 sectorsX, u32 sectorsY, u32 sectorSize, f32 cellSize
u32 offset[sectorsX * sectorsY]            od początku pliku, wiersz po wierszu, wiersz górny pierwszy
sector: u16 count (bajty, które następują), u16 mode ((log2 sectorSize) << 4 | LW, LW = 4),
        potem strumień bitów czytany od najstarszego bitu:
  PRE   2 * (log2(sectorSize) - 5) bitów, dotąd zawsze 0
  LIT   pierwsza próbka: znak (1), n (LW bitów), wielkość (n + 1 bitów)
  potem aż sektor się zapełni:
    0 LIT       następna = poprzednia + LIT
    1 RUN LIT   poprzednia próbka powtarza się RUN razy (k: 3 bity, m: k + 1 bitów, RUN = m + 1),
                potem (chyba że sektor jest pełny) następna = poprzednia + LIT
  wartości są 16-bitowe: odczytuj je modulo 65536
```

Niepełne sektory przy prawej i dolnej krawędzi są dopełniane i przycinane. Ten sam kodek obejmuje
mapę wody i mapę wysokości odległego LOD.

## Dopasowania do punktów orientacyjnych {#landmark-fits}

Tam, gdzie rogów mapy nie da się użyć, `landmarks.py` dopasowuje przekształcenie afiniczne z metrów gry
na Ziemię metodą najmniejszych kwadratów: pozycje w grze z własnych plików użytkownika (bloki `Airfield` misji,
bazy danych położeń kariery), prawdziwe pozycje z tabel opublikowanych współrzędnych miejsc w kodzie.
`georeference` w JSON niesie macierz, początek, każdy punkt orientacyjny z jego błędem oraz rms.
