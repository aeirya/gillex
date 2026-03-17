# Gilaki verbs lexical-database

## Background

Gilaki is an Indo-European language used by the Gilak ethical minority local to northern Iran's Gilan area. There are around 3 million Gilaks (Ivanov & Dodykhudoeva, 2015) and the vast majority of them are bilingual speakers of Persian, which has long acted as a superstrate language. 

As Persian is the official language both in the area and the wider region, this has unsurprisingly lead to a situation of diglosia, as defined by Ferguson (1959). The sociolinguistic situation is such that the very speakers of Gilaki often consider Persian a superior language, even claiming that Gilaki doesn't really exist, which, as Ferguson puts it: 

> cannot be called a deliberate attempt to deceive the questioner, but seems almost a self-deception.

From the linguistic perspective, however, Gilaki behaves like a textbook substrate language. While the Persian influence is obviously not negligible, it has it's own defined and separate grammar system.

In this database, we aim to document the verb system of Gilaki, using a system heavily inspired by the Basque EDBL (Aduriz et al. 1998, Aldezabal et al. 2001). In the following sections, we will explain the linguistic paradigms that govern the language usage, their impact on the database design and the final architecture.

## Linguistic paradigms
### Writing system and phonology

One of the main complications for Natural Language Processing in Gilaki is the fact that the language has no unified writing system. There have been several attempts at establishing a standardised writing system, however, none has become widespread enough to be considered standard (Rastorgueva et al. 2012). As a result of this, the current situation is that there are multiple competing systems, which seem to be subject to linguistic variation patterns that traditionally govern the behaviour of spoken varieties, such as sociological indexing, as defined by Eckert (2019). Therefore, different strata tend to write the same language in different ways. 

In this database, we will be using the writing standardisation used in the book The Gilaki Language (Rastorgueva et al. 2012) for consistency reasons and because this system leverages the phonological level which unlike the writing shows a degree of stability. This will also allow downstream users to use a G2P system to 'translate' the database into any writing standardisation they need to operate within. 

More concretely the author's standardisation attempts a one-to-one mapping between phonemes and graphemes. As it stands, the system translates to the IPA as follows:

|           | Front                    | Central    | Back                     |
| --------- | ------------------------ | ---------- | ------------------------ |
| Close     | /i/ - \<i> ; /i:/ - <ı̄> |            | /u/ - \<u> ; /u:/ - <ū> |
| Close-mid |                          |            | /o/ - \<o> ; /o:/ - \<o> |
| Open-mid  | /ɛ/ - \<e>; /ɛ:/ - \<e>  | /ə/ - \<ə> |                          |
| Open      | /æ/ - \<a>               |            | /ɑ/ - \<å>               |

It should be noted, however, that both of the grammars we consulted (Rastorgueva et al. 2012, Purhadi 2018) imply that the phonological value of the long vowels is rather archaic and (mostly) out of use.

|                   | Bilabial                | Labiodental             | Alveolar                    | Postalveolar            | Velar                   | Uvular                      | Pharyngeal |
| ----------------- | ----------------------- | ----------------------- | --------------------------- | ----------------------- | ----------------------- | --------------------------- | ---------- |
| Plosive           | /p/ - \<p> ; /b/ - \<b> |                         | /t/ - \<t> ; /t/ - \<t>     |                         | /k/ - \<k> ; /g/ - \<g> |                             |            |
| Nasal             | /m/ - \<m>              |                         | /n/ - \<n>                  |                         |                         |                             |            |
| Tap or Flap       |                         |                         | /ɾ/ - \<r>                  |                         |                         |                             |            |
| Fricative         |                         | /f/ - \<f> ; /v/ - \<v> | /s/ - \<s> ; /z/ - \<z>     | /ʃ/ - \<š> ; /ʒ/ - \<ž> |                         |                             |            |
| Affricates        |                         |                         | /t͡ʃ/ - \<č> ; /d͡ʒ/ - \<ǰ> |                         |                         | /$\chi$/ -\<x> ; /ʁ/ - \<ɣ> | /h/ - \<h> |
| Lateral fricative |                         |                         | /l/ - \<l>                  |                         |                         |                             |            |
| Approximant       |                         |                         | /j/ - \<y>                  |                         |                         |                             |            |

*NOTE*: We are aware that the \<x> and \<ɣ> symbols are usually used to represent velar sounds, however, Rastorgueva et al. (2012, p.15) label them explicitly as uvular and uses them as such in their writing standardisation, which we have decided to adopt for the reasons mentioned above. 

### Key verbal morphology


As is frequently the case with minority languages, especially in mountainous regions, the morphology of Gilaki has a decent number of irregularities, the theoretical explanation of which is, unfortunately, beyond the scope of this report. We would like to direct the interested readers to, Rastorgueva et al. (2012), as it makes an detailed explanation of most of these.

Some regular and consistent patterns, nevertheless, do merit further explanation:

Firstly, Gilaki exhibits a coexistence of two stems for each lemma, one present and one past. The present stem is used to form the present future tense, the imperative mood and the subjunctive present future tense. The past stem is used for the past tense and the participle. The infinitive is also based on the past stem and one of the following suffixes: `-ən` / `-an` / `-en` / `-on`.

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
## The database design

The database contains the following tables:

---
# Project scope disclaimer

This project is an assignment hand-in for the Language Resources Course at the NLP Master's Programme at EHU/UPV.

It is also crucial to mention the author's qualification for this task: 
- **Gabriel** has formal linguistic training, however, lacks direct knowledge of the Gilaki language
- **Aeirya** is a gilak and a passive-native speaker of the language, but lacks linguistic training.
- **Naeem** is a purely technical contributor. 

We did the best we could with the knowledge, resources and time we had, however, the limitations stemming from our backgrounds and inability to consult Iranian internet due to the ongoing war still apply.

# References

Ivanov, V. B., & Dodykhudoeva, L. R. (2015). _Socio- and ethnolinguistic features of Gilaki and Mazandarani_. ИСТИНА. [https://istina.ficp.ac.ru/publications/article/10343068/](https://istina.ficp.ac.ru/publications/article/10343068/)

Ferguson, C. A. (1959). Diglossia. _WORD_, 15(2), 325–340. https://doi.org/10.1080/00437956.1959.11659702

Aduriz, I., Aldezabal, I., Ansa, O., Artola, X., & Díaz de Ilarraza, A. (1998). EDBL: A multi-purposed lexical support for the treatment of Basque. In _Proceedings of the First International Conference on Language Resources and Evaluation_ (Vol. II, pp. 821–826). Granada, Spain.

Aldezabal, I., Ansa, O., Arrieta, B., Artola, X., Ezeiza, A., Hernández, G., & Lersundi, M. (2001). EDBL: A general lexical basis for the automatic processing of Basque. In _IRCS Workshop on Linguistic Databases_. Philadelphia, PA, USA.

Eckert, P. (2019). The limits of meaning: Social indexicality, variation, and the cline of interiority. _Language_ _95_(4), 751-776. [https://dx.doi.org/10.1353/lan.2019.0072](https://dx.doi.org/10.1353/lan.2019.0072).

Rastorgueva, V. S., Kerimova, A. A., Mamedzade, A. K., Pireiko, L. A., Edel’man, D. I., & Lockwood, R. M. (2012). _The Gilaki language_. Retrieved from [https://urn.kb.se/resolve?urn=urn:nbn:se:uu:diva-182789](https://urn.kb.se/resolve?urn=urn:nbn:se:uu:diva-182789)

Purhadi, M. (2018). _Zabān-e Gilaki_ [The Gilaki language]. Nashr-e Farhang-e Ilia.