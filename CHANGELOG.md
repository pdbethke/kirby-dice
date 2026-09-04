# Changelog

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
