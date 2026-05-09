# GilLex
Gilaki Language Lexical Database

Gillex is a prototype lexical database for Gilaki verbal morphology. The
current schema is maintained in DBML and the example seed data for the revised
schema lives in `data/raw/v2`.

## Layers

Gillex uses one canonical schema with two loadable data layers:

- `core`: the report-facing dataset in `data/raw/v2`. This is the main
  academic submission: small, coherent, and linguistically motivated.
- `full`: the core dataset plus optional extension rows from
  `data/raw/v2_extensions`. This demonstrates how the project can scale without
  changing the schema or complicating the core explanation.

Build and validate the core layer:

```bash
python3 scripts/build_dataset.py --layer core
```

Build and validate the full layer:

```bash
python3 scripts/build_dataset.py --layer full
```

The builder writes SQLite inspection databases to `build/` and report-facing
exports to `data/release/core` or `data/release/full`.

## Database Schema

![ER Diagram](docs/schema/db_diagram.svg)

The old full ER diagram is useful as a rough overview, but the revised schema
is best understood through the modular notes in
`docs/schema/architecture.md`.

## Report Support

The most useful generated files for the report are:

- `data/release/core/resource_counts.csv`
- `data/release/core/lexical_entries.tsv`
- `data/release/core/verb_forms.tsv`
- `data/release/core/mwlu_components.tsv`
- `data/release/core/continuation_arcs.tsv`
- `data/release/core/report_examples.json`

For a short final checklist, see `docs/submission_readiness.md`.

## Licensing

The repository currently uses the MIT License for code and scripts.

Recommended data-license plan:

- code/scripts: MIT License
- original lexical data created for Gillex: CC BY 4.0, or CC BY-SA 4.0 if
  share-alike reuse is desired
- source-derived facts: include citations and avoid copying protected source
  text beyond short lexical facts

The final data license should be confirmed against the requirements of the
course, institution, and source materials.
