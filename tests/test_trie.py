import os
import tempfile

import pytest

from trie import Trie, TrieNode


# --- TrieNode ---

def test_trienode_initial_state():
    node = TrieNode()
    assert node.children == {}
    assert node.is_end_of_word is False


# --- Trie bool ---

def test_empty_trie_is_falsy():
    assert not Trie()


def test_nonempty_trie_is_truthy():
    trie = Trie()
    trie.insert("a")
    assert trie


# --- Insert and Search ---

@pytest.fixture
def trie():
    return Trie()


def test_insert_and_find_single_word(trie):
    trie.insert("hello")
    assert trie.search("hello") is True


def test_search_missing_word(trie):
    trie.insert("hello")
    assert trie.search("world") is False


def test_prefix_is_not_a_word(trie):
    trie.insert("hello")
    assert trie.search("hel") is False


def test_word_is_not_found_as_longer_string(trie):
    trie.insert("hi")
    assert trie.search("hint") is False


@pytest.mark.parametrize("word", ["hello", "world", "hi", "her", "hero"])
def test_insert_multiple_words(trie, word):
    trie.insert_words(["hello", "world", "hi", "her", "hero"])
    assert trie.search(word) is True


def test_overlapping_words(trie):
    trie.insert_words(["her", "hero", "heros"])
    assert trie.search("her") is True
    assert trie.search("hero") is True
    assert trie.search("heros") is True
    assert trie.search("he") is False


def test_single_character_word(trie):
    trie.insert("a")
    assert trie.search("a") is True
    assert trie.search("b") is False


# --- Qu handling ---

def test_qu_word_is_found(trie):
    trie.insert("quiet")
    assert trie.search("quiet") is True


def test_qu_stored_as_single_node(trie):
    trie.insert("quiet")
    assert "qu" in trie.root.children
    assert "q" not in trie.root.children


def test_qu_in_middle_of_word(trie):
    trie.insert("disqualify")
    assert trie.search("disqualify") is True


def test_q_not_followed_by_u_is_excluded(trie):
    trie.insert("qi")
    # search() returns None for Q-without-U words (bare return)
    assert not trie.search("qi")


def test_rejected_q_word_leaves_no_orphan_nodes(trie):
    # BUG: insert("qi") creates a 'qu' node in root.children before
    # discovering that 'i' follows instead of 'u'. `del current_node`
    # only deletes the local variable — the orphaned 'qu' node remains
    # in the trie. A correct fix should leave the trie completely empty.
    trie.insert("qi")
    assert trie.root.children == {}, (
        "Inserting a rejected Q-without-U word should not leave orphan nodes"
    )


def test_q_at_end_of_word_is_stored_as_qu(trie):
    trie.insert("suq")
    # When Q is the last letter, it's stored as a 'qu' node (s -> u -> qu)
    # The Q-without-U rejection only fires when the *next* char isn't 'u'
    assert "qu" in trie.root.children["s"].children["u"].children


@pytest.mark.parametrize("word", ["quiet", "queen", "quiz", "quote"])
def test_multiple_qu_words(trie, word):
    trie.insert_words(["quiet", "queen", "quiz", "quote"])
    assert trie.search(word) is True


# --- Display ---

def test_display_outputs_words(trie, capsys):
    trie.insert_words(["hi", "he"])
    trie.display()
    output = capsys.readouterr().out.strip().split("\n")
    assert sorted(output) == ["he", "hi"]


# --- Serialization ---

def test_save_and_load_preserves_words(trie, tmp_path):
    words = ["hello", "world", "quiet", "disqualify"]
    trie.insert_words(words)
    pkl = tmp_path / "trie.pkl"

    trie.save_to_file(str(pkl))
    loaded = Trie.load_from_file(str(pkl))

    for word in words:
        assert loaded.search(word) is True, f"'{word}' should survive serialization"
    assert loaded.search("missing") is False


def test_empty_trie_serialization(trie, tmp_path):
    pkl = tmp_path / "trie.pkl"
    trie.save_to_file(str(pkl))
    loaded = Trie.load_from_file(str(pkl))
    assert not loaded
