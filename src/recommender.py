import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
from tabulate import tabulate

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float
    popularity: float = 0.0
    release_decade: str = ""
    is_nostalgic: bool = False
    is_aggressive: bool = False
    is_euphoric: bool = False

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool
    favorite_vibe: Optional[str] = None  # "nostalgic", "aggressive", or "euphoric"

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"

NUMERIC_FIELDS = {"energy", "tempo_bpm", "valence", "danceability", "acousticness", "popularity"}
BOOLEAN_FIELDS = {"is_nostalgic", "is_aggressive", "is_euphoric"}


def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file, converting numeric and boolean columns
    to their Python types.
    Required by src/main.py
    """
    print(f"Loading songs from {csv_path}...")
    songs = []
    with open(csv_path, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            for field in NUMERIC_FIELDS:
                row[field] = float(row[field])
            for field in BOOLEAN_FIELDS:
                row[field] = row[field].strip().lower() == "true"
            row["id"] = int(row["id"])
            songs.append(row)
    return songs

ACOUSTIC_MATCH_POINTS = 0.5
VIBE_MATCH_POINTS = 0.5
ACOUSTIC_THRESHOLD = 0.6
VIBE_FIELDS = {
    "nostalgic": "is_nostalgic",
    "aggressive": "is_aggressive",
    "euphoric": "is_euphoric",
}


def _score_with_weights(
    user_prefs: Dict, song: Dict, genre_weight: float, mood_weight: float, energy_weight: float
) -> Tuple[float, List[str]]:
    """
    Shared scoring core used by every scoring mode (the "Strategy" objects
    below just plug in different weights here). Rewards a genre match, a
    mood match, energy closeness, an acoustic-preference match, a favorite
    vibe tag match, and a small popularity bonus.
    """
    score = 0.0
    reasons = []

    if song["genre"] == user_prefs["favorite_genre"]:
        score += genre_weight
        reasons.append(f"genre match (+{genre_weight:.1f})")

    if song["mood"] == user_prefs["favorite_mood"]:
        score += mood_weight
        reasons.append(f"mood match (+{mood_weight:.1f})")

    energy_similarity = (1.0 - abs(song["energy"] - user_prefs["target_energy"])) * energy_weight
    score += energy_similarity
    reasons.append(f"energy similarity (+{energy_similarity:.2f})")

    is_acoustic = song["acousticness"] > ACOUSTIC_THRESHOLD
    likes_acoustic = user_prefs.get("likes_acoustic", False)
    if is_acoustic == likes_acoustic:
        score += ACOUSTIC_MATCH_POINTS
        reasons.append(f"acoustic preference match (+{ACOUSTIC_MATCH_POINTS:.1f})")

    favorite_vibe = user_prefs.get("favorite_vibe")
    vibe_field = VIBE_FIELDS.get(favorite_vibe)
    if vibe_field and song.get(vibe_field):
        score += VIBE_MATCH_POINTS
        reasons.append(f"{favorite_vibe} vibe match (+{VIBE_MATCH_POINTS:.1f})")

    popularity_bonus = song.get("popularity", 0.0) / 100 * 0.2
    score += popularity_bonus
    reasons.append(f"popularity bonus (+{popularity_bonus:.2f})")

    return score, reasons


def score_song_balanced(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Default strategy: genre +2.0, mood +1.0, energy similarity up to +1.0."""
    return _score_with_weights(user_prefs, song, genre_weight=2.0, mood_weight=1.0, energy_weight=1.0)


def score_song_genre_first(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Strategy that leans harder on genre: genre +3.0, mood +0.5, energy up to +0.5."""
    return _score_with_weights(user_prefs, song, genre_weight=3.0, mood_weight=0.5, energy_weight=0.5)


def score_song_mood_first(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Strategy that leans harder on mood: genre +0.5, mood +3.0, energy up to +0.5."""
    return _score_with_weights(user_prefs, song, genre_weight=0.5, mood_weight=3.0, energy_weight=0.5)


def score_song_energy_focused(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Strategy that leans harder on energy: genre +0.5, mood +0.5, energy up to +3.0."""
    return _score_with_weights(user_prefs, song, genre_weight=0.5, mood_weight=0.5, energy_weight=3.0)


SCORING_MODES = {
    "balanced": score_song_balanced,
    "genre-first": score_song_genre_first,
    "mood-first": score_song_mood_first,
    "energy-focused": score_song_energy_focused,
}


def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores a single song against user preferences using the default
    ("balanced") Algorithm Recipe. Required by recommend_songs() and src/main.py.
    """
    return score_song_balanced(user_prefs, song)


ARTIST_REPEAT_PENALTY = 1.0
GENRE_REPEAT_PENALTY = 0.5


def recommend_songs(
    user_prefs: Dict,
    songs: List[Dict],
    k: int = 5,
    mode: str = "balanced",
    diversify: bool = False,
) -> List[Tuple[Dict, float, str]]:
    """
    Scores every song using the chosen scoring strategy (see SCORING_MODES),
    then ranks them highest-to-lowest and returns the top k. The scoring
    function is the "judge" for a single song; sorted() finds the best of
    them across the whole catalog.

    If diversify is True, songs are picked one at a time, and a song's
    score is penalized if its artist or genre already appears earlier in
    the results, so one artist or genre can't dominate the top k.
    Required by src/main.py
    """
    scorer = SCORING_MODES.get(mode, score_song_balanced)

    scored = []
    for song in songs:
        score, reasons = scorer(user_prefs, song)
        explanation = ", ".join(reasons)
        scored.append((song, score, explanation))

    if not diversify:
        ranked = sorted(scored, key=lambda item: item[1], reverse=True)
        return ranked[:k]

    remaining = sorted(scored, key=lambda item: item[1], reverse=True)
    results = []
    seen_artists = set()
    seen_genres = set()

    while remaining and len(results) < k:
        best_index = None
        best_adjusted_score = None
        for i, (song, score, explanation) in enumerate(remaining):
            adjusted_score = score
            if song["artist"] in seen_artists:
                adjusted_score -= ARTIST_REPEAT_PENALTY
            if song["genre"] in seen_genres:
                adjusted_score -= GENRE_REPEAT_PENALTY
            if best_adjusted_score is None or adjusted_score > best_adjusted_score:
                best_adjusted_score = adjusted_score
                best_index = i

        song, score, explanation = remaining.pop(best_index)
        if song["artist"] in seen_artists or song["genre"] in seen_genres:
            explanation += f", diversity-adjusted score: {best_adjusted_score:.2f}"
        results.append((song, score, explanation))
        seen_artists.add(song["artist"])
        seen_genres.add(song["genre"])

    return results


def format_recommendations_table(recommendations: List[Tuple[Dict, float, str]]) -> str:
    """
    Formats a list of (song, score, explanation) tuples as a readable table
    with columns for rank, title, artist, score, and reasons.
    """
    rows = []
    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        rows.append([rank, song["title"], song["artist"], f"{score:.2f}", explanation])

    headers = ["#", "Title", "Artist", "Score", "Reasons"]
    return tabulate(rows, headers=headers, tablefmt="github")
