import pytest

from helpers import normalize_qu


def test_plain_word():
    assert list(normalize_qu("hello")) == ["h", "e", "l", "l", "o"]


def test_qu_at_start():
    assert list(normalize_qu("quiet")) == ["qu", "i", "e", "t"]


def test_qu_in_middle():
    assert list(normalize_qu("disqualify")) == [
        "d", "i", "s", "qu", "a", "l", "i", "f", "y",
    ]


def test_qu_at_end():
    assert list(normalize_qu("torqu")) == ["t", "o", "r", "qu"]


def test_q_without_u_raises():
    with pytest.raises(ValueError, match="Q.*without.*u"):
        list(normalize_qu("qi"))


def test_q_at_end_of_string_raises():
    with pytest.raises(ValueError, match="Q.*without.*u"):
        list(normalize_qu("abcq"))


def test_empty_string():
    assert list(normalize_qu("")) == []


def test_single_non_q_character():
    assert list(normalize_qu("a")) == ["a"]


def test_just_qu():
    assert list(normalize_qu("qu")) == ["qu"]
