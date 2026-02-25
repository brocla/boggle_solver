import pytest
import importlib

# is-boggleable.py has a hyphen, so we need importlib
is_boggleable = importlib.import_module("is-boggleable")
can_form_word = is_boggleable.can_form_word
boggle_dice = is_boggleable.boggle_dice
dice_faces = is_boggleable.dice_faces


# --- Module-level constants ---

def test_boggle_dice_has_16_dice():
    assert len(boggle_dice) == 16


def test_each_die_has_6_faces():
    for die in boggle_dice:
        assert len(die) == 6


def test_dice_faces_matches_boggle_dice():
    for i, die in enumerate(boggle_dice):
        assert dice_faces[i] == set(die.lower())


# --- Words that CAN be formed (from expected output in the file) ---

@pytest.mark.parametrize("word", [
    "sweater",
    "parallel",
    "assessment",
    "inaccessibility",
    "Jinx",
    "quiet",
    "Quintessential",
    "Quarantineable",


])
def test_formable_words(word):
    assert can_form_word(word) is True


# --- Words that CANNOT be formed (from expected output in the file) ---

@pytest.mark.parametrize("word", [
    "bookkeeper",
    "successful",
    "quiZZical",
])
def test_unformable_words(word):
    assert can_form_word(word) is False


# --- Edge cases ---

def test_empty_word():
    assert can_form_word("") is True


def test_single_letter():
    # 'a' appears on the AEANEG die
    assert can_form_word("a") is True


def test_letter_not_on_any_die():
    # 'z' only appears on LNHNRZ; one 'z' should work
    assert can_form_word("z") is True


def test_repeated_letter_exceeds_available_dice():
    # 'z' appears on only one die, so 'zz' can't be formed
    assert can_form_word("zz") is False


def test_word_using_all_16_dice():
    # Pick one letter from each die to form a 16-char "word"
    # AEANEG->a, WNGEEH->w, AHSPCO->h, LNHNRZ->n,
    # ASPFFK->f, TSTIYD->t, OBJOAB->b, OWTOAT->o,
    # IOTMUC->m, ERTTYL->y, RYVDEL->v, TOESSI->s,
    # LREIXD->x, TERWHV->r, EIUNES->u, NUIHMQ->q
    word = "awhnftbomyvsxruq"
    assert can_form_word(word) is True


# --- Backtracking behavior ---

def test_backtracking_finds_alternate_die_assignment():
    # 'e' appears on multiple dice (AEANEG, WNGEEH, EIUNES, ERTTYL, etc.)
    # A word with multiple e's requires backtracking to assign different dice
    assert can_form_word("eee") is True


def test_backtracking_fails_when_dice_exhausted():
    # 'e' appears on 8 dice, so 9 e's should fail
    assert can_form_word("eeeeeeeee") is False


# --- Qu handling (possible dormant bug) ---

def test_qu_word_lowercase():
    # "quiet" is lowercase — the Qu special-case path (char == 'Q') on line 50
    # only triggers for uppercase 'Q', while dice_faces are lowercase.
    # If the Qu code path is dead, this still passes because 'q' matches
    # the NUIHMQ die (lowercased to {'n','u','i','h','m','q'}) as a normal letter.
    # This test documents that "quiet" works, but does NOT prove the Qu path fires.
    assert can_form_word("quiet") is True


def test_uppercase_words_are_normalized():
    # With word.lower() on entry, uppercase input now works correctly.
    # The Qu special case (char == 'Q', qu_face) is STILL dead code:
    # since the word is lowercased first, char is never uppercase 'Q'.
    # The word matches purely through normal lowercase letter matching.
    assert can_form_word("QUIET") is True
    assert can_form_word("JINX") is True
