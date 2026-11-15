---
title: Como os arquivos são lidos
nav_order: 5
lang: pt
source: reading.md
source_hash: "3c0d5d19e02e"
nav_exclude: true
search_exclude: true
---
# Como os arquivos são lidos {#how-the-files-are-read}

| Parte | Situação |
|---|---|
| Arquivos (`data/*.gtp`, Great Battles) | a tabela de arquivos (registros `S16R`, `STRMFAT?`, `DIR!`/`FILE`) e as entradas (cabeçalho `STRMFILE`, dados guardados como estão); todo `Maps*.gtp` da instalação de teste |
| `height.hini` | `height_map`, `water_map`, `heightMul`, `SeaLevel`, os limites da área de jogo e `MapNW/NE/SE/SW`; todos os da instalação de teste |
| Mapas de altura (`height.dat`) | o codec abaixo; todo setor dos mapas decodificado por completo enquanto era entendido usa o seu fluxo de bits exatamente (no máximo o preenchimento de bytes que sobra), o resto verificado pelo cabeçalho. Conferido bit a bit contra os arquivos `distlod.raw` não comprimidos que o jogo entrega ao lado dos seus `distlod.dat`, e contra o mapa de altura de LOD distante de um mapa (correlação 0,999) |
| Alturas | metros = x bruto × heightMul / 256 - SeaLevel × heightMul. O mar de um mapa decodifica exatamente na altura que os comentários do seu hini indicam; a borda de outro, no seu `bounds_level` |
| Posicionamento | bilinear entre os quatro cantos do hini, linha 0 ao norte, coluna 0 ao oeste. Conferido em um mapa contra cidades, costas e mares conhecidos (alturas das cidades a cerca de 10 m das reais, os mares abaixo do nível do mar). Os cantos formam um quadrilátero, não a projeção própria do jogo, então espere algumas centenas de metros de erro no meio de um mapa grande. O hini de uma família de mapas traz os cantos de outro mapa (eles abrangem uma fração do seu tamanho real); isso é detectado, e essa família é então posicionada por um ajuste por marcos: cidades e aeródromos dos próprios bancos de dados de localização do jogo (`*.ldfbin`) contra as suas posições reais, rms de cerca de dois quilômetros (cidades contra os aeródromos que levam o seu nome, e coordenadas dos lugares reais a cerca de um quilômetro); o JSON lista cada marco e o seu resíduo |
| Máscara de água (`water.wtr`: quatro níveis de pirâmide de ladrilhos, cada ladrilho uma tabela de blocos de 400 m, cada bloco terra, cheio ou parcialmente com água, com a sua forma num fluxo de bits) | o contêiner é lido em todo mapa (nenhum byte sobra nos arquivos decodificados por completo); a forma dentro de um bloco parcialmente com água **não é decodificada**. Blocos cheios são água; em blocos parcialmente com água, uma amostra é água onde o mapa de água (`height_w.dat`, mesmo codec do mapa de altura) está acima do solo, ou, ao lado de um lago, onde o solo não está mais alto que o lago; blocos de terra são secos. Isso remove o pântano que o mapa de água sozinho aponta como água. Rios mais estreitos que a grade de saída saem quebrados em pedaços |
| Pegadas das cidades (as malhas de decalque que `textures.tini` lista: `towns.mesh`, `cities.mesh`, `city_*.mesh`, `roads_fields.mesh`, ...: ladrilhos de 25,6 km de triângulos planos texturizados) | lidas em todo mapa; mantêm-se as faces cuja textura é de cidade, vilarejo ou solo industrial. Conferidas contra as cidades reais em alguns mapas (uma cidade nas duas margens de um rio, uma confluência). São pegadas: o jogo posiciona os edifícios em tempo de execução, e os arquivos não trazem edifícios |
| Aeródromos, pontes, edifícios | **não lidos**: aeródromos são objetos de missão, edifícios vêm do posicionamento próprio do jogo |
| Florestas (`forest_map.wtr`) | os seus blocos são lidos do mesmo jeito, mas quase todo bloco é "parcialmente floresta", então sem o fluxo de bits não há máscara de floresta utilizável; não desenhada |
| As texturas do solo | não lidas |

## O codec do mapa de altura {#the-heightmap-codec}

Levantado só a partir dos arquivos de dados; nenhum código do jogo foi lido ou desmontado.
Little-endian:

```text
u32 width, u32 height, u32 sectorsX, u32 sectorsY, u32 sectorSize, f32 cellSize
u32 offset[sectorsX * sectorsY]            a partir do início do arquivo, por linha, linha de cima primeiro
setor: u16 count (bytes que seguem), u16 mode ((log2 sectorSize) << 4 | LW, LW = 4),
        depois um fluxo de bits lido do mais significativo para o menos significativo:
  PRE   2 * (log2(sectorSize) - 5) bits, sempre 0 até agora
  LIT   a primeira amostra: sinal (1), n (bits de LW), magnitude (n + 1 bits)
  depois, até o setor encher:
    0 LIT       próximo = anterior + LIT
    1 RUN LIT   a amostra anterior se repete RUN vezes (k: 3 bits, m: k + 1 bits, RUN = m + 1),
                depois (a menos que o setor esteja cheio) próximo = anterior + LIT
  os valores são de 16 bits: leia-os em módulo 65536
```

Setores parciais nas bordas direita e inferior são preenchidos e recortados. O mesmo
codec vale para o mapa de água e para o mapa de altura de LOD distante.

## Ajustes por marcos {#landmark-fits}

Quando os cantos de um mapa não podem ser usados, `landmarks.py` ajusta uma
transformação afim dos metros do jogo para a terra pelos mínimos quadrados: posições no jogo vindas dos
próprios arquivos do usuário (blocos `Airfield` de missão, os bancos de dados de localização da carreira),
posições reais vindas de tabelas das coordenadas publicadas dos lugares, no código. O
`georeference` do JSON traz a matriz, a origem, cada marco com o seu resíduo e o rms.
