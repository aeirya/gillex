# Gilaki verbs lexical-database

## Background

Gilaki is an Indo-European language used by the Gilak ethical minority local to northern Iran's Gilan area. There are around 3 million Gilaks (**CITE - Russian article**) and the vast majority of them are bilingual speakers of Persian, which has long acted as a superstrate language. 

As Persian is the official language both in the area and the wider region, this has unsurprisingly lead to a situation of diglosia, as defined by [[Diglosia]]. The sociolinguistic situation is such that the very speakers of Gilaki often consider Persian a superior language, even claiming that Gilaki doesn't really exist, which, as [[Diglosia]] puts it: 

> cannot be called a deliberate attempt to deceive the questioner, but seems almost a self-deception.

From the linguistic perspective, however, Gilaki behaves like a textbook substrate language. While the Persian influence is obviously not negligible, it has it's own defined and separate grammar system.

In this database, we aim to document the verb system of Gilaki, using a system heavily inspired by the Basque EDBL (**CITA**). In the following sections, we will explain the linguistic paradigms that govern the language usage, their impact on the database design and the final architecture.

## Linguistic paradigms
### Writing system and phonology

One of the main complications for Natural Language Processing in Gilaki is the fact that the language has no unified writing system. There have been several attempts at establishing a standardised writing system, however, none has become widespread enough to be considered standard (**CITA - The Gilaki Language**). As a result of this, the current situation is that there are multiple competing systems, which seem to be subject to linguistic variation patterns that traditionally govern the behaviour of spoken varieties, such as *indexing, as defined by [[Penelope Eckert Ph.D.]]* Therefore, different strata tend to write the same language in different ways. 

In this database, we will be using the writing standardisation used in the book The Gilaki Language (**Cita**) for consistency reasons and because this system leverages the phonological level which unlike the writing shows a degree of stability. This will also allow downstream users to use a G2P system to 'translate' the database into any writing standardisation they need to operate within. 

More concretely, (**author's**) standardisation attempts a one-to-one mapping between phonemes and graphemes. As it stands, the system translates to the IPA (**CITA**) as follows:

|           | Front                    | Central    | Back                     |
| --------- | ------------------------ | ---------- | ------------------------ |
| Close     | /i/ - \<i> ; /i:/ - <ı̄> |            | /u/ - \<u> ; /u:/ - <ū> |
| Close-mid | /e/ - \<e>; /e:/ - \<e>  |            | /o/ - \<o> ; /o:/ - \<o> |
| Open-mid  |                          | /ə/ - \<ə> |                          |
| Open      | /a/ - \<a>               |            | /ɑ/ - \<å>               |

It should be noted, however, that both of the grammars we consulted (**Citas**) imply that the phonological value of the long vowels is rather archaic and (mostly) out of use.

|                   | Bilabial                | Labiodental             | Alveolar                    | Postalveolar            | Velar                   | Uvular                    | Pharyngeal |
| ----------------- | ----------------------- | ----------------------- | --------------------------- | ----------------------- | ----------------------- | ------------------------- | ---------- |
| Plosive           | /p/ - \<p> ; /b/ - \<b> |                         | /t/ - \<t> ; /t/ - \<t>     |                         | /k/ - \<k> ; /g/ - \<g> |                           |            |
| Nasal             | /m/ - \<m>              |                         | /n/ - \<n>                  |                         |                         |                           |            |
| Tap or Flap       |                         |                         | /ɾ/ - \<r>                  |                         |                         |                           |            |
| Fricative         |                         | /f/ - \<f> ; /v/ - \<v> | /s/ - \<s> ; /z/ - \<z>     | /ʃ/ - \<š> ; /ʒ/ - \<ž> |                         |                           |            |
| Affricates        |                         |                         | /t͡ʃ/ - \<č> ; /d͡ʒ/ - \<ǰ> |                         |                         | /$\chi$/ -\<x> ; /ʁ/ \<ɣ> | /h/ - \<h> |
| Lateral fricative |                         |                         | /l/ - \<l>                  |                         |                         |                           |            |
| Approximant       |                         |                         |                             |                         |                         |                           |            |

*NOTE*: We are aware that the \<x> and \<ɣ> symbols are usually used to represent velar sounds, however, (**CITA**, p.15) labels them explicitly as uvular and uses them as such in their writing standardisation, which we have decided to adopt for the reasons mentioned above. 

**What exactly is \<y>? Maybe /j/? Consult this with Aeirya**

### Key verbal morphology

As is frequently the case with minority languages, especially in mountainous regions, the morphology of Gilaki has a decent number of irregularities, the theoretical explanation of which is, unfortunately, beyond the scope of this report. We would like to direct the interested readers to, (**CITA**), as it makes an detailed explanation of most of these.

Some regular and consistent patterns, nevertheless, do merit further explanation:

Firstly, Gilaki exhibits a coexistence of two stems for each lemma, one present and one past. The infinitive is based on the past stem and one of the following suffixes: `-ən` / `-an` / `-en` / `-on`.

In terms of conjugation, there are three moods with unevenly spread tenses:

- Indicative
	- Present-Future
	- Present Definite
	- Future Categoric
	- Past Neutral
	- Past Continuous
	- Past Definite
	- Pluperfect
- Subjunctive
	- Present-Future (also called Aorist)
	- Past tense
- Imperative

The inflective affixes for person and number are mostly consistent across all of these. The regular plurals are formed as follows, independently of tense and mood:

|     | Consistent plural suffix |
| --- | ------------------------ |
| 1.p | -im(i)                   |
| 2.p | -id(i)                   |
| 3.p | -id(i)                   |

Regular singulars, however, show a degree of consistent variation:

|     | Present future | Past neutral / Subjunctive Present Future | Past continuous |
| --- | -------------- | ----------------------------------------- | --------------- |
| 1.p | -əm            | -əm                                       | -im             |
| 2.p | -i             | -i                                        | -i              |
| 3.p | -e             | -ə                                        | -i              |
*The tenses not mentioned in the table are formed using auxiliar verbs.*

Negation can be achieved using one of the following prefixes: `na-` / `ni-` / `nu-`. The morpheme carrying the negation itself seems to be the `/n/` while the vowel appears to be defined purely by phonosyntax. 

**THERE IS ABSOLUTELY NO WAY I CAN FIT THE MORPHOLOGICAL RULES FOR EVERY SINGLE TENSE INTO THE REPORT PAGE LIMIT**
## The database design

The database contains the following tables:

---
# Project scope disclaimer

This project is an assignment hand-in for the Language Resources Course at the NLP Master's Programme at EHU/UPV.

It is also crucial to mention the author's qualification for this task: 
- **Gabriel** has formal linguistic training, however, lacks direct knowledge of the Gilaki language
- **Aeirya** is a gilak and a passive speaker of the language, but lacks linguistic training.
- **Naeem** is a purely technical contributor. 

We did the best we could with the knowledge, resources and time we had, however, the limitations stemming from our backgrounds and inability to consult Iranian internet due to the ongoing war still apply.