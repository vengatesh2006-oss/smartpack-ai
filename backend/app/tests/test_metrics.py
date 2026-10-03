import pytest
from backend.app.services.metrics import safe_div, calculate_metrics_from_counts

def test_safe_div():
    assert safe_div(10, 2) == 5.0
    assert safe_div(10, 0) == 0.0

def test_calculate_metrics_from_counts_normal():
    metrics = calculate_metrics_from_counts(tp=10, tn=10, fp=5, fn=5, manual_reviews=2, total_scans=32)
    # accuracy = 20 / 30 = 66.67%
    assert metrics["accuracy"] == 66.67
    # precision = 10 / 15 = 66.67%
    assert metrics["precision"] == 66.67
    # recall = 10 / 15 = 66.67%
    assert metrics["recall"] == 66.67
    # fp_rate = 5 / 15 = 33.33%
    assert metrics["false_positive_rate"] == 33.33

def test_calculate_metrics_from_counts_zeros():
    metrics = calculate_metrics_from_counts(tp=0, tn=0, fp=0, fn=0, manual_reviews=0, total_scans=0)
    assert metrics["accuracy"] == 0.0
    assert metrics["precision"] == 0.0
    assert metrics["recall"] == 0.0
    assert metrics["f1_score"] == 0.0
    assert metrics["false_positive_rate"] == 0.0
    assert metrics["manual_review_rate"] == 0.0
