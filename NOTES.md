# Notes

## v1 — first build

Wrote `casino.py` to pass `tests/test_casino.py` unchanged (`uv run pytest`:
14 passed). Built `index.html` as a browser table against a simple computer
opponent (always captures the biggest group it can, otherwise places its
lowest card), reimplementing the same rules in JS since the page has no
server or Python runtime.

## Playtest 1

Played a deal. Found: capturing a plain 2 (not the 2 of Spades) from the
table with a matching 2 from hand didn't move the score.

Asked the agent about it, expecting a bug. Turns out it's correct: most
captured cards are worth 0 points on their own in this scoring system - only
Aces, the 10 of Diamonds, the 2 of Spades, sweeps, and the two majority
bonuses (27+ cards, 7+ spades) score anything. A plain 2 just sits in the
pile building toward the majority bonus silently. No change made - agent
offered to add a card-count display alongside the score so progress toward
the majority bonuses is visible even when points don't move; decided it
wasn't needed.
