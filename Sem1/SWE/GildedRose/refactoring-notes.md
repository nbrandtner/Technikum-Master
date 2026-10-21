# Refactoring notes

## Approach

I started with the original Python code and added tests before changing it.
The first 23 tests passed against the starter. I then moved the different update
rules into small methods and ran the same tests again.

After that I added eight tests for Conjured items. They failed with the old
behavior. I added the faster quality loss and checked that all 31 tests passed.

## Main changes

- Sulfuras is skipped at the start of the loop.
- Brie, backstage passes and degrading items each have a small update method.
- Normal and Conjured items share the same logic, with a different daily loss.
- `sell_in` is decreased once, after the quality update.
- The `Item` class and the `items` attribute are unchanged.

I kept the name checks and a few helper methods. A separate class for every item
type felt unnecessary for this size of exercise.

## Rules and assumptions

The values below use `sell_in` at the start of the update.

| Item | Before expiry (`sell_in > 0`) | Expired (`sell_in <= 0`) |
| --- | --- | --- |
| Normal | Quality -1 | Quality -2 |
| Conjured | Quality -2 | Quality -4 |
| Aged Brie | Quality +1 | Quality +2 |
| Backstage passes | +1 above 10 days, +2 from 6 to 10, +3 from 1 to 5 | Quality becomes 0 |
| Sulfuras | No change | No change |

Quality stays between 0 and 50 for non-legendary items. Sulfuras keeps its quality
of 80 and its sell-in value.

Names starting with `Conjured ` are treated as Conjured items. Name matching is
case-sensitive. Other special items keep the exact names from the starter.
Starting values are assumed to be valid; I did not add input validation to `Item`.

## Checks

The tests cover the sell-in boundaries, quality limits, mixed and empty
inventories, and updates over several days. The regression test compares 2,772
starting states with the original code for 20 days each: all qualities from 0 to
50 for normal items, Brie and passes, plus quality 80 for Sulfuras, with sell-in
values from -2 to 15. Conjured items have separate tests because their behavior
is intentionally different from the starter.
