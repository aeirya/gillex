# Gilaki verbs lexical-database

## Background

Gilaki is an Indo-European language used by the Gilak ethical minority local to northern Iran's Gilan area. There are around 3 million Gilaks (**CITE - Russian article**) and the vast majority of them are bilingual speakers of Persian, which has long acted as a superstrate language. 

As Persian is the official language both in the area and the wider region, this has unsurprisingly lead to a situation of diglosia, as defined by [[Diglosia]]. The sociolinguistic situation is such that the very speakers of Gilaki often consider Persian a superior language, even claiming that Gilaki doesn't really exist, which, as [[Diglosia]] puts it: 

> cannot be called a deliberate attempt to deceive the questioner, but seems almost a self-deception.

From the linguistic perspective, however, Gilaki behaves like a textbook substrate language. While the Persian influence is obviously not negligible, it has it's own separate grammar system with defined affixes which operate under a mostly *syntetic* (double-check), while Persian behaves mostly as an *agglutinative* (double-check) language.

In this database, we aim to document the verb system of Gilaki, using a system heavily inspired by the Basque EDBL (**CITA**). In the following sections, we will explain the linguistic paradigms that govern the language usage, their impact on the database design and the final architecture.

## Linguistic paradigms
### Writing system and phonology

One of the main complications for Natural Language Processing in Gilaki is the fact that the language is unwritten. There have been several attempts at establishing a standardised writing system, however, none has become widespread enough to be considered standard (**CITA - The Gilaki Language**). As a result of this, the current situation is that there are multiple competing systems, which seem to be subject to linguistic variation patterns that traditionally govern the behaviour of spoken varieties, such as *indexing, as defined by [[Penelope Eckert Ph.D.]]* Therefore, different strata tend to write the same language in different ways. 

In this database, we will be using the writing standardisation used in the book The Gilaki Language (**Cita**) for consistency reasons and because this system leverages the phonological level which unlike the writing shows a degree of stability. This will also allow downstream users to use a G2P system to 'translate' the database into the writing standardisation they need to operate within. 

More concretely, (**author's**) standardisation attempts a one-to-one mapping between phonemes and graphemes. As it stands, the system translates to the IPA as follows:

|           | Front                    | Central    | Back                     |
| --------- | ------------------------ | ---------- | ------------------------ |
| Close     | /i/ - \<i> ; /i:/ - <ı̄> |            | /u/ - \<u> ; /u:/ - <ū> |
| Close-mid | /e/ - \<e>               |            | /o/ - \<o>               |
| Open-mid  |                          | /ə/ - \<ə> |                          |
| Open      | /a/ - \<a>               |            | /ɑ/ - \<å>               |

|                     | Bilabial                | Labiodental | Dental | Alveolar                    | Postalveolar | Palatal | Velar                   | Uvular | Pharyngeal | Glottal |
| ------------------- | ----------------------- | ----------- | ------ | --------------------------- | ------------ | ------- | ----------------------- | ------ | ---------- | ------- |
| Plosive             | /p/ - \<p> ; /b/ - \<b> |             |        | /t/ - \<t> ; /t/ - \<t>     |              |         | /k/ - \<k> ; /g/ - \<g> |        |            |         |
| Nasal               | /m/ - \<m>              |             |        | /n/ - \<n>                  |              |         |                         |        |            |         |
| Trill               |                         |             |        |                             |              |         |                         |        |            |         |
| Tap or Flap         |                         |             |        |                             |              |         |                         |        |            |         |
| Fricative           |                         |             |        |                             |              |         |                         |        |            |         |
| Affricates          |                         |             |        | /t͡ʃ/ - \<č> ; /d͡ʒ/ - \<ǰ> |              |         |                         |        |            |         |
| Lateral fricative   |                         |             |        |                             |              |         |                         |        |            |         |
| Approximant         |                         |             |        |                             |              |         |                         |        |            |         |
| Lateral approximant |                         |             |        |                             |              |         |                         |        |            |         |



## The database design