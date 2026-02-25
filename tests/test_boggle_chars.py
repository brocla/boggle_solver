import pytest

from boggle_chars import boggle_chars


def test_plain_word():
    assert list(boggle_chars("hello")) == ["h", "e", "l", "l", "o"]


def test_qu_at_start():
    assert list(boggle_chars("quiet")) == ["qu", "i", "e", "t"]


def test_qu_in_middle():
    assert list(boggle_chars("disqualify")) == [
        "d", "i", "s", "qu", "a", "l", "i", "f", "y",
    ]


def test_qu_at_end():
    assert list(boggle_chars("torqu")) == ["t", "o", "r", "qu"]


def test_q_without_u_raises():
    with pytest.raises(ValueError, match="Q.*without.*u"):
        list(boggle_chars("qi"))


def test_q_at_end_of_string_raises():
    with pytest.raises(ValueError, match="Q.*without.*u"):
        list(boggle_chars("abcq"))


def test_empty_string():
    assert list(boggle_chars("")) == []


def test_single_non_q_character():
    assert list(boggle_chars("a")) == ["a"]


def test_just_qu():
    assert list(boggle_chars("qu")) == ["qu"]
