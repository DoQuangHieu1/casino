"""Hungarian two-player Cassino, with a 52-card French deck."""
from itertools import combinations
from typing import NamedTuple

RANKS = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
_VALUE = {rank: i + 1 for i, rank in enumerate(RANKS)}


def value(card):
    return _VALUE[card[:-1]]


class Move(NamedTuple):
    hand: frozenset
    table: frozenset


class State(NamedTuple):
    hands: tuple
    table: tuple
    talon: tuple
    piles: tuple
    sweeps: tuple
    player: int
    last_capturer: int


def new_deal(deck, first=0):
    hands = [(), ()]
    hands[first] = tuple(deck[0:3])
    hands[1 - first] = tuple(deck[3:6])
    return State(
        hands=tuple(hands),
        table=tuple(deck[6:10]),
        talon=tuple(deck[10:]),
        piles=((), ()),
        sweeps=(0, 0),
        player=first,
        last_capturer=first,
    )


def _table_subsets_summing_to(table, target):
    cards = list(table)
    found = []

    def search(i, remaining, chosen):
        if remaining == 0 and chosen:
            found.append(tuple(chosen))
            return
        if i >= len(cards) or remaining <= 0:
            return
        card = cards[i]
        card_value = value(card)
        if card_value <= remaining:
            chosen.append(card)
            search(i + 1, remaining - card_value, chosen)
            chosen.pop()
        search(i + 1, remaining, chosen)

    search(0, target, [])
    return found


def legal_moves(state):
    hand = state.hands[state.player]
    table = state.table
    moves = [Move(frozenset({card}), frozenset()) for card in hand]
    for size in range(1, len(hand) + 1):
        for combo in combinations(hand, size):
            target = sum(value(c) for c in combo)
            for subset in _table_subsets_summing_to(table, target):
                moves.append(Move(frozenset(combo), frozenset(subset)))
    return moves


def play(state, move):
    player = state.player
    hand = state.hands[player]
    if not move.hand or not move.hand <= set(hand):
        raise ValueError("you do not hold those cards")

    if move.table:
        if not move.table <= set(state.table):
            raise ValueError("those cards are not on the table")
        if sum(value(c) for c in move.hand) != sum(value(c) for c in move.table):
            raise ValueError("that does not add up")
    elif len(move.hand) != 1:
        raise ValueError("place exactly one card")

    table_was_empty = not state.table

    hands = list(state.hands)
    hands[player] = tuple(c for c in hand if c not in move.hand)

    piles = list(state.piles)
    sweeps = list(state.sweeps)
    last_capturer = state.last_capturer

    if move.table:
        table = tuple(c for c in state.table if c not in move.table)
        piles[player] += tuple(sorted(move.hand)) + tuple(sorted(move.table))
        last_capturer = player
        if not table:
            sweeps[player] += 1
    else:
        table = state.table + tuple(move.hand)

    next_player = player if table_was_empty else 1 - player

    talon = state.talon
    if not hands[next_player] and talon:
        if not hands[1 - next_player]:
            dealt = {last_capturer: talon[0:3], 1 - last_capturer: talon[3:6]}
            hands = [dealt[0], dealt[1]]
            talon = talon[6:]
            next_player = last_capturer
        else:
            n = min(3, len(talon))
            hands[next_player] = talon[:n]
            talon = talon[n:]

    if not hands[0] and not hands[1] and not talon:
        if table:
            piles[last_capturer] += tuple(sorted(table))
            table = ()
    elif not hands[next_player]:
        next_player = 1 - next_player

    return State(
        hands=tuple(hands),
        table=table,
        talon=talon,
        piles=tuple(piles),
        sweeps=tuple(sweeps),
        player=next_player,
        last_capturer=last_capturer,
    )


def deal_over(state):
    return not state.hands[0] and not state.hands[1] and not state.talon


def score(state):
    points = []
    for p in (0, 1):
        pile = state.piles[p]
        points.append(
            (3 if len(pile) >= 27 else 0)
            + (2 if sum(c.endswith("S") for c in pile) >= 7 else 0)
            + sum(c.startswith("A") for c in pile)
            + (2 if "10D" in pile else 0)
            + (1 if "2S" in pile else 0)
            + state.sweeps[p]
        )
    return tuple(points)
