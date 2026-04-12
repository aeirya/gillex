import sqlite3
import pandas as pd
import os

# -------------------------------
# STEP 0: Connect Database
# -------------------------------
conn = sqlite3.connect("../schema/gilaki.db")
cursor = conn.cursor()

# (FKs disabled in schema already, so no need here)

# -------------------------------
# STEP 1: Run Schema
# -------------------------------
with open("../schema/schema.sql", "r", encoding="utf-8") as f:
    cursor.executescript(f.read())

print("Schema loaded successfully ✅")

# -------------------------------
# STEP 2: Load CSV Files
# -------------------------------
data_folder = "../data/raw"

# ✅ ONLY tables that exist in your schema + CSV
tables = [
    "lexical_unit",
    "lemma",
    "person",
    "number",
    "mood",
    "aspect",
    "verb_tenses",
    "dialect",
    "language",
    "dict_entry",
    "verb_lemma",
    "form",
    "lexical_unit_dialects",
    "gloss",
    "verb_form"
]

for table in tables:
    file_path = os.path.join(data_folder, f"{table}.csv")

    if os.path.exists(file_path):
        try:
            df = pd.read_csv(file_path, encoding="utf-8")

            # ✅ Fix header spaces automatically
            df.columns = df.columns.str.strip()

            # ✅ Clean string values safely (no warning)
            for col in df.columns:
                if df[col].dtype == "object":
                    df[col] = df[col].astype(str).str.strip()

            print(f"\nLoading {table}.csv...")
            print(df.head())

            # -----------------------
            # INSERT DIRECTLY (NO MANUAL FIXES)
            # -----------------------
            df.to_sql(table, conn, if_exists="append", index=False)

            print(f"✅ Loaded {table}.csv")

        except Exception as e:
            print(f" Error loading {table}.csv → {e}")

    else:
        print(f" File not found: {file_path}")

# -------------------------------
# STEP 3: Test Query
# -------------------------------
print("\nTest Query Output:")
cursor.execute("SELECT * FROM lemma LIMIT 5;")
print(cursor.fetchall())
print("\nPresentation Query Output:")

print("\n--- FULL LINGUISTIC ANALYSIS ---")

cursor.execute("""
SELECT 
    vf.form,
    l.lemma,
    vt.name,
    m.value,
    a.aspect,
    n.value,
    p.value
FROM verb_form vf
JOIN form f ON vf.form_id = f.id
JOIN lemma l ON f.lemma_id = l.id
JOIN verb_tenses vt ON vf.tense_id = vt.verb_tense_id
JOIN mood m ON vf.mood_id = m.mood_id
JOIN aspect a ON vf.aspect_id = a.aspect_id
JOIN number n ON vf.number_id = n.number_id
JOIN person p ON vf.person_id = p.person_id
LIMIT 10;
""")
print(cursor.fetchall())
rows = cursor.fetchall()
print('naeem')
for row in rows:
    print(row)
    print('naeem')

# -------------------------------
# FINAL STEP
# -------------------------------
conn.commit()
conn.close()

print("\n🎉 FULL DATABASE READY!")