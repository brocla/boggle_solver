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


def boggle_chars(text):
    """Yield characters from text, combining 'q' and following 'u' into 'qu'.

    Raises ValueError if 'q' appears without a following 'u'.

    >>> list(boggle_chars("quiet"))
    ['qu', 'i', 'e', 't']
    >>> list(boggle_chars("disqualify"))
    ['d', 'i', 's', 'qu', 'a', 'l', 'i', 'f', 'y']
    """
    it = iter(text)
    for char in it:
        if char == "q":
            following = next(it, None)
            if following != "u":
                raise ValueError("'Q' without a 'u'.")
            yield "qu"
        else:
            yield char


class TrieNode:
    # __slots__ = ['children', 'is_end_of_word']
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False

class Trie:
    # __slots__ = ['root']
    def __init__(self):
        self.root = TrieNode()

    def __bool__(self):
        return bool(self.root.children)
    
    def _walk(self, word):
        """Walk the trie along the boggle-normalized chars of word.

        Returns the node at the end of the path, or None if any
        character is missing or the word has Q without U.
        """
        try:
            chars = list(boggle_chars(word))
        except ValueError:
            return None
        current_node = self.root
        for char in chars:
            if char not in current_node.children:
                return None
            current_node = current_node.children[char]
        return current_node

    def insert(self, word):
        try:
            chars = list(boggle_chars(word))
        except ValueError:
            return
        current_node = self.root
        for char in chars:
            if char not in current_node.children:
                current_node.children[char] = TrieNode()
            current_node = current_node.children[char]
        current_node.is_end_of_word = True

    def insert_words(self, words):
        for word in words:
            self.insert(word)

    def search(self, word):
        node = self._walk(word)
        if node is None:
            return False
        return node.is_end_of_word

    def display(self):
        def _display(node, prefix):
            if node.is_end_of_word:
                print(prefix)
            for char, next_node in node.children.items():
                _display(next_node, prefix + char)
       
        _display(self.root, '')

    def save_to_file(self, filename):
        with open(filename, 'wb') as file:
            pickle.dump(self, file, protocol=-1)

    @staticmethod
    def load_from_file(filename):
        with open(filename, 'rb') as file:
            return pickle.load(file)


if __name__ == "__main__":
        
    ### Be Careful. Creating a pickle file from __main__ will give Attribute errors if a module tries to load it.
    ### Use Make_trie_dict.py to make the actual file.
    ### kcb 3/2025

    # Example usage:
    # words = ["hello", "world", "hi", "her", "hero", "heros", "quiet", "disqualify"]
    words = open('words.txt').read().split()
    trie = Trie()
    trie.insert_words(words)
    # print("Words in Trie:")
    # trie.display()

    # Save the Trie to a file
    trie.save_to_file('trie.pkl')

    # Load the Trie from the file
    loaded_trie = Trie.load_from_file('trie.pkl')
    # print("\nWords in Loaded Trie:")
    # loaded_trie.display()

    # Searching words in the loaded Trie
    search_words = ["hello", "her", "he", "hero", "world", "quiet", "disqualify"]
    print("\nSearch results in loaded Trie:")
    for word in search_words:
        print(f"'{word}': {'Found' if loaded_trie.search(word) else 'Not Found'}")