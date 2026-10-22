# Lesson 3.2: Keep Going!

**Time:** 45 min · **You need:** Thonny · **New words:** while loop,
infinite loop, break, counter

## Goal *(read this to the learner)*

> A `for` loop goes round a set number of times. But what if you don't
> know how many times? A game should keep going *until you win*, not for
> exactly 10 turns. Today you'll learn the `while` loop, and build a
> guessing game that you can always win in 7 guesses, if you're clever.

## Before the lesson *(guide, 5 min)*

- [ ] Read this whole lesson once.
- [ ] Know how to stop a runaway program: Thonny's red **Stop** button
      (or Ctrl+F2); in the terminal, **Ctrl+C**.

## Warm-up (5 min)

"Keep clapping *while* I'm holding my hand up." Hold your hand up for a
random time, then drop it. "Did you know how many claps when you started?"
*(No: you kept going while something was true.)*

## Activity

1. **A countdown.** New file, `~/lab/python/stage3/countdown.py`:
   ```python
   n = 10
   while n > 0:
       print(n)
       n = n - 1
   print("BLAST OFF!")
   ```
   **They should see:** 10 down to 1, then `BLAST OFF!`.

   **Say:** "`while n > 0:` means 'keep doing the indented lines, as long
   as `n` is more than 0'. Python checks the condition at the top, every
   time round. When it's false, the loop ends."

2. **A loop that never ends.** **Say:** "What happens if we forget to make
   `n` smaller?" Delete the line `n = n - 1` and run it.

   **They should see:** `10` printed again and again, forever.

   **Say:** "That's an **infinite loop**. `n` is always 10, so it's always
   more than 0. Press the red **Stop** button." Put the line back.

   **Say:** "Every programmer makes infinite loops. The trick is knowing
   how to stop them. In the terminal, it's Ctrl+C, the same as in the
   Mineshaft."

3. **A shortcut.** **Say:** "Programmers write `n = n - 1` so often that
   there's a short way: `n -= 1`. And `score = score + 10` can be
   `score += 10`." Change the countdown to use `-=`.

4. **Guess my number.** New file, `guess.py`:
   ```python
   import random

   secret = random.randint(1, 100)
   guesses = 0
   guess = 0

   print("I'm thinking of a number from 1 to 100.")

   while guess != secret:
       guess = int(input("Your guess: "))
       guesses += 1
       if guess < secret:
           print("Too low!")
       elif guess > secret:
           print("Too high!")

   print(f"You got it in {guesses} guesses!")
   ```
   **Say:** "`!=` means 'is not equal to'. So the loop keeps going while
   your guess isn't the secret. We set `guess = 0` at the start so the
   loop has something to check the very first time."

   Let them play several times. Write down how many guesses each game took.

5. **The clever strategy.** **Ask:** "What's the best first guess?"
   Let them think. *(50: whatever the answer, it rules out half the
   numbers.)* "Then if it's too high, the best next guess is...?" *(25.)*

   **Say:** "Each guess cuts the numbers left in half: 100, 50, 25, 13,
   7, 4, 2, 1. That's 7 guesses, at most, every time! This trick is called
   **binary search**, and you'll meet it again when you study algorithms."

   Swap roles: the learner thinks of a number, and you guess with binary
   search out loud.

6. **Loops that stop from the inside: `break`.** New file, `menu.py`:
   ```python
   print("Welcome to the joke robot!")

   while True:
       command = input("Type joke, hello or quit: ")
       if command == "quit":
           break
       elif command == "hello":
           print("Beep boop. Hello, human.")
       elif command == "joke":
           print("Why did the robot go on holiday? It needed to recharge.")
       else:
           print("Does not compute.")

   print("Bye!")
   ```
   **Say:** "`while True` would go forever, because `True` is always true.
   `break` is the emergency exit: it jumps straight out of the loop. This
   is how most games and menus work: loop forever, until the player
   quits."

## If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| The same thing prints forever | An infinite loop: the condition never becomes false | Stop it (red Stop button or Ctrl+C). Check that something in the loop changes the variable the condition uses. |
| `NameError: name 'guess' is not defined` on the `while` line | The variable is checked before it has anything in it | Give it a starting value above the loop: `guess = 0`. |
| The loop never runs at all | The condition is false the first time | Check the starting value, and `<` against `>`. |
| `SyntaxError: 'break' outside loop` | `break` isn't indented inside the loop | Indent it so it's inside the `while`. |
| Typing `Quit` doesn't quit | Capital letters | Compare with `command.lower() == "quit"`. |
| `ValueError: invalid literal for int()` | Typed a word, or pressed Enter with nothing | Type a number. (Lesson 3.10's challenge shows how to check.) |

## Talk about it

- When would you use `for`, and when `while`? *(`for` when you know how
  many times; `while` when you keep going until something happens.)*
- What's an infinite loop, and how do you stop one?
- Why can you always guess a number from 1 to 100 in 7 guesses?
  *(Each guess halves what's left, and 2 × 2 × 2 × 2 × 2 × 2 × 2 = 128,
  which is more than 100.)*

## Challenge *(if there's time, or for next time)*

- Make the computer guess *your* number with binary search. You answer
  "high", "low" or "yes". *(Keep a `low` and a `high`, and guess the middle:
  `(low + high) // 2`.)*
- How many guesses would 1 to 1000 need? 1 to a million? *(10; 20.)*
- Add a limit: if you haven't got it in 10 guesses, you lose.
- The "Are we there yet?" program: it keeps asking until you type `yes`.

## Checkpoint

The learner can, without help:
- [ ] Write a `while` loop that stops when a condition becomes false
- [ ] Stop an infinite loop, in Thonny and in the terminal
- [ ] Use `while True` and `break` to make a menu that repeats until quit
- [ ] Explain the halving strategy for the guessing game

## Lab notebook

Write the table of your guessing-game scores. Draw the halving: a line from
1 to 100, cut in half, then half again. Add *while loop*, *infinite loop*,
*break* and *binary search* to the dictionary.

## Guide's background *(optional reading)*

`while` is the more general loop: anything a `for` loop does, a `while`
loop can do too, but `for` is clearer when you know how many times. The
`while True: ... break` pattern is the heart of nearly every interactive
program; your web browser and every game run a loop like it, waiting for
something to happen.

**Binary search** is one of the most important algorithms there is. Each
step halves the possibilities, so the number of steps grows very slowly:
about 20 guesses find one number in a million, and about 30 find one in a
billion. Stage 7 explains why, using logarithms ("how many times can you
halve this?"). For now, the guessing game gives the learner a feel for it.
