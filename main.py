"""One word from grandma about AI.

Judges a shortlist of candidate words against the five rubric criteria
(in priority order) and writes the winning word to the output file.

Criteria, in order:
  1. reads as the single word a grandma would text about AI
  2. real grandmother's texting voice, warm and a little baffled
  3. funny in one word, joke lands without caption or context
  4. tied to AI, robots or machines, not fitting any subject
  5. fresh pick, not the obvious one, still instantly readable

Sub-scores are 0-5 per criterion, from the head-to-head judging in
NOTES.md. The selector ranks lexicographically by criteria 1 to 5.
"""

import os
import sys

DEFAULT_OUTPUT = "/output/entry.txt"

# word -> (c1, c2, c3, c4, c5)
LEXICON = {
    # The winner: the canonical grandma typo of the brand she uses daily.
    "googel": (5, 5, 5, 5, 5),
    # Strong runners-up from the head-to-head rounds.
    "Rosie": (5, 5, 4, 4, 4),
    "Microwave": (5, 5, 5, 3, 5),
    "Toaster": (4, 4, 4, 3, 4),
    "Tinman": (4, 4, 3, 4, 3),
    "Sweetiebot": (4, 4, 3, 4, 3),
    "Computery": (4, 3, 3, 4, 3),
    "Voodoo": (3, 3, 3, 2, 3),
    "Hocuspocus": (3, 3, 3, 2, 2),
    # Modal picks: the obvious words the whole field chose.
    # Low freshness (criterion 5) is their fatal flaw.
    "Robit": (4, 4, 3, 5, 1),
    "Witchcraft": (3, 3, 4, 2, 1),
    "Doohickey": (3, 4, 3, 3, 1),
}


def select_word(lexicon):
    """Rank candidates lexicographically by criteria 1 to 5, pick the best.

    Ties on the full tuple break alphabetically so the choice is stable.
    """
    ranked = sorted(lexicon.items(), key=lambda kv: (-kv[1][0], -kv[1][1],
                                                      -kv[1][2], -kv[1][3],
                                                      -kv[1][4], kv[0]))
    return ranked[0][0]


def write_word(word, path):
    """Write the word with no trailing newline, creating dirs as needed."""
    directory = os.path.dirname(path)
    if directory:
        os.makedirs(directory, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as handle:
        handle.write(word)


def self_check(word, path):
    """Re-read the output and verify it matches the selected word exactly."""
    with open(path, "rb") as handle:
        raw = handle.read()
    if raw != word.encode("utf-8"):
        raise ValueError("output bytes %r != selected word bytes" % raw)
    text = raw.decode("utf-8")
    if not 1 <= len(text) <= 30:
        raise ValueError("output length %d outside 1-30 chars" % len(text))
    if not text.strip():
        raise ValueError("output is whitespace-only")
    if text != word:
        raise ValueError("output %r != selected word %r" % (text, word))
    return len(raw)


def main():
    path = os.environ.get("MAKEFUN_OUTPUT", DEFAULT_OUTPUT)
    word = select_word(LEXICON)
    write_word(word, path)
    size = self_check(word, path)
    print("wrote %r (%d bytes) to %s" % (word, size, path))
    return 0


if __name__ == "__main__":
    sys.exit(main())
