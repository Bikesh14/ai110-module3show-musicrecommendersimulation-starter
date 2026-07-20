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

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this
