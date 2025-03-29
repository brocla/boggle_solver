from trie import Trie, TrieNode

def make(words_file, out_file):
    words = open(words_file).read().split()
    trie = Trie()
    trie.insert_words(words)
    trie.save_to_file(out_file)

if __name__ == "__main__":
    make('words.txt', 'trie.pkl')

