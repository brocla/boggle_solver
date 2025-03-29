#!/usr/bin/python
"""Solve Boggle game

## Usage: boggle.py [OPTIONS] [LETTERS]...

Options:
  --size INTEGER  
  --help        

## Example
    `python.py lnto epro stie nesi`

    
Default is a 4x4 board. Option -size overrides
If no letters are given, random letters are chosen.

Note: Enter Qu as if it were a single letter.
The trie.py program is provided to format dictionaries.

"""
import random
from trie import Trie, TrieNode
import click


# TODO: Write tests
# NOTE: The dictionary is lowercase, so the board gets translated to lowercase too.

# these are the actual distributions of letters on official 4x4 Boggle cubes
# Note: Boggle has no solo 'Q', only 'Qu'.
CUBES = [
    "AEANEG", "WNGEEH", "AHSPCO", "LNHNRZ",
    "ASPFFK", "TSTIYD", "OBJOAB", "OWTOAT",
    "IOTMUC", "ERTTYL", "RYVDEL", "TOESSI",
    "LREIXD", "TERWHV", "EIUNES", ("N", "U", "I", "H", "M", "Qu"),
]


@click.command()
@click.option('--size', type=int, default=4)
@click.argument('letters', nargs=-1, type=str)
def cli(letters, size):
    game = Boggle(letters=''.join(letters), size=size)
    game.display_board()
    words2 = game.find_words()
    print(len(words2), "words found:", sorted(words2, key=len))


def false():
    while True:
        yield False


class Boggle:
    """play the classic Boggle word game by Parker Brothers"""

    # the boggle dictionary is large, and slow to load.
    # Share a single copy among all instances.
    dictionary = Trie()

    def __init__(self, size=4, letters=None):
        self.size = size
        if self.size < 2:
            raise ValueError("Board size too small")
        
        if letters:
            self.board = self.form_board(self.load(letters))
        else:
            self.board = self.form_board(self.generate_random_boggle_letters())
        self.visited = self.form_board(false())

        if not self.dictionary:
            self.dictionary = Trie.load_from_file("trie.pkl")

    

    def load(self, letters):
        # clean-up the input
        letters = ''.join([ltr.lower() for ltr in letters if ltr.isalpha()])

        # make a list of characters where 'qu' is considered a single character
        if 'qu' in letters:
            letters = letters.replace('qu', '5')
            letters = list(letters)
            letters[letters.index('5')] = 'qu'

        if len(letters) != self.size * self.size:
            raise ValueError(f"{len(letters)} letters cannot be formatted into a {self.size}x{self.size} board")
        
        yield from iter(letters)
    
    def form_board(self, letter):
        """make a square matrix from a generator of letters"""
        return [[next(letter) for _ in range(self.size)] for _ in range(self.size)]


    def generate_random_boggle_letters(self):
        random.shuffle(CUBES)
        while True:
            for cube in CUBES:
                yield random.choice(cube).lower()
        
    
    def find_words(self):
        found_words = set()
        for i in range(self.size):
            for j in range(self.size):
                first_letter = self.board[i][j]
                candidates = self.dictionary.root.children
                self.search_word(i, j, candidates[first_letter], first_letter, found_words)
        return found_words


    def search_word(self, x, y, node, path, found_words):
        """note: recursive dfs"""

        if node.is_end_of_word and len(path) > 2:
            found_words.add(path)

        is_on_grid = (0 <= x < self.size) and (0 <= y < self.size)
        if not is_on_grid or self.visited[x][y]:
            return

        self.visited[x][y] = True

        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx or dy:
                    nx, ny = x + dx, y + dy

                    is_on_grid = (0 <= nx < self.size) and (0 <= ny < self.size)
                    if not is_on_grid:
                        continue

                    next_letter = self.board[nx][ny]
                    if next_letter in node.children and not self.visited[nx][ny]:
                        self.search_word(
                            nx,
                            ny,
                            node.children[next_letter],
                            path + next_letter,
                            found_words,
                        )
        self.visited[x][y] = False

    def display_board(self):
        for row in self.board:
            print(" ".join(row))
        print()


if __name__ == "__main__":
    cli()
