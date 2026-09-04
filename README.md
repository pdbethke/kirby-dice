# kirby-dice

Fair, seeded, replayable dice for the Kirby HERO System platform.

This package rolls dice and does nothing else. It has **no dependencies** and
holds **no game rules** — what a roll means is the caller's business.

## Attribution

The roller is based in part on the work of **Bill Bame**, shared informally
and with thanks. No licence condition attaches to it; the credit is here
because it is owed.

## Why this is its own package

Players are, reasonably, funny about dice. A roller buried inside a combat
engine can *assert* that it is fair. One that ships on its own can prove it.

**The dice are fair, and the tests say how we know.** `tests/test_fairness.py`
runs chi-square uniformity over 60,000 rolls, checks independence across all
36 ordered pairs of consecutive rolls, and pins the mean within five sigma of
3.5. Every test is seeded and therefore deterministic — a fairness test that
fails once a fortnight only teaches people to re-run CI. Two of the tests
guard the guards: a loaded die must trip the uniformity assertion, and twenty
unseeded rollers must not share a seed.

**Every fight can be replayed.** A roller always reports the seed it rolls
from, including when you did not give it one:

```python
from kirby_dice import RandomRoller

roller = RandomRoller()
fight = [roller.roll_dice(3) for _ in range(40)]

# Record roller.seed alongside the fight, and it replays die for die.
replay = RandomRoller(seed=roller.seed)
assert [replay.roll_dice(3) for _ in range(40)] == fight
```

An unseeded `random.Random()` draws from OS entropy, so the seed never exists
as a value and a fight cannot be reproduced once fought. `RandomRoller` picks
its own seed with `secrets.randbits(64)` instead — unguessable, so being
recordable does not make the next roll predictable.

## Usage

```python
from kirby_dice import RandomRoller, FakeRoller

RandomRoller(seed=42).roll_dice(3)          # -> [1, 1, 6]
RandomRoller().roll_dice(2, sides=20)       # any number of sides

FakeRoller([[3, 4, 5]]).roll_dice(3)        # -> [3, 4, 5], for tests
```

`DiceRoller` is a `Protocol`, so any object with a matching `roll_dice` will
do — that is the seam consumers inject through.

### There is no `roll_half_die()`

A HERO half die is an extra whole d6 that the **caller** converts, next to the
rest of its damage rules. This package had such a method once. It had no
callers, and its mapping disagreed with the live conversion in the combat
engine — the same d6 gave different results depending on which you asked. Two
homes for one rule is how they drift apart. Roll dice here; convert them there.

## Licence

PolyForm Noncommercial License 1.0.0 — see `LICENSE`.
