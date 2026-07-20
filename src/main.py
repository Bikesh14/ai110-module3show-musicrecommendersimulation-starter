"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from src.recommender import load_songs, recommend_songs, format_recommendations_table, SCORING_MODES


def run_profile(songs, user_prefs, mode="balanced", diversify=False, k=5) -> None:
    recommendations = recommend_songs(user_prefs, songs, k=k, mode=mode, diversify=diversify)

    print(
        f"\nUser profile: genre={user_prefs['favorite_genre']}, "
        f"mood={user_prefs['favorite_mood']}, energy={user_prefs['target_energy']} "
        f"(mode={mode}, diversify={diversify})"
    )
    print()
    print(format_recommendations_table(recommendations))


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    # Starter example profile
    user_prefs = {
        "favorite_genre": "pop",
        "favorite_mood": "happy",
        "target_energy": 0.8,
        "likes_acoustic": False,
        "favorite_vibe": "euphoric",
    }

    for mode in SCORING_MODES:
        run_profile(songs, user_prefs, mode=mode)

    run_profile(songs, user_prefs, mode="balanced", diversify=True)


if __name__ == "__main__":
    main()
