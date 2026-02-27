import pytest

from is_boggleable import can_form_word, boggle_dice, dice_faces


# --- Module-level constants ---

def test_boggle_dice_has_16_dice():
    assert len(boggle_dice) == 16


def test_each_die_has_6_faces():
    for die in boggle_dice:
        assert len(die) == 6


def test_dice_faces_matches_boggle_dice():
    for i, die in enumerate(boggle_dice):
        assert dice_faces[i] == {face.lower() for face in die}


def test_last_die_has_qu_as_single_face():
    # The last die models "Qu" as one face, matching real Boggle
    last_faces = dice_faces[-1]
    assert "qu" in last_faces
    assert "q" not in last_faces


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
    "ubiquitous",
    "unpicturesque",
    "battleworthiness",
    "electrochemistry",
    "faintheartedness",
    "imperceptibility",
])
def test_formable_words(word):
    assert can_form_word(word) is True


# --- Words that CANNOT be formed (from expected output in the file) ---

@pytest.mark.parametrize("word", [
    "bookkeeper",
    "successful",
    "quiZZical",
    "strengthlessness",
    "baby",
    "babble",
    "fork",
    "Knife",
    "job",
    "banjo",
    "fake",
    "Pineapple",
    "QUATTUORDECILLION ",
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
    # LREIXD->x, TERWHV->r, EIUNES->u, (N,U,I,H,M,Qu)->qu
    # Note: "qu" from the last die counts as one face but two letters
    word = "awhnftbomyvsxruqu"
    assert can_form_word(word) is True


# --- Backtracking behavior ---

def test_backtracking_finds_alternate_die_assignment():
    # 'e' appears on multiple dice (AEANEG, WNGEEH, EIUNES, ERTTYL, etc.)
    # A word with multiple e's requires backtracking to assign different dice
    assert can_form_word("eee") is True


def test_backtracking_fails_when_dice_exhausted():
    # 'e' appears on 8 dice, so 9 e's should fail
    assert can_form_word("eeeeeeeee") is False


# --- Qu handling ---

def test_qu_uses_one_die():
    # "quiet" uses the Qu die for 'qu', then separate dice for i, e, t.
    # That's 4 dice total, not 5.
    assert can_form_word("quiet") is True


def test_qu_word_uppercase():
    assert can_form_word("QUIET") is True
    assert can_form_word("JINX") is True


def test_q_without_u_returns_false():
    # Words with Q not followed by U are rejected (normalize_qu raises ValueError)
    assert can_form_word("qi") is False


def test_qu_frees_u_die_for_other_letters():
    # Since "qu" is one face on one die, the 'u' on the EIUNES die
    # and the 'u' on the Qu die itself are still available for other letters.
    # "quorum" = qu(Qu die) + o + r + u(separate die) + m
    assert can_form_word("quorum") is True
