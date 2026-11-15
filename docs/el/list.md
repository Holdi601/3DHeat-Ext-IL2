---
title: "Εύρεση χαρτών: list"
nav_order: 2
lang: "el"
source: list.md
source_hash: "8c7cf438be16"
nav_exclude: true
search_exclude: true
---
# Εύρεση χαρτών: `list` {#finding-maps-list}

```text
heat3d-il2-level list [--game FOLDER ...]
python -m heat3d_ext_il2 list ...          the same, without installing
```

Δεν έχετε ξαναδουλέψει με τη γραμμή εντολών; Διαβάστε πρώτα το [Πριν ξεκινήσετε](before-you-start.md).

1. Εγκαταστήστε μία φορά: `git clone https://github.com/Holdi601/3DHeat-Ext-IL2`, ανοίξτε
   ένα τερματικό σε αυτόν τον φάκελο και τρέξτε `python -m pip install -e .` (Python 3.10
   ή νεότερη· φέρνει το numpy· το `python -m pip install -e .[fast]` προσθέτει το numba).
2. Τρέξτε `heat3d-il2-level list`.
3. Κάθε χάρτης τυπώνει μία γραμμή, χωρισμένη με tab: το όνομά του (το όνομα που παίρνει το `extract`),
   το παιχνίδι (`Great Battles`, ή `Korea` για [το δεύτερο παιχνίδι](archives-without-table.md)), ο χάρτης υψομέτρων που διαβάζει, και
   πού βρίσκεται στη γη - το πλαίσιο γεωγραφικού πλάτους/μήκους από τις γωνίες του χάρτη, ή η
   προσαρμογή οροσήμων που τον τοποθετεί, ή «not placed on the earth».
   Η τελευταία γραμμή (στο stderr) μετρά τους χάρτες και ονομάζει τις εγκαταστάσεις.

![list σε συνθετική εγκατάσταση](../assets/img/list.svg)

Η εικόνα είναι μια εκτέλεση σε εγκατάσταση που φτιάχνουν τα τεστ
(`tests/synth.py`), όχι από το παιχνίδι.

## Πού βρίσκονται οι εγκαταστάσεις {#where-the-installs-are-found}

Μέσω Steam· αλλιώς `--game <folder>` (επαναλαμβανόμενο, ένα ανά εγκατάσταση) ή η
μεταβλητή περιβάλλοντος `HEAT3D_IL2_GAME`. Εγκατάσταση είναι ένας φάκελος του οποίου το `data`
περιέχει archives `Maps*.gtp`.

| Επιλογή | Κάνει |
|---|---|
| `--game FOLDER` | ένας φάκελος IL-2· επαναλάβετέ το για περισσότερες εγκαταστάσεις |

Κωδικός εξόδου: 0 έγινε, 2 δεν βρέθηκε εγκατάσταση.
