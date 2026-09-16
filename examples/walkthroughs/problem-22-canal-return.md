# Walkthrough: `problem-22-canal-return`

Split: **return**. River, Marble, River again. authors=2 but 1+sum(changes)=3. Binary hinges cannot name the return.

```
units=6 hinges=5 detector=threshold cut=0.300
pred=[0, 1, 0, 1, 0]
gold=[0, 1, 0, 1, 0]
accuracy=1.000 macro-F1=1.000 change-F1=1.000 (tp=2 fp=0 fn=0 tn=3)
cusum peak hinge=3
authors=2 but 1+sum(changes)=3: a writer came back. Binary hinges cannot name who.

[0] hold  blend=0.164  reg=0.142  fw=0.095  char=0.317  d=0.861  gold=0
     drivers: words_per_unit:11.000->13.000, mean_word_len:4.364->3.846, fw_ratio:0.455->0.615
     L: I walked back along the towpath after the survey boat left.
     R: I sat on the same coping stone and I watched the moorhen again.
[1] SNAP  blend=0.306  reg=0.333  fw=0.104  char=0.383  d=0.838  gold=1
     drivers: words_per_unit:13.000->11.000, mean_word_len:3.846->4.727, fw_ratio:0.615->0.182
     L: I sat on the same coping stone and I watched the moorhen again.
     R: Lot 14 addendum: pintle wear 1.8 mm on the river face; photograph she...
[2] hold  blend=0.173  reg=0.143  fw=0.063  char=0.430  d=1.283  gold=0
     drivers: words_per_unit:11.000->8.000, mean_word_len:4.727->6.750, fw_ratio:0.182->0.125
     L: Lot 14 addendum: pintle wear 1.8 mm on the river face; photograph she...
     R: Revised reserve 110 GBP; condition note updated after desalination.
[3] SNAP  blend=0.363  reg=0.363  fw=0.218  char=0.405  d=2.472  gold=1
     drivers: words_per_unit:8.000->14.000, mean_word_len:6.750->3.929, fw_ratio:0.125->0.500
     L: Revised reserve 110 GBP; condition note updated after desalination.
     R: I put the printed addendum in the garden book and I closed the latch.
[4] hold  blend=0.154  reg=0.160  fw=0.100  char=0.298  d=0.092  gold=0
     drivers: mean_word_len:3.929->3.429, fw_ratio:0.500->0.643, i_rate:0.143->0.071
     L: I put the printed addendum in the garden book and I closed the latch.
     R: I still think the gate should stay on the canal, not in a hall.
```
