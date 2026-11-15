---
title: "Dosya tablosu olmayan arşivler"
nav_order: 6
lang: "tr"
source: archives-without-table.md
source_hash: "58c4c46721e5"
nav_exclude: true
search_exclude: true
---
# Arşivlerinde dosya tablosu olmayan bir oyun {#a-game-whose-archives-have-no-file-table}

IL-2 Series: Korea, arşivlerinde okunabilir bir dosya tablosu tutmaz (adlar her arşivin sonundaki bir blokta karıştırılmıştır) ve ayar dosyaları okunabilir biçimde saklanmaz. `list` haritasını `Korea` oyunuyla gösterir. Yani:

- yükseklik haritası ve su haritası, başlıklarıyla bulunur (`height.dat` düzeni, 128 örnekli sektörler; çok büyük bir ızgara, ince bir hücre boyutuyla);
- yerkürede, görevlerinin yerleştirdiği hava alanlarının (`data/Missions/**/*.Mission`, makinenizde okunur) gerçek hava alanlarının yayımlanmış koordinatlarına uydurulmasıyla yerleştirilir (`korea.py`). Artıklar on metreler ile birkaç yüz metre arasındadır. JSON her yer işaretini ve artığını listeler;
- heightMul ve SeaLevel tahmin edilir: görevlerdeki gemiler denizin üzerinde durur; bu yüzden yüksekliklerinin su haritasının en yaygın (deniz) değerinin üstünde olması ölçeği verir. Yükseklikler makul çıkar (deniz seviyesinin altındaki deniz, birkaç metre yükseklikteki kıyı kasabaları); daha ileri denetlenmedi. JSON bunları tahmin edilmiş olarak işaretler.
