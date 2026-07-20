# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works

Real-world recommenders like Spotify or YouTube usually combine two approaches. **Collaborative filtering** predicts what a user will like based on the behavior of *other* users with similar taste ("people who liked what you liked also liked X"), while **content-based filtering** predicts what a user will like based on the *attributes* of the items themselves (genre, mood, tempo) compared against that user's own stated or inferred preferences. Collaborative filtering can surface surprising, cross-genre picks but needs a large pool of other users' interaction data and struggles with brand-new items (the "cold start" problem). Content-based filtering has no cold-start problem and is easy to explain, but it tends to stay inside a user's existing taste rather than discovering anything new.

This simulation is a **content-based recommender**: it has no other-user interaction data, only a catalog of songs with fixed attributes and a single user's taste profile. It prioritizes transparency and explainability over discovery — every recommendation can be traced back to which attributes matched and by how much, rather than a black-box similarity score learned from millions of other listeners.

Features used:

- **`Song`**: `genre`, `mood`, `energy`, `tempo_bpm`, `valence`, `danceability`, `acousticness`
- **`UserProfile`**: `favorite_genre`, `favorite_mood`, `target_energy`, `likes_acoustic`

The `Recommender` scores each song by rewarding a genre match, rewarding a mood match, rewarding energy values close to the user's `target_energy` (not just high or low energy in isolation), and adjusting for whether the song's acousticness lines up with `likes_acoustic`. Songs are then ranked by descending score and the top `k` are returned as recommendations.

### Algorithm Recipe

For each song, given a user's taste profile (`favorite_genre`, `favorite_mood`, `target_energy`):

- **+2.0 points** if `song.genre == user.favorite_genre`
- **+1.0 point** if `song.mood == user.favorite_mood`
- **+ (1.0 − |song.energy − user.target_energy|)** similarity points — rewards energy values *close to* the target, not just high or low energy on its own

**Data flow:**

```
Input (UserProfile: favorite_genre, favorite_mood, target_energy)
        │
        ▼
Process (loop over every Song in songs.csv, apply the scoring rule above)
        │
        ▼
Output (rank all scored songs descending, return the Top K)
```

**Potential biases to watch for:**

- The system over-prioritizes **genre** (2.0) over **mood** (1.0), so a song that matches genre but clashes with mood will often outrank a song that nails the mood but is in a different genre. A user who cares more about "vibe" than genre label might feel underserved.
- It has no way to discover music outside a user's stated genre/mood — unlike collaborative filtering, it can't surprise a user with a great song from a genre they've never told the system they like.
- The catalog is tiny and hand-picked, so results are only as diverse as the songs already in `data/songs.csv`.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows
   ```
2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

Output of `python -m src.main` with the default profile (`favorite_genre=pop`, `favorite_mood=happy`, `target_energy=0.8`):

```
Loading songs from data/songs.csv...
Loaded songs: 20

User profile: genre=pop, mood=happy, energy=0.8

Top recommendations:

Sunrise City (Neon Echo) - Score: 3.98
Because: genre match (+2.0), mood match (+1.0), energy similarity (+0.98)

Victory Lap (Orbit Bloom) - Score: 2.92
Because: genre match (+2.0), energy similarity (+0.92)

Gym Hero (Max Pulse) - Score: 2.87
Because: genre match (+2.0), energy similarity (+0.87)

Rooftop Lights (Indigo Parade) - Score: 1.96
Because: mood match (+1.0), energy similarity (+0.96)

Sunset Sway (Indigo Parade) - Score: 1.75
Because: mood match (+1.0), energy similarity (+0.75)
```

**Screenshot or video** *(optional)*: 

---

## Testing With Diverse Profiles

Three test profiles, including one deliberately conflicting "edge case" profile, to see how the system behaves outside the default.

**High-Energy Pop** — `favorite_genre=pop, favorite_mood=happy, target_energy=0.9`

```
Sunrise City (Neon Echo) - Score: 3.92
Because: genre match (+2.0), mood match (+1.0), energy similarity (+0.92)
Victory Lap (Orbit Bloom) - Score: 2.98
Because: genre match (+2.0), energy similarity (+0.98)
Gym Hero (Max Pulse) - Score: 2.97
Because: genre match (+2.0), energy similarity (+0.97)
Rooftop Lights (Indigo Parade) - Score: 1.86
Because: mood match (+1.0), energy similarity (+0.86)
Sunset Sway (Indigo Parade) - Score: 1.65
Because: mood match (+1.0), energy similarity (+0.65)
```

**Chill Lofi** — `favorite_genre=lofi, favorite_mood=chill, target_energy=0.4`

```
Midnight Coding (LoRoom) - Score: 3.98
Because: genre match (+2.0), mood match (+1.0), energy similarity (+0.98)
Library Rain (Paper Lanterns) - Score: 3.95
Because: genre match (+2.0), mood match (+1.0), energy similarity (+0.95)
Focus Flow (LoRoom) - Score: 3.00
Because: genre match (+2.0), energy similarity (+1.00)
Spacewalk Thoughts (Orbit Bloom) - Score: 1.88
Because: mood match (+1.0), energy similarity (+0.88)
Coffee Shop Stories (Slow Stereo) - Score: 0.97
Because: energy similarity (+0.97)
```

**Deep Intense (conflicting edge case)** — `favorite_genre=ambient, favorite_mood=intense, target_energy=0.3`

This profile is internally contradictory: `ambient`/low-energy songs and `intense`-mood/high-energy songs pull in opposite directions.

```
Spacewalk Thoughts (Orbit Bloom) - Score: 2.98
Because: genre match (+2.0), energy similarity (+0.98)
Storm Runner (Voltline) - Score: 1.39
Because: mood match (+1.0), energy similarity (+0.39)
Gym Hero (Max Pulse) - Score: 1.37
Because: mood match (+1.0), energy similarity (+0.37)
Iron Descent (Voltline) - Score: 1.33
Because: mood match (+1.0), energy similarity (+0.33)
Riverbank Letters (Willow & Fern) - Score: 0.99
Because: energy similarity (+0.99)
```

The system doesn't detect the contradiction — it just adds up whatever points are available. Since genre is weighted higher than mood (2.0 vs 1.0), the genre match wins out and an ambient/chill song tops the list even though the user said they wanted "intense." A genuinely "intense" song like Storm Runner only manages a mood match plus a poor energy-similarity score, because its real energy (0.91) is nowhere near the requested 0.3.

---

## Experiments You Tried

**Accuracy check (Chill Lofi profile):** The top result, Midnight Coding, is a lofi/chill song with energy 0.42 against a target of 0.4 — this matches intuition well; it's exactly the kind of "vibe" a chill-lofi listener would expect. Library Rain follows closely for the same reason. This confirms the scoring logic is doing its job correctly for profiles where genre, mood, and energy all point the same direction.

**Weight shift experiment:** Doubled the energy weight (multiplying the energy-similarity term by 2.0) and halved the genre weight (1.0 instead of 2.0) for the Chill Lofi profile. The top 3 results stayed the same (Midnight Coding, Library Rain, Focus Flow) because they still win on the combination of genre + mood + energy, but their scores compressed much closer together with 4th place (Spacewalk Thoughts, ambient/chill) — going from a 3.00-vs-1.88 gap down to 3.00-vs-2.76. This shows that with the original weights genre is a decisive tiebreaker, but shrinking it makes energy-similarity alone nearly enough to close the gap between genre matches and near-misses.

**Feature removal experiment:** Commented out the mood-match term entirely and used `favorite_genre=pop, target_energy=0.85`. With mood scoring in place, Sunrise City (happy) clearly outranks the other pop songs. With mood removed, Sunrise City (happy, energy 0.82) and Victory Lap (triumphant, energy 0.88) tie exactly at 2.97 — both just genre + energy similarity — even though only one of them matches the user's stated mood. This confirms mood is the only signal separating "vibe" from raw genre/energy stats once two songs share a genre and similar energy.

---

## Limitations and Risks

- **The system over-prioritizes genre.** Because genre (+2.0) outweighs mood (+1.0), a genre match will almost always beat a mood match, even for a user who cares more about "vibe" than genre labels — the Deep Intense test above shows an ambient/chill song outranking actually-intense songs purely on genre.
- **It cannot detect contradictory preferences.** A profile like `favorite_mood=intense, target_energy=0.3` is self-contradictory (intense songs tend to be high-energy), but the scoring function has no concept of internal consistency — it just adds up whatever points are available and returns a top-k list regardless.
- **It has a "filter bubble" problem.** The system can only ever recommend songs that already match a user's stated genre/mood — it has no mechanism (like collaborative filtering) to surprise a user with something outside their stated taste, so tastes never expand.
- **The dataset is tiny and skewed toward pop/lofi.** With 20 songs and only 1-3 songs per genre outside pop/lofi, users with niche or narrow taste (e.g., classical) get very few candidates to rank, so recommendations can look repetitive.
- **It ignores tempo, valence, danceability, and acousticness** (`likes_acoustic` isn't wired into `score_song` yet) — a user who cares about danceability or lyrical positivity gets no benefit from those columns even though they're in the CSV.

See `model_card.md` for a deeper breakdown of bias and future work.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Building this recommender made concrete something that's easy to say abstractly: a recommendation is just a weighted sum of feature matches, and the weights *are* the personality of the system. Changing `GENRE_MATCH_POINTS` from 2.0 to 1.0 didn't just tweak a number — it changed what the system implicitly believes matters most to a listener. Real systems like Spotify make thousands of these same weighting decisions, just learned from data instead of hand-picked, which means their biases are harder to see and audit than mine, not because they don't exist.

The bias risk that stood out most was the genre-over-mood weighting creating a "filter bubble": since the system can only score songs against the exact genre/mood strings a user provides, it can never suggest something outside that lane the way a human friend recommending music might. Real systems face a version of this at scale — over-indexing on past behavior can trap users in a narrower and narrower slice of what they've already liked, which is a fairness/diversity concern, not just an accuracy one.
