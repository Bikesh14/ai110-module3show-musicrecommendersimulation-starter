# AI Interactions Log

> **Stretch features only.** Only fill in the sections that apply to stretch features you attempted. If you did not attempt a stretch feature, leave its section blank or delete it. This file is not required for the core project.

---

## Agentic Workflow (SF8)

> Document your experience using an AI agent (e.g., Cursor Agent, Claude, Copilot) to make multi-step changes autonomously.

**What task did you give the agent?**

Implement Optional Extensions Challenge 1 (Advanced Song Features): add 5+ new song attributes to `data/songs.csv` and update the scoring logic in `src/recommender.py` to use them.

**Prompts used:**

"Add 5+ new attributes to the dataset — popularity (0-100), release decade, and detailed mood tags like nostalgic/aggressive/euphoric. Update both `songs.csv` and the scoring logic so these new attributes actually affect the score, not just get loaded and ignored."

**What did the agent generate or change?**

- Added `popularity`, `release_decade`, `is_nostalgic`, `is_aggressive`, `is_euphoric` columns to `data/songs.csv` for all 20 songs.
- Updated `Song` and `UserProfile` dataclasses in `src/recommender.py` with the new fields (plus a new `favorite_vibe` preference).
- Updated `load_songs` to parse the new numeric and boolean columns.
- Updated the scoring logic to add a popularity bonus and a vibe-tag match bonus, and to actually use `likes_acoustic` (previously loaded but never scored).

**What did I verify or fix manually?**

Ran `python -m src.main` and `pytest` after the change to confirm the new columns loaded correctly and scores still made sense (e.g., a euphoric-vibe preference bumped songs tagged `is_euphoric` in the output). Spot-checked a few of the popularity/decade/mood-tag values the agent filled in against the existing mood and genre for each song, since those were invented values rather than pulled from a real source.

---

## Design Pattern (SF10)

> Document how AI helped you choose or implement a design pattern.

**Which design pattern did you use?**

Strategy pattern (function-based), for Optional Extensions Challenge 2 (Multiple Scoring Modes).

**How did AI help you brainstorm or implement it?**

I asked: "I want main.py to switch between Genre-First, Mood-First, and Energy-Focused ranking without duplicating the scoring code three times. What's a simple design pattern for this in a codebase that's mostly plain functions and dicts, not classes?" The suggestion was a lightweight Strategy pattern implemented as functions instead of a class hierarchy: one shared scoring function that takes weights as parameters, and a small set of named wrapper functions (one per mode) that call it with different weights. A dictionary (`SCORING_MODES`) maps mode names to the wrapper functions, so `recommend_songs` just looks up the right strategy by name.

**How does the pattern appear in your final code?**

`src/recommender.py`: `_score_with_weights()` is the shared algorithm, `score_song_balanced`, `score_song_genre_first`, `score_song_mood_first`, and `score_song_energy_focused` are the interchangeable strategies, and `SCORING_MODES` is the strategy registry that `recommend_songs(mode=...)` selects from.

---

## Diversity and Fairness Logic (Optional Extensions Challenge 3)

**What task did you give the agent?**

Add a diversity penalty so the top-k recommendations don't cluster around one artist or genre.

**Prompts used:**

"Write a rule that penalizes a song's score if its artist is already in the top recommendations list. It should still let a repeated artist appear if nothing else scores high enough, just less likely to."

**What did the agent generate or change?**

Added a `diversify` option to `recommend_songs` in `src/recommender.py`. When enabled, songs are picked into the results one at a time (instead of a single sort): each remaining song's score is temporarily reduced if its artist or genre already appears in the results so far, and the best-adjusted song is picked next. The penalty is a soft nudge, not a hard block, so a repeated artist can still make the list if it's still the best option.

**What did I verify or fix manually?**

Ran the recommender with and without `diversify=True` on the same profile and confirmed the artist "Indigo Parade," which had two songs in the top 5 without diversification, dropped to one, with a different artist filling the freed slot.

---

## Visual Summary Table (Optional Extensions Challenge 4)

**What task did you give the agent?**

Improve the readability of the terminal output using a table library.

**Prompts used:**

"Suggest a way to use tabulate (or similar) to print the recommendations as a table. Make sure the reasons for each score are still included as a column, not dropped for the sake of a cleaner table."

**What did the agent generate or change?**

Added `tabulate` to `requirements.txt`, and a `format_recommendations_table()` function in `src/recommender.py` that turns the list of `(song, score, explanation)` tuples into a GitHub-flavored markdown table with columns for rank, title, artist, score, and reasons. `src/main.py` now prints this table instead of one `print()` block per song.

**What did I verify or fix manually?**

Ran `python -m src.main` and checked that the reasons column still showed the full explanation string for each song, and that the table rendered correctly in a plain terminal.
