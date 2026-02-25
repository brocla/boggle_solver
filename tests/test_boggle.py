import pytest
from boggle import Boggle, CUBES


# --- Boggle.__init__ ---


def test_board_size_too_small():
    with pytest.raises(ValueError, match="too small"):
        Boggle(size=1, letters="a")


def test_default_board_is_4x4():
    game = Boggle(letters="abcdefghijklmnop")
    assert game.size == 4
    assert len(game.board) == 4
    assert all(len(row) == 4 for row in game.board)


def test_custom_board_size():
    game = Boggle(size=2, letters="abcd")
    assert game.size == 2
    assert len(game.board) == 2
    assert all(len(row) == 2 for row in game.board)


def test_random_board_when_no_letters():
    game = Boggle(size=4)
    assert len(game.board) == 4
    assert all(len(row) == 4 for row in game.board)


# --- Boggle.load ---


def test_load_lowercases_letters():
    game = Boggle(letters="ABCDEFGHIJKLMNOP")
    flat = [ch for row in game.board for ch in row]
    assert flat == list("abcdefghijklmnop")


def test_load_strips_non_alpha():
    game = Boggle(letters="a1b2c3d4e5f6g7h8i9j0k!l@m#n$o%p^")
    flat = [ch for row in game.board for ch in row]
    assert flat == list("abcdefghijklmnop")


def test_load_handles_qu_as_single_letter():
    game = Boggle(letters="abcdefghijklmnoqu")
    flat = [ch for row in game.board for ch in row]
    assert "qu" in flat
    assert len(flat) == 16


def test_load_rejects_q_without_u():
    with pytest.raises(ValueError, match="Q.*without.*u"):
        Boggle(letters="abcdefghijklmnoq")


def test_load_wrong_letter_count():
    with pytest.raises(ValueError, match="cannot be formatted"):
        Boggle(letters="abc")


# --- Boggle.form_board ---


def test_form_board_creates_square_matrix():
    game = Boggle(letters="abcdefghijklmnop")
    assert game.board == [
        ["a", "b", "c", "d"],
        ["e", "f", "g", "h"],
        ["i", "j", "k", "l"],
        ["m", "n", "o", "p"],
    ]


# --- Boggle.visited ---


def test_visited_board_initialized_to_false():
    game = Boggle(letters="abcdefghijklmnop")
    for row in game.visited:
        for cell in row:
            assert cell is False


# --- Boggle.find_words ---


def test_find_words_returns_set():
    game = Boggle(letters="abcdefghijklmnop")
    result = game.find_words()
    assert isinstance(result, set)


def test_find_words_only_returns_words_longer_than_2():
    game = Boggle(letters="abcdefghijklmnop")
    result = game.find_words()
    for word in result:
        assert len(word) > 2


def test_find_words_with_known_board():
    # "toessinelreixdly" spells out a board that should contain common words
    # Using letters from: t o e s / s i n e / l r e i / x d l y
    game = Boggle(letters="toessinelreixdly")
    result = game.find_words()
    # These words should be findable via adjacent paths on this board
    # "toes" = t(0,0)->o(0,1)->e(0,2)->s(0,3)
    # "sine" = s(1,0)->i(1,1)->n(1,2)->e(1,3)
    # "rein" = r(2,1)->e(2,2)->i(2,3)->n(1,2)
    assert "toes" in result
    assert "sine" in result
    assert "rein" in result


def test_find_words_with_letter_not_in_trie():
    # If the dictionary doesn't contain any words starting with a letter
    # on the board, find_words raises KeyError because it does
    # candidates[first_letter] without checking membership first.
    from trie import Trie
    game = Boggle(size=2, letters="xxxx")
    game.dictionary = Trie()  # empty trie — no letters at all
    game.dictionary.insert("hello")  # only 'h' in root children
    result = game.find_words()  # KeyError: 'x' not in root.children
    assert isinstance(result, set)


def test_find_words_does_not_reuse_same_cell():
    # On a 2x2 board "eses", the path can't reuse a cell
    game = Boggle(size=2, letters="eses")
    result = game.find_words()
    # No word should use the same position twice
    # (tested indirectly: visited logic prevents it)
    for word in result:
        assert len(word) <= 4  # max cells on 2x2


# --- Boggle.display_board ---


def test_display_board(capsys):
    game = Boggle(letters="abcdefghijklmnop")
    game.display_board()
    output = capsys.readouterr().out
    assert "a b c d" in output
    assert "m n o p" in output


# --- Boggle.generate_random_boggle_letters ---


def test_random_letters_come_from_cubes():
    game = Boggle(size=4)
    flat = [ch for row in game.board for ch in row]
    # Each letter should be a lowercase version of a face from CUBES
    all_faces = set()
    for cube in CUBES:
        for face in cube:
            all_faces.add(face.lower())
    for letter in flat:
        assert letter in all_faces


