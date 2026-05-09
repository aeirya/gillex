#!/usr/bin/env python3
"""Validate Gillex CSV layers, build an inspection DB, and export report views.

The project has one canonical DBML schema. The default ``core`` layer loads the
small report-facing seed data in ``data/raw/v2``. The ``full`` layer appends
optional extension rows from ``data/raw/v2_extensions`` using the same table
names and columns.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sqlite3
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parents[1]


@dataclass
class Column:
    name: str
    required: bool = False
    primary_key: bool = False
    ref_table: str | None = None
    ref_column: str | None = None


@dataclass
class Table:
    name: str
    columns: list[Column] = field(default_factory=list)
    primary_key: list[str] = field(default_factory=list)

    @property
    def column_names(self) -> list[str]:
        return [column.name for column in self.columns]


def parse_dbml(path: Path) -> dict[str, Table]:
    """Parse the compact subset of DBML used by ``schema/gillexdb.dbml``."""
    text = path.read_text(encoding="utf-8")
    tables: dict[str, Table] = {}

    for match in re.finditer(r"^Table\s+(\w+)\s*{(?P<body>.*?)}", text, re.M | re.S):
        table = Table(match.group(1))
        in_indexes = False
        for raw_line in match.group("body").splitlines():
            line = raw_line.split("//", 1)[0].strip()
            if not line:
                continue
            if line.startswith("indexes"):
                in_indexes = True
                continue
            if in_indexes:
                if line == "}":
                    in_indexes = False
                    continue
                pk_match = re.match(r"\(([^)]+)\)\s*\[([^\]]+)\]", line)
                if pk_match and "pk" in pk_match.group(2):
                    table.primary_key = [part.strip() for part in pk_match.group(1).split(",")]
                continue

            column_match = re.match(r"([A-Za-z_]\w*)\s+([A-Za-z_]\w*)\b(.*)", line)
            if not column_match:
                continue
            name, _, tail = column_match.groups()
            ref_match = re.search(r"ref:\s*>\s*(\w+)\.(\w+)", tail)
            column = Column(
                name=name,
                required="not null" in tail,
                primary_key="[pk" in tail,
                ref_table=ref_match.group(1) if ref_match else None,
                ref_column=ref_match.group(2) if ref_match else None,
            )
            table.columns.append(column)
            if column.primary_key and name not in table.primary_key:
                table.primary_key.append(name)
        tables[table.name] = table
    return tables


def normalize_cell(value: str | None) -> str:
    return "" if value is None else value.strip()


def read_layer_csvs(
    data_dir: Path,
    schema: dict[str, Table],
    *,
    layer_name: str,
    required_all_tables: bool,
) -> tuple[dict[str, list[dict[str, str]]], list[str]]:
    rows_by_table: dict[str, list[dict[str, str]]] = defaultdict(list)
    errors: list[str] = []
    files = sorted(data_dir.rglob("*.csv")) if data_dir.exists() else []

    if required_all_tables:
        seen = {path.stem for path in files}
        missing = [name for name in schema if name not in seen]
        if missing:
            errors.append(f"{layer_name}: missing CSV files for tables: {', '.join(missing)}")

    for path in files:
        table_name = path.stem
        if table_name not in schema:
            errors.append(f"{layer_name}: {path.relative_to(ROOT)} does not match a DBML table")
            continue

        with path.open(newline="", encoding="utf-8") as handle:
            reader = csv.DictReader(handle)
            if reader.fieldnames is None:
                errors.append(f"{layer_name}: {path.relative_to(ROOT)} has no header")
                continue
            header = [field.strip() for field in reader.fieldnames]
            expected = schema[table_name].column_names
            if header != expected:
                errors.append(
                    f"{layer_name}: {path.relative_to(ROOT)} header mismatch: "
                    f"expected {expected}, got {header}"
                )
                continue

            for row_number, row in enumerate(reader, start=2):
                if None in row:
                    errors.append(f"{layer_name}: {path.relative_to(ROOT)} row {row_number} has extra cells")
                    continue
                normalized = {key.strip(): normalize_cell(value) for key, value in row.items()}
                if any(normalized.values()):
                    normalized["_source_file"] = str(path.relative_to(ROOT))
                    rows_by_table[table_name].append(normalized)

    return rows_by_table, errors


def merge_rows(*layers: dict[str, list[dict[str, str]]]) -> dict[str, list[dict[str, str]]]:
    merged: dict[str, list[dict[str, str]]] = defaultdict(list)
    for layer in layers:
        for table_name, rows in layer.items():
            merged[table_name].extend(rows)
    return merged


def validate_rows(schema: dict[str, Table], rows_by_table: dict[str, list[dict[str, str]]]) -> list[str]:
    errors: list[str] = []
    keys: dict[tuple[str, str], set[str]] = defaultdict(set)

    for table in schema.values():
        rows = rows_by_table.get(table.name, [])
        if not table.primary_key:
            continue
        seen: set[tuple[str, ...]] = set()
        for index, row in enumerate(rows, start=2):
            key = tuple(row.get(column, "") for column in table.primary_key)
            if any(value == "" for value in key):
                errors.append(f"{table.name}: row {index} has empty primary key {table.primary_key}")
                continue
            if key in seen:
                errors.append(f"{table.name}: duplicate primary key {table.primary_key}={key}")
            seen.add(key)
            if len(table.primary_key) == 1:
                keys[(table.name, table.primary_key[0])].add(key[0])

    for table in schema.values():
        rows = rows_by_table.get(table.name, [])
        for index, row in enumerate(rows, start=2):
            for column in table.columns:
                value = row.get(column.name, "")
                if column.required and value == "":
                    errors.append(f"{table.name}: row {index} has empty required column {column.name}")
                if column.ref_table and value:
                    ref_values = keys.get((column.ref_table, column.ref_column or ""))
                    if ref_values is None:
                        continue
                    if value not in ref_values:
                        errors.append(
                            f"{table.name}: row {index} {column.name}={value} "
                            f"does not exist in {column.ref_table}.{column.ref_column}"
                        )
    return errors


def quote_identifier(name: str) -> str:
    return '"' + name.replace('"', '""') + '"'


def build_sqlite(db_path: Path, schema: dict[str, Table], rows_by_table: dict[str, list[dict[str, str]]]) -> None:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    if db_path.exists():
        db_path.unlink()
    with sqlite3.connect(db_path) as conn:
        for table in schema.values():
            columns = ", ".join(f"{quote_identifier(name)} TEXT" for name in table.column_names)
            conn.execute(f"CREATE TABLE {quote_identifier(table.name)} ({columns})")
            rows = rows_by_table.get(table.name, [])
            if not rows:
                continue
            placeholders = ", ".join("?" for _ in table.column_names)
            names = ", ".join(quote_identifier(name) for name in table.column_names)
            values = [[row.get(name, "") for name in table.column_names] for row in rows]
            conn.executemany(f"INSERT INTO {quote_identifier(table.name)} ({names}) VALUES ({placeholders})", values)


def row_index(rows: Iterable[dict[str, str]], key: str) -> dict[str, dict[str, str]]:
    return {row[key]: row for row in rows if row.get(key)}


def write_tsv(path: Path, fieldnames: list[str], rows: Iterable[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, delimiter="\t", extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def write_csv(path: Path, fieldnames: list[str], rows: Iterable[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def export_report_views(export_dir: Path, schema: dict[str, Table], rows_by_table: dict[str, list[dict[str, str]]], layer: str) -> None:
    export_dir.mkdir(parents=True, exist_ok=True)

    counts = [{"table": name, "rows": str(len(rows_by_table.get(name, []))), "layer": layer} for name in schema]
    write_csv(export_dir / "resource_counts.csv", ["table", "rows", "layer"], counts)

    lexical_units = row_index(rows_by_table.get("lexical_unit", []), "id")
    lemmas = row_index(rows_by_table.get("lemma", []), "lexical_unit_id")
    dict_entries = row_index(rows_by_table.get("dict_entry", []), "lexical_unit_id")
    forms = row_index(rows_by_table.get("form", []), "lexical_unit_id")
    tam = row_index(rows_by_table.get("verb_tam", []), "id")
    moods = row_index(rows_by_table.get("mood", []), "id")
    tenses = row_index(rows_by_table.get("tense", []), "id")
    aspects = row_index(rows_by_table.get("aspect", []), "id")
    polarities = row_index(rows_by_table.get("polarity", []), "id")

    gloss_by_entry: dict[str, str] = {}
    for gloss in rows_by_table.get("gloss", []):
        if gloss.get("language_id") == "en" and (gloss.get("is_primary") == "true" or gloss["dict_entry_id"] not in gloss_by_entry):
            gloss_by_entry[gloss["dict_entry_id"]] = gloss.get("gloss", "")

    morphemes_by_form: dict[str, list[dict[str, str]]] = defaultdict(list)
    for part in rows_by_table.get("form_morpheme", []):
        morphemes_by_form[part["form_id"]].append(part)
    for parts in morphemes_by_form.values():
        parts.sort(key=lambda row: int(row["component_no"]))

    verb_rows: list[dict[str, str]] = []
    for verb_form in rows_by_table.get("verb_form", []):
        form_unit = lexical_units.get(verb_form["form_id"], {})
        form = forms.get(verb_form["form_id"], {})
        entry = dict_entries.get(form.get("dict_entry_id", verb_form["verb_lemma_id"]), {})
        lemma_unit = lexical_units.get(entry.get("lemma_id", ""), {})
        tam_row = tam.get(verb_form["tam_id"], {})
        segmentation = "+".join(part["surface"] for part in morphemes_by_form.get(verb_form["form_id"], []))
        morph_gloss = "+".join(part["gloss"] for part in morphemes_by_form.get(verb_form["form_id"], []))
        verb_rows.append(
            {
                "form": form_unit.get("canonical_form", ""),
                "segmentation": segmentation,
                "morpheme_gloss": morph_gloss,
                "lemma": lemma_unit.get("canonical_form", ""),
                "lemma_gloss": gloss_by_entry.get(entry.get("lexical_unit_id", ""), ""),
                "english_translation": verb_form.get("notes", ""),
                "person": verb_form.get("person_id", ""),
                "number": verb_form.get("number_id", ""),
                "mood": moods.get(tam_row.get("mood_id", ""), {}).get("label", ""),
                "tense": tenses.get(tam_row.get("tense_id", ""), {}).get("label", ""),
                "aspect": aspects.get(tam_row.get("aspect_id", ""), {}).get("label", ""),
                "polarity": polarities.get(verb_form.get("polarity_id", ""), {}).get("label", ""),
                "generation_status": form.get("generation_status_id", ""),
            }
        )
    write_tsv(
        export_dir / "verb_forms.tsv",
        [
            "form",
            "segmentation",
            "morpheme_gloss",
            "lemma",
            "lemma_gloss",
            "english_translation",
            "person",
            "number",
            "mood",
            "tense",
            "aspect",
            "polarity",
            "generation_status",
        ],
        verb_rows,
    )

    entry_rows: list[dict[str, str]] = []
    for entry in rows_by_table.get("dict_entry", []):
        entry_unit = lexical_units.get(entry["lexical_unit_id"], {})
        lemma_unit = lexical_units.get(entry["lemma_id"], {})
        entry_rows.append(
            {
                "entry_id": entry["lexical_unit_id"],
                "headword": entry_unit.get("canonical_form", ""),
                "lemma": lemma_unit.get("canonical_form", ""),
                "pos": entry.get("pos_id", ""),
                "gloss_en": gloss_by_entry.get(entry["lexical_unit_id"], ""),
                "usage_label": entry.get("usage_label", ""),
            }
        )
    write_tsv(export_dir / "lexical_entries.tsv", ["entry_id", "headword", "lemma", "pos", "gloss_en", "usage_label"], entry_rows)

    mwlu_rows: list[dict[str, str]] = []
    mwlu_names = {row["lexical_unit_id"]: lexical_units.get(row["lexical_unit_id"], {}).get("canonical_form", "") for row in rows_by_table.get("multiword_lexical_unit", [])}
    for component in rows_by_table.get("mwlu_component", []):
        mwlu_rows.append(
            {
                "mwlu": mwlu_names.get(component["mwlu_id"], ""),
                "component_no": component["component_no"],
                "component": lexical_units.get(component.get("component_lexical_unit_id", ""), {}).get("canonical_form", component.get("literal_form", "")),
                "role": component.get("role_id", ""),
                "can_inflect": component.get("can_inflect", ""),
                "inflects_like": lexical_units.get(component.get("inflects_like_lemma_id", ""), {}).get("canonical_form", ""),
            }
        )
    write_tsv(export_dir / "mwlu_components.tsv", ["mwlu", "component_no", "component", "role", "can_inflect", "inflects_like"], mwlu_rows)

    continuation_rows: list[dict[str, str]] = []
    classes = row_index(rows_by_table.get("continuation_class", []), "id")
    morpheme_units = {row["lexical_unit_id"]: lexical_units.get(row["lexical_unit_id"], {}).get("canonical_form", "") for row in rows_by_table.get("morpheme", [])}
    for arc in rows_by_table.get("continuation_arc", []):
        continuation_rows.append(
            {
                "from_class": classes.get(arc["from_class_id"], {}).get("name", arc["from_class_id"]),
                "morpheme": morpheme_units.get(arc.get("morpheme_id", ""), ""),
                "to_class": classes.get(arc.get("to_class_id", ""), {}).get("name", arc.get("to_class_id", "")),
                "feature_constraint": arc.get("feature_constraint", ""),
                "output_feature": arc.get("output_feature", ""),
                "notes": arc.get("notes", ""),
            }
        )
    write_tsv(
        export_dir / "continuation_arcs.tsv",
        ["from_class", "morpheme", "to_class", "feature_constraint", "output_feature", "notes"],
        continuation_rows,
    )

    examples = [
        {
            "form": row["form"],
            "segmentation": row["segmentation"],
            "gloss": row["morpheme_gloss"],
            "translation": row["english_translation"] or row["lemma_gloss"],
        }
        for row in verb_rows
        if row["segmentation"]
    ]
    (export_dir / "report_examples.json").write_text(json.dumps(examples, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def build_layer(args: argparse.Namespace) -> int:
    schema = parse_dbml(args.schema)
    core_rows, errors = read_layer_csvs(args.core_dir, schema, layer_name="core", required_all_tables=True)
    extension_rows: dict[str, list[dict[str, str]]] = {}
    if args.layer == "full":
        extension_rows, extension_errors = read_layer_csvs(args.extension_dir, schema, layer_name="extension", required_all_tables=False)
        errors.extend(extension_errors)
    rows_by_table = merge_rows(core_rows, extension_rows)
    errors.extend(validate_rows(schema, rows_by_table))

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    if not args.no_db:
        build_sqlite(args.db, schema, rows_by_table)
        print(f"wrote {args.db.relative_to(ROOT)}")
    if not args.no_exports:
        export_report_views(args.export_dir, schema, rows_by_table, args.layer)
        print(f"wrote exports in {args.export_dir.relative_to(ROOT)}")
    print(f"validated {args.layer} layer: {sum(len(rows) for rows in rows_by_table.values())} rows across {len(schema)} tables")
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build and validate the Gillex layered dataset")
    parser.add_argument("--layer", choices=["core", "full"], default="core", help="core seed only, or core plus optional extensions")
    parser.add_argument("--schema", type=Path, default=ROOT / "schema/gillexdb.dbml")
    parser.add_argument("--core-dir", type=Path, default=ROOT / "data/raw/v2")
    parser.add_argument("--extension-dir", type=Path, default=ROOT / "data/raw/v2_extensions")
    parser.add_argument("--db", type=Path, default=None, help="SQLite output path")
    parser.add_argument("--export-dir", type=Path, default=None, help="directory for report-facing exports")
    parser.add_argument("--no-db", action="store_true", help="validate and export without writing SQLite")
    parser.add_argument("--no-exports", action="store_true", help="validate/build without writing report exports")
    args = parser.parse_args()
    if args.db is None:
        args.db = ROOT / "build" / f"gillex_{args.layer}.sqlite"
    if args.export_dir is None:
        args.export_dir = ROOT / "data/release" / args.layer
    return args


if __name__ == "__main__":
    raise SystemExit(build_layer(parse_args()))
