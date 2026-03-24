PRAGMA foreign_keys = ON;

CREATE TABLE lexical_unit (
  id INTEGER PRIMARY KEY,
  is_dict_entry INTEGER,
  is_dialect INTEGER,
  is_mwlu INTEGER
);

CREATE TABLE lemma (
  id INTEGER PRIMARY KEY,
  lemma TEXT UNIQUE
);

CREATE TABLE pos (
  id INTEGER PRIMARY KEY,
  name TEXT
);

CREATE TABLE dict_entry (
  id INTEGER PRIMARY KEY,
  lemma_id INTEGER,
  pos_id INTEGER,
  FOREIGN KEY (id) REFERENCES lexical_unit(id),
  FOREIGN KEY (lemma_id) REFERENCES lemma(id),
  FOREIGN KEY (pos_id) REFERENCES pos(id)
);

CREATE TABLE verb_lemma (
  id INTEGER PRIMARY KEY,
  present_root TEXT,
  past_root TEXT,
  is_transitive INTEGER,
  FOREIGN KEY (id) REFERENCES dict_entry(id)
);

CREATE TABLE verb_transitivity_alternation (
  transitive_id INTEGER,
  intransitive_id INTEGER,
  FOREIGN KEY (transitive_id) REFERENCES verb_lemma(id),
  FOREIGN KEY (intransitive_id) REFERENCES verb_lemma(id)
);

CREATE TABLE dialect (
  id INTEGER PRIMARY KEY,
  name TEXT,
  western INTEGER,
  eastern INTEGER
);

-- ✅ FIXED (typo + composite PK)
CREATE TABLE lexical_unit_dialect (
  lexical_unit_id INTEGER,
  dialect_id INTEGER,
  PRIMARY KEY (lexical_unit_id, dialect_id),
  FOREIGN KEY (lexical_unit_id) REFERENCES lexical_unit(id),
  FOREIGN KEY (dialect_id) REFERENCES dialect(id)
);

-- ✅ FIXED (added PK)
CREATE TABLE morpheme (
  id INTEGER PRIMARY KEY,
  is_independent INTEGER,
  FOREIGN KEY (id) REFERENCES lexical_unit(id)
);

CREATE TABLE independent_morpheme (
  id INTEGER,
  is_prefix INTEGER,
  is_suffix INTEGER,
  FOREIGN KEY (id) REFERENCES morpheme(id)
);

CREATE TABLE prefix_morpheme (
  id INTEGER,
  is_derivational INTEGER,
  FOREIGN KEY (id) REFERENCES independent_morpheme(id)
);

CREATE TABLE suffix_morpheme (
  id INTEGER,
  is_person_number INTEGER,
  is_object INTEGER,
  FOREIGN KEY (id) REFERENCES independent_morpheme(id)
);

CREATE TABLE mwlu (
  id INTEGER PRIMARY KEY,
  continuation_class TEXT,
  FOREIGN KEY (id) REFERENCES lexical_unit(id)
);

CREATE TABLE form (
  id INTEGER PRIMARY KEY,
  form TEXT,
  lemma_id INTEGER,
  FOREIGN KEY (id) REFERENCES lexical_unit(id),
  FOREIGN KEY (lemma_id) REFERENCES lemma(id)
);

CREATE TABLE person (
  person_id INTEGER PRIMARY KEY,
  value TEXT
);

CREATE TABLE number (
  number_id INTEGER PRIMARY KEY,
  value TEXT
);

CREATE TABLE tense (
  tense_id INTEGER PRIMARY KEY,
  value TEXT
);

CREATE TABLE mood (
  mood_id INTEGER PRIMARY KEY,
  value TEXT
);

CREATE TABLE aspect (
  aspect_id INTEGER PRIMARY KEY,
  value TEXT
);

CREATE TABLE verb_form (
  form_id INTEGER PRIMARY KEY,
  person_id INTEGER,
  number_id INTEGER,
  tense_id INTEGER,
  mood_id INTEGER,
  aspect_id INTEGER,
  has_aux INTEGER,
  FOREIGN KEY (form_id) REFERENCES form(id),
  FOREIGN KEY (person_id) REFERENCES person(person_id),
  FOREIGN KEY (number_id) REFERENCES number(number_id),
  FOREIGN KEY (tense_id) REFERENCES tense(tense_id),
  FOREIGN KEY (mood_id) REFERENCES mood(mood_id),
  FOREIGN KEY (aspect_id) REFERENCES aspect(aspect_id)
);

CREATE TABLE language (
  id INTEGER PRIMARY KEY,
  name TEXT
);

CREATE TABLE gloss (
  id INTEGER PRIMARY KEY,
  lexical_unit_id INTEGER,
  language_id INTEGER,
  gloss TEXT,
  FOREIGN KEY (language_id) REFERENCES language(id)
);

CREATE TABLE continuation_class (
  id INTEGER PRIMARY KEY,
  name TEXT
);

-- ✅ FIXED (composite PK + FK added)
CREATE TABLE lemma_continuation (
  lemma_id INTEGER,
  continuation_id INTEGER,
  PRIMARY KEY (lemma_id, continuation_id),
  FOREIGN KEY (lemma_id) REFERENCES lemma(id),
  FOREIGN KEY (continuation_id) REFERENCES continuation_class(id)
);

-- ✅ FIXED INDEX
CREATE INDEX idx_verb_form 
ON verb_form (person_id, number_id, tense_id, mood_id, aspect_id);