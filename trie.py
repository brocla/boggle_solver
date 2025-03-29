import pickle

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
    
    def insert(self, word):
        current_node = self.root
        Qu = False
        for char in word:

            # Manage `Qu`
            # Boggle doesn't handle words with Q, not followed by U. exclude them.
            if Qu and char != 'u':
                del current_node
                return
            
            # have to skip U becasue it has been grouped with previous Q
            if char == 'u' and Qu:
                Qu = False
                continue

            # Every Q is grouped with a U
            if char == 'q':
                char = 'qu'
                Qu = True

            if char not in current_node.children:
                current_node.children[char] = TrieNode()
            current_node = current_node.children[char]
        current_node.is_end_of_word = True

    def insert_words(self, words):
        for word in words:
            self.insert(word)

    def search(self, word):
        current_node = self.root
        Qu = False
        for char in word:

            # Manage `Qu`
            # Boggle doesn't handle words with Q, but not followed by U. ignore them.
            if Qu and char != 'u':
                return
            
            # have to skip U becasue it has been grouped with previous Q
            if char == 'u' and Qu:
                Qu = False
                continue

            # Every Q is grouped with a U
            if char == 'q':
                char = 'qu'
                Qu = True

            if char not in current_node.children:
                return False
            current_node = current_node.children[char]
        return current_node.is_end_of_word

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