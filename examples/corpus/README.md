# Teaching corpus

Twelve original documents, hand-written for this lab. They are **not**
PAN/Reddit data. Thresholds in `scarfjoint` were swept on this set.
Do not quote the collection score as a shared-task result.

Paragraphs are separated by a blank line. Gold files use the PAN
shape plus teaching keys (`band`, `paragraph_authors`, `topic_note`).

| id | band | file | gold `changes` |
| --- | --- | --- | --- |
| 01 | easy | `easy/problem-01-ferry-marsh-knit.txt` | `[0, 1, 0, 1, 0]` |
| 02 | easy | `easy/problem-02-bees-sizing-market.txt` | `[0, 1, 0, 1, 0]` |
| 03 | easy | `easy/problem-03-skate-glacier-plants.txt` | `[0, 1, 0, 1, 0]` |
| 04 | medium | `medium/problem-04-bouldering.txt` | `[0, 1, 0, 1, 0]` |
| 05 | medium | `medium/problem-05-community-radio.txt` | `[0, 1, 0, 1, 0]` |
| 06 | medium | `medium/problem-06-sourdough.txt` | `[0, 1, 0, 1, 0]` |
| 07 | hard | `hard/problem-07-darkroom.txt` | `[0, 1, 0, 1, 0]` |
| 08 | hard | `hard/problem-08-orchard-pruning.txt` | `[0, 1, 0, 1, 0]` |
| 09 | hard | `hard/problem-09-tidal-gauge.txt` | `[0, 1, 0, 1, 0]` |
| 10 | single | `single_author/problem-10-lighthouse.txt` | `[0, 0, 0, 0, 0]` |
| 11 | single | `single_author/problem-11-violin-repair.txt` | `[0, 0, 0, 0]` |
| 12 | single | `single_author/problem-12-map-librarian.txt` | `[0, 0, 0, 0, 0]` |

Easy documents change **topic and author** together. Medium documents
hold a topic and change register. Hard documents hold a topic and
keep neighbouring voices close. Single-author documents are the
accuracy trap.
