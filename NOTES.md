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
pile building toward the majority bonus silently.

Asked the agent to add a display for progress toward the majority bonuses
since points alone don't show it. Agent added: cards captured and spades
captured per player (the two numbers that decide the 27-card and 7-spade
bonuses), plus how many cards are left in the stock. Score bar now reads
`You: 0 pts (0 cards, 0♠) | Computer: 0 pts (0 cards, 0♠) | Stock: 42 left`,
updating live.
