# Walkthrough: `problem-21-spark-three-chats`

Split: **control**. Single Spark voice jumping from film to tram to honey. Control false-alarm bait.

```
units=6 hinges=5 detector=threshold cut=0.300
pred=[1, 1, 0, 0, 1]
gold=[0, 0, 0, 0, 0]
accuracy=0.400 macro-F1=0.286 change-F1=0.000 (tp=0 fp=3 fn=0 tn=2)
cusum peak hinge=3

[0] SNAP  blend=0.338  reg=0.374  fw=0.137  char=0.307  d=0.918  gold=0  FALSE ALARM
     drivers: words_per_unit:14.000->11.000, mean_word_len:3.714->4.455, fw_ratio:0.571->0.455
     L: yo did you see frame 14 or are we all just pretending it isn't magic?
     R: i'm printing it tomorrow and you should come if you're free!
[1] SNAP  blend=0.302  reg=0.311  fw=0.183  char=0.407  d=0.664  gold=0  FALSE ALARM
     drivers: words_per_unit:11.000->13.000, mean_word_len:4.455->4.308, contraction_rate:0.182->0.077
     L: i'm printing it tomorrow and you should come if you're free!
     R: anyway the 4:40 died at the bridge again and we're packed in like pic...
[2] hold  blend=0.261  reg=0.260  fw=0.165  char=0.381  d=0.680  gold=0
     drivers: words_per_unit:13.000->11.000, mean_word_len:4.308->3.636, you_rate:0.000->0.091
     L: anyway the 4:40 died at the bridge again and we're packed in like pic...
     R: you wanna walk from there or wait for the next one?
[3] hold  blend=0.290  reg=0.286  fw=0.160  char=0.373  d=1.444  gold=0
     drivers: words_per_unit:11.000->16.000, question_rate:0.091->0.000, informal_rate:0.091->0.000
     L: you wanna walk from there or wait for the next one?
     R: also I opened the dark honey and you have to taste this, it's all wet...
[4] SNAP  blend=0.442  reg=0.486  fw=0.148  char=0.415  d=2.600  gold=0  FALSE ALARM
     drivers: words_per_unit:16.000->7.000, mean_word_len:3.688->4.000, vocative_rate:0.000->0.143
     L: also I opened the dark honey and you have to taste this, it's all wet...
     R: don't finish the jar without me, ok?
```
