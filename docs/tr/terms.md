---
title: "Hız, testler, koşullar"
nav_order: 7
lang: tr
source: terms.md
source_hash: "5f420f7d2d05"
nav_exclude: true
search_exclude: true
---
# Hız, testler, koşullar {#speed-tests-terms}

## Hız {#speed}

Çözme, numba kurulu değilse saf Python'dur (`python -m pip install -e .[fast]`): orta boy bir harita numba olmadan yaklaşık 15 sn, numba ile yaklaşık bir saniye sürer. En büyük harita, birkaç yüz milyon örnek, numba ile yaklaşık 7 sn sürer (ilk çalıştırma derleme de yapar). Bellek, bir sektör satırı ile çıktı ızgarası kadar kalır.

## Testler {#tests}

```bash
python -m pytest -q
```

`tests/synth.py` arşivleri, yükseklik haritalarını (yukarıdaki kodlayıcının bir kodlayıcısı), `height.hini` dosyalarını ve dosya tablosu olmayan arşivleri kodla oluşturur.

## Koşullar {#the-terms}

IL-2 Sturmovik: Great Battles ve IL-2 Series'in (1C Game Studios / 777 Studios) lisans sözleşmesi **bulunamadı**: kurulumda yok (orada `data/Licenses.txt` yalnızca üçüncü taraf lisanslarını tutar), yayımcının sitesinde yok ve Steam EULA sayfası yüklenmedi. Buna dayanmadan önce kendiniz denetleyin. Bu araç arşivleri yalnızca okur, hiçbirini değiştirmez. Yazdığı seviyeler kendi makinenizde kalır: **asla yayımlamayın**. Burada hiçbir oyun verisi dağıtılmaz; testler okudukları her dosyayı kendileri oluşturur.

## Lisans {#licence}

MIT: bkz. [`LICENSE`](https://github.com/Holdi601/3DHeat-Ext-IL2/blob/main/LICENSE). numpy (BSD-3-Clause) ve isteğe bağlı olarak numba (BSD-2-Clause) kullanır. `heat3d_update`, 3DHeat araçlarının ortak güncelleyicisidir.
