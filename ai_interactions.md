# AI Interactions Log

This file documents how AI assistance was used on the optional stretch features for the Music Recommender Simulation.

---

## Agentic Workflow (SF8)

**Task:** Implement Challenge 1 (Advanced Song Features) — add five or more new song attributes to the dataset and wire them into the scoring logic.

**Prompt:**
> Add 5+ new attributes to the dataset: popularity (0-100), release decade, and detailed mood tags like nostalgic, aggressive, and euphoric. Update both `songs.csv` and the scoring logic so these attributes actually affect the score, not just get loaded and ignored.

**Changes made:**
- Added `popularity`, `release_decade`, `is_nostalgic`, `is_aggressive`, and `is_euphoric` columns to `data/songs.csv`.
- Added matching fields to the `Song` dataclass and a new `favorite_vibe` field to `UserProfile` in `src/recommender.py`.
- Updated `load_songs()` to parse the new numeric and boolean columns.
- Updated scoring to add a popularity bonus and a vibe-tag match bonus, and to start using `likes_acoustic`, which was previously loaded but never scored.

**Manual verification:** Ran `python -m src.main` and `pytest` to confirm the new columns load correctly and affect scores as expected (e.g., a `favorite_vibe="euphoric"` preference raises the score of songs tagged `is_euphoric`).

---

## Design Pattern (SF10)

**Pattern used:** Strategy pattern, implemented with functions instead of classes.

**Task:** Implement Challenge 2 (Multiple Scoring Modes) — support Genre-First, Mood-First, and Energy-Focused ranking without duplicating scoring code.

**How AI helped:** Asked for a design pattern that fits a codebase built on plain functions and dicts rather than classes. The suggestion: one shared scoring function that takes weights as parameters, plus a small named wrapper function per mode that calls it with different weights. A dictionary maps mode names to wrapper functions, so the caller just looks up a strategy by name.

**Where it appears in the code (`src/recommender.py`):**
- `_score_with_weights()` — the shared scoring algorithm
- `score_song_balanced`, `score_song_genre_first`, `score_song_mood_first`, `score_song_energy_focused` — the interchangeable strategies
- `SCORING_MODES` — the strategy registry, selected via `recommend_songs(mode=...)`

---

## Diversity and Fairness Logic (Challenge 3)

**Task:** Prevent the top-k recommendations from clustering around one artist or genre.

**Prompt:**
> Write a rule that penalizes a song's score if its artist is already in the top recommendations list. It should still allow a repeated artist if nothing else scores high enough, not block it outright.

**Changes made:** Added a `diversify` option to `recommend_songs()`. When enabled, songs are picked into the results one at a time instead of by a single sort — each remaining song's score is temporarily reduced if its artist or genre already appears in the results so far, and the best-adjusted song is picked next. The penalty is a soft deduction, not a hard filter, so a repeated artist can still be picked if it's still the best option left.

**Manual verification:** Ran the same profile with and without `diversify=True`. Without it, one artist held two of the top five slots; with it, that artist dropped to one slot and a different artist filled the freed spot.

---

## Visual Summary Table (Challenge 4)

**Task:** Improve terminal output readability using a table library.

**Prompt:**
> Suggest a way to use tabulate to print the recommendations as a table. Keep the reasons for each score as a column — don't drop them for a cleaner table.

**Changes made:** Added `tabulate` to `requirements.txt`, plus a `format_recommendations_table()` function in `src/recommender.py` that turns each `(song, score, explanation)` tuple into a row with rank, title, artist, score, and reasons columns. `src/main.py` now prints this table instead of one `print()` block per song.

**Manual verification:** Ran `python -m src.main` and confirmed the table renders cleanly in a plain terminal, with the full reasons string still visible for each song.
