.. _crosswords:

`data/corpora/crosswords` -- Crossword puzzles and clues
========================================================

The `crosswords/` subdirectory contains all the crosswords Rob could find in
`.puz` format, a vaguely standard format that we can decode using
`scripts/puz.rb`.

The `clues/` subdirectory contains the clues and answers extracted from these
crosswords, which may be useful in building something that can look up
crossword clues.

The compiled clues are in `clues/combined_straight.txt` and `clues/combined_cryptic.txt`, depending on whether they are for straight or cryptic crosswords.

