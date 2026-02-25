#!/usr/bin/python
"""
Check if a word can be formed using the letters on a Boggle board.
## Usage: is-boggleable.py [WORD]...
# Example:
    `python is-boggleable.py sweater bookkeeper successful parallel assessment inaccessibility jinx
"""
from collections import Counter

# Boggle dice configuration.
# Each list item represents a six-sided die from the Boggle game. 
boggle_dice = [
    "AEANEG", "WNGEEH", "AHSPCO", "LNHNRZ",
    "ASPFFK", "TSTIYD", "OBJOAB", "OWTOAT",
    "IOTMUC", "ERTTYL", "RYVDEL", "TOESSI",
    "LREIXD", "TERWHV", "EIUNES", "NUIHMQ"
]

# Convert each die face into a set of characters
dice_faces = [set(die.lower()) for die in boggle_dice]

# Special case for the "Qu" die face
qu_face = {'Q', 'U'}

def can_form_word(word):
    """Return True if the word can be spelled using the 16 Boggle dice.

    Each die may only be used once. This is a constraint-satisfaction problem:
    assign one die to each letter such that no die is reused. A backtracking
    search tries each available die for the current letter, recurses on the
    rest of the word, and undoes the choice if it leads to a dead end.
    """
    word = word.lower()

    def backtrack(index, used):
        """Recursively assign dice to letters starting at index.

        Backtracking works by making a tentative choice (marking a die as
        used), then exploring whether the remaining letters can be satisfied.
        If they can't, the choice is undone (the die is removed from 'used')
        and the next candidate die is tried. This exhaustive search guarantees
        a solution is found if one exists.
        """
        if index == len(word):
            return True
        char = word[index]
        
        # Iterate over each die face
        for i, face in enumerate(dice_faces):
            if i not in used and (char in face or (char == 'Q' and qu_face <= face)):
                # Use this die face
                used.add(i)
                if backtrack(index + 1, used):
                    return True
                # Backtrack
                used.remove(i)
        
        return False
    
    # Start backtracking from the first character of the word
    return backtrack(0, set())


if __name__ == "__main__":

    # Example usage:
    words_to_check = ["sweater", "bookkeeper", "successful", "parallel", "assessment", "inaccessibility", "jinx"]
        
    for word in words_to_check:
        if can_form_word(word):
            print(f"Word '{word}' can be formed.")
        else:
            print(f"Word '{word}' cannot be formed.")


    # Word 'sweater' can be formed.
    # Word 'bookkeeper' cannot be formed.
    # Word 'successful' cannot be formed.
    # Word 'parallel' can be formed.
    # Word 'assessment' can be formed.
    # Word 'inaccessibility' can be formed.
    # Word 'jinx' can be formed.