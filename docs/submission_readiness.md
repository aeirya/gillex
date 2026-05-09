# Submission Readiness Notes

This is the minimal remaining-work assessment for turning GilLex into a clean
academic submission.

## Current State

The project is coherent enough to submit as a prototype lexical database:

- one canonical DBML schema;
- a small core dataset that demonstrates every major subsystem;
- optional extension rows that do not complicate the core explanation;
- a report structured as an academic resource paper;
- deterministic validation, SQLite build, and report exports.

## What Is Intentionally Out of Scope

The submission should not add a neural model, crawler, large generated paradigm,
or full morphology generator. Those would distract from the main contribution:
a linguistically motivated lexical database architecture for Gilaki verbs.

## Minimum Pre-Submission Checklist

1. Run `python3 scripts/build_dataset.py --layer core`.
2. Check `data/release/core/resource_counts.csv` for the counts reported in the paper.
3. Use `data/release/core/verb_forms.tsv` and `report_examples.json` for examples.
4. Confirm the licensing choice for lexical data: CC BY 4.0 is the simplest default; CC BY-SA 4.0 is stricter.
5. Make sure the report presents EDBL as inspiration, not as a schema being copied.
6. Keep optional extension material framed as scalability evidence, not as required core coverage.

## Remaining Linguistic Work After Submission

- verify all forms and segmentations with a fluent speaker and primary sources;
- expand beyond verbs only after the verb subsystem is stable;
- add more dialect evidence only when source-backed;
- implement finite-state export from continuation classes if the project continues.
