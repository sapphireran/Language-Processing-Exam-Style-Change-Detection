# Study documents

All of these texts are original. None of them come from PAN, Reddit, or a
course handout. I wrote them so that I would know the gold cuts before
running a detector.

Sentence-level files use **one sentence per line**. That is a study
convention, not a claim about how English works. Paragraph-level files
separate units with a blank line.

| id | units | gold cuts | what it is for |
| --- | ---: | ---: | --- |
| `01_single_commute` | 10 sentences | 0 | negative control, one diary voice |
| `02_recipe_then_maillard` | 13 sentences | 1 | easy length + register jump; topic also moves |
| `03_forum_three_voices` | 12 sentences | 2 | slang / moderator / parent |
| `04_minutes_return` | 12 sentences | 2 | chair → intern → chair (author 1 returns) |
| `05_same_topic_hard` | 8 sentences | 1 | both blocks are about BPE |
| `06_gift_abstract` | 2 paragraphs | 1 | student abstract + grafted supervisor prose |
| `07_collage_paragraphs` | 5 paragraphs | 4 | three cooks, two returns |
| `08_sms_essay_mix` | 8 sentences | 1 | SMS then a short essay |
| `09_lab_notebook` | 5 paragraphs | 0 | negative control at paragraph grain |
| `10_exam_mashup` | 16 sentences | 3 | notes / chat / textbook / notes |

Truth files live in `truth/` and use a PAN-shaped `changes` array of
length `n_units - 1`. `authors` is optional Task-2 flavour.

A score of 1.0 on this folder is a sanity check, not a shared-task
result. The hard file is still a toy: eight sentences, one rehearsed
contrast.
