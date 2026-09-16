"""Macro-F1 evaluation over paragraph-boundary labels."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class BinaryCounts:
    tp: int
    fp: int
    tn: int
    fn: int

    @property
    def support(self) -> int:
        return self.tp + self.fp + self.tn + self.fn


def confusion(gold: list[int], pred: list[int]) -> BinaryCounts:
    if len(gold) != len(pred):
        raise ValueError(f"length mismatch: gold={len(gold)} pred={len(pred)}")
    tp = fp = tn = fn = 0
    for y, yhat in zip(gold, pred, strict=True):
        if y not in (0, 1) or yhat not in (0, 1):
            raise ValueError("labels must be 0 or 1")
        if y == 1 and yhat == 1:
            tp += 1
        elif y == 0 and yhat == 1:
            fp += 1
        elif y == 0 and yhat == 0:
            tn += 1
        else:
            fn += 1
    return BinaryCounts(tp=tp, fp=fp, tn=tn, fn=fn)


def _safe_div(num: float, den: float) -> float:
    return 0.0 if den == 0.0 else num / den


def precision_recall_f1(counts: BinaryCounts, positive: int) -> tuple[float, float, float]:
    if positive == 1:
        prec = _safe_div(counts.tp, counts.tp + counts.fp)
        rec = _safe_div(counts.tp, counts.tp + counts.fn)
    else:
        prec = _safe_div(counts.tn, counts.tn + counts.fn)
        rec = _safe_div(counts.tn, counts.tn + counts.fp)
    f1 = _safe_div(2 * prec * rec, prec + rec)
    return prec, rec, f1


def macro_f1(gold: list[int], pred: list[int]) -> float:
    counts = confusion(gold, pred)
    if counts.support == 0:
        return 1.0
    f1_neg = precision_recall_f1(counts, 0)[2]
    f1_pos = precision_recall_f1(counts, 1)[2]
    return (f1_neg + f1_pos) / 2.0


@dataclass(frozen=True)
class DocumentScore:
    problem_id: str
    gold: list[int]
    pred: list[int]
    macro_f1: float
    counts: BinaryCounts


@dataclass(frozen=True)
class EvaluationResult:
    documents: list[DocumentScore]

    @property
    def mean_macro_f1(self) -> float:
        if not self.documents:
            return 0.0
        return sum(doc.macro_f1 for doc in self.documents) / len(self.documents)

    @property
    def pooled(self) -> BinaryCounts:
        tp = sum(doc.counts.tp for doc in self.documents)
        fp = sum(doc.counts.fp for doc in self.documents)
        tn = sum(doc.counts.tn for doc in self.documents)
        fn = sum(doc.counts.fn for doc in self.documents)
        return BinaryCounts(tp=tp, fp=fp, tn=tn, fn=fn)

    @property
    def pooled_macro_f1(self) -> float:
        gold = [label for doc in self.documents for label in doc.gold]
        pred = [label for doc in self.documents for label in doc.pred]
        return macro_f1(gold, pred)


def evaluate_changes(
    gold_by_id: dict[str, list[int]],
    pred_by_id: dict[str, list[int]],
) -> EvaluationResult:
    missing = sorted(set(gold_by_id) - set(pred_by_id))
    extra = sorted(set(pred_by_id) - set(gold_by_id))
    if missing:
        raise ValueError(f"missing predictions for: {', '.join(missing)}")
    if extra:
        raise ValueError(f"predictions without gold: {', '.join(extra)}")
    documents = []
    for problem_id in sorted(gold_by_id):
        gold = gold_by_id[problem_id]
        pred = pred_by_id[problem_id]
        documents.append(
            DocumentScore(
                problem_id=problem_id,
                gold=gold,
                pred=pred,
                macro_f1=macro_f1(gold, pred),
                counts=confusion(gold, pred),
            )
        )
    return EvaluationResult(documents=documents)
