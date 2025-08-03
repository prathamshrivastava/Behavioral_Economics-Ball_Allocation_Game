#  GridBall: A Behavioral Game of Greed vs. Altruism

**GridBall** is an interactive web-based game for 3 players that explores decision-making dynamics between private gain and public cost. It's designed as an experimental tool for behavioral economics studies.

##  Game Concept

Each player sees:
- **9 balls** per round
- A **Private Grid** and a **Public Grid**

Over **10 rounds**, players must decide how to allocate their 9 balls between these two grids, weighing personal rewards against group penalties.

###  Rules

- Players are grouped into **teams of 3**.
- Each player plays **independently** in each round.

#### Private Grid:
- Each ball placed gives **decreasing points**:
  - 1st ball: 18 points  
  - 2nd ball: 16 points  
  - 3rd ball: 14 points  
  - ... and so on, down to 2 points.

#### Public Grid:
- Each ball placed gives **15 points** to the placing player.
- **But** it causes **-5 points** to be subtracted from the score of each of the other two players.

###  Scoring
- Scores are calculated live and displayed after each rounds.
- Strategic balance is key: selfish moves hurt others, while altruism may reduce your personal gain.

---

## Game Arena

![Game Arena](https://github.com/prathamshrivastava/Behavioral_Economics-Ball_Allocation_Game/blob/main/GameArena.png)

---

##  File Structure

```bash
├── Game.html         # Frontend game interface
├── results.html      # Results screen after all rounds
├── init.py           # Backend logic: rounds, scoring, and game state
├── README.md         # Project documentation
