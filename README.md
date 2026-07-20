# 🎵 Music Recommender Simulation

A small content-based music recommender. Give it a taste profile (favorite genre, favorite mood, target energy, and a few optional preferences) and it scores every song in a catalog, ranks them, and returns the top matches with a plain-language explanation for each score.

---

## How It Works

Real recommenders like Spotify or YouTube typically combine two approaches:

- **Collaborative filtering** predicts what you'll like based on what similar users liked. It can surface surprising picks but needs a large pool of other users' data.
- **Content-based filtering** predicts what you'll like based on the attributes of the items themselves (genre, mood, tempo) compared to your own stated preferences. It works even for brand-new items, but it tends to stay within your existing taste.

This project is a **content-based recommender** — it has no data from other users, only a catalog of songs and one user's taste profile. Every recommendation can be traced back to exactly which attributes matched and by how much.

### Data

- **`Song`**: `genre`, `mood`, `energy`, `tempo_bpm`, `valence`, `danceability`, `acousticness`, `popularity`, `release_decade`, `is_nostalgic`, `is_aggressive`, `is_euphoric`
- **`UserProfile`**: `favorite_genre`, `favorite_mood`, `target_energy`, `likes_acoustic`, `favorite_vibe`

### Scoring

Each song earns points for:

- A genre match
- A mood match
- How close its energy is to the user's target energy (closer = more points, not just "high is good")
- Whether its acoustic level matches the user's `likes_acoustic` preference
- Whether it's tagged with the user's `favorite_vibe` (`nostalgic`, `aggressive`, or `euphoric`)
- A small popularity bonus

All songs are scored, sorted highest to lowest, and the top `k` are returned with the reasons behind each score.

### Scoring Modes

The genre/mood/energy weights can be swapped via `recommend_songs(mode=...)`:

| Mode | Genre | Mood | Energy |
|---|---|---|---|
| `balanced` (default) | 2.0 | 1.0 | up to 1.0 |
| `genre-first` | 3.0 | 0.5 | up to 0.5 |
| `mood-first` | 0.5 | 3.0 | up to 0.5 |
| `energy-focused` | 0.5 | 0.5 | up to 3.0 |

### Diversity Option

`recommend_songs(diversify=True)` reduces a song's score if its artist or genre already appears earlier in the results, so the top list doesn't cluster around one artist or genre.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the app:

   ```bash
   python -m src.main
   ```

### Running Tests

```bash
python -m pytest
```

---

## Sample Output

`python -m src.main` runs the default profile (`favorite_genre=pop`, `favorite_mood=happy`, `target_energy=0.8`, `favorite_vibe=euphoric`) through every scoring mode:

```
Loaded songs: 20

User profile: genre=pop, mood=happy, energy=0.8 (mode=balanced, diversify=False)

|   # | Title          | Artist        |   Score | Reasons                                                                                                                                                  |
|-----|----------------|---------------|---------|----------------------------------------------------------------------------------------------------------------------------------------------------------|
|   1 | Sunrise City   | Neon Echo     |    5.16 | genre match (+2.0), mood match (+1.0), energy similarity (+0.98), acoustic preference match (+0.5), euphoric vibe match (+0.5), popularity bonus (+0.18) |
|   2 | Victory Lap    | Orbit Bloom   |    4.06 | genre match (+2.0), energy similarity (+0.92), acoustic preference match (+0.5), euphoric vibe match (+0.5), popularity bonus (+0.14)                    |
|   3 | Gym Hero       | Max Pulse     |    4.01 | genre match (+2.0), energy similarity (+0.87), acoustic preference match (+0.5), euphoric vibe match (+0.5), popularity bonus (+0.14)                    |
|   4 | Rooftop Lights | Indigo Parade |    3.09 | mood match (+1.0), energy similarity (+0.96), acoustic preference match (+0.5), euphoric vibe match (+0.5), popularity bonus (+0.13)                     |
|   5 | Sunset Sway    | Indigo Parade |    2.85 | mood match (+1.0), energy similarity (+0.75), acoustic preference match (+0.5), euphoric vibe match (+0.5), popularity bonus (+0.10)                     |
```

Same profile with `diversify=True` — Indigo Parade drops from two slots to one, and each repeat gets a visible diversity-adjusted score:

```
User profile: genre=pop, mood=happy, energy=0.8 (mode=balanced, diversify=True)

|   # | Title          | Artist        |   Score | Reasons                                                                                                                                                               |
|-----|----------------|---------------|---------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|   1 | Sunrise City   | Neon Echo     |    5.16 | genre match (+2.0), mood match (+1.0), energy similarity (+0.98), acoustic preference match (+0.5), euphoric vibe match (+0.5), popularity bonus (+0.18)              |
|   2 | Victory Lap    | Orbit Bloom   |    4.06 | genre match (+2.0), energy similarity (+0.92), acoustic preference match (+0.5), euphoric vibe match (+0.5), popularity bonus (+0.14), diversity-adjusted score: 3.56 |
|   3 | Gym Hero       | Max Pulse     |    4.01 | genre match (+2.0), energy similarity (+0.87), acoustic preference match (+0.5), euphoric vibe match (+0.5), popularity bonus (+0.14), diversity-adjusted score: 3.51 |
|   4 | Rooftop Lights | Indigo Parade |    3.09 | mood match (+1.0), energy similarity (+0.96), acoustic preference match (+0.5), euphoric vibe match (+0.5), popularity bonus (+0.13)                                  |
|   5 | Sunset Sway    | Indigo Parade |    2.85 | mood match (+1.0), energy similarity (+0.75), acoustic preference match (+0.5), euphoric vibe match (+0.5), popularity bonus (+0.10), diversity-adjusted score: 1.85  |
```

---

## Testing With Diverse Profiles

Three profiles were used to stress-test the scoring, including one built to contradict itself:

- **High-Energy Pop** (`genre=pop, mood=happy, energy=0.9`) — matched intuition; the pop/happy/high-energy song came out on top.
- **Chill Lofi** (`genre=lofi, mood=chill, energy=0.4`) — also matched intuition; the closest lofi/chill/low-energy songs ranked highest.
- **Deep Intense** (`genre=ambient, mood=intense, energy=0.3`) — a contradictory profile, since "intense" songs are usually high energy, not low. The system still returned a confident top-5 list, built from whichever partial matches scored highest, with no indication the inputs didn't make sense together.

Two additional experiments were run directly against the scoring code:

- Lowering the genre weight and raising the energy weight kept the same top 3 songs, but shrank the score gap between them and the next songs.
- Removing the mood check entirely caused two same-genre songs with different moods to tie at the same score — mood was the only thing telling them apart.

---

## Limitations and Risks

- **Genre outweighs mood** in the default scoring mode, so a genre match usually beats a mood match, even for a user who cares more about vibe than genre label.
- **No contradiction detection** — a profile like `favorite_mood=intense, target_energy=0.3` is self-contradictory, but the system has no way to notice and will confidently rank around it anyway.
- **Filter bubble** — the system can only recommend songs matching a user's stated genre/mood; it has no way to surprise a user with something outside their stated taste.
- **Small, uneven catalog** — most genres have only 1-2 songs, so niche tastes get very few candidates.
- **Some columns are unused** — `tempo_bpm`, `valence`, `danceability`, and `release_decade` are loaded but not scored yet.

See [`model_card.md`](model_card.md) for the full breakdown of design, evaluation, and bias.

---

## Optional Extensions

Beyond the core recommender, this project also includes:

1. **Advanced song features** — `popularity`, `release_decade`, and mood tags (`is_nostalgic`, `is_aggressive`, `is_euphoric`), all wired into scoring.
2. **Multiple scoring modes** — `balanced`, `genre-first`, `mood-first`, `energy-focused` (see table above), built as a Strategy pattern.
3. **Diversity and fairness logic** — the `diversify` option described above.
4. **Formatted table output** — recommendations print as a table via `tabulate`, including a reasons column.

See [`ai_interactions.md`](ai_interactions.md) for how each of these was built and verified.
