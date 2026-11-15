---
title: "Haritaları bulma: list"
nav_order: 2
lang: "tr"
source: list.md
source_hash: "8c7cf438be16"
nav_exclude: true
search_exclude: true
---
# Haritaları bulma: `list` {#finding-maps-list}

```text
heat3d-il2-level list [--game FOLDER ...]
python -m heat3d_ext_il2 list ...          the same, without installing
```

Komut satırında yeni misiniz? Önce [Başlamadan önce](before-you-start.md) sayfasını okuyun.

1. Bir kez kurun: `git clone https://github.com/Holdi601/3DHeat-Ext-IL2`, o klasörde bir terminal açın ve `python -m pip install -e .` çalıştırın (Python 3.10 veya daha yeni; numpy'yi getirir. `python -m pip install -e .[fast]` numba'yı ekler).
2. `heat3d-il2-level list` çalıştırın.
3. Her harita, sekmeyle ayrılmış tek bir satır yazar: adı (`extract`'in aldığı ad), oyunu (`Great Battles`, ya da [ikinci oyun](archives-without-table.md) için `Korea`), okuduğu yükseklik haritası ve yerkürede nerede durduğu. Bu, haritanın köşelerinden gelen enlem/boylam kutusu, ya da onu yerleştiren yer işareti uydurması, ya da "not placed on the earth" (yerkürede yerleştirilmedi) olur. Son satır (stderr üzerinde) haritaları sayar ve kurulumları adlandırır.

![Sentetik bir kurulumda list](../assets/img/list.svg)

Resim, oyunda değil, testlerin ürettiği bir kurulumda (`tests/synth.py`) yapılan bir çalıştırmadır.

## Kurulumların nerede bulunduğu {#where-the-installs-are-found}

Steam üzerinden; aksi halde `--game <folder>` (tekrarlanabilir, kurulum başına bir tane) ya da `HEAT3D_IL2_GAME` ortam değişkeni. Bir kurulum, `data` klasörü `Maps*.gtp` arşivlerini tutan bir klasördür.

| Seçenek | Ne yapar |
|---|---|
| `--game FOLDER` | bir IL-2 klasörü; birden çok kurulum için tekrarlayın |

Çıkış durumu: 0 tamam; 2 kurulum bulunamadı.
