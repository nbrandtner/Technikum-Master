# Gilded Rose Kata

My solution to the Gilded Rose refactoring kata, including Conjured items.

I chose Python because it keeps the update rules easy to read. The tests use
`unittest`, so there are no extra packages to install.

## Run

Open a terminal in this folder. You need Python 3.

```powershell
python -m unittest discover -v
```

To see the inventory change over five days:

```powershell
python demo.py 5
```

The demo includes day 0, which is the starting inventory.

## Files

- `gilded_rose.py`: the refactored update logic and the unchanged `Item` class.
- `tests/test_gilded_rose.py`: tests for the item rules and boundary cases.
- `tests/test_legacy_behavior.py`: checks the existing items against the starter.
- `tests/fixtures/gilded_rose_original.py`: an unchanged copy of the starter, used only by the tests.
- `demo.py`: a small command line example.
- `docs/refactoring-notes.md`: my approach and the main decisions.
