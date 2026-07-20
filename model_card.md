# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

**VibeMatch 1.0**

---

## 2. Goal / Task

VibeMatch suggests songs a listener will like based on a few taste settings they give it. It takes a favorite genre, a favorite mood, and a target energy level, and returns a ranked list of the best-matching songs from the catalog. It does not look at listening history or other users — only the attributes of the songs and the one profile it's given.

---

## 3. Data Used

The catalog is a CSV file with 20 songs. Each song has: `genre`, `mood`, `energy`, `tempo_bpm`, `valence`, `danceability`, and `acousticness`. It started with 10 songs and I added 10 more to cover genres and moods that were missing, like metal, classical, r&b, and moods like sad, romantic, and triumphant.

Limits: most genres only have 1-2 songs, so niche tastes get very few options. Only `genre`, `mood`, and `energy` are actually used in scoring right now — `tempo_bpm`, `valence`, `danceability`, and `acousticness` are loaded but ignored.

---

## 4. Algorithm Summary

Each song gets a score:

- +2 points if the song's genre matches the user's favorite genre
- +1 point if the song's mood matches the user's favorite mood
- Up to +1 point based on how close the song's energy is to the user's target energy (closer = more points, not just "high energy is good")

All songs get scored this way, then get sorted highest to lowest, and the top few are returned along with the reasons for each score.

---

## 5. Observed Behavior / Biases

Genre counts for more than mood (2 points vs. 1 point), so a genre match almost always beats a mood match. This means a user who cares more about mood than genre label can get recommendations that technically fit their genre but miss their vibe. It also means genres with more songs in the catalog (like pop and lofi) get recommended more confidently than genres with only 1-2 songs.

---

## 6. Evaluation Process

I tested three profiles:

- **High-Energy Pop** (`genre=pop, mood=happy, energy=0.9`)
- **Chill Lofi** (`genre=lofi, mood=chill, energy=0.4`)
- **Deep Intense** (`genre=ambient, mood=intense, energy=0.3`) — a profile I made up on purpose to contradict itself, since "intense" songs are usually high energy, not low.

The first two profiles gave results that matched my intuition right away. The third one was the interesting case: the system still gave a confident top-5 list, just built from whatever partial matches scored highest, with no sign that the inputs didn't make sense together.

I also ran two small experiments directly on the scoring code:

- Lowered the genre weight and raised the energy weight — the top 3 results stayed the same, but the score gap between them and the next songs got much smaller.
- Removed the mood check entirely — two pop songs with different moods (one happy, one triumphant) tied at the exact same score, showing mood was the only thing telling them apart.

---

## 7. Intended Use and Non-Intended Use

**Intended use:** a classroom exercise to explore how a simple content-based recommender turns a few taste attributes into a ranked list, and to practice noticing bias and limitations in that process.

**Not intended for:**
- Real listeners or a production app — the catalog is tiny and made up.
- Any claim that this is how real streaming platforms work — real systems mostly use collaborative filtering plus much larger, learned models, not a hand-picked point system.
- Any use where the ranking needs to be fair across many users — this system has no way to check or correct for the genre-over-mood bias described above.

---

## 8. Ideas for Improvement

1. Add `acousticness`, `tempo_bpm`, and `danceability` into the scoring, and actually use `likes_acoustic` instead of ignoring it.
2. Add a check that flags contradictory profiles (like "intense" mood with very low target energy) instead of silently returning a confident-looking list.
3. Add a diversity rule so the top results don't all come from the same artist or the same 1-2 well-represented genres.

---

## 9. Personal Reflection

My biggest learning moment was seeing that a recommender is really just a list of weighted opinions turned into numbers — deciding genre is worth 2 points and mood is worth 1 point is a value judgment, not a neutral fact, and changing that number changes what the system "believes" a listener cares about.

I used my AI coding assistant throughout: to research collaborative vs. content-based filtering before writing any code, to help design the scoring formula and explain why both a scoring rule and a ranking rule are needed, and to implement `load_songs`, `score_song`, and `recommend_songs`. I double-checked its work by actually running the weight-shift and mood-removal experiments myself instead of trusting a description of what "should" happen — one of my first draft claims about the weight-shift experiment turned out to be wrong when I actually ran it, so I corrected it against the real output.

What surprised me most is how confident a very simple algorithm can feel. Even a plain point-adding system with no learning at all produced ranked lists that felt intuitive for normal profiles, and it never hesitated even on a profile I deliberately made contradictory — it just added up whatever points existed. That's what changed my thinking about real recommendation apps: a system sounding confident says nothing about whether its assumptions about you were actually correct.

If I kept extending this, I'd add the unused features (tempo, danceability, acousticness) to the score first, since that's the most direct way to make recommendations feel more personalized without changing the overall design.
