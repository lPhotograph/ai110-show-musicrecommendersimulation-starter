import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass, asdict

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

def _user_to_prefs(user: UserProfile) -> Dict:
    """Turn a UserProfile into the prefs dict that score_song expects."""
    return {
        "favorite_genre": user.favorite_genre,
        "favorite_mood": user.favorite_mood,
        "target_energy": user.target_energy,
        "likes_acoustic": user.likes_acoustic,
    }


class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py

    This reuses the same scoring recipe as score_song() by converting each
    Song dataclass to a dict, so the OOP and functional paths stay in sync.
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Score every song for this user and return the top k, best first."""
        prefs = _user_to_prefs(user)

        scored = []
        for song in self.songs:
            score, _ = score_song(prefs, asdict(song))
            energy_gap = abs(user.target_energy - song.energy)
            scored.append((song, score, energy_gap))

        # Highest score first; tie-break by energy closeness, then id.
        scored.sort(key=lambda item: (-item[1], item[2], item[0].id))

        return [song for song, _, _ in scored[:k]]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Return a short, human-readable reason for why this song fits the user."""
        prefs = _user_to_prefs(user)
        _, reasons = score_song(prefs, asdict(song))
        if reasons:
            return "; ".join(reasons)
        return "no strong match, included to round out your list"

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file and returns a list of dictionaries.

    Each row becomes one dict. The id is converted to an int and the
    numeric feature columns are converted to floats so the scoring logic
    can do math on them. Text columns (title, artist, genre, mood) stay
    as strings.

    Required by src/main.py
    """
    numeric_fields = (
        "energy",
        "tempo_bpm",
        "valence",
        "danceability",
        "acousticness",
    )

    songs: List[Dict] = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Skip fully blank lines (e.g. a trailing newline in the CSV).
            if not row.get("id"):
                continue
            song = dict(row)
            song["id"] = int(song["id"])
            for field in numeric_fields:
                song[field] = float(song[field])
            songs.append(song)

    return songs

# Weights for the Algorithm Recipe (see README "My Algorithm Recipe").
GENRE_WEIGHT = 2.0
MOOD_WEIGHT = 1.5
ENERGY_WEIGHT = 2.0
ACOUSTIC_WEIGHT = 1.5

# A song counts as "acoustic" above this, and "electronic" below the low mark.
ACOUSTIC_HIGH = 0.6
ACOUSTIC_LOW = 0.4


def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores a single song against user preferences.

    Judges ONE song on its own (no comparing to other songs). Adds points
    with the four-rule recipe and collects a short reason for every rule
    that actually fired.

    user_prefs may contain: favorite_genre, favorite_mood, target_energy,
    likes_acoustic. Any missing key just skips that rule instead of crashing.

    Returns (score, reasons).
    Required by recommend_songs() and src/main.py
    """
    score = 0.0
    reasons: List[str] = []

    # Rule 1: genre match (exact text match).
    favorite_genre = user_prefs.get("favorite_genre")
    if favorite_genre is not None and favorite_genre == song["genre"]:
        score += GENRE_WEIGHT
        reasons.append(f"matches your favorite genre ({song['genre']})")

    # Rule 2: mood match (exact text match).
    favorite_mood = user_prefs.get("favorite_mood")
    if favorite_mood is not None and favorite_mood == song["mood"]:
        score += MOOD_WEIGHT
        reasons.append(f"fits your mood ({song['mood']})")

    # Rule 3: energy closeness. Reward being CLOSE to the target, not just
    # high or low. Both values are on a 0-1 scale, so the gap is at most 1.
    target_energy = user_prefs.get("target_energy")
    if target_energy is not None:
        closeness = 1.0 - abs(target_energy - song["energy"])
        closeness = max(0.0, closeness)  # never go negative
        score += ENERGY_WEIGHT * closeness
        if closeness >= 0.85:
            reasons.append("energy is very close to what you wanted")
        elif closeness >= 0.6:
            reasons.append("energy is fairly close to what you wanted")

    # Rule 4: acoustic feel matches the user's taste.
    likes_acoustic = user_prefs.get("likes_acoustic")
    if likes_acoustic is not None:
        acousticness = song["acousticness"]
        if likes_acoustic and acousticness >= ACOUSTIC_HIGH:
            score += ACOUSTIC_WEIGHT
            reasons.append("has the acoustic feel you like")
        elif not likes_acoustic and acousticness <= ACOUSTIC_LOW:
            score += ACOUSTIC_WEIGHT
            reasons.append("has the electronic feel you like")

    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Ranks the whole catalog and returns the top k recommendations.

    Steps:
      1. Score every song with score_song (the loop).
      2. Sort by score, highest first.
      3. Break ties by energy closeness, then by id, so the order is stable.
      4. Keep the top k and turn each song's reasons into one explanation string.

    Returns a list of (song_dict, score, explanation).
    Required by src/main.py
    """
    target_energy = user_prefs.get("target_energy")

    scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)

        # Tie-breakers: closer energy wins, then lower id (stable + deterministic).
        if target_energy is not None:
            energy_gap = abs(target_energy - song["energy"])
        else:
            energy_gap = 0.0

        if reasons:
            explanation = "; ".join(reasons)
        else:
            explanation = "no strong match, included to round out your list"

        scored.append((song, score, explanation, energy_gap))

    # Highest score first; on a tie, smallest energy gap; then smallest id.
    scored.sort(key=lambda item: (-item[1], item[3], item[0]["id"]))

    # Drop the internal tie-break value before returning.
    return [(song, score, explanation) for song, score, explanation, _ in scored[:k]]
