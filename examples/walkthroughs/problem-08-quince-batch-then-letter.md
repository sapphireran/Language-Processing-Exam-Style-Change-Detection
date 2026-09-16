# Walkthrough: `problem-08-quince-batch-then-letter`

Split: **medium**. Same quince paste. Marble batch sheet, then a Hearth parcel letter.

```
units=6 hinges=5 detector=threshold cut=0.300
pred=[0, 0, 1, 0, 0]
gold=[0, 0, 1, 0, 0]
accuracy=1.000 macro-F1=1.000 change-F1=1.000 (tp=1 fp=0 fn=0 tn=4)
cusum peak hinge=1

[0] hold  blend=0.263  reg=0.287  fw=0.080  char=0.438  d=0.409  gold=0
     drivers: mean_word_len:3.615->6.250, words_per_unit:13.000->12.000, fw_ratio:0.077->0.250
     L: Batch Q-19: quince paste, 14 kg fruit; sugar 11.2 kg; lemon 180 ml; s...
     R: Pans were lined with silicone; cooling racks numbered 4 through 9; re...
[1] hold  blend=0.171  reg=0.176  fw=0.098  char=0.426  d=0.063  gold=0
     drivers: mean_word_len:6.250->4.083, fw_ratio:0.250->0.167, passive_rate:0.083->0.000
     L: Pans were lined with silicone; cooling racks numbered 4 through 9; re...
     R: Cut size 40 mm squares; wrap in greaseproof; shelf life 90 days at 16 C.
[2] SNAP  blend=0.365  reg=0.385  fw=0.154  char=0.380  d=2.113  gold=1
     drivers: words_per_unit:12.000->18.000, fw_ratio:0.167->0.500, semi_rate:0.167->0.000
     L: Cut size 40 mm squares; wrap in greaseproof; shelf life 90 days at 16 C.
     R: Dearest Tomas, the quince finally set, and I have wrapped a square fo...
[3] hold  blend=0.215  reg=0.207  fw=0.166  char=0.348  d=0.444  gold=0
     drivers: words_per_unit:18.000->17.000, mean_word_len:4.056->3.588, fw_ratio:0.500->0.588
     L: Dearest Tomas, the quince finally set, and I have wrapped a square fo...
     R: You must eat it with the hard cheese I sent, and do write if it trave...
[4] hold  blend=0.280  reg=0.264  fw=0.190  char=0.394  d=1.488  gold=0
     drivers: words_per_unit:17.000->13.000, mean_word_len:3.588->4.385, fw_ratio:0.588->0.462
     L: You must eat it with the hard cheese I sent, and do write if it trave...
     R: I remain your stubborn aunt, quite proud of the amber colour this year!
```
