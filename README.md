# Memory Museum

A memory-matching card game built with Python and Pygame. Match pairs of cards to
uncover and restore a hidden painting, then track your progress across five levels
with saved best times, best attempts, and overall statistics.

## Group / Member Information
Member 1: [Anika Sultana Anu, 23-51807-2]
Member 2: [Most Fatematuz Zohora Chadni, 23-51812-2]
Member 3: [Jannat Jarin, 23-51827-2]
Member 4: [Nusrat Jahan Sumaiya, 23-51831-2]

## About the Project

Memory Museum takes the classic memory-card game and gives it a purpose: each level
is a famous painting cut into 8 pieces. Flip cards to find matching pairs, and each
match restores one piece of the painting. Complete all 8 matches to reveal the full
painting, unlock the next level, and (if you beat your previous best) set a new
record.

The game keeps track of your best attempts and best time for every level, saves
that progress to a file so it's remembered the next time you play, and includes a
statistics screen that summarizes your performance across all levels using NumPy.

## Features

- Five playable levels, each based on a different painting
- Classic flip-two-cards memory matching gameplay
- Level unlocking — complete a level to unlock the next one
- Best score tracking (fewest attempts, fastest time) per level, saved between
  sessions
- "New Record" detection when you beat a previous best
- Statistics screen showing total/average/best time and attempts across all
  completed levels
- Persistent save data using a JSON file, with recovery if the file is missing or
  corrupted
- "How To Play" screen with instructions
- Simple, mouse-driven menu interface


## Project Structure

```
MemoryMuseum/
├── main.py              # Entry point — creates and starts the Game
├── game.py               # Main Game class: screens, input, game loop, statistics
├── card.py               # Card class: a single flippable/matchable card
├── painting.py            # Painting class: level data and image handling
├── scores.json            # Saved best attempts/time per level (auto-created)
├── requirements.txt        # Python package dependencies
├── assets/
│   └── images/
│       ├── welcome_screen.jpg
│       ├── level_screen.jpg
│       ├── starry_night.jpg
│       ├── mona_lisa.jpg
│       ├── the_scream.jpg
│       ├── girl_with_pearl.jpg
│       └── the_weeping_woman.jpg
└── README.md
```

## Python Concepts Used

- Variables & data types 
- Operators 
- Branching (if/elif/else)
- Loops (for/while) 
- Functions/methods 
- List 
- Tuple 
- Set 
- Dictionary 
- File handling 
- Exception handling 
- OOP 

## Data Structures

- List
- Tuple
- Set
- Dictionary


## Library / Module Use

- Pygame
- NumPy

## How to Run

1. Make sure Python 3 is installed.
2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```
3. Run the game from the project folder:
   ```
   python main.py
   ```

## How to Play

1. From the welcome screen, choose **Start Game**.
2. Select any unlocked level.
3. Click two cards to reveal them.
4. If they match, that piece of the painting is restored and the cards stay
   face-up. If they don't match, they flip back down.
5. Match all 8 pairs to complete the painting and finish the level.
6. Fewer attempts and a faster time give you a better chance at a New Record.
7. Completing a level unlocks the next one.
8. Check Best Score for your saved records per level, or Statistics for a
   summary of your progress across all levels.

