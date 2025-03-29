#!/usr/bin/python
from collections import Counter

# Boggle dice configuration
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
    # Count characters in the word
    word_count = Counter(word)
    
    # Function to check if we can use the Boggle dice to form the word
    def backtrack(index, used):
        if index == len(word):
            return True
        char = word[index]
        
        # Iterate over each die face
        for i in range(len(boggle_dice)):
            if i not in used and (char in dice_faces[i] or (char == 'Q' and qu_face <= dice_faces[i])):
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
