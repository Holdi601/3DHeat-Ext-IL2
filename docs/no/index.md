---
title: Hjem
nav_order: 1
lang: "no"
source: index.md
source_hash: "e5c9a5aa5acb"
nav_exclude: true
search_exclude: true
permalink: /no/
---
# 3DHeat IL-2 {#dheat-il-2}

**Hva er det?** Et lite program som gjør kartene i **IL-2 Sturmovik:
Great Battles**, lest fra **din egen installasjon**, om til 3D-modeller - nivåer -
du kan fly over i [3DHeat](https://github.com/Holdi601/3DHeat)-visningsprogrammet
([dokumentasjon](https://holdi601.github.io/3DHeat/)): åsene, elvene,
innsjøene, havet og byene, plassert der de ligger på jorden. Et andre IL-2-spill
der arkivene skjuler filtabellen deres, leses så langt arkivene tillater
([detaljer](archives-without-table.md)).

**Hvorfor skulle jeg bruke det?** For å se dine IL-2-flyvninger over spillets eget kart.

**Eksempel:** `heat3d-il2-level extract <map> -o levels` ->
`levels/<map>/<map>.glb` (nivået) + `<map>.json` (hvor den ligger på
jorden). Et høydekart er et rutenett av høyder, som et relieffkart; et Tacview-
opptak er en fil med en flyvning som Tacview skriver.

Til hva det er nyttig:

- **Flyvninger over spillets eget kart.** Et IL-2 Tacview-opptak, konvertert av
  3DHeat Watcher med samme origo, havner på nivået uten plasseringssteg.
- **Alle kart på en gang.** `extract --all` skriver hvert kart som finnes; sesonger som deler et
  høydekart skrives én gang.
- **Hvor på jorden.** Hvert nivås `.json` bærer sine hjørner og boksen i breddegrad/lengdegrad,
  og hvordan de ble funnet.

![Fra en IL-2-installasjon til et 3DHeat-nivå](../assets/img/no/flow.svg)

## Hurtigstart {#quick-start}

Ny til kommandolinjen? Les [Før du starter](before-you-start.md) først.
Kjør disse i mappen du klonet eller pakket ut:

```bash
python -m pip install -e .                         # installerer kommandoen heat3d-il2-level
python -m pip install -e .[fast]                            # med numba: dekoding 20 til 50 ganger raskere
heat3d-il2-level list                              # hvert kart som finnes, med sin boks i breddegrad/lengdegrad
heat3d-il2-level extract <map> -o levels           # ett kart (navnene slik `list` skriver dem; jokertegn er tillatt)
heat3d-il2-level extract --all -o levels           # hvert kart
```

Du bør se en linje per kart fra `list`, og `ok ...` fra `extract`.
Last deretter inn `levels/<map>/<map>.glb` i visningsprogrammets Bakgrunn / nivå-panel
([Nivåer](https://holdi601.github.io/3DHeat/levels.html)).

Nivåene den skriver er laget av spillets data: de blir **på din egen
maskin**; publiser dem aldri ([Vilkår](terms.md)).

Hver spilleser er sitt eget lille prosjekt med egen lisensfil, egne utgivelser og egen saksliste, slik at den kan installeres, oppdateres, vedlikeholdes - eller trekkes tilbake på forespørsel fra en rettighetshaver - for seg selv, uten at det påvirker visningsprogrammet eller de andre verktøyene.

## Sider {#pages}

| Side | Hva den dekker |
|---|---|
| [Før du starter](before-you-start.md) | Python, en terminal, en første kjøring |
| [Finne kart: list](list.md) | hvor installasjonene finnes, hva `list` skriver ut |
| [Bygge nivåer: extract](extract.md) | hvert alternativ, steg for steg, eksempler |
| [Nivåfilene og rammene](output.md) | `.glb`-delene, `.json`, `enu`- og `game`-rammene |
| [Slik leses filene](reading.md) | arkiver, høydekartkodeken, vann, byer, landemerketilpasninger |
| [Arkiver uten filtabell](archives-without-table.md) | det andre spillet, lest så langt arkivene tillater |
| [Fart, tester, vilkår](terms.md) | numba, testene, hva som leses og hva som ikke følger med, lisensen |
| [Kommandoreferanse](../cli-reference.md) | hvert alternativ, generert fra koden |
| [Vedlikeholde dokumentasjonen](maintaining.md) | sjekklisten for utgivelse |

## Relatert {#related}

- 3DHeat-visningsprogrammet: [github.com/Holdi601/3DHeat](https://github.com/Holdi601/3DHeat),
  dokumentasjon på [holdi601.github.io/3DHeat](https://holdi601.github.io/3DHeat/).
- Telemetri for disse nivåene: [3DHeat Watcher](https://holdi601.github.io/3DHeat-Watcher/)
  konverterer IL-2 Tacview-opptak; visningsprogrammets filformater, inkludert beholderen med én fil per
  kamp, er beskrevet i [Én fil per kamp (.3dheat)](https://holdi601.github.io/3DHeat/container.html).

## 3DHeat-verktøyene {#the-3dheat-tools}

| Verktøy | Hva det gjør | Kode | Dokumentasjon |
|---|---|---|---|
| 3DHeat-visningsprogram | viser dataene: varmekart, løpsanalyse, kampgjennomgang | [3DHeat](https://github.com/Holdi601/3DHeat) | [dokumentasjon](https://holdi601.github.io/3DHeat/) |
| GameFiles | nivåer og løyper fra et spills egne filer | [3DHeat-GameFiles](https://github.com/Holdi601/3DHeat-GameFiles) | [dokumentasjon](https://holdi601.github.io/3DHeat-GameFiles/) |
| GameCapture | telemetri fra runder, og nivåer bygget opp fra spillopptak | [3DHeat-GameCapture](https://github.com/Holdi601/3DHeat-GameCapture) | [dokumentasjon](https://holdi601.github.io/3DHeat-GameCapture/) |
| Unreal Exporter | en Unreal Editor-plugin: et nivå som én `.glb` | [3DHeat-UnrealExporter](https://github.com/Holdi601/3DHeat-UnrealExporter) | [dokumentasjon](https://holdi601.github.io/3DHeat-UnrealExporter/) |
| CS2 | Counter-Strike 2-demoer og kart | [3DHeat-CS2](https://github.com/Holdi601/3DHeat-CS2) | [dokumentasjon](https://holdi601.github.io/3DHeat-CS2/) |
| Watcher | tar opp det spill publiserer mens du spiller | [3DHeat-Watcher](https://github.com/Holdi601/3DHeat-Watcher) | [dokumentasjon](https://holdi601.github.io/3DHeat-Watcher/) |
| Ext-WarThunder | War Thunder-replayer | [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder) | [dokumentasjon](https://holdi601.github.io/3DHeat-Ext-WarThunder/) |
| Ext-WoT | World of Tanks-replayer | [3DHeat-Ext-WoT](https://github.com/Holdi601/3DHeat-Ext-WoT) | [dokumentasjon](https://holdi601.github.io/3DHeat-Ext-WoT/) |
| Ext-WoWs | World of Warships-replayer | [3DHeat-Ext-WoWs](https://github.com/Holdi601/3DHeat-Ext-WoWs) | [dokumentasjon](https://holdi601.github.io/3DHeat-Ext-WoWs/) |
| Ext-Squad | Squad-serverdemoer | [3DHeat-Ext-Squad](https://github.com/Holdi601/3DHeat-Ext-Squad) | [dokumentasjon](https://holdi601.github.io/3DHeat-Ext-Squad/) |
| Ext-DCS | DCS World-kart som 3D-nivåer | [3DHeat-Ext-DCS](https://github.com/Holdi601/3DHeat-Ext-DCS) | [dokumentasjon](https://holdi601.github.io/3DHeat-Ext-DCS/) |
| Ext-IL2 | IL-2 Great Battles-kart som 3D-nivåer | [3DHeat-Ext-IL2](https://github.com/Holdi601/3DHeat-Ext-IL2) | [dokumentasjon](https://holdi601.github.io/3DHeat-Ext-IL2/) |
