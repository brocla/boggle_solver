#!/usr/bin/python
"""
Check if a word can be formed using the letters on a Boggle board.
"""

import click
from helpers import normalize_qu, boggle_dice

# Convert each die into a set of faces (lowercased).
# String dice become single-char sets; the tuple die preserves "qu" as one face.
dice_faces = [{face.lower() for face in die} for die in boggle_dice]


def can_form_word(word):
    """Return True if the word can be spelled using the 16 Boggle dice.

    Each die may only be used once. This is a constraint-satisfaction problem:
    assign one die to each letter such that no die is reused. A backtracking
    search tries each available die for the current letter, recurses on the
    rest of the word, and undoes the choice if it leads to a dead end.
    """
    try:
        chars = list(normalize_qu(word.lower()))
    except ValueError:
        return False

    def backtrack(index, used):
        """Recursively assign dice to letters starting at index.

        Backtracking works by making a tentative choice (marking a die as
        used), then exploring whether the remaining letters can be satisfied.
        If they can't, the choice is undone (the die is removed from 'used')
        and the next candidate die is tried. This exhaustive search guarantees
        a solution is found if one exists.
        """
        if index == len(chars):
            return True
        char = chars[index]

        # Iterate over each die face
        for i, face in enumerate(dice_faces):
            if i not in used and char in face:
                # Use this die face
                used.add(i)
                if backtrack(index + 1, used):
                    return True
                # Backtrack
                used.remove(i)

        return False

    # Start backtracking from the first character of the word
    return backtrack(0, set())


@click.command()
@click.argument("word")
def cli(word):
    """Check if a word can be formed using the 16 Boggle dice."""
    click.echo(can_form_word(word))


if __name__ == "__main__":
    cli()
