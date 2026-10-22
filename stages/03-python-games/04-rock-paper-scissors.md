# Lesson 3.4: Rock, Paper, Scissors

**Time:** 2 sessions of 45 min · **You need:** Thonny; paper for a
flowchart · **New words:** and, or, not, Boolean, continue

## Goal *(read this to the learner)*

> Time for your first complete game against the computer! It'll be best of
> five: the first to win 3 rounds wins the match. To build it, you need
> everything from the last three lessons, plus a way to check two things
> at once.

## Before the lesson *(guide, 5 min)*

- [ ] Read this whole lesson once.
- [ ] Make a folder: `mkdir -p ~/lab/python/rps`

## Warm-up (5 min)

Play three rounds of rock, paper, scissors with your hands. "How do you
decide who wins? Say the rules." *(Rock beats scissors, scissors beat
paper, paper beats rock. The same is a draw.)*

## Activity

### Session 1: plan, and the new tools

1. **Plan on paper.** Together, draw a flowchart of one round:
   - The player chooses.
   - Is it a real move? If not, ask again.
   - The computer chooses at random.
   - Are they the same? → draw.
   - Did the player win? → player gets a point.
   - Otherwise → computer gets a point.

   Then around it: "Keep playing rounds *while* nobody has 3 points."

2. **Checking two things at once: `and`.** In the Shell:
   ```python
   player = "rock"
   computer = "scissors"
   player == "rock" and computer == "scissors"
   player == "rock" and computer == "paper"
   ```
   *(`True`, then `False`.)* **Say:** "`and` is only `True` if *both* sides
   are true."

3. **`or`.**
   ```python
   day = "saturday"
   day == "saturday" or day == "sunday"
   ```
   **Say:** "`or` is `True` if *either* side is true, or both."

4. **`not`.**
   ```python
   "lizard" in ["rock", "paper", "scissors"]
   "lizard" not in ["rock", "paper", "scissors"]
   ```
   **Say:** "`True` and `False` are called **Boolean** values. `and`, `or`
   and `not` are the whole of Boolean logic, and in Stage 4 you'll build
   them out of redstone!"

5. **The truth table.** On paper, fill in this table together, for `and`
   and then for `or`:

   | A | B | A and B | A or B |
   |---|---|---|---|
   | True | True | True | True |
   | True | False | False | True |
   | False | True | False | True |
   | False | False | False | False |

### Session 2: build the game

6. **The game.** New file, `~/lab/python/rps/rps.py`:
   ```python
   import random

   moves = ["rock", "paper", "scissors"]
   player_score = 0
   computer_score = 0

   print("ROCK, PAPER, SCISSORS! First to 3 wins.")

   while player_score < 3 and computer_score < 3:
       player = input("rock, paper or scissors? ").lower().strip()
       if player not in moves:
           print("That's not a move! Try again.")
           continue

       computer = random.choice(moves)
       print(f"The computer chose {computer}.")

       if player == computer:
           print("A draw!")
       elif ((player == "rock" and computer == "scissors")
             or (player == "scissors" and computer == "paper")
             or (player == "paper" and computer == "rock")):
           print("You win this round!")
           player_score += 1
       else:
           print("The computer wins this round.")
           computer_score += 1

       print(f"Score: you {player_score}, computer {computer_score}")
       print()

   if player_score == 3:
       print("YOU WON THE MATCH!")
   else:
       print("The computer won the match. Rematch?")
   ```
   Type it a piece at a time, running it as you go (the scoring parts can
   wait until the rest works).

   **Say:** "Some new things here. `.strip()` removes spaces from the ends,
   in case someone types ` rock `. `continue` skips the rest of the loop
   and goes straight back to the top, so a wrong move doesn't count. And
   that long `elif` is split across three lines: Python allows that inside
   brackets."

7. **Test it properly.** **Say:** "How do we know every rule works? Play
   until you've seen every combination: rock against all three, paper
   against all three, scissors against all three." Make a 3 × 3 grid on
   paper and tick each one as it happens. Also try `banana`, `ROCK`, and
   just pressing Enter.

## If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| The game never ends | The scores never change, or the `while` condition is wrong | Check `+= 1` is in both the win and lose parts, and the `while` uses `and`. |
| The game ends after one round | `or` used in the `while` instead of `and` | It should keep going while *both* scores are under 3. |
| A win is counted as a loss | One of the three winning rules is wrong | Check each `(player == ... and computer == ...)` against the real rules. |
| `SyntaxError` on the long `elif` | A bracket is missing | Count them: the whole condition is in one pair of `( )`, with each rule in its own pair. |
| `ROCK` is "not a move" | `.lower()` is missing | `input(...).lower().strip()`. |
| `SyntaxError: 'continue' not properly in loop` | `continue` isn't inside the loop | Check its indentation. |

## Talk about it

- What's the difference between `and` and `or`?
- Why does the `while` use `and`? *(Keep going only while both scores are
  under 3. As soon as one reaches 3, stop.)*
- Could the computer cheat? How would you know? *(Read the code: it
  chooses with `random.choice(moves)`, which never looks at your move. The
  code is the proof.)*

## Challenge *(if there's time, or for next time)*

- **Five moves:** add `lizard` and `spock`. Each move now beats two
  others: rock beats scissors and lizard; paper beats rock and spock;
  scissors beat paper and lizard; lizard beats paper and spock; spock
  beats rock and scissors. That's 10 winning rules, and a lot of `or`s.
  Lesson 3.8 has a much neater way.
- Keep a list of the player's moves. Does the player pick rock most?
- A sneaky computer: it picks whatever beats the player's *most common*
  move so far. Can you still beat it?

## Checkpoint

The learner can, without help:
- [ ] Explain `and`, `or` and `not`, with the truth table
- [ ] Use `continue` to skip a bad input
- [ ] Test a game by trying every combination, and unexpected input

## Lab notebook

Glue in the flowchart and the truth table. Draw the 3 × 3 grid of all the
combinations, with who wins in each square. Add *Boolean*, *and*, *or*,
*not* and *continue* to the dictionary.

## Guide's background *(optional reading)*

This is the learner's first full game loop: input, check, update the
game's state (the scores), show the result, and repeat until an end
condition. Every game, from Pong to Minecraft, runs this loop many times a
second.

**Boolean logic** (`and`, `or`, `not`) is named after George Boole, who
worked out its rules in the 1850s. It's the bridge to Stage 4, where the
same truth tables become logic gates and redstone circuits, and then to
Stage 6, where those gates become a whole computer. If you work with PLCs,
ladder logic is exactly this: contacts in series are `and`, contacts in
parallel are `or`, and a normally-closed contact is `not`.

Testing every combination in a grid is a real testing technique. With 3
moves for each player there are only 9 cases, so you can check them all.
