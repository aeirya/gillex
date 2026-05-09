# Gillex v2 seed CSVs

These files are the core, report-facing dataset for the revised DBML schema in
`schema/gillexdb.dbml`.

The older CSVs under `data/raw` are left untouched. This folder is intentionally
small: it demonstrates the complete architecture without making the academic
report depend on a large or unevenly checked dataset.

The seed covers:

- one simple verb lemma: `kudǝn`
- one transitive verb lemma: `daan`
- a few inflected forms of `kudǝn`
- negation and person-number morphemes
- one derivational-prefix example
- one compound/light-verb lexical unit: `xǝndǝ kudǝn`
- dialect and orthography variation rows
- continuation-class rows for later FST-style export

Optional extension rows live in `data/raw/v2_extensions` and can be loaded with:

```bash
python3 scripts/build_dataset.py --layer full
```
