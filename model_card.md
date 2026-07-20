# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

**VibeMatch 1.0**

---

## 2. Goal / Task

VibeMatch suggests songs a listener will like based on a few taste settings: a favorite genre, a favorite mood, and a target energy level. It returns a ranked list of the best-matching songs from a fixed catalog. It does not use listening history or data from other users — only the attributes of the songs and the one profile it's given.

---

## 3. Data Used

The catalog is a CSV file (`data/songs.csv`) with 20 songs. Each song has:

- `genre`, `mood` — text labels
- `energy`, `tempo_bpm`, `valence`, `danceability`, `acousticness`, `popularity` — numbers
- `release_decade` — text label (e.g. "1990s")
- `is_nostalgic`, `is_aggressive`, `is_euphoric` — true/false mood tags

The catalog covers 15 genres (pop, lofi, rock, ambient, jazz, synthwave, indie pop, hip-hop, folk, metal, classical, r&b, edm, country, reggae) and 10 moods (happy, chill, intense, relaxed, moody, focused, energetic, sad, romantic, triumphant).

**Limits:** most genres have only 1-2 songs, so niche tastes get very few options. `release_decade`, `tempo_bpm`, `valence`, and `danceability` are loaded but not currently used in scoring.

---

## 4. Algorithm Summary

Each song gets a score built from several parts:

- Points for a genre match
- Points for a mood match
- Points for how close the song's energy is to the user's target energy (closer = more points)
- A small bonus if the song's acoustic level matches the user's acoustic preference
- A small bonus if the song's mood tag (nostalgic, aggressive, or euphoric) matches the user's favorite vibe
- A small bonus for popularity

All songs are scored this way, sorted from highest to lowest, and the top few are returned along with the reasons behind each score.

The genre/mood/energy point values can be adjusted by scoring mode — see the **Design Notes** below.

---

## 5. Design Notes

**Scoring modes:** the point values above can shift depending on the mode selected in `recommend_songs(mode=...)`:

| Mode | Genre | Mood | Energy |
|---|---|---|---|
| Balanced (default) | 2.0 | 1.0 | up to 1.0 |
| Genre-First | 3.0 | 0.5 | up to 0.5 |
| Mood-First | 0.5 | 3.0 | up to 0.5 |
| Energy-Focused | 0.5 | 0.5 | up to 3.0 |

**Diversity option:** `recommend_songs(diversify=True)` reduces a song's score if its artist or genre already appears earlier in the results, so the top list doesn't cluster around one artist or genre.

---

## 6. Observed Behavior / Biases

In the default (Balanced) mode, genre counts for more than mood, so a genre match usually beats a mood match. A user who cares more about mood than genre label can get results that fit their genre but miss their vibe. Genres with more songs in the catalog (pop, lofi) also get recommended more confidently than genres with only 1-2 songs.

---

## 7. Evaluation Process

Three profiles were tested:

- **High-Energy Pop** (`genre=pop, mood=happy, energy=0.9`)
- **Chill Lofi** (`genre=lofi, mood=chill, energy=0.4`)
- **Deep Intense** (`genre=ambient, mood=intense, energy=0.3`) — built on purpose to contradict itself, since "intense" songs are usually high energy, not low.

The first two profiles produced results that matched intuition. The third profile still produced a confident top-5 list, built from whatever partial matches scored highest, with no signal that the inputs didn't make sense together.

Two scoring experiments were also run directly against the code:

- Lowering the genre weight and raising the energy weight kept the same top 3 songs, but shrank the score gap between them and the next songs.
- Removing the mood check entirely caused two same-genre songs with different moods to tie at the same score, showing mood was the only thing telling them apart.

---

## 8. Intended Use and Non-Intended Use

**Intended use:** a classroom exercise for exploring how a simple content-based recommender turns a few taste attributes into a ranked list, and for practicing how to spot bias and limitations in that process.

**Not intended for:**
- Real listeners or a production app — the catalog is small and made up.
- Representing how real streaming platforms work — those mostly use collaborative filtering and much larger, learned models, not a fixed point system.
- Any use where fairness across many users matters — this system has no way to check or correct the genre-over-mood bias described above.

---

## 9. Ideas for Improvement

1. Bring `tempo_bpm`, `valence`, and `danceability` into scoring instead of leaving them unused.
2. Detect contradictory profiles (e.g., "intense" mood with very low energy) and flag them instead of returning a confident-looking list anyway.
3. Expand the diversity logic to also balance across moods and decades, not just artists and genres.

---

## 10. Reflection

Building the scoring logic made the tradeoffs concrete: choosing how many points a genre match is worth versus a mood match directly decides what kind of "taste" the system favors. The most useful test was the deliberately contradictory profile — it showed the system will always return a confident-looking list, even from inputs that don't make sense together, because nothing in the scoring checks for that.

Next step if extended further: add a contradiction check (see Ideas for Improvement above) so the system can flag unclear input instead of silently ranking around it.
