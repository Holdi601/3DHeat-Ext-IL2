---
title: "Dosyalar nasıl okunur"
nav_order: 5
lang: tr
source: reading.md
source_hash: "3c0d5d19e02e"
nav_exclude: true
search_exclude: true
---
# Dosyalar nasıl okunur {#how-the-files-are-read}

| Parça | Durum |
|---|---|
| Arşivler (`data/*.gtp`, Great Battles) | dosya tablosu (`S16R`, `STRMFAT?`, `DIR!`/`FILE` kayıtları) ve girişler (`STRMFILE` başlığı, veri olduğu gibi saklanır); test kurulumundaki her `Maps*.gtp` |
| `height.hini` | `height_map`, `water_map`, `heightMul`, `SeaLevel`, oyun sınırları ve `MapNW/NE/SE/SW`; test kurulumundakilerin hepsi |
| Yükseklik haritaları (`height.dat`) | aşağıdaki kodlayıcı. Üzerinde çalışırken tamamen çözülen haritaların her sektörü bit akışını tam olarak kullanır (en fazla kalan bayt dolgusu hariç); gerisi başlıkla denetlenir. Oyunun `distlod.dat` yanında gönderdiği sıkıştırılmamış `distlod.raw` dosyalarına bit bit karşı denetlendi, bir haritanın kendi uzak-LOD yükseklik haritasına karşı da denetlendi (korelasyon 0,999) |
| Yükseklikler | metre = ham x heightMul / 256 - SeaLevel x heightMul. Bir haritanın denizi, hini yorumlarının verdiği yüksekliğin tam olarak aynısına çözülür; bir başkasının sınırı `bounds_level` değerine |
| Yerleştirme | hini'nin dört köşesi arasında doğrusal enterpolasyon; 0. satır kuzey, 0. sütun batı. Bir haritada bilinen kasabalara, kıyılara ve denizlere karşı denetlendi (kasaba yükseklikleri gerçek olanlardan yaklaşık 10 m içinde, denizler deniz seviyesinin altında). Köşeler bir dörtgen oluşturur, oyunun kendi izdüşümü değildir; bu yüzden büyük bir haritanın ortasında birkaç yüz metre hata beklenmeli. Bir harita ailesinin hini'si başka bir haritanın köşelerini taşır (gerçek boyutunun bir kesrini kapsarlar); bu tespit edilir ve o aile bunun yerine bir yer işareti uydurmasıyla yerleştirilir: oyunun kendi konum veritabanlarındaki (`*.ldfbin`) kasabalar ve hava alanları, gerçek konumlarına karşı, birkaç kilometrelik kök ortalama kare (kasabalar, adlarını taşıyan hava alanlarına karşı; gerçek yerlerin koordinatları yaklaşık bir kilometreye kadar). JSON her yer işaretini ve artığını listeler |
| Su maskesi (`water.wtr`: dört piramit düzeyi karo; her karo 400 m bloklarının bir tablosu; her blok kara, tam ya da kısmen su, şekli bir bit akışında) | kapsayıcı her haritada okunur (tamamen çözülen dosyalarda artan bayt yok). Kısmen sulu bir bloğun içindeki şekil **çözülmez**. Tam bloklar sudur; kısmen sulu bloklarda bir örnek, su haritasının (`height_w.dat`, yükseklik haritasıyla aynı kodlayıcı) zeminin üstünde olduğu yerde sudur, ya da bir gölün yanında zemin gölden yüksek değilse sudur; kara blokları kuraktır. Bu, su haritasının tek başına su olarak bildirdiği bataklığı kaldırır. Çıktı ızgarasından dar olan nehirler parçalara bölünmüş çıkar |
| Kasaba izleri (`textures.tini`'nin listelediği decal ağları: `towns.mesh`, `cities.mesh`, `city_*.mesh`, `roads_fields.mesh`, ...: 25,6 km'lik düz dokulu üçgen karolar) | her haritada okunur; dokusu kasaba, köy ya da sanayi zemini olan yüzler tutulur. Birkaç haritada gerçek kasabalara karşı denetlendi (bir nehrin iki yakasında bir kasaba, bir birleşme noktası). Bunlar izlerdir: oyun binaları çalışma zamanında yerleştirir, dosyalarda bina yoktur |
| Hava alanları, köprüler, binalar | **okunmaz**: hava alanları görev nesneleridir, binalar oyunun kendi yerleşiminden gelir |
| Ormanlar (`forest_map.wtr`) | blokları aynı biçimde okunur, ama neredeyse her blok "kısmen orman"dır; bit akışı olmadan kullanılabilir bir orman maskesi yoktur; çizilmez |
| Zeminin dokuları | okunmaz |

## Yükseklik haritası kodlayıcısı {#the-heightmap-codec}

Yalnızca veri dosyalarından çalışılarak çıkarıldı; hiçbir oyun kodu okunmadı ya da sökülmedi. Little-endian:

```text
u32 width, u32 height, u32 sectorsX, u32 sectorsY, u32 sectorSize, f32 cellSize
u32 offset[sectorsX * sectorsY]            from the start of the file, row-major, top row first
sector: u16 count (bytes that follow), u16 mode ((log2 sectorSize) << 4 | LW, LW = 4),
        then a bitstream read MSB first:
  PRE   2 * (log2(sectorSize) - 5) bits, always 0 so far
  LIT   the first sample: sign (1), n (LW bits), magnitude (n + 1 bits)
  then until the sector is full:
    0 LIT       next = previous + LIT
    1 RUN LIT   the previous sample repeats RUN times (k: 3 bits, m: k + 1 bits, RUN = m + 1),
                then (unless the sector is full) next = previous + LIT
  values are 16-bit: read them modulo 65536
```

Sağ ve alt kenarlardaki kısmi sektörler dolgulu ve kırpılmıştır. Aynı kodlayıcı su haritasını ve uzak-LOD yükseklik haritasını da tutar.

## Yer işareti uydurmaları {#landmark-fits}

Bir haritanın köşeleri kullanılamadığında, `landmarks.py` oyunun metrelerinden yerküreye en küçük kareler yöntemiyle bir afin dönüşüm uydurur. Oyun konumları kullanıcının kendi dosyalarından gelir (görev `Airfield` blokları, kariyer konum veritabanları); gerçek konumlar ise kodda yer alan, yayımlanmış koordinatlardan oluşan tablolardan gelir. JSON'un `georeference` değeri matrisi, başlangıç noktasını, her yer işaretini artığıyla ve kök ortalama kareyi taşır.
