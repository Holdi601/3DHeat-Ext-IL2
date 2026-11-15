---
title: "Δημιουργία επιπέδων: extract"
nav_order: 3
lang: "el"
source: extract.md
source_hash: "2a45af525c58"
nav_exclude: true
search_exclude: true
---
# Δημιουργία επιπέδων: `extract` {#building-levels-extract}

```text
heat3d-il2-level extract (<map> ... | --all) -o <folder> [--game FOLDER ...]
                 [--max-grid N] [--frame enu|game] [--origin LAT LON]
                 [--no-water] [--no-towns] [--skip-existing]
```

## Βήμα προς βήμα {#step-by-step}

Δεν έχετε ξαναδουλέψει με τη γραμμή εντολών; Διαβάστε πρώτα το [Πριν ξεκινήσετε](before-you-start.md).

1. Βρείτε το όνομα του χάρτη με το [`list`](list.md).
2. Τρέξτε `heat3d-il2-level extract <map> -o levels`. Τα ονόματα μπορούν να έχουν μπαλαντέρ,
   σε εισαγωγικά (`"<family>_*"`)· το `--all` παίρνει κάθε χάρτη.
3. Για να βάλετε μια εγγραφή πάνω στο επίπεδο χωρίς βήμα τοποθέτησης, δώστε την αρχή της:
   `--origin <lat> <lon>` ίσο με το `geo` της εγγραφής (το σημείο αναφοράς της συνεδρίας της).
   Χωρίς αυτό, αρχή είναι το κέντρο του χάρτη, και το `geo` του `.json` λέει ποιο είναι.
4. Η εντολή τυπώνει μια γραμμή ανά χάρτη καθώς τον αποκωδικοποιεί, μετά
   `ok <glb> <triangles> (<frame> frame)` ή `failed <map>: <why>`.
5. Φορτώστε το `<folder>/<map>/<map>.glb` στο πάνελ «Φόντο / πίστα» του προβολέα.

![extract σε συνθετική εγκατάσταση](../assets/img/extract.svg)

Στα μέτρα του ίδιου του παιχνιδιού, χωρίς το νερό:

![extract --frame game --no-water](../assets/img/extract-game.svg)

Μια δεύτερη εκτέλεση πάνω σε χάρτες που έχουν ήδη γραφτεί:

![extract --all --skip-existing](../assets/img/extract-skip.svg)

## Επιλογές {#options}

| Επιλογή | Προεπιλογή | Κάνει |
|---|---|---|
| `maps` | - | ονόματα χαρτών όπως τα τυπώνει το `list`· επιτρέπονται μπαλαντέρ |
| `--all` | off | κάθε χάρτη· οι εποχές που μοιράζονται χάρτη υψομέτρων και χάρτη νερού γράφονται μία φορά |
| `-o`, `--out` | υποχρεωτικό | ο φάκελος εξόδου· κάθε χάρτης μπαίνει στο `<out>/<map>/` |
| `--game FOLDER` | βρίσκεται | ένας φάκελος IL-2 (επαναλαμβάνεται) |
| `--max-grid N` | `1024` | το πολύ τόσα δείγματα υψομέτρου ανά πλευρά (1024: περίπου 2 εκατομμύρια τρίγωνα)· ο χάρτης δειγματοληπτείται ανά *k* δείγματα ώστε να χωρέσει |
| `--frame` `enu` ή `game` | `enu` | `enu`: μέτρα ανατολικά, υψόμετρο, βόρεια της `--origin`, όπως οι πίνακες Tacview του Watcher· `game`: τα μέτρα του ίδιου του παιχνιδιού (x βορράς, y πάνω, z ανατολή). Ένας χάρτης που δεν μπορεί να τοποθετηθεί στη γη γράφεται σε `game` ό,τι κι αν ζητηθεί |
| `--origin LAT LON` | το κέντρο του χάρτη | η αρχή του πλαισίου `enu` (το `geo` μιας εγγραφής) |
| `--no-water` | off | αφήνει έξω το νερό |
| `--no-towns` | off | αφήνει έξω τα ίχνη των πόλεων |
| `--skip-existing` | off | αφήνει τους χάρτες που έχουν ήδη `.glb` |

Κάθε επιλογή, όπως την τυπώνει το πρόγραμμα: [Αναφορά εντολών](../cli-reference.md).

Ορίστε το `HEAT3D_DEBUG` για να τυπωθεί ολόκληρο το traceback ενός χάρτη που απέτυχε. Το `.glb`
γράφεται στο `<map>.glb.part` και μετονομάζεται όταν ολοκληρωθεί.

Κωδικός εξόδου: 0 κάθε χάρτης γράφτηκε, 1 κάποιος απέτυχε (οι άλλοι γράφονται κανονικά), 2 δεν
βρέθηκε εγκατάσταση ή κανένας χάρτης δεν ταίριαξε.

## Παραδείγματα {#examples}

```bash
heat3d-il2-level extract <map> -o levels                         # one map, enu frame round its centre
heat3d-il2-level extract <map> --origin <lat> <lon> -o levels    # in the flat map of a recording with that geo
heat3d-il2-level extract "<family>_*" --max-grid 2048 -o levels  # finer, several maps
heat3d-il2-level extract --all --skip-existing -o levels         # every map, only the new ones
heat3d-il2-level extract <map> --frame game -o levels            # the game's own metres, as mission files have them
```

Τι υπάρχει στα αρχεία: [Τα αρχεία επιπέδου και τα πλαίσια](output.md).
