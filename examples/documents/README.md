# Hand-written exam documents

These are original study texts, not PAN dumps and not scraped web pages.
Each file is blank-line-separated paragraphs. Gold labels live in
`truth/` as PAN-shaped JSON.

| file | pattern | gold `changes` | why it is here |
| --- | --- | --- | --- |
| `01_single_ferns` | A A A | 0 0 | casual single author |
| `02_easy_bikes_then_vellum` | A A B B | 0 1 0 | topic *and* register jump |
| `03_medium_cph_rent` | A B A B | 1 1 1 | same city, two registers |
| `04_hard_circadian` | A B A B | 1 1 1 | two academic voices, one topic |
| `05_gift_poster` | A B A B | 1 1 1 | gift-authorship / lab confession |
| `06_three_boardgame` | A B C B C | 1 1 1 1 | three authors |
| `07_return_ferry` | A B A | 1 1 | returning author (A-B-A) |
| `08_minutes_then_slack` | A B A B | 1 1 1 | same meeting, two media |
| `09_magnets_kid_vs_paper` | A B A B | 1 1 1 | audience shift, shared facts |
| `10_exam_paste` | A B A | 1 1 | student + encyclopaedia paste |
| `11_sourdough_two_bakers` | A B A B | 1 1 1 | imperative vs bakery science |
| `12_landlord_letter` | A A A A | 0 0 0 | formal single author |
| `13_collage_four_voices` | A B C B | 1 1 1 | short collage |
| `14_rain_lyric_vs_met` | A B A B | 1 1 1 | lyric vs forecast |

`changes[i] = 1` means paragraphs `i` and `i+1` have different authors.
A binary change vector cannot encode that P1 and P3 of `07` are the
same person; that is a clustering question, not a PAN-2023 label.

Author cards in `../authors/` restack these voices into new A-B-A drills
(`scdkit mix examples/authors ABA`).
