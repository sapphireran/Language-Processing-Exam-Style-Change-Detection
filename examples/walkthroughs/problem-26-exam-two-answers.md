# Walkthrough: `problem-26-exam-two-answers`

Split: **paste**. Two exam answers on the same CUSUM question glued together. A paste, not a collaboration.

```
units=6 hinges=5 detector=threshold cut=0.300
pred=[0, 0, 0, 0, 0]
gold=[0, 0, 1, 0, 0]
accuracy=0.800 macro-F1=0.444 change-F1=0.000 (tp=0 fp=0 fn=1 tn=4)
cusum peak hinge=2

[0] hold  blend=0.224  reg=0.194  fw=0.228  char=0.388  d=0.677  gold=0
     drivers: words_per_unit:23.000->21.000, mean_word_len:3.696->4.238, fw_ratio:0.391->0.619
     L: A CUSUM plot adds each new score minus the running mean, so a new wri...
     R: I would still not trust it on a six-sentence document because the mea...
[1] hold  blend=0.223  reg=0.177  fw=0.203  char=0.385  d=1.989  gold=0
     drivers: words_per_unit:21.000->14.000, mean_word_len:4.238->4.000, upper_ratio:0.011->0.107
     L: I would still not trust it on a six-sentence document because the mea...
     R: I would rather treat CUSUM as a picture and cut with a pairwise score.
[2] hold  blend=0.262  reg=0.235  fw=0.241  char=0.350  d=1.257  gold=1  MISS
     drivers: words_per_unit:14.000->18.000, mean_word_len:4.000->5.111, passive_rate:0.000->0.111
     L: I would rather treat CUSUM as a picture and cut with a pairwise score.
     R: It should be noted, however, that CUSUM remains attractive when docum...
[3] hold  blend=0.182  reg=0.155  fw=0.196  char=0.344  d=0.432  gold=0
     drivers: words_per_unit:18.000->19.000, mean_word_len:5.111->5.684, passive_rate:0.111->0.000
     L: It should be noted, however, that CUSUM remains attractive when docum...
     R: A slope change may therefore be reported as supporting evidence, whil...
[4] hold  blend=0.167  reg=0.136  fw=0.133  char=0.334  d=0.889  gold=0
     drivers: words_per_unit:19.000->16.000, mean_word_len:5.684->5.188, hedge_rate:0.053->0.125
     L: A slope change may therefore be reported as supporting evidence, whil...
     R: Accordingly the present answer prefers CUSUM as a diagnostic rather t...
```
