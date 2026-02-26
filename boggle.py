#!/usr/bin/python
"""Solve Boggle game

## Usage: boggle [OPTIONS] [LETTERS]...

Options:
  --size INTEGER  
  --help        

## Example
    `boggle lnto epro stie nesi`

    
Default is a 4x4 board. Option -size overrides
If no letters are given, random letters are chosen.

Note: Enter Qu as if it were a single letter.
The trie.py program is provided to format dictionaries.

"""
import click
from itertools import repeat
import random
from helpers import normalize_qu, boggle_dice
from trie import Trie, TrieNode

DIRECTIONS = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]


@click.command()
@click.option("--size", type=int, default=4)
@click.argument("letters", nargs=-1, type=str)
def cli(letters, size):
    """Run the Boggle solver from the command line."""
    game = Boggle(letters=letters, size=size)
    game.display_board()
    words = game.find_words()
    click.secho(f"{len(words)} words found:", fg="yellow")
    click.secho(sorted(words, key=len))


class Boggle:
    """solve the classic Boggle word game by Parker Brothers"""

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
        self.visited = self.form_board(repeat(False))

        if not self.dictionary:
            self.dictionary = Trie.load_from_file()

    def load(self, raw_chars):
        """Parse user input into boggle-normalized letters."""
        cleaned_chars = [ch.lower() for ch in "".join(raw_chars) if ch.isalpha()]
        boggle_chars = list(normalize_qu(cleaned_chars))

        if len(boggle_chars) != self.size * self.size:
            raise ValueError(
                f"{len(boggle_chars)} letters cannot be formatted into a {self.size}x{self.size} board"
            )

        yield from boggle_chars

    def form_board(self, letter):
        """make a square matrix from a generator of letters"""
        return [[next(letter) for _ in range(self.size)] for _ in range(self.size)]

    def generate_random_boggle_letters(self):
        """Yield random letters by rolling each Boggle cube in shuffled order."""
        cubes = list(boggle_dice)  # copy to avoid modifying the original
        random.shuffle(cubes)
        while True:
            for cube in cubes:
                yield random.choice(cube)

    def find_words(self):
        """Return the set of all dictionary words found on the board."""
        found_words = set()
        for i in range(self.size):
            for j in range(self.size):
                first_letter = self.board[i][j]
                candidates = self.dictionary.root.children
                if first_letter in candidates:
                    self.search_word(
                        i, j, candidates[first_letter], first_letter, found_words
                    )
        return found_words

    def search_word(self, x, y, node, path, found_words):
        """Recursively explore adjacent cells to find words via DFS."""
        is_on_grid = (0 <= x < self.size) and (0 <= y < self.size)
        if not is_on_grid or self.visited[x][y]:
            return

        if node.is_end_of_word and len(path) > 2:
            found_words.add(path)

        self.visited[x][y] = True

        for dx, dy in DIRECTIONS:
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

    def to_dict(self):
        """Return the board and found words as a serializable dictionary."""
        words = self.find_words()
        return {
            "board": self.board,
            "size": self.size,
            "words": sorted(words, key=len),
            "count": len(words),
        }

    def display_board(self):
        """Print the board grid to the terminal."""
        for row in self.board:
            click.echo(" ".join(row))
        click.echo()


if __name__ == "__main__":
    cli()
