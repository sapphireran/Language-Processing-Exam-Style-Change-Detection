# Topic is not style

The easy PAN split is a compliment I do not want. If paragraph 1 is
about world news and paragraph 2 is about legal advice, a bag of
content words will scream `CHANGE` and I will look clever for the
wrong reason.

Style-change is only interesting when the topic is *not* allowed to
do the work. That is why the hard split exists, and why I wrote a
**trap** band: one house, three subjects.

## The trap files

- `problem-19-press-three-topics` — ink, rent, bicycle, all in the
  compositor's clauses
- `problem-20-notice-three-topics` — dogs, bins, scaffolding, all in
  shall-speak
- `problem-21-chat-three-topics` — lunch, a board game, a dripping tap

A content model should light those hinges up. Quoin should not, or
should light them more dimly than a press-to-notice hinge. The lab
`07_topic_confound.py` prints both views: character 3-gram distance
(which still leaks some topic) versus function-word L1 (which should
stay small) versus the blended Quoin score.

## Gift authorship is the other topic lesson

`problem-24-gift-abstract` plants one paragraph that sounds like a
paper abstract in the middle of exam notes. The *topic* is still
style-change detection. The *house* is not. If I only measured nouns
(`compression`, `F1`, `paragraph`) I would miss the gift. If I measure
`we present` / even sentence length / zero hedging, I should catch it.

## What I will say about transformers

A pretrained encoder has seen more topic than I can list. Fine-tuning
on easy data will teach it to be a topic detector unless the training
split punishes that. I would still use one for a real submission. I
would also hold out a same-topic slice and refuse to quote an easy
score as the headline.
