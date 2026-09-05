# Changelog

## 0.1.1 — 2026-09-05

### Fixed

The `LICENSE` file described a different package. It was copied from kirby-cost
when this repo was created and its notes section still said this work "is a
Python port of the HERO Designer cost engine" and "derives from HERO Designer
source licensed from CompNet Design, Inc."

Neither is true. kirby-dice rolls dice; it holds no game data and no rules, and
it derives from Bill Bame's informally-shared work, not from the HERO Designer
source. In a project that keeps its licensing lanes deliberately separate, a
published package asserting a derivation it does not have is worth a release to
correct.

No code changed. The PolyForm Noncommercial 1.0.0 text itself was never wrong
and is untouched.

## 0.1.0 — 2026-09-04

First release. Extracted from `kirby_combat.dice`, where the roller had lived
since 2026-04-24, as item 6 of the carve-out program.

The move is not about size — the package is under 100 lines. It is about what
a dice module is *for*: putting Bill Bame's attribution where nobody can miss
it, and making fairness and replayability things a reader can check rather
than take on trust.

### Added

* `DiceRoller` protocol, `RandomRoller`, `FakeRoller`.
* `RandomRoller.seed` — always a real number, so any fight can be replayed.
* A fairness suite the roller never had while it was a private helper.

### Not carried over

* `roll_half_die()`. Removed in kirby-combat 0.10.0: no callers anywhere, and
  a d6 mapping that disagreed with the live half-die conversion.
