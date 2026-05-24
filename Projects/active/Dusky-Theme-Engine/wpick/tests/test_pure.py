from __future__ import annotations

import pytest

from wpick.assigner import _cosine_similarity


def test_cosine_similarity_identical() -> None:
    v = [0.5, 0.5, 0.5]
    assert _cosine_similarity(v, v) == pytest.approx(1.0)


def test_cosine_similarity_orthogonal() -> None:
    sim = _cosine_similarity([1.0, 0.0], [0.0, 1.0])
    assert sim == pytest.approx(0.0)


def test_cosine_similarity_zero_vector() -> None:
    assert _cosine_similarity([0.0, 0.0], [1.0, 0.0]) == pytest.approx(0.0)
    assert _cosine_similarity([0.0, 0.0], [0.0, 0.0]) == pytest.approx(0.0)
