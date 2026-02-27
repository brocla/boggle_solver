"""MCP server exposing Boggle tools: solve a board and check if a word is boggleable."""

import json
from mcp.server.fastmcp import FastMCP
from boggle import Boggle
from is_boggleable import can_form_word

mcp = FastMCP("Boggle")


@mcp.tool()
def solve_boggle(letters: str = "", size: int = 4) -> str:
    """Generate and/or solve a Boggle board.

    If letters are provided, solves that board. If omitted, generates a
    random board by rolling the official Boggle dice, then solves it.
    Returns the board layout and all valid words found.

    Args:
        letters: Board letters (e.g. "lntoeprostienesi"). Leave empty to generate a random board.
        size: Board dimension (default 4 for a 4x4 grid).
    """
    game = Boggle(letters=letters or None, size=size)
    return json.dumps(game.to_dict(), indent=2)


@mcp.tool()
def is_boggleable(word: str) -> bool:
    """Check if a word can be spelled using the 16 standard Boggle dice.

    Each die may only be used once. Returns True if possible, False otherwise.

    Args:
        word: The word to check (e.g. "sweater").
    """
    return can_form_word(word)


if __name__ == "__main__":
    mcp.run()
