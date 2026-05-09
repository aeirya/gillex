# Gillex Schema Architecture

This note turns the report feedback into concrete schema decisions.

## Layering Policy

Gillex has one schema and two data layers. The `core` layer is the small
report-facing dataset in `data/raw/v2`. The `full` layer appends optional rows
from `data/raw/v2_extensions` using the same table names and columns. This keeps
the academic explanation focused while still showing that the database can grow.

## Main Changes

- `lexical_unit` is the central identity table for lemmas, dictionary entries, forms, morphemes, and multiword lexical units.
- Boolean subtype flags such as `is_inflected`, `is_dialect`, and `is_mwlu` are removed. Subtype and relation tables now carry those meanings.
- `morpheme.lexical_unit_id` explicitly references `lexical_unit.id`, so morphemes are first-class lexical units.
- `verb_lemma.dict_entry_id` references `dict_entry.lexical_unit_id`, so verbal roots extend a verb dictionary entry.
- `form` stores form provenance and generation status; `verb_form` stores person, number, TAM, polarity, and auxiliary information.
- `form_morpheme` stores optional segmentation of surface forms into morphemes.
- `lexical_unit_dialect`, `lexical_unit_variant`, and `orthographic_form` replace the old `is_dialect` flag.
- `multiword_lexical_unit`, `mwlu_component`, and `compound_verb` represent light-verb constructions.
- `continuation_class`, `lemma_continuation_class`, and `continuation_arc` support future finite-state morphology exports.

## Subsystems

### Lexical Units

`lexical_unit` gives every relevant object a stable ID. `lemma` stores citation forms. `dict_entry` stores POS/sense-level entries. `gloss` stores translations.

Example: `kudǝn` is a lexical unit, a lemma, and a verb dictionary entry glossed as "to do".

### Morphemes

`morpheme` links a lexical unit to a type and function. `morpheme_allomorph` stores variants such as `nǝ`, `ni`, and `nu`. `form_morpheme` gives analyses like `nǝ + kun + əm`.

### Verbs and Inflected Forms

`verb_lemma` extends a dictionary entry with present and past roots. `form` links an observed/generated form to the entry. `verb_form` adds TAM and agreement features.

Example: `bukudəm` links to `kudǝn`, with past root `kud`, 1SG agreement, positive polarity, and past neutral perfective TAM.

### Dialects and Variants

Dialect information is evidence-driven. A unit has dialect data only when it has a row in `lexical_unit_dialect` or `lexical_unit_variant`.

### MWLUs and Compound Verbs

`multiword_lexical_unit` stores the whole expression. `mwlu_component` stores its parts. `compound_verb` identifies the light verb and nonverbal head.

Example: `xǝndǝ kudǝn` "to laugh" consists of `xǝndǝ` plus the light verb `kudǝn`.

### Continuation Classes

Continuation classes describe legal morphotactic paths. A root can start in `V_ROOT`; negation may keep it in `V_ROOT`; an agreement suffix may lead to `FINAL`.

Example path: `kun` + `nǝ-` + `-əm` produces a negative first-person singular form.

## Validation and Exports

Run `python3 scripts/build_dataset.py --layer core` before submission. It checks
that CSV headers match the DBML schema, required columns are filled, primary keys
are unique, and foreign-key-style references resolve. It also creates a SQLite
inspection database and small TSV/JSON exports for report tables and examples.
