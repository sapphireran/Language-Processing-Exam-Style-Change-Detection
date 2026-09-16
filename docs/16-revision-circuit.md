# Revision circuit

A single pass I can run the night before.

1. Read the [cheatsheet](cheatsheet.md) out loud. If a line
   surprises me, open the note it points at.
2. Inspect document 16 (hard, same well) and document 20 (trap).
   ```
   PYTHONPATH=src:. python3 -m kerf inspect \
     examples/corpus/problem-16-stilling-caliper-then-seminar.txt
   PYTHONPATH=src:. python3 -m kerf inspect \
     examples/corpus/problem-20-caliper-well-then-caliper-booth.txt
   ```
3. Score the bank. Confirm never-fire accuracy is still the liar
   and that the live miss is still document 27's last hinge.
   ```
   PYTHONPATH=src:. python3 -m kerf score examples/corpus
   ```
4. Walk [oral cards](10-oral-cards.md) without the file. Then
   check.
5. Write one model answer from [11](11-written-model-answers.md)
   on paper. Time: fifteen minutes. If I need the repo, I do not
   know it.
6. Run the labs, not because the exam will ask for a CLI, but
   because a number I have seen is a number I can defend.
   ```
   PYTHONPATH=src:. python3 examples/labs/run_all.py
   ```

If I have another hour I rewrite the split-score formula from
memory and invent a four-paragraph ABA on a new topic (not one
from the bank) and mark it by hand before I run kerf.
