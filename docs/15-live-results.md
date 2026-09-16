# Live results

Numbers from `scripts/write_live_results.py` on this revision. Teaching scores, not a leaderboard.

## Headlines

- Default cut **0.30**
- Documents 26, hinges 140
- Mean per-document macro-F1 **0.695**
- Mean accuracy 0.829 (do not quote this first)
- Micro macro-F1 0.770
- Never-fire mean macro-F1 0.445
- Always-fire mean macro-F1 0.156
- Hand-calculation trap: accuracy 0.800, macro-F1 0.444

## By split

| split | n | mean macro-F1 |
| --- | ---: | ---: |
| easy | 6 | 0.784 |
| medium | 6 | 0.792 |
| hard | 6 | 0.540 |
| control | 3 | 0.429 |
| return | 1 | 1.000 |
| collage | 2 | 0.829 |
| gift | 1 | 1.000 |
| paste | 1 | 0.444 |

Hard is supposed to look worse than medium. If it does not, the blender is cheating with topic.

## Spotlight

- `problem-01-canal-then-lot` (easy): gold `000100` pred `000100` macro-F1 1.000
- `problem-08-quince-batch-then-letter` (medium): gold `00100` pred `00100` macro-F1 1.000
- `problem-13-two-mycologists` (hard): gold `0001000` pred `0000000` macro-F1 0.462
- `problem-19-river-three-topics` (control): gold `0000000` pred `0000000` macro-F1 0.500
- `problem-21-spark-three-chats` (control): gold `00000` pred `11001` macro-F1 0.286
- `problem-22-canal-return` (return): gold `01010` pred `01010` macro-F1 1.000
- `problem-25-tidepool-gift-abstract` (gift): gold `000100` pred `000100` macro-F1 1.000
- `problem-26-exam-two-answers` (paste): gold `00100` pred `00000` macro-F1 0.444

## Top of the threshold grid

| τ | mean macro-F1 | micro macro-F1 | mean acc |
| ---: | ---: | ---: | ---: |
| 0.30 | 0.695 | 0.770 | 0.829 |
| 0.28 | 0.660 | 0.726 | 0.789 |
| 0.32 | 0.650 | 0.756 | 0.845 |
| 0.26 | 0.635 | 0.690 | 0.742 |
| 0.34 | 0.632 | 0.748 | 0.847 |

## Full table

```
documents=26 hinges=140 cut=0.300
mean macro-F1=0.695  mean accuracy=0.829  micro macro-F1=0.770

document                                   split      gold               pred                  mF1    acc
problem-01-canal-then-lot                  easy       000100             000100              1.000  1.000
problem-02-couchette-then-hvac             easy       00100              00100               1.000  1.000
problem-03-vinyl-then-reserve              easy       00100              00110               0.762  0.800
problem-04-amber-then-label                easy       000100             000110              0.778  0.833
problem-05-pond-letter-then-notice         easy       00100              11100               0.583  0.600
problem-06-compost-then-chat               easy       00100              00111               0.583  0.600
problem-07-miso-sop-then-chat              medium     00100              00111               0.583  0.600
problem-08-quince-batch-then-letter        medium     00100              00100               1.000  1.000
problem-09-hive-then-honey                 medium     00100              00100               1.000  1.000
problem-10-steinway-invoice-then-nocturne  medium     00100              00100               1.000  1.000
problem-11-darkroom-then-zine              medium     00100              00111               0.583  0.600
problem-12-tram-chat-then-minutes          medium     00100              11100               0.583  0.600
problem-13-two-mycologists                 hard       0001000            0000000             0.462  0.857
problem-14-two-planners                    hard       00100              00000               0.444  0.800
problem-15-two-letterpress                 hard       00100              00000               0.444  0.800
problem-16-two-observers                   hard       000100             000100              1.000  1.000
problem-17-two-callers                     hard       00100              00000               0.444  0.800
problem-18-two-go-notes                    hard       00100              00000               0.444  0.800
problem-19-river-three-topics              control    0000000            0000000             0.500  1.000
problem-20-quill-three-agenda              control    00000              00000               0.500  1.000
problem-21-spark-three-chats               control    00000              11001               0.286  0.400
problem-22-canal-return                    return     01010              01010               1.000  1.000
problem-23-miso-collage                    collage    01010              01110               0.800  0.800
problem-24-sauna-four-voices               collage    0101010            0111010             0.857  0.857
problem-25-tidepool-gift-abstract          gift       000100             000100              1.000  1.000
problem-26-exam-two-answers                paste      00100              00000               0.444  0.800
```

Regenerate:

```bash
PYTHONPATH=src python3 scripts/write_live_results.py
```
