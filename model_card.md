# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

VibeMatch 1.0

It matches songs to your vibe using your favorite genre, mood, and energy level.

---

## 2. Intended Use  

VibeMatch is a small learning project. It shows how a simple recommender turns data into song picks.

What it is for:

- Learning how content-based recommendations work.
- Playing with user tastes and seeing how the results change.
- Classroom exploration, not real users.

What it is not for:

- Real music apps or real users.
- Any important or high-stakes choice.
- Judging songs, artists, or people in a fair way. It is too simple for that.

It assumes the user can name one favorite genre, one mood, an energy level, and whether they like acoustic music.

---

## 3. How the Model Works  

Each song starts with 0 points. Then the model adds points with four simple rules:

- Same genre as your favorite: add 2 points.
- Same mood as your favorite: add 1.5 points.
- Energy close to what you want: up to 2 points.
- Acoustic feel matches your taste: add 1.5 points.

The energy rule rewards being close to your target, not just high or low. So if you want 0.9 and a song is 0.91, it gets almost full points. A song far from your target gets fewer.

After every song has a score, the model sorts them from most points to least and shows the top 5. Each pick comes with a short reason, like "matches your favorite genre" or "energy is very close to what you wanted."

I built this from the starter files. I filled in the loading, scoring, and ranking, added more songs, and made the user profile use four clear preferences.

---

## 4. Data  

The catalog has 18 songs. It started with 10 and I added 8 more.

Each song has these features:

- id, title, artist
- genre and mood (words)
- energy, tempo, valence, danceability, acousticness (numbers from 0 to 1)

The scoring only uses genre, mood, energy, and acousticness for now.

Genres include pop, lofi, rock, jazz, ambient, synthwave, indie pop, classical, hip hop, metal, folk, edm, r&b, blues, and reggae. Moods include happy, chill, intense, relaxed, moody, focused, peaceful, groovy, aggressive, nostalgic, energetic, romantic, melancholic, and uplifting.

Limits of the data:

- It is small. 18 songs is tiny.
- The songs are made up, not real.
- Most genres only appear once, and lofi appears the most (3 times).
- The energy values clump at the low and high ends, with few songs in the middle.
- It has no lyrics, language, or real listening history.

---

## 5. Strengths  

- It works well for clear tastes. A pop fan gets pop, a lofi fan gets lofi.
- It is best at the energy extremes. Chill users and high-energy users get tight, on-target lists.
- The energy rule feels right. It picks songs near your target instead of just the loudest or quietest.
- It always gives a reason for each pick, so the results are easy to understand.
- It never crashes on weird input. Empty or unknown tastes still return a safe list.
- The top pick usually matched my own gut feeling for who the profile was.

---

## 6. Limitations and Bias 

One weakness I found during my experiments is an "energy dead zone" that quietly favors some users over others. The song catalog is bimodal in energy: out of 18 songs, 8 are low energy (0.45 or below) and 7 are high energy (0.72 or above), but only 3 sit in the middle. Because energy closeness is the one rule that fires for every user, this shape decides who gets served well: a chill user (target around 0.3) and a high-energy user (target around 0.9) each have 7 to 8 songs sitting right on their target, so their whole top 5 is a tight match. A moderate-energy user (target around 0.6) finds only one perfect song, and the rest of their list has to reach into the low or high clusters, so their recommendations are noticeably less consistent even though their taste is perfectly reasonable. In other words, the way I calculate the energy gap does not ignore mid-energy listeners outright, but it systematically gives them worse recommendations, and my weight-shift experiment (energy weighted 4x) made this even more pronounced.

---

## 7. Evaluation  

I tested the recommender with three normal user profiles and three adversarial / edge-case profiles to see if the scoring could be tricked. For each one I looked at the top 5 songs and their reasons. All output below is real terminal output from running the recommender.

### Normal profile 1: High-Energy Pop

```
Profile: genre=pop, mood=happy, energy=0.9, acoustic=no
 6.84  Sunrise City       (pop/happy)
       Because: matches your favorite genre (pop); fits your mood (happy); energy is very close to what you wanted; has the electronic feel you like
 5.44  Gym Hero           (pop/intense)
       Because: matches your favorite genre (pop); energy is very close to what you wanted; has the electronic feel you like
 4.72  Rooftop Lights     (indie pop/happy)
       Because: fits your mood (happy); energy is very close to what you wanted; has the electronic feel you like
 3.48  Storm Runner       (rock/intense)
       Because: energy is very close to what you wanted; has the electronic feel you like
 3.40  Neon Overdrive     (edm/energetic)
       Because: energy is very close to what you wanted; has the electronic feel you like
```

### Normal profile 2: Chill Lofi

```
Profile: genre=lofi, mood=chill, energy=0.3, acoustic=yes
 6.90  Library Rain       (lofi/chill)
       Because: matches your favorite genre (lofi); fits your mood (chill); energy is very close to what you wanted; has the acoustic feel you like
 6.76  Midnight Coding    (lofi/chill)
       Because: matches your favorite genre (lofi); fits your mood (chill); energy is very close to what you wanted; has the acoustic feel you like
 5.30  Focus Flow         (lofi/focused)
       Because: matches your favorite genre (lofi); energy is very close to what you wanted; has the acoustic feel you like
 4.96  Spacewalk Thoughts (ambient/chill)
       Because: fits your mood (chill); energy is very close to what you wanted; has the acoustic feel you like
 3.36  Coffee Shop Stories (jazz/relaxed)
       Because: energy is very close to what you wanted; has the acoustic feel you like
```

### Normal profile 3: Deep Intense Rock

```
Profile: genre=rock, mood=intense, energy=0.85, acoustic=no
 6.88  Storm Runner       (rock/intense)
       Because: matches your favorite genre (rock); fits your mood (intense); energy is very close to what you wanted; has the electronic feel you like
 4.84  Gym Hero           (pop/intense)
       Because: fits your mood (intense); energy is very close to what you wanted; has the electronic feel you like
 3.44  Sunrise City       (pop/happy)
       Because: energy is very close to what you wanted; has the electronic feel you like
 3.32  Rooftop Lights     (indie pop/happy)
       Because: energy is very close to what you wanted; has the electronic feel you like
 3.30  Night Drive Loop   (synthwave/moody)
       Because: energy is very close to what you wanted; has the electronic feel you like
```

The three normal profiles all behaved as expected: the "perfect" song landed on top with all four rules firing, and the list then filled in with partial matches. The system clearly separated the three tastes.

### Adversarial profile: conflicting preferences

I built a profile that asks for things that don't go together: metal genre, sad (melancholic) mood, very high energy (0.95), AND an acoustic feel. No real song can be all of these at once.

```
Profile: genre=metal, mood=melancholic, energy=0.95, acoustic=yes
 3.96  Iron Verdict       (metal/aggressive)
       Because: matches your favorite genre (metal); energy is very close to what you wanted
 3.90  Rainy Avenue Blues (blues/melancholic)
       Because: fits your mood (melancholic); has the acoustic feel you like
 2.44  Midnight Coding    (lofi/chill)
       Because: has the acoustic feel you like
 2.40  Focus Flow         (lofi/focused)
       Because: has the acoustic feel you like
 2.36  Old Pine Road      (folk/nostalgic)
       Because: has the acoustic feel you like
```

This is the most revealing result. Because no song can satisfy the contradiction, the scores stay low and the top two are pulled in opposite directions: a loud electronic metal track (matching genre + energy) is basically tied with a slow acoustic sad song (matching mood + acoustic). The system has no idea these preferences conflict, it just adds up whatever happens to match. Even worse, songs that match only ONE preference (like lofi tracks that are simply acoustic) rank surprisingly high. This shows the additive model can be "tricked": a single strong attribute can carry a song that fits the user in no other way.

### Edge case: empty profile (no preferences)

```
Profile: {} (no preferences given)
 0.00  Sunrise City       (pop/happy)
       Because: no strong match, included to round out your list
 0.00  Midnight Coding    (lofi/chill)
       Because: no strong match, included to round out your list
 0.00  Storm Runner       (rock/intense)
       Because: no strong match, included to round out your list
 0.00  Library Rain       (lofi/chill)
       Because: no strong match, included to round out your list
 0.00  Gym Hero           (pop/intense)
       Because: no strong match, included to round out your list
```

With no preferences, every rule is skipped and every song scores 0.00. It does not crash, and the fallback reason kicks in. The order is just the catalog order (by id), because the id tie-breaker decides everything.

### Edge case: genre and mood that aren't in the catalog

```
Profile: genre=kpop, mood=party, energy=0.5, acoustic=no
 3.46  Velvet Hours       (r&b/romantic)
       Because: energy is very close to what you wanted; has the electronic feel you like
 3.30  Island Sunlight    (reggae/uplifting)
       Because: energy is very close to what you wanted; has the electronic feel you like
 3.14  Sidewalk Flow      (hip hop/groovy)
       Because: energy is fairly close to what you wanted; has the electronic feel you like
 3.00  Night Drive Loop   (synthwave/moody)
       Because: energy is fairly close to what you wanted; has the electronic feel you like
 2.98  Rooftop Lights     (indie pop/happy)
       Because: energy is fairly close to what you wanted; has the electronic feel you like
```

"kpop" and "party" don't exist in the data, so the genre and mood rules never fire. The system falls back to ranking purely on energy closeness and acoustic feel. It degrades gracefully instead of returning nothing.

### Comparing the profiles

- Pop vs Lofi: total opposites, no songs in common. Pop pulls loud electronic tracks, Lofi pulls quiet acoustic ones. Makes sense since their energy and acoustic tastes are flipped.
- Pop vs Rock: lists overlap a lot because both want high energy. The difference is the top pick: Pop crowns a happy song, Rock crowns an intense one. Energy picks the pool, genre and mood pick the winner.
- Lofi vs Rock: opposite ends again, no overlap. One stays low energy, the other high. This is the energy dead zone in action.
- Normal vs conflicting profile: normal profiles score around 6.8, the conflicting one tops out at 3.96. Makes sense, since no single song can match preferences that fight each other.
- Normal vs empty profile: normal profiles spread out the scores, the empty one makes everything 0.00 and just uses id order. With no preferences there is nothing to sort by.
- In-catalog vs unknown genre: real genres score near 6 to 7, unknown ones cap around 3.4 on energy and acoustic alone. Shows how much genre and mood add.

### What I looked for and what surprised me

- I checked that each normal profile put its "obvious" best song on top, and it did.
- I checked that the recommender never crashed on weird input (empty, unknown genres), and it didn't.
- The surprise was the conflicting profile: I expected low scores, but I did not expect songs matching only one preference (just "acoustic") to beat more balanced songs. It made the "over-prioritizes any single matching feature" weakness very visible.

---

## 8. Future Work  

If I kept building this, I would:

- Teach it that genres can be similar. Right now rock gets no credit for metal, even though they are close. A similarity map would fix this.
- Use more of the features. Tempo, valence, and danceability are in the data but not scored yet. Adding them would tell songs apart better.
- Add more songs, especially mid-energy ones. A bigger and more even catalog would help the users who now get weak lists.

---

## 9. Personal Reflection  

I learned that a recommender is really just a scoring rule plus a sort. The "smart" feeling comes from simple math on a few features.

The surprising part was how much the data shape matters. My energy rule looked fair, but because the songs clump at the extremes, mid-energy users quietly got worse results. I did not plan that bias, it just came from the data.

Now I think about music apps differently. When one suggests a song, I picture the points being added up behind it, and I wonder which of my habits it is really scoring.
