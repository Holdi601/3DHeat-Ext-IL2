---
title: "Seviyeleri oluşturma: extract"
nav_order: 3
lang: tr
source: extract.md
source_hash: "69fb5c2ddfa7"
nav_exclude: true
search_exclude: true
---
# Seviyeleri oluşturma: `extract` {#building-levels-extract}

```text
heat3d-il2-level extract (<map> ... | --all) -o <folder> [--game FOLDER ...]
                 [--max-grid N] [--frame enu|game] [--origin LAT LON]
                 [--no-water] [--no-towns] [--skip-existing]
```

## Adım adım {#step-by-step}

Komut satırında yeni misiniz? Önce [Başlamadan önce](before-you-start.md) sayfasını okuyun.

1. Haritanın adını [`list`](list.md) ile bulun.
2. `heat3d-il2-level extract <map> -o levels` çalıştırın. Adlar joker karakter kullanabilir, tırnak içinde (`"<family>_*"`); `--all` her haritayı alır.
3. Bir kaydı, yerleştirme adımı olmadan seviyeye oturtmak için başlangıç noktasını verin: `--origin <lat> <lon>`, kaydın `geo` değeri (oturumunun referans noktası) olarak. Bu olmadan haritanın merkezi başlangıç noktası olur ve `.json` dosyasındaki `geo` hangisi olduğunu söyler.
4. Komut, her haritayı çözerken bir satır yazar; sonra `ok <glb> <triangles> (<frame> frame)` ya da `failed <map>: <why>` yazar.
5. `<folder>/<map>/<map>.glb` dosyasını görüntüleyicinin Arka plan / bölüm panelinde yükleyin.

![Sentetik bir kurulumda extract](../assets/img/extract.svg)

Oyunun kendi metrelerinde, su olmadan:

![extract --frame game --no-water](../assets/img/extract-game.svg)

Zaten yazılmış haritaların üzerine ikinci bir çalıştırma:

![extract --all --skip-existing](../assets/img/extract-skip.svg)

## Seçenekler {#options}

| Seçenek | Varsayılan | Ne yapar |
|---|---|---|
| `maps` | - | `list`'in yazdığı gibi harita adları; joker karakter kullanılabilir |
| `--all` | kapalı | her harita; aynı yükseklik ve su haritasını paylaşan mevsimler bir kez yazılır |
| `-o`, `--out` | gerekli | çıktı klasörü; her harita `<out>/<map>/` içine gider |
| `--game FOLDER` | bulunur | bir IL-2 klasörü (tekrarlanabilir) |
| `--max-grid N` | `1024` | yükseklik haritası örneklerinin bir kenardaki en fazla sayısı (1024: yaklaşık 2 milyon üçgen); harita, sığması için her *k* örnekte bir alınır |
| `--frame` `enu` ya da `game` | `enu` | `enu`: `--origin`in doğusunda metre, rakım ve kuzeyinde; Watcher'ın Tacview tablolarındaki gibi. `game`: oyunun kendi metreleri (x kuzey, y yukarı, z doğu). Yerkürede yerleştirilemeyen bir harita, ne istenirse istensin `game` çerçevesinde yazılır |
| `--origin LAT LON` | haritanın merkezi | `enu` çerçevesinin başlangıç noktası (bir kaydın `geo`'su) |
| `--no-water` | kapalı | suyu dışarıda bırak |
| `--no-towns` | kapalı | kasaba izlerini dışarıda bırak |
| `--skip-existing` | kapalı | `.glb`'si zaten olan haritaları bırak |

Her seçenek, programın yazdığı gibi: [Komut başvurusu](../cli-reference.md).

Başarısız bir haritanın tam izini yazdırmak için `HEAT3D_DEBUG` ortam değişkenini ayarlayın. `.glb` dosyası `<map>.glb.part` olarak yazılır ve tamamlanınca yeniden adlandırılır.

Çıkış durumu: 0 her harita yazıldı; 1 herhangi biri başarısız (diğerleri yine de yazılır); 2 kurulum ya da eşleşen harita bulunamadı.

## Örnekler {#examples}

```bash
heat3d-il2-level extract <map> -o levels                         # one map, enu frame round its centre
heat3d-il2-level extract <map> --origin <lat> <lon> -o levels    # in the flat map of a recording with that geo
heat3d-il2-level extract "<family>_*" --max-grid 2048 -o levels  # finer, several maps
heat3d-il2-level extract --all --skip-existing -o levels         # every map, only the new ones
heat3d-il2-level extract <map> --frame game -o levels            # the game's own metres, as mission files have them
```

Dosyalarda ne var: [Seviye dosyaları ve çerçeveler](output.md).
