"""
This file defines a Trie data structure optimized for Boggle.

Provides insertion, search, serialization via pickle, and display of stored words.
Words containing 'Q' not followed by 'U' are excluded during insertion.

A 'Trie' is a data structure where each node represents a letter and 
paths from root to leaf spell out words.

A Trie is efficient for Boggle because it prunes entire branches of invalid prefixes at once,
rather than checking every word in the dictionary individually.
"""

import pickle
from helpers import normalize_qu
import os
from importlib import resources
from pathlib import Path


class TrieNode:
    """A single node in the trie, holding children and an end-of-word flag."""

    def __init__(self):
        self.children = {}
        self.is_end_of_word = False


class Trie:
    """A prefix tree that stores words using boggle-normalized characters."""

    def __init__(self):
        self.root = TrieNode()

    def __bool__(self):
        """Return True if the trie contains any words."""
        return bool(self.root.children)

    def _walk(self, word):
        """Walk the trie along the boggle-normalized chars of word.

        Returns the node at the end of the path, or None if any
        character is missing or the word has Q without U.
        """
        current_node = self.root
        for char in normalize_qu(word):
            if char not in current_node.children:
                return None
            current_node = current_node.children[char]
        return current_node

    def insert(self, word):
        """Add a word to the trie, silently skipping words with Q not followed by U."""
        try:
            chars = list(normalize_qu(word))
        except ValueError:
            return
        current_node = self.root
        for char in chars:
            if char not in current_node.children:
                current_node.children[char] = TrieNode()
            current_node = current_node.children[char]
        current_node.is_end_of_word = True

    def insert_words(self, words):
        """Insert each word from an iterable into the trie."""
        for word in words:
            self.insert(word)

    def search(self, word):
        """Return True if word is in the trie, False if not."""
        node = self._walk(word)
        if node is None:
            return False
        return node.is_end_of_word

    def words(self):
        """Yield all words stored in the trie."""

        def _collect(node, prefix):
            if node.is_end_of_word:
                yield prefix
            for char, child in node.children.items():
                yield from _collect(child, prefix + char)

        yield from _collect(self.root, "")

    def display(self):
        """Print all words in the trie, one per line."""
        print("\n".join(self.words()))

    def save_to_file(self, filename):
        """Serialize the trie to a pickle file."""
        with open(filename, "wb") as file:
            pickle.dump(self, file, protocol=-1)

    # @staticmethod
    # def load_from_file(filename):
    #     """Load and return a trie from a pickle file."""
    #     with open(filename, "rb") as file:
    #         return pickle.load(file)

    # @staticmethod
    # def load_from_file(filename=None):
    #     """Load and return a trie from a pickle file."""
    #     if filename is None:
    #         # Try to find trie.pkl in the package installation directory
    #         try:
    #             # For Python 3.9+
    #             if hasattr(resources, 'files'):
    #                 trie_path = resources.files('boggle').joinpath('trie.pkl')
    #                 with resources.as_file(trie_path) as file:
    #                     with open(file, "rb") as f:
    #                         return pickle.load(f)
    #         except (AttributeError, FileNotFoundError):
    #             pass
            
    #         # Fallback: look in the directory where this module is located
    #         module_dir = os.path.dirname(os.path.abspath(__file__))
    #         filename = os.path.join(module_dir, 'trie.pkl')
        
    #     with open(filename, "rb") as file:
    #         return pickle.load(file)

    @staticmethod
    def load_from_file(filename=None):
        """Load and return a trie from a pickle file."""
        if filename is None:
            filename = Path(__file__).parent / "trie.pkl"
        with open(filename, "rb") as file:
            return pickle.load(file)

if __name__ == "__main__":

    ### Be Careful. Creating a pickle file from __main__ will give Attribute errors if a module tries to load it.
    ### Use Make_trie_dict.py to make the actual file.
    ### kcb 3/2025

    # Example usage:
    # words = ["hello", "world", "hi", "her", "hero", "heros", "quiet", "disqualify"]
    words = open("words.txt").read().split()
    trie = Trie()
    trie.insert_words(words)
    # print("Words in Trie:")
    # trie.display()

    # Save the Trie to a file
    trie.save_to_file("trie.pkl")

    # Load the Trie from the file
    loaded_trie = Trie.load_from_file("trie.pkl")
    # print("\nWords in Loaded Trie:")
    # loaded_trie.display()

    # Searching words in the loaded Trie
    search_words = ["hello", "her", "he", "hero", "world", "quiet", "disqualify"]
    print("\nSearch results in loaded Trie:")
    for word in search_words:
        print(f"'{word}': {'Found' if loaded_trie.search(word) else 'Not Found'}")
