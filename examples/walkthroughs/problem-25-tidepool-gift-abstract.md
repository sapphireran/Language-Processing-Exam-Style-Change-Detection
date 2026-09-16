# Walkthrough: `problem-25-tidepool-gift-abstract`

Split: **gift**. Student I-voice essay, then a gifted conference abstract pasted under it.

```
units=7 hinges=6 detector=threshold cut=0.300
pred=[0, 0, 0, 1, 0, 0]
gold=[0, 0, 0, 1, 0, 0]
accuracy=1.000 macro-F1=1.000 change-F1=1.000 (tp=1 fp=0 fn=0 tn=5)
cusum peak hinge=2

[0] hold  blend=0.140  reg=0.129  fw=0.130  char=0.367  d=0.072  gold=0
     drivers: mean_word_len:4.250->3.750, i_rate:0.083->0.167, fw_ratio:0.417->0.500
     L: I spent the afternoon in the tide pool behind the harbour wall.
     R: I counted sixteen anemones and I lost a boot to the weed.
[1] hold  blend=0.156  reg=0.137  fw=0.136  char=0.360  d=0.287  gold=0
     drivers: words_per_unit:12.000->11.000, mean_word_len:3.750->3.364, fw_ratio:0.500->0.636
     L: I counted sixteen anemones and I lost a boot to the weed.
     R: The water was so clear I could see my own knees.
[2] hold  blend=0.170  reg=0.175  fw=0.109  char=0.347  d=0.101  gold=0
     drivers: mean_word_len:3.364->3.636, fw_ratio:0.636->0.545, passive_rate:0.091->0.182
     L: The water was so clear I could see my own knees.
     R: I think the pool is smaller than it was last April.
[3] SNAP  blend=0.350  reg=0.354  fw=0.211  char=0.376  d=1.788  gold=1
     drivers: words_per_unit:11.000->22.000, mean_word_len:3.636->5.182, passive_rate:0.182->0.000
     L: I think the pool is smaller than it was last April.
     R: We present a four-year survey of intertidal pools which demonstrates,...
[4] hold  blend=0.223  reg=0.203  fw=0.261  char=0.327  d=0.338  gold=0
     drivers: words_per_unit:22.000->21.000, mean_word_len:5.182->6.048, comma_rate:0.091->0.000
     L: We present a four-year survey of intertidal pools which demonstrates,...
     R: Anemone counts remain stable whilst algal cover has increased; the pa...
[5] hold  blend=0.290  reg=0.269  fw=0.187  char=0.403  d=2.349  gold=0
     drivers: words_per_unit:21.000->7.000, mean_word_len:6.048->7.143, fw_ratio:0.429->0.286
     L: Anemone counts remain stable whilst algal cover has increased; the pa...
     R: Implications for municipal dredging policy are discussed.
```
