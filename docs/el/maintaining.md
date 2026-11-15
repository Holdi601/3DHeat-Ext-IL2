---
title: "Συντήρηση αυτών των σελίδων"
nav_order: 91
lang: "el"
source: maintaining.md
source_hash: "a37a32cc5026"
nav_exclude: true
search_exclude: true
---
# Συντήρηση αυτών των σελίδων {#maintaining-these-docs}

Μια λίστα ελέγχου για κάθε κυκλοφορία, ώστε οι σελίδες να μην μένουν πίσω από τον κώδικα.

1. **Ξαναδημιουργήστε την αναφορά.** Το `python tools/gen_docs_reference.py` ξαναγράφει την
   [Αναφορά εντολών](../cli-reference.md) από το ίδιο το `--help` του προγράμματος και τις
   στήλες εξόδου. Το `python tools/gen_docs_reference.py --check` βγαίνει με 1 όταν
   η σελίδα που έχει γίνει commit είναι ξεπερασμένη.
2. **Απαριθμήστε τι αλλάξτε.** `git log v<VERSION>..HEAD --oneline`, όπου
   `<VERSION>` είναι η τελευταία κυκλοφορημένη έκδοση (το αρχείο `VERSION` κατά την κυκλοφορία).
   Δώστε σε κάθε νέο χαρακτηριστικό, επιλογή και στήλη εξόδου μια θέση σε μια σελίδα, και
   μια γραμμή στην ενότητα **Docs** του [`CHANGELOG.md`](https://github.com/Holdi601/3DHeat-Ext-IL2/blob/main/CHANGELOG.md).
3. **Ανεξάρτητος έλεγχος.** Κάποιος που δεν έγραψε τις σελίδες διαβάζει το
   README και κάθε σελίδα που αλλάξτε, μαζί με τις εικόνες, τρεις φορές: ως αρχάριος που δεν έχει ξαναχρησιμοποιήσει
   τερματικό, ως οκτάχρονο παιδί, και ως ειδικός
   που ελέγχει κάθε επιλογή με το `--help`. Τα παραδείγματα χρησιμοποιούν μόνο επινοημένα ονόματα
   και αριθμούς.
4. **Διορθώστε** ό,τι βρει ο έλεγχος.
5. **Μεταφράσεις.** Κάθε μεταφρασμένη σελίδα καταγράφει το hash της αγγλικής σελίδας
   από την οποία φτιάχτηκε. Μεταφράστε ξανά τις σελίδες των οποίων αλλάξτε η αγγλική πηγή,
   και μετά ελέγξτε κάθε γλώσσα: καθαρό κείμενο, σωστές ετικέτες διαγραμμάτων, οι ίδιες
   λέξεις με τη μεταφρασμένη διεπαφή του ίδιου του προβολέα.
6. **Τρέξτε τις δοκιμές** (`pytest`).
7. **Κάντε push** μόνο μετά την έγκριση του ιδιοκτήτη.

## Μεταφράσεις: οι εντολές {#translations-the-commands}

Ο ιστότοπος μεταφράζεται στις 40 γλώσσες του προβολέα 3DHeat: τα αγγλικά στο `docs/`, κάθε άλλη
γλώσσα στο `docs/<lang>/` με τα ίδια ονόματα αρχείων. Το `tools/docs_i18n.py` κρατά τα βιβλία:

```bash
python tools/docs_i18n.py hashes             # after any English change: record each page's hash
python tools/docs_i18n.py svg-strings        # after any picture change: the labels to translate
python tools/docs_i18n.py status             # per language: current, outdated, missing pages
python tools/docs_i18n.py todo --lang de     # the German pages to (re)translate
python tools/docs_i18n.py svg-build --lang de    # German pictures from docs/assets/i18n/svg/de.json
python tools/docs_i18n.py finish --lang de   # stamp the German pages with their English hash
python tools/docs_i18n.py check              # exit 1 when hashes or labels are stale
```

Μεταφράστε μόνο ό,τι απαριθμεί το `todo`: κρατήστε όπως είναι το Markdown, τους συνδέσμους, τον κώδικα, τα ονόματα αρχείων και στηλών,
μεταφράστε τίτλους και περιγραφές εικόνων, και χρησιμοποιήστε τις λέξεις του ίδιου του προβολέα 3DHeat για τα κουμπιά
και τα πάνελ του (το `src/i18n/locales/<lang>/` του). Οι παραγόμενες σελίδες αναφοράς και οι εικόνες τερματικού μένουν
στα αγγλικά. Στον ιστότοπο, μια ξεπερασμένη μετάφραση το λέει και συνδέει την αγγλική σελίδα· μια σελίδα που λείπει
πέφτει πίσω στα αγγλικά. Το μενού γλωσσών της κεφαλίδας και η ανακατεύθυνση της αρχικής σελίδας με βάση τη γλώσσα του προγράμματος περιήγησης
προέρχονται από το `docs/_includes/`.
