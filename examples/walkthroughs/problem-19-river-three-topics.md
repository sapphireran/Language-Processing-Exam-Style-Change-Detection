# Walkthrough: `problem-19-river-three-topics`

Split: **control**. Single River voice. Topic jumps (greenhouse, quince, night bus) must not count as style changes.

```
units=8 hinges=7 detector=threshold cut=0.300
pred=[0, 0, 0, 0, 0, 0, 0]
gold=[0, 0, 0, 0, 0, 0, 0]
accuracy=1.000 macro-F1=0.500 change-F1=0.000 (tp=0 fp=0 fn=0 tn=7)
cusum peak hinge=3

[0] hold  blend=0.082  reg=0.049  fw=0.062  char=0.265  d=0.544  gold=0
     drivers: words_per_unit:13.000->12.000, mean_word_len:4.154->3.750, fw_ratio:0.538->0.500
     L: I cracked the greenhouse vent and I wrote the humidity in the book.
     R: I pinched two side shoots and I dropped them in the trug.
[1] hold  blend=0.087  reg=0.038  fw=0.089  char=0.246  d=1.071  gold=0
     drivers: words_per_unit:12.000->14.000, mean_word_len:3.750->3.786, i_rate:0.167->0.143
     L: I pinched two side shoots and I dropped them in the trug.
     R: I turned the quince jars on the pantry shelf and I wiped the rings.
[2] hold  blend=0.089  reg=0.053  fw=0.037  char=0.228  d=1.054  gold=0
     drivers: words_per_unit:14.000->12.000, mean_word_len:3.786->3.333, i_rate:0.143->0.167
     L: I turned the quince jars on the pantry shelf and I wiped the rings.
     R: I held one jar to the window and I liked the colour.
[3] hold  blend=0.156  reg=0.124  fw=0.058  char=0.334  d=1.705  gold=0
     drivers: words_per_unit:12.000->9.000, mean_word_len:3.333->4.333, fw_ratio:0.500->0.444
     L: I held one jar to the window and I liked the colour.
     R: I caught the night bus after the last rehearsal.
[4] hold  blend=0.266  reg=0.242  fw=0.181  char=0.419  d=1.725  gold=0
     drivers: words_per_unit:9.000->12.000, mean_word_len:4.333->3.417, i_rate:0.111->0.333
     L: I caught the night bus after the last rehearsal.
     R: I counted four bridges and I kept my bag on my knees.
[5] hold  blend=0.253  reg=0.221  fw=0.208  char=0.394  d=1.594  gold=0
     drivers: words_per_unit:12.000->15.000, mean_word_len:3.417->3.133, i_rate:0.333->0.133
     L: I counted four bridges and I kept my bag on my knees.
     R: I got off at the depot and I walked the last lane in the rain.
[6] hold  blend=0.197  reg=0.176  fw=0.130  char=0.316  d=1.065  gold=0
     drivers: words_per_unit:15.000->13.000, i_rate:0.133->0.308, mean_word_len:3.133->3.000
     L: I got off at the depot and I walked the last lane in the rain.
     R: I hung my coat by the stove and I slept in my shirt.
```
