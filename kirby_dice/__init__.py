"""Dice for the Kirby HERO System platform: fair, seeded, and replayable.

This package rolls dice and does nothing else. It holds no game rules — what
a roll MEANS is the caller's business, and deliberately so: a rule with two
homes is a rule that drifts.

**Attribution.** This dice roller is based in part on the work of Bill Bame,
shared informally and with thanks. No licence condition attaches to it; the
credit is here because it is owed. It was missing entirely until 2026-08-28,
and giving it a module of its own is part of why this package exists.

**Why a separate package.** Players are, reasonably, funny about dice. A
roller buried inside a combat engine can assert that it is fair. One that
ships on its own can prove it:

* ``tests/test_fairness.py`` — chi-square uniformity, independence of
  consecutive rolls, mean and range, all seeded so they are deterministic.
* ``RandomRoller.seed`` — every roller reports the seed it rolls from, so a
  fight recorded with its seed can be replayed die for die.
"""
from kirby_dice.roller import DiceRoller, RandomRoller
from kirby_dice.fake import FakeRoller

__all__ = ["DiceRoller", "RandomRoller", "FakeRoller"]
