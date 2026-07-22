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
Explain your design in plain language.


Apps like Spotify and YouTube guess what you'll like next in two main ways. One is by looking at other people: if someone with taste like yours loved a song, it gets suggested to you too. The other is by looking at the songs themselves: it checks things like tempo, mood, and energy, and finds songs similar to the ones you already like. Big apps mix both.

My version keeps it simple and only uses the second idea, since I don't have data on other users. It looks at each song's features and compares them to what the user says they like. It gives points when the genre and mood match, and more points when the song's energy and acoustic feel are close to what the user wants (not just high or low). Then it sorts all the songs by their points and shows the top few, with a short reason for each one.

Here's what each part uses:

Each Song has: id, title, artist, genre, mood, energy, tempo_bpm, valence, danceability, and acousticness. Out of these, my scoring only uses genre, mood, energy, and acousticness for now. The rest (tempo, valence, danceability) are there if I want to add them later.

Each UserProfile stores: favorite_genre, favorite_mood, target_energy, and likes_acoustic.

How they match up:

- `favorite_genre` → `genre` (points if they're the same)
- `favorite_mood` → `mood` (points if they're the same)
- `target_energy` → `energy` (more points the closer they are)
- likes_acoustic to acousticness (points if the acoustic feel matches what the user likes)

### My Algorithm Recipe

Every song starts at 0 points. Then I add points with four simple rules:

- Genre match: if the song's genre is the same as the user's favorite genre, add 2 points.
- Mood match: if the song's mood is the same as the user's favorite mood, add 1.5 points.
- Energy closeness: up to 2 points for how close the song's energy is to what the user wants.
- Acoustic match: if the acoustic feel lines up with what the user likes, add 1.5 points.

For the energy rule I don't reward "high" or "low", I reward being close to what the user asked for. The idea is: energy points = 2 times (1 minus the gap between the user's energy and the song's energy). So if the user wants 0.9 and the song is 0.91, that is almost a perfect match. A song at 0.4 is far away, so it gets fewer points.

Picking the songs: I score every song with these rules, sort them from most points to least, break ties using energy closeness, and show the top few (like the top 5). Each pick also gets a short reason based on which rules matched.

Here is an example taste profile for a rock fan who likes it energetic:

- favorite_genre: rock
- favorite_mood: intense
- target_energy: 0.9
- likes_acoustic: false

With this profile, Storm Runner (intense rock, high energy) scores around 7 while Midnight Coding (chill lofi) scores around 1, so the system clearly tells them apart.

### Biases I expect

- It leans too hard on genre. Genre is worth the most points, so a song that matches the user's mood and energy really well can still lose to a same-genre song that isn't actually a better fit.
- The matching is too strict. Genre and mood only count if the text matches exactly. A rock fan gets no credit for metal, and someone who likes "intense" gets nothing for "aggressive", even though these are close.
- The song list is small and uneven. With only 18 songs and some genres showing up just once, the results lean toward whatever genres and moods are common in the data.
- It ignores some features. Tempo, valence, and danceability are not scored yet, so two songs that feel different but share genre, mood, and energy look the same to the system.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

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

This is the real output from running `python -m src.main` with the example profile
(favorite_genre: pop, favorite_mood: happy, target_energy: 0.8, likes_acoustic: false):


Top recommendations:

Sunrise City - Score: 6.96
Because: matches your favorite genre (pop); fits your mood (happy); energy is very close to what you wanted; has the electronic feel you like

Gym Hero - Score: 5.24
Because: matches your favorite genre (pop); energy is very close to what you wanted; has the electronic feel you like

Rooftop Lights - Score: 4.92
Because: fits your mood (happy); energy is very close to what you wanted; has the electronic feel you like

Night Drive Loop - Score: 3.40
Because: energy is very close to what you wanted; has the electronic feel you like

Storm Runner - Score: 3.28
Because: energy is very close to what you wanted; has the electronic feel you like


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



