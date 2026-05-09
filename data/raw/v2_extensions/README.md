# Gillex optional extension rows

This directory demonstrates the project layering policy without introducing a
second schema. The core academic submission is `data/raw/v2`. Files in this
directory use the same table names and columns, and are appended only when the
builder is run with `--layer full`.

The rows here are intentionally small. They show how additional inflected forms
can be added while keeping the report-facing core dataset simple.

