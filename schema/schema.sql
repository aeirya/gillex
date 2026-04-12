PRAGMA foreign_keys = OFF;

-- -------------------------
-- CORE TABLES
-- -------------------------

CREATE TABLE lexical_unit (
  id INTEGER PRIMARY KEY,
  is_dict_entry INTEGER,
  is_dialect INTEGER,
  is_mwlu INTEGER
);

CREATE TABLE lemma (
  id INTEGER PRIMARY KEY,
  lemma TEXT
);

CREATE TABLE dict_entry (
  id INTEGER PRIMARY KEY,
  lemma_id INTEGER,
  pos TEXT
);

CREATE TABLE verb_lemma (
  id INTEGER PRIMARY KEY,
  present_root TEXT,
  past_root TEXT,
  is_transitive INTEGER
);

-- -------------------------
-- DIALECT
-- -------------------------

CREATE TABLE dialect (
  id TEXT PRIMARY KEY,
  name TEXT,
  western TEXT,
  eastern TEXT
);

CREATE TABLE lexical_unit_dialect (
  lexical_unit_id INTEGER,
  dialect_id TEXT
);

-- -------------------------
-- FORM
-- -------------------------

CREATE TABLE form (
  id INTEGER PRIMARY KEY,
  lemma_id INTEGER,
  form TEXT
);

-- -------------------------
-- ENUM TABLES (MATCH CSV EXACTLY)
-- -------------------------

CREATE TABLE person (
  person_id INTEGER PRIMARY KEY,
  value TEXT
);

CREATE TABLE number (
  number_id TEXT PRIMARY KEY,
  value TEXT
);

CREATE TABLE mood (
  mood_id TEXT PRIMARY KEY,
  value TEXT
);

CREATE TABLE aspect (
  aspect_id TEXT PRIMARY KEY,
  aspect TEXT
);

-- 🔥 EXACT MATCH WITH CSV
CREATE TABLE verb_tenses (
  verb_tense_id TEXT PRIMARY KEY,
  shortname TEXT,
  name TEXT
);

-- -------------------------
-- VERB FORM (MATCH CSV EXACTLY)
-- -------------------------

CREATE TABLE verb_form (
  form_id INTEGER,
  form TEXT,
  person_id INTEGER,
  number_id TEXT,
  tense_id TEXT,
  mood_id TEXT,
  aspect_id TEXT,
  has_aux TEXT
);

-- -------------------------
-- OTHER TABLES
-- -------------------------

CREATE TABLE language (
  id TEXT PRIMARY KEY,
  name TEXT
);

CREATE TABLE gloss (
  id INTEGER,
  lexical_unit_id INTEGER,
  language_id TEXT,
  gloss TEXT
);

CREATE TABLE continuation_class (
  id INTEGER,
  name TEXT
);

CREATE TABLE lemma_continuation (
  lemma_id INTEGER,
  continuation_id INTEGER
);