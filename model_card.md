# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

**VibeMatch 1.0**

---

## 2. Intended Use  

VibeMatch generates a ranked list of songs from a small catalog that best match a listener's stated genre, mood, and energy preferences. It assumes the user can articulate their taste as a few simple attributes (a favorite genre, a favorite mood, a target energy level) rather than inferring taste from listening history. It is a classroom exploration of how a content-based recommender works, not a production system — it has no accounts, no persistence, and no real listener data behind it.

---

## 3. How the Model Works  

Every song in the catalog gets a score built from three pieces: 2 points if the song's genre matches the listener's favorite genre, 1 point if the song's mood matches the listener's favorite mood, and up to 1 point based on how close the song's energy level is to the energy the listener asked for (an exact match earns the full point, and the reward shrinks the further apart they are). All songs are scored this way and then sorted from highest to lowest score, and the top few are shown to the listener along with a plain-language reason for each ("genre match", "mood match", "energy similarity").

This differs from the starter logic, which just returned the first songs in the catalog with no real scoring at all — the starter shipped `TODO`s in `load_songs`, `score_song`, and `recommend_songs`, and this project's core work was implementing all three functions and the CSV-to-score-to-rank pipeline that connects them.

---

## 4. Data  

The catalog has grown from the original **10** songs to **20** songs. It spans genres including pop, lofi, rock, ambient, jazz, synthwave, indie pop, hip-hop, folk, metal, classical, r&b, edm, country, and reggae, and moods including happy, chill, intense, relaxed, moody, focused, energetic, sad, romantic, and triumphant. I added 10 songs specifically to cover genres and moods that weren't represented in the starter set (e.g., there was no metal, classical, or r&b song, and no "sad," "romantic," or "triumphant" mood before).

Even at 20 songs, most genres only have 1-2 entries, so the catalog is still far too small to reflect real musical taste — there's no representation of many popular genres (K-pop, EDM subgenres, world music, spoken word), and moods are reduced to a single label per song when real songs often blend several moods at once.

---

## 5. Strengths  

The system works best for users whose taste is "coherent" — where genre, mood, and energy preference all point in a consistent direction. For example, a Chill Lofi profile (`favorite_genre=lofi, favorite_mood=chill, target_energy=0.4`) correctly surfaces Midnight Coding and Library Rain at the top, both of which really are lofi, chill, low-energy tracks — the recommendation matches intuition exactly. The energy-similarity scoring (rewarding *closeness* to a target rather than just "high" or "low") correctly distinguishes a chill lofi song from an intense one even within the same broad mood family, which is a pattern I was worried a simpler scoring rule might miss.

---

## 6. Limitations and Bias 

The scoring function does not consider `tempo_bpm`, `valence`, `danceability`, or `acousticness` (the `likes_acoustic` field on `UserProfile` isn't wired into the score at all yet), so two songs that are identical in genre, mood, and energy but wildly different in danceability or tempo will score identically. Genres like classical, metal, and country are underrepresented (1-2 songs each), so users with those tastes get very shallow recommendation lists. The system also over-prioritizes genre (2.0 points) relative to mood (1.0 point), so it can unintentionally favor users whose favorite genre happens to be well-represented in the catalog (pop, lofi) over users whose favorite mood is a strong signal but whose genre is niche. Most strikingly, the scoring function has no way to detect internally contradictory preferences — testing a profile of `favorite_genre=ambient, favorite_mood=intense, target_energy=0.3` (a self-contradictory combination, since "intense" songs tend to be high-energy) still produced a confident top-5 list, just one built by whichever partial matches happened to score highest, with no signal to the user that their inputs didn't cohere.

---

## 7. Evaluation  

I tested three profiles: **High-Energy Pop** (`genre=pop, mood=happy, energy=0.9`), **Chill Lofi** (`genre=lofi, mood=chill, energy=0.4`), and a deliberately conflicting **Deep Intense** profile (`genre=ambient, mood=intense, energy=0.3`). For each, I looked at whether the #1 result actually matched the stated genre and mood, and whether the ranking order made intuitive sense given the reasons printed alongside each score.

The two coherent profiles (High-Energy Pop, Chill Lofi) both produced top results that matched all three criteria and felt intuitively correct. The surprise was the Deep Intense profile: rather than failing or returning nonsense, the system produced a confident-looking ranked list topped by an ambient/chill song — technically a genre match, but not remotely "intense." That the system gives no indication that the inputs were contradictory was the most interesting finding of the evaluation.

I also ran two small experiments directly against `score_song`: shifting the genre/energy weights (genre 2.0 → 1.0, energy multiplier 1.0 → 2.0) compressed the score gap between genre-matching songs and near-misses without changing the top 3 results, and removing the mood term entirely caused two same-genre, similar-energy songs with different moods (Sunrise City/happy and Victory Lap/triumphant) to tie exactly at 2.97 — concretely showing that mood is the only signal separating those two songs once genre and energy are held constant.

---

## 8. Future Work  

- Wire `likes_acoustic` and `acousticness` into `score_song`, and add `tempo_bpm`/`danceability`/`valence` as optional weighted terms so users with more specific taste get more nuanced scores.
- Add a simple contradiction check that warns a user when their stated mood and energy preference are historically uncorrelated in the catalog (e.g., "intense" moods with low energy), rather than silently returning a list.
- Introduce a small diversity constraint on the top-k results (e.g., no more than 2 songs from the same artist) so recommendations don't cluster around one artist purely because they happen to score well.
- Support multi-value preferences (e.g., "I like happy *or* chill") instead of a single favorite genre/mood, to better reflect how real listeners' tastes span more than one category at once.

---

## 9. Personal Reflection  

Building the scoring function made it obvious that a recommender is really just a set of weighted opinions about what matters, expressed as numbers instead of sentences — choosing `GENRE_MATCH_POINTS = 2.0` over `1.0` is a value judgment about what a listener cares about most, not a neutral technical choice. The most unexpected discovery was how confidently the system produced a ranked list even when I gave it a self-contradictory profile; nothing about the code "knew" the inputs didn't make sense, it just kept adding points. That changed how I think about real recommendation apps — a system that never seems to hesitate or say "I'm not sure" isn't necessarily more accurate, it might just be less equipped to notice when its assumptions about a user have gone wrong.
