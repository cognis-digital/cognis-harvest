"""Evaluation metrics (stdlib only)."""

from __future__ import annotations


def prf(pred_set, truth_set) -> dict:
    pred, truth = set(pred_set), set(truth_set)
    tp = len(pred & truth)
    fp = len(pred - truth)
    fn = len(truth - pred)
    p = tp / (tp + fp) if (tp + fp) else 1.0
    r = tp / (tp + fn) if (tp + fn) else 1.0
    f = (2 * p * r / (p + r)) if (p + r) else 0.0
    return {"precision": round(p, 4), "recall": round(r, 4), "f1": round(f, 4),
            "tp": tp, "fp": fp, "fn": fn}


def classification_metrics(pred: dict, truth: dict, classes) -> dict:
    total = len(truth)
    correct = sum(1 for k in truth if pred.get(k) == truth[k])
    per = {}
    for c in classes:
        tp = sum(1 for k in truth if truth[k] == c and pred.get(k) == c)
        fp = sum(1 for k in truth if truth[k] != c and pred.get(k) == c)
        fn = sum(1 for k in truth if truth[k] == c and pred.get(k) != c)
        p = tp / (tp + fp) if (tp + fp) else 1.0
        r = tp / (tp + fn) if (tp + fn) else 1.0
        f = (2 * p * r / (p + r)) if (p + r) else 0.0
        per[c] = {"precision": round(p, 4), "recall": round(r, 4), "f1": round(f, 4)}
    return {"overall_accuracy": round(correct / total, 4) if total else 0.0, "per_class": per}


def confusion_matrix(pred: dict, truth: dict, classes) -> dict:
    m = {a: {b: 0 for b in classes} for a in classes}
    for k, t in truth.items():
        p = pred.get(k, t)
        if t in m and p in m[t]:
            m[t][p] += 1
    return m


def macro_f1(pred: dict, truth: dict, classes) -> float:
    per = classification_metrics(pred, truth, classes)["per_class"]
    f1s = [per[c]["f1"] for c in classes]
    return round(sum(f1s) / len(f1s), 4) if f1s else 0.0


def area_mape(pred_counts: dict, true_counts: dict, crop_classes, pixel_area_ha: float) -> float:
    errs = []
    for c in crop_classes:
        t = true_counts.get(c, 0) * pixel_area_ha
        p = pred_counts.get(c, 0) * pixel_area_ha
        if t > 0:
            errs.append(abs(p - t) / t)
    return round(sum(errs) / len(errs), 4) if errs else 0.0
