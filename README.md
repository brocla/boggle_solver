# Boggle

A collection of Python tools for the classic Boggle word game by Parker
Brothers. Beyond the game itself, the project demonstrates two interesting
programming ideas: a **trie** data structure for fast prefix lookups, and
**constraint-satisfaction with backtracking** for combinatorial search.

## Programs

### boggle.py — Solve a Boggle board

Given a grid of letters, `boggle.py` finds every valid English word by
searching all paths through adjacent cells (including diagonals). It uses a
depth-first search: starting from each cell, it walks the trie one node at a
time and abandons a path the moment it leaves the trie — pruning entire
branches of dead-end prefixes rather than checking every dictionary word.

```
$ python boggle.py lnto epro stie nesi
l n t o
e p r o
s t i e
n e s i

87 words found:
['pro', 'opt', 'rep', ...]
```

If no letters are given, random letters are rolled from the official Boggle
dice. The `--size` option supports boards larger than 4×4:

```
$ python boggle.py --size 5
```

Enter `Qu` as two letters — the program combines them automatically.

### is_boggleable.py — Can a word be spelled with Boggle dice?

A different question from solving a board: given a word, could it *ever*
appear in a game of Boggle? Each of the 16 dice shows six specific faces, and
each die may only be used once per word. This is a constraint-satisfaction
problem solved with backtracking — it tries assigning a die to each letter,
and when it hits a dead end it undoes the last choice and tries the next
candidate.

```
$ python is_boggleable.py sweater
True

$ python is_boggleable.py bookkeeper
False

$ python is_boggleable.py quiet
True
```

### trie.py — Trie data structure

A trie (prefix tree) stores the dictionary so that word lookup and prefix
checking are both fast. Each node represents a single character, and the path
from root to any node spells out a prefix. Nodes marked `is_end_of_word`
indicate complete dictionary words.

Why a trie instead of a plain set? A set can answer "is this a word?" but
cannot answer "does any word *start with* these letters?" — and that second
question is what makes the board solver fast. When `search_word` in
`boggle.py` walks the board, it follows the trie in lockstep. If the current
path isn't a prefix of any word, the trie has no matching child node and the
search prunes the entire branch immediately. Without this prefix-pruning a
4×4 board would require exploring an enormous number of paths; with it, most
paths are cut short after a few letters.

```python
>>> from trie import Trie
>>> t = Trie()
>>> t.insert("hello")
>>> t.insert("help")
>>> t.search("hello")
True
>>> t.search("hel")
False
>>> list(t.words())
['hello', 'help']
```

The trie also handles serialization — `save_to_file` and `load_from_file`
use pickle so the dictionary only needs to be parsed once.


## The Dictionary

The file `words.txt` contains roughly 173,000 English words, one per line.
On first run, `boggle.py` loads a pre-built trie from `trie.pkl`.

If you want to use a different word list, replace `words.txt` and rebuild
the trie:

```
$ python make_trie_dict.py
```

This reads `words.txt`, inserts every word into a fresh `Trie`, and writes
`trie.pkl`. Building from `make_trie_dict.py` (rather than from a `__main__`
block inside `trie.py`) avoids pickle namespace errors when other modules
load the file.  This tool is only run to create a dictionary from a new list of words.

## MCP Server

`boggle_mcp.py` wraps both the board solver and the boggleability checker as
a [Model Context Protocol](https://modelcontextprotocol.io/) (MCP) server.
MCP is an open standard that lets large language models like Anthropic's
Claude call external tools during a conversation. With the server running, an
LLM can solve a Boggle board or check whether a word is boggleable without
the user ever leaving the chat — the model invokes the tools directly, gets
structured results back, and weaves them into its response. This makes it
easy to build AI-powered workflows on top of the same core algorithms that
the command-line programs use.
