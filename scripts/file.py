import sqlite3
import pandas as pd
import os

# -------------------------------
# STEP 0: Connect Database
# -------------------------------
conn = sqlite3.connect("../schema/gilaki.db")
cursor = conn.cursor()

# Enable foreign keys (important for SQLite)
cursor.execute("PRAGMA foreign_keys = ON;")

# -------------------------------
# STEP 1: Run Schema
# -------------------------------
schema_path = "../schema/schema.sql"

if os.path.exists(schema_path):
    with open(schema_path, "r") as f:
        cursor.executescript(f.read())
    print("Schema loaded successfully ✅")
else:
    print("Schema file not found ❌")
    exit()

# -------------------------------
# STEP 2: Load CSV Files
# -------------------------------
data_folder = "../data/raw"   # ✅ correct path

tables = [
    "lemma",
    "person",
    "number",
    "tense",
    "mood",
    "form",
    "verb_form"
]

for table in tables:
    file_path = os.path.join(data_folder, f"{table}.csv")

    if os.path.exists(file_path):
        try:
            df = pd.read_csv(file_path)

            print(f"\nLoading {table}.csv...")
            print(df.head())  # 👀 debug preview

            df.to_sql(table, conn, if_exists="append", index=False)

            print(f"✅ Loaded {table}.csv")

        except Exception as e:
            print(f"❌ Error loading {table}.csv → {e}")

    else:
        print(f"⚠️ File not found: {file_path}")

# -------------------------------
# STEP 3: Test Query
# -------------------------------
try:
    print("\nTest Query Output:")
    cursor.execute("SELECT * FROM lemma LIMIT 5;")
    print(cursor.fetchall())
except Exception as e:
    print("❌ Query failed:", e)

# -------------------------------
# FINAL STEP
# -------------------------------
conn.commit()
conn.close()

print("\n🎉 Database setup complete!")