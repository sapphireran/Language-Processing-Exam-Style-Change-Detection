# Topic is not style

The oldest false friend in this exam.

`problem-19-stall-three-topics` talks about dumpling skins, a night
bus, and a cat on a kiln roof. Gold is five zeros. The stall voice
keeps *I* and a contraction in every line. The default detector stays
quiet.

`problem-20-notice-three-topics` does the same trick with ice
thickness, a kiln lock, and a seed lot, all in *shall* / *must*.
Also quiet.

`problem-21-chat-three-topics` is the control that **fails**. Short
wire units (`yeah`, `lol`, `btw`) jerk the leftover channels. The
named error is `chat_jitter`. If you are asked for a limitation, this
is a better sentence than "we need more data."

## Why character n-grams fail the control

A character 3-gram bag on six lines is mostly content (`kil`, `bus`,
`cat`). Cosine distance lights up at every topic join. That is why
the default blend gives char-3 weight **zero** and still shows the
number in `inkfold explain`, so you can watch the leak.

## A content model is not a style model

If a question offers you TF-IDF on content words as a style-change
feature, the answer is: that system is a topic-change detector and
will fire on problem-19. Closed class first. Content only as a
diagnostic.

## Hard pairs are the other side of the same coin

Two organ tuners on one mixture share topic *and* register. Gold
says two authors. We miss. Topic-matching does not save you, and
register-matching is the miss. You cannot have "topic is not style"
and "same-register pairs are easy" in the same paragraph.
