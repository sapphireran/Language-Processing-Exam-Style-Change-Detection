# Walkthrough: `problem-01-canal-then-lot`

Split: **easy**. River field journal snaps to a Marble auction lot. Topic and register move together.

```
units=7 hinges=6 detector=threshold cut=0.300
pred=[0, 0, 0, 1, 0, 0]
gold=[0, 0, 0, 1, 0, 0]
accuracy=1.000 macro-F1=1.000 change-F1=1.000 (tp=1 fp=0 fn=0 tn=5)
cusum peak hinge=2

[0] hold  blend=0.205  reg=0.179  fw=0.094  char=0.360  d=1.951  gold=0
     drivers: words_per_unit:10.000->13.000, mean_word_len:4.600->3.769, i_rate:0.100->0.231
     L: I walked the towpath before the first hire boat stirred.
     R: I counted eight lock gates and I wrote the numbers on my cuff.
[1] hold  blend=0.268  reg=0.264  fw=0.144  char=0.357  d=1.310  gold=0
     drivers: words_per_unit:13.000->11.000, mean_word_len:3.769->4.273, i_rate:0.231->0.000
     L: I counted eight lock gates and I wrote the numbers on my cuff.
     R: The bottom gate leaked a thin silver thread onto the cill.
[2] hold  blend=0.172  reg=0.158  fw=0.046  char=0.296  d=1.269  gold=0
     drivers: words_per_unit:11.000->13.000, mean_word_len:4.273->3.769, fw_ratio:0.273->0.462
     L: The bottom gate leaked a thin silver thread onto the cill.
     R: I ate the last plum on the coping stone and watched a moorhen.
[3] SNAP  blend=0.316  reg=0.338  fw=0.145  char=0.405  d=0.682  gold=1
     drivers: words_per_unit:13.000->12.000, mean_word_len:3.769->3.167, fw_ratio:0.462->0.083
     L: I ate the last plum on the coping stone and watched a moorhen.
     R: Lot 14: oak lock-gate leaf, 3.2 m by 0.48 m; iron strap hinges, c. 1891.
[4] hold  blend=0.241  reg=0.232  fw=0.044  char=0.442  d=1.959  gold=0
     drivers: words_per_unit:12.000->9.000, mean_word_len:3.167->5.444, comma_rate:0.167->0.000
     L: Lot 14: oak lock-gate leaf, 3.2 m by 0.48 m; iron strap hinges, c. 1891.
     R: The object retains original pintles; surface chloride 12 g/kg.
[5] hold  blend=0.241  reg=0.247  fw=0.039  char=0.381  d=1.335  gold=0
     drivers: words_per_unit:9.000->11.000, mean_word_len:5.444->4.273, comma_rate:0.000->0.273
     L: The object retains original pintles; surface chloride 12 g/kg.
     R: A later paint skin, alkyd, 0.3 mm, covers the landward face only.
```
